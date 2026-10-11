import io
import re
import pytest
from pypdf import PdfWriter
from fastapi.testclient import TestClient
from app import create_app
from analyzer import ProviderFailure
from conftest import ready

CONFIG = {'key':'TEST_STUB_NOT_REAL','passcode':'test-owner-only','model':'TEST_STUB','base_url':'http://testserver','cookie_secure':False}

def csrf(page):
    return re.search(r'name="csrf" value="([^"]+)"', page.text).group(1)

def form_for(row, page):
    return {'csrf':csrf(page),'version':str(row['version']),'token':row['current_token'],'passcode':CONFIG['passcode'],'action':'approve'}

def test_get_never_pays_and_tampered_form_amount_is_ignored(store, sample):
    row = ready(store, sample)
    with TestClient(create_app(store,lambda i,c:sample[2],lambda:CONFIG)) as client:
        page = client.get(f'/owner/{row["id"]}',params={'version':1,'token':row['current_token']})
        assert page.status_code == 200
        assert '25,000.00' in page.text
        assert store.history() == []
        form = form_for(row,page)
        form.update(amount_minor='1',account='ATTACKER')
        response = client.post(f'/owner/{row["id"]}',data=form)
        assert response.status_code == 200
        assert 'Demo transfer committed' in response.text
        assert store.history()[0]['amount_minor'] == 2500000
        assert store.history()[0]['account'] == 'DEMO-V001-ACCOUNT-A'
        assert client.post(f'/owner/{row["id"]}',data=form).url == response.url
        assert len(store.history()) == 1

def test_full_intake_analysis_owner_receipt_and_notice_flow(store,sample):
    with TestClient(create_app(store,lambda i,c:sample[2],lambda:CONFIG)) as client:
        page=client.get('/')
        review=client.post('/analyze',data={'csrf':csrf(page),'invoice_text':sample[0],'context_text':sample[1]})
        assert 'AWAITING OWNER' in review.text and 'Open owner review' in review.text
        assert 'AWAITING OWNER' in client.get('/inbox').text
        request_id=review.url.path.split('/')[-1]
        row=store.get(request_id)
        owner=client.get(f'/owner/{request_id}',params={'version':row['version'],'token':row['current_token']})
        receipt=client.post(f'/owner/{request_id}',data=form_for(row,owner))
        assert 'Demo transfer committed' in receipt.text
        assert '475,000.00' in receipt.text
        assert '25,000.00' in client.get('/history').text

def test_readable_pdf_text_input_can_reach_owner_review(store,sample):
    from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject
    writer=PdfWriter();page=writer.add_blank_page(width=612,height=792)
    font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
    content=['BT /F1 10 Tf 30 750 Td 14 TL']
    for line in sample[0].strip().splitlines():
        escaped=line.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
        content.append('('+escaped+') Tj T*')
    content.append('ET');stream=DecodedStreamObject();stream.set_data('\n'.join(content).encode('ascii'))
    page[NameObject('/Contents')]=writer._add_object(stream)
    out=io.BytesIO();writer.write(out)
    def pdf_provider(invoice,context):
        assert 'TOTAL REQUESTED: PKR 25,000' in invoice
        assert 'Base goods: 2 Laptop Model L units x PKR 10,000 = PKR 20,000' in invoice
        output=sample[2].model_copy(deep=True)
        # The provider receives extracted PDF text, whose blank-line spacing can
        # differ from the original TXT. Its evidence must quote THAT actual input.
        for name in type(output.invoice.field_evidence).model_fields:
            for proof in getattr(output.invoice.field_evidence,name): proof.quote=invoice
        for line in output.invoice.lines:
            for proof in line.evidence: proof.quote=invoice
        return output
    with TestClient(create_app(store,pdf_provider,lambda:CONFIG)) as client:
        home=client.get('/')
        response=client.post('/analyze',data={'csrf':csrf(home),'context_text':sample[1]},files={'invoice_file':('readable.pdf',out.getvalue(),'application/pdf')})
        assert response.status_code == 200 and 'AWAITING OWNER' in response.text

def test_cross_site_and_missing_csrf_are_blocked(store, sample):
    row = ready(store,sample)
    with TestClient(create_app(store,lambda i,c:sample[2],lambda:CONFIG)) as client:
        page = client.get(f'/owner/{row["id"]}',params={'version':1,'token':row['current_token']})
        form = form_for(row,page)
        assert client.post(f'/owner/{row["id"]}',data=form,headers={'Origin':'https://evil.invalid'}).status_code == 403
        form.pop('csrf')
        assert client.post(f'/owner/{row["id"]}',data=form).status_code == 403
        assert not store.history()

