import hmac
import io
import secrets
from pathlib import Path
from urllib.parse import urlsplit
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from pypdf import PdfReader
from analyzer import analyze, ProviderFailure, prompt_version
from gates import validate, GateError, context_reference_check
from schemas import Analysis
from settings import ROOT, settings, session_secret
from store import Store, PaymentBlocked

MAX_FILE = 2 * 1024 * 1024
MAX_TEXT = 40000
CHECK_NAMES = {'COST_COVERAGE': 'Is this cost already included?', 'APPROVAL_MEANING': 'Was this extra actually approved?', 'LATEST_UPDATE': 'Did a later message change it?'}


async def input_text(form, label):
    text = str(form.get(label + '_text', '')).strip()
    upload = form.get(label + '_file')
    if upload and getattr(upload, 'filename', ''):
        if text:
            raise HTTPException(400, f'For {label}, use either pasted text or a file. Clear one before analyzing.')
        suffix = Path(upload.filename).suffix.lower()
        if suffix not in {'.txt', '.pdf'}:
            raise HTTPException(400, 'Only TXT and text-based PDF files are supported. Paste text for other formats.')
        raw = await upload.read(MAX_FILE + 1)
        if len(raw) > MAX_FILE:
            raise HTTPException(413, 'Each file must be 2 MB or smaller.')
        try:
            if suffix == '.txt':
                text = raw.decode('utf-8-sig').strip()
            else:
                reader = PdfReader(io.BytesIO(raw))
                if len(reader.pages) > 20:
                    raise HTTPException(400, 'Use a short PDF of no more than 20 pages.')
                text = '\n'.join(page.extract_text() or '' for page in reader.pages).strip()
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, 'Could not read the file. Use UTF-8 TXT or paste its text; encrypted/damaged PDFs are unsupported.') from None
    if not text:
        raise HTTPException(400, f'REVIEW: {label} has no readable text. Paste text or use a selectable-text PDF. Scanned PDFs need manual transcription.')
    if len(text) > MAX_TEXT:
        raise HTTPException(413, f'{label} must contain at most {MAX_TEXT:,} characters. Use just this invoice and its relevant deal/messages.')
    return text


