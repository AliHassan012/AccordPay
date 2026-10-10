import re
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app import create_app
from gates import context_reference_check

CONFIG={'key':'TEST_STUB','passcode':'TEST_STUB','model':'TEST_STUB','base_url':'http://testserver','cookie_secure':False}

def test_order_alone_can_establish_linkage_but_not_approval():
    assert context_reference_check('Invoice reference: INV-17\nOrder reference: ORDER-22','Deal for order-22.') is None

def test_prefixes_and_similar_item_names_are_not_reference_matches():
    message=context_reference_check('Invoice reference: INV-7\nOrder reference: ORDER-7','Laptop agreement INV-70 and ORDER-70')
    assert 'No matching context found' in message

def test_unknown_invoice_layout_requests_a_reference():
    assert 'Could not identify' in context_reference_check('An invoice for laptops','Laptop contract')

@pytest.mark.parametrize('context',['Unrelated agreement about monitors.','Invoice INV-D030 / Order ORDER-D030'])
def test_no_matching_context_skips_ai_and_blocks_payment(store,sample,context):
    def provider(*args):raise AssertionError('Gemini must not run for missing context')
    with TestClient(create_app(store,provider,lambda:CONFIG)) as client:
        home=client.get('/')
        csrf=re.search(r'name="csrf" value="([^"]+)"',home.text).group(1)
        response=client.post('/analyze',data={'csrf':csrf,'invoice_text':sample[0],'context_text':context})
        assert response.status_code==200
        assert 'No matching context found' in response.text
        assert 'REVIEW' in response.text and 'Open owner review' not in response.text
        assert 'No validated AI analysis' in response.text
        row=store.get(response.url.path.split('/')[-1])
        assert row['status']=='REVIEW' and row['analysis'] is None and row['current_token'] is None
        assert row['invoice']==sample[0].strip() and row['context']==context
        assert store.history()==[] and store.balances()=={'owner':50000000,'vendor':0}

def test_actual_mismatched_pdf_pair_skips_provider(store):
    folder=Path(__file__).resolve().parents[1]/'delivery'/'INVOICES_AND_CONTRACTS_12'
    def provider(*args):raise AssertionError('Gemini must not be called')
    with TestClient(create_app(store,provider,lambda:CONFIG)) as client:
        home=client.get('/');csrf=re.search(r'name="csrf" value="([^"]+)"',home.text).group(1)
        response=client.post('/analyze',data={'csrf':csrf},files={'invoice_file':('Invoice_07.pdf',(folder/'Invoice_07.pdf').read_bytes(),'application/pdf'),'context_file':('Contract_01.pdf',(folder/'Contract_01.pdf').read_bytes(),'application/pdf')})
        assert 'No matching context found' in response.text and 'INV-PDF12-07' in response.text
        assert 'REVIEW' in response.text and 'Open owner review' not in response.text
        assert store.history()==[]

def test_all_matching_pdf_pairs_pass_only_the_linkage_check():
    from pypdf import PdfReader
    folder=Path(__file__).resolve().parents[1]/'delivery'/'INVOICES_AND_CONTRACTS_12'
    for n in range(1,13):
        invoice=PdfReader(folder/f'Invoice_{n:02}.pdf').pages[0].extract_text()
        context=PdfReader(folder/f'Contract_{n:02}.pdf').pages[0].extract_text()
        assert context_reference_check(invoice,context) is None