def test_hosted_forms_preserve_origin_metadata_and_validate_both_steps(store,sample):
    hosted={**CONFIG,'base_url':'https://example.test','cookie_secure':True}
    with TestClient(create_app(store,lambda i,c:sample[2],lambda:hosted),base_url=hosted['base_url']) as client:
        page=client.get('/')
        assert page.headers['Referrer-Policy'] == 'same-origin'
        form={'csrf':csrf(page),'invoice_text':sample[0],'context_text':sample[1]}
        for origin in ('null','https://evil.invalid'):
            assert client.post('/analyze',data=form,headers={'Origin':origin}).status_code == 403
        headers={'Origin':hosted['base_url'],'Referer':hosted['base_url']+'/'}
        assert client.post('/analyze',data={**form,'csrf':'incorrect'},headers=headers).status_code == 403
        review=client.post('/analyze',data=form,headers=headers)
        assert review.status_code == 200 and 'AWAITING OWNER' in review.text
        row=store.get(review.url.path.split('/')[-1])
        owner=client.get(f'/owner/{row["id"]}',params={'version':row['version'],'token':row['current_token']})
        assert owner.headers['Referrer-Policy'] == 'same-origin'
        approval=form_for(row,owner)
        for origin in ('null','https://evil.invalid'):
            assert client.post(f'/owner/{row["id"]}',data=approval,headers={'Origin':origin}).status_code == 403
        assert client.post(f'/owner/{row["id"]}',data=approval,headers={**headers,'Referer':'https://evil.invalid/'}).status_code == 403
        assert not store.history()
        receipt=client.post(f'/owner/{row["id"]}',data=approval,headers=headers)
        assert receipt.status_code == 200 and 'Demo transfer committed' in receipt.text
        assert len(store.history()) == 1

def test_opaque_local_browser_still_needs_csrf_and_is_not_allowed_when_hosted(store,sample):
    local={**CONFIG,'base_url':'http://127.0.0.1:8000'}
    with TestClient(create_app(store,lambda i,c:sample[2],lambda:local),base_url=local['base_url']) as client:
        page=client.get('/')
        form={'csrf':csrf(page),'invoice_text':sample[0],'context_text':sample[1]}
        assert client.post('/analyze',data=form,headers={'Origin':'null'}).status_code == 200
        form.pop('csrf')
        assert client.post('/analyze',data=form,headers={'Origin':'null'}).status_code == 403
    hosted={**CONFIG,'base_url':'https://example.test'}
    with TestClient(create_app(store,lambda i,c:sample[2],lambda:hosted),base_url=hosted['base_url']) as client:
        page=client.get('/')
        assert client.post('/analyze',data={'csrf':csrf(page),'invoice_text':sample[0],'context_text':sample[1]},headers={'Origin':'null'}).status_code == 403

@pytest.mark.parametrize('failure', ['api','malformed','evidence'])
def test_provider_failure_or_invalid_output_cannot_pay(store, sample, failure):
    def provider(i,c):
        if failure == 'api': raise ProviderFailure('Controlled API failure')
        if failure == 'malformed': return {'unsafe':True}
        output = sample[2].model_copy(deep=True)
        output.findings[0].evidence[0].quote = 'No such quote'
        return output
    with TestClient(create_app(store,provider,lambda:CONFIG)) as client:
        page = client.get('/')
        response = client.post('/analyze',data={'csrf':csrf(page),'invoice_text':sample[0],'context_text':sample[1]})
        assert response.status_code == 200
        assert 'Payment unavailable' in response.text
        assert 'Open owner review' not in response.text
        assert not store.history()
        assert client.get('/inbox').status_code == 200

def test_txt_upload_never_uses_filename_as_path_and_escapes_documents(store,sample):
    invoice = sample[0] + '\n<script>alert("untrusted")</script>'
    with TestClient(create_app(store,lambda i,c:sample[2],lambda:CONFIG)) as client:
        page=client.get('/')
        response=client.post('/analyze',data={'csrf':csrf(page),'context_text':sample[1]},files={'invoice_file':('../../unsafe.txt',invoice.encode(),'text/plain')})
        assert response.status_code == 200
        assert '&lt;script&gt;' in response.text
        assert '<script>alert' not in response.text
        assert not (store.path.parent/'unsafe.txt').exists()

def test_empty_pdf_unsupported_and_oversize_inputs_are_clear(store,sample):
    writer=PdfWriter();writer.add_blank_page(width=300,height=300);stream=io.BytesIO();writer.write(stream)
    with TestClient(create_app(store,lambda i,c:sample[2],lambda:CONFIG)) as client:
        page=client.get('/');token=csrf(page)
        response=client.post('/analyze',data={'csrf':token,'context_text':sample[1]},files={'invoice_file':('scan.pdf',stream.getvalue(),'application/pdf')})
        assert response.status_code == 400 and 'no readable text' in response.text
        response=client.post('/analyze',data={'csrf':token,'context_text':sample[1]},files={'invoice_file':('x.exe',b'x','application/octet-stream')})
        assert response.status_code == 400
        response=client.post('/analyze',data={'csrf':token,'context_text':sample[1]},files={'invoice_file':('large.txt',b'x'*(2*1024*1024+1),'text/plain')})
        assert response.status_code == 413
        assert not store.history()
