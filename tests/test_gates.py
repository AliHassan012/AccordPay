import pytest
from pydantic import ValidationError
from gates import validate, GateError, paisa
from schemas import Analysis
from settings import trusted_setup
from analyzer import provider_schema

def test_positive_control_and_backend_disposition_priority(sample):
    invoice, context, analysis = sample
    assert validate(analysis, invoice, context, trusted_setup())['state'] == 'AWAITING_OWNER'
    analysis.findings[0].status = 'UNCLEAR'
    assert validate(analysis, invoice, context, trusted_setup())['state'] == 'REVIEW'
    analysis.findings[1].status = 'ISSUE'
    assert validate(analysis, invoice, context, trusted_setup())['state'] == 'HOLD'

@pytest.mark.parametrize('amount', ['NaN','-1','1e5','1,000','0.001','Infinity',' 25000'])
def test_invalid_money_never_passes(amount):
    with pytest.raises(GateError):
        paisa(amount)

def test_fractional_quantity_uses_exact_money(sample):
    assert paisa('0.29') == 29
    invoice, context, analysis = sample
    analysis.invoice.lines[0].quantity = '3'
    with pytest.raises(GateError):
        validate(analysis, invoice, context, trusted_setup())

@pytest.mark.parametrize('change', ['total','quote','source','account','quantity','reference','metadata'])
def test_unsupported_critical_inputs_block_readiness(sample, change):
    invoice, context, analysis = sample
    if change == 'total': analysis.invoice.total = '25001'
    if change == 'quote': analysis.findings[0].evidence[0].quote = 'Invented approval'
    if change == 'source': analysis.invoice.field_evidence.total[0].document_id = 'context'
    if change == 'account': analysis.invoice.account = 'ATTACKER-ACCOUNT'
    if change == 'quantity': analysis.invoice.lines[0].quantity = '3'
    if change == 'reference': analysis.findings[0].evidence[0].reference = 'M99'
    if change == 'metadata': context = context.replace('OWNER-01', 'unknown')
    with pytest.raises(GateError):
        validate(analysis, invoice, context, trusted_setup())

def test_structured_output_is_exactly_three_unique_checks(sample):
    data = sample[2].model_dump()
    data['findings'][1]['check'] = data['findings'][0]['check']
    with pytest.raises(ValidationError): Analysis.model_validate(data)
    data = sample[2].model_dump()
    data['execute_payment'] = True
    with pytest.raises(ValidationError): Analysis.model_validate(data)

def test_provider_schema_contains_no_unresolved_references():
    import json
    encoded = json.dumps(provider_schema())
    assert '$ref' not in encoded and '$defs' not in encoded
    assert 'field_evidence' in encoded