def create_app(store=None, analyze_fn=None, config_fn=settings):
    application = FastAPI(title='AccordPay — DEMO FUNDS', docs_url=None, redoc_url=None)
    application.state.store = store or Store()
    provider = analyze_fn or analyze
    templates = Jinja2Templates(directory=str(ROOT / 'templates'))
    templates.env.filters['money'] = lambda minor: f'{(minor or 0)/100:,.2f}'
    cfg = config_fn()
    application.add_middleware(SessionMiddleware, secret_key=session_secret(), same_site='strict', https_only=cfg.get('cookie_secure', False))
    host = urlsplit(cfg['base_url']).hostname
    application.add_middleware(TrustedHostMiddleware, allowed_hosts=list({host, '127.0.0.1', 'localhost', 'testserver'} - {None}))
    application.mount('/static', StaticFiles(directory=str(ROOT / 'static')), name='static')

    @application.middleware('http')
    async def safety_headers(request: Request, call_next):
        if request.method == 'POST':
            chunks, count = [], 0
            async for chunk in request.stream():
                count += len(chunk)
                if count > 5 * 1024 * 1024:
                    return HTMLResponse('Request too large. Use two files of at most 2 MB each.', status_code=413)
                chunks.append(chunk)
            request._body = b''.join(chunks)
        response = await call_next(request)
        # Native form POSTs under no-referrer can send Origin:null, including
        # Chrome on HTTPS. Keep same-origin metadata for CSRF verification;
        # same-origin still suppresses referrers to external destinations.
        response.headers.update({'Cache-Control': 'no-store', 'Referrer-Policy': 'same-origin', 'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'Content-Security-Policy': "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'"})
        return response

    def page(request, name, **context):
        if 'csrf' not in request.session:
            request.session['csrf'] = secrets.token_urlsafe(32)
        return templates.TemplateResponse(request=request, name=name, context={'csrf': request.session['csrf'], 'check_names': CHECK_NAMES, **context})

    def csrf_check(request, form):
        expected = request.session.get('csrf', '')
        actual = str(form.get('csrf', ''))
        if not expected or not actual or not hmac.compare_digest(actual, expected):
            raise HTTPException(403, 'This form is missing its browser verification. Reload the page and try again.')
        origin = request.headers.get('origin')
        referrer = request.headers.get('referer')
        configured = config_fn()['base_url']
        allowed = {configured, str(request.base_url).rstrip('/')}
        # Legacy local pages can use an opaque Origin:null.
        # Permit that local-only case AFTER signed-session CSRF verification.
        # Hosted pages still reject null and all foreign origins; no wildcard.
        opaque_local = (origin == 'null' and not referrer and request.url.hostname in {'127.0.0.1', 'localhost'} and urlsplit(configured).hostname in {'127.0.0.1', 'localhost'})
        if origin and origin.rstrip('/') not in allowed and not opaque_local:
            raise HTTPException(403, 'Cross-site form submission blocked. No funds moved.')
        if referrer:
            parsed = urlsplit(referrer)
            if f'{parsed.scheme}://{parsed.netloc}' not in allowed:
                raise HTTPException(403, 'Cross-site form submission blocked. No funds moved.')

    @application.exception_handler(HTTPException)
    async def readable_error(request, exc):
        response = page(request, 'error.html', message=str(exc.detail))
        response.status_code = exc.status_code
        return response

    @application.exception_handler(PaymentBlocked)
    async def blocked_error(request, exc):
        response = page(request, 'error.html', message=str(exc))
        response.status_code = 409
        return response

    @application.get('/health')
    def health():
        return {'status': 'ok', 'demo_funds_only': True}

    @application.get('/', response_class=HTMLResponse)
    def home(request: Request):
        config = config_fn()
        return page(request, 'intake.html', invoice='', context='', request_id=None, key_ready=bool(config['key']), owner_ready=bool(config['passcode']), balances=application.state.store.balances())

    @application.get('/examples/{case}', response_class=HTMLResponse)
    def example(request: Request, case: str):
        if case not in [f'D{i:02}' for i in range(1, 10)]:
            raise HTTPException(404, 'Development example not found.')
        folder = ROOT / 'assets' / 'development' / case
        config = config_fn()
        return page(request, 'intake.html', invoice=(folder / 'invoice.txt').read_text(encoding='utf-8'), context=(folder / 'deal_and_messages.txt').read_text(encoding='utf-8'), request_id=None, selected_case=case, key_ready=bool(config['key']), owner_ready=bool(config['passcode']), balances=application.state.store.balances())

    @application.get('/requests/{request_id}/edit', response_class=HTMLResponse)
    def edit(request: Request, request_id: str):
        row = application.state.store.get(request_id)
        if not row:
            raise HTTPException(404, 'Request not found.')
        if row['status'] == 'PAID':
            raise PaymentBlocked('Paid requests cannot be edited.')
        config = config_fn()
        return page(request, 'intake.html', invoice=row['invoice'] or '', context=row['context'] or '', request_id=request_id, key_ready=bool(config['key']), owner_ready=bool(config['passcode']), balances=application.state.store.balances())

    @application.post('/analyze')
    async def run_analysis(request: Request):
        form = await request.form()
        csrf_check(request, form)
        invoice, context = await input_text(form, 'invoice'), await input_text(form, 'context')
        saved_id = str(form.get('request_id', '')).strip() or None
        request_id, version = application.state.store.begin(saved_id)
        config = config_fn()
        output, error = None, None
        try:
            linkage_message = context_reference_check(invoice, context)
            if linkage_message:
                raise GateError(linkage_message)
            output = await run_in_threadpool(provider, invoice, context)
            output = Analysis.model_validate(output)
            result = validate(output, invoice, context, application.state.store.setup)
        except GateError as exc:
            error = str(exc)
            result = {'state': 'REVIEW', 'gate_messages': [error]}
        except ProviderFailure as exc:
            error = str(exc)
            result = {'state': 'ERROR', 'gate_messages': [error]}
        except Exception:
            error = 'Analysis output could not be validated. Check the inputs and try again. Payment is blocked.'
            result = {'state': 'ERROR', 'gate_messages': [error]}
            output = None
        application.state.store.finish(request_id, version, invoice, context, output, result, config['model'], prompt_version(), error)
        return RedirectResponse('/requests/' + request_id, status_code=303)

    @application.get('/requests/{request_id}', response_class=HTMLResponse)
    def review(request: Request, request_id: str):
        row = application.state.store.get(request_id)
        if not row:
            raise HTTPException(404, 'Request not found.')
        return page(request, 'review.html', row=row)

    @application.get('/owner/{request_id}', response_class=HTMLResponse)
    def owner(request: Request, request_id: str, token: str = '', version: int = 0):
        application.state.store.verify_token(request_id, token, version)
        row = application.state.store.get(request_id)
        return page(request, 'owner.html', row=row, token=token, version=version, owner_ready=bool(config_fn()['passcode']))

    @application.post('/owner/{request_id}')
    async def decide(request: Request, request_id: str):
        form = await request.form()
        csrf_check(request, form)
        try:
            version = int(str(form.get('version', '0')))
        except ValueError:
            raise HTTPException(400, 'Invalid request version.') from None
        receipt = application.state.store.decide(request_id, version, str(form.get('token', '')), str(form.get('passcode', '')), config_fn()['passcode'], str(form.get('action', '')))
        target = '/receipts/' + receipt['id'] if receipt else '/requests/' + request_id
        return RedirectResponse(target, status_code=303)

    @application.get('/receipts/{receipt_id}', response_class=HTMLResponse)
    def receipt(request: Request, receipt_id: str):
        row = application.state.store.receipt(receipt_id)
        if not row:
            raise HTTPException(404, 'Receipt not found.')
        return page(request, 'receipt.html', receipt=row, balances=application.state.store.balances())

    @application.get('/history', response_class=HTMLResponse)
    def history(request: Request):
        return page(request, 'history.html', history=application.state.store.history(), balances=application.state.store.balances())

    @application.get('/inbox', response_class=HTMLResponse)
    def inbox(request: Request):
        return page(request, 'inbox.html', notices=application.state.store.inbox())

    return application


app = create_app()
