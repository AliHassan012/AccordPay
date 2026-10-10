import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from schemas import Analysis
from settings import ROOT, trusted_setup
from store import Store
from gates import validate


@pytest.fixture
def sample():
    folder = ROOT / 'assets' / 'development' / 'D03'
    invoice = (folder / 'invoice.txt').read_text(encoding='utf-8')
    context = (folder / 'deal_and_messages.txt').read_text(encoding='utf-8')
    proof = {'document_id': 'invoice', 'reference': 'Invoice', 'quote': invoice.strip()}
    message = next(line for line in context.splitlines() if line.startswith('M2 |'))
    evidence = {'document_id': 'context', 'reference': 'M2', 'quote': message}
    # Controlled test model output, never an app provider or runtime asset.
    data = {
        'invoice': {
            'vendor_name': 'Campus Tech Supplies (fictional)', 'vendor_id': 'V001',
            'invoice_ref': 'INV-D03', 'order_ref': 'ORDER-D03', 'currency': 'PKR',
            'account': 'DEMO-V001-ACCOUNT-A', 'purpose': 'Laptop Model L',
            'lines': [
                {'description': 'Laptop Model L', 'pricing_basis': 'unit', 'quantity': '2', 'unit_price': '10000', 'amount': '20000', 'evidence': [proof]},
                {'description': 'Rush delivery', 'pricing_basis': 'lump_sum', 'quantity': '1', 'unit_price': '5000', 'amount': '5000', 'evidence': [proof]},
            ],
            'discount': '0', 'tax': '0', 'total': '25000',
            'field_evidence': {key: [proof] for key in ['vendor_name', 'vendor_id', 'invoice_ref', 'order_ref', 'currency', 'account', 'purpose', 'discount', 'tax', 'total']},
        },
        'findings': [{'check': check, 'status': 'SUPPORTED', 'explanation': 'Controlled test output; not live language evaluation.', 'evidence': [evidence]} for check in ['COST_COVERAGE', 'APPROVAL_MEANING', 'LATEST_UPDATE']],
        'clarification_needed': [],
    }
    return invoice, context, Analysis.model_validate(data)


@pytest.fixture
def store(tmp_path):
    return Store(tmp_path / 'test.sqlite3', trusted_setup())


def ready(store, sample):
    invoice, context, analysis = sample
    request_id, version = store.begin()
    result = validate(analysis, invoice, context, store.setup)
    return store.finish(request_id, version, invoice, context, analysis, result, 'TEST_STUB', 'TEST_STUB')
