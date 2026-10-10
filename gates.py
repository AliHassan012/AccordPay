import re
from decimal import Decimal, InvalidOperation
from schemas import Analysis, Evidence


class GateError(ValueError):
    pass


def context_reference_check(invoice_text, context_text):
    """Check document linkage before paying for AI; never establishes approval."""
    references = []
    for label in ('Invoice', 'Order'):
        pattern = r'(?im)^\s*' + label + r'\s+(?:reference|ref\.?|number|no\.?|#)\s*[:#]?\s*([A-Z0-9][A-Z0-9._/-]{0,79})'
        values = set(re.findall(pattern, invoice_text, flags=re.IGNORECASE))
        # A following PDF field label is not an identifier. Unknown layouts go
        # to review rather than inventing a reference or relying on filenames.
        values = {v.rstrip('.,;:') for v in values if any(ch.isdigit() for ch in v)}
        if len(values) > 1:
            return 'The invoice contains multiple ' + label.lower() + ' references. Use one invoice and its relevant contract/chat. Payment is blocked.'
        if values:
            references.append((label, values.pop()))
    if not references:
        return 'Could not identify an invoice or order reference in the invoice. Include a clearly labelled Invoice reference or Order reference so its contract/chat can be matched. Payment is blocked.'
    for _, value in references:
        if re.search(r'(?<![\w/-])' + re.escape(value) + r'(?![\w/-]|\.[\w])', context_text, flags=re.IGNORECASE):
            return None
    identified = ' '.join(label + ' reference: ' + value + '.' for label, value in references)
    return 'No matching context found for this invoice in the contract/chat. ' + identified + ' Upload the matching contract/chat or include the correct invoice/order reference. Payment is blocked.'


def decimal(value: str, label: str) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r'\d+(?:\.\d{1,6})?', value):
        raise GateError(f'{label} must be a non-negative plain decimal string.')
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise GateError(f'{label} is invalid.') from None
    if not result.is_finite() or result > Decimal('1000000000'):
        raise GateError(f'{label} is outside this demo’s supported range.')
    return result


def paisa(value: str, label='Amount') -> int:
    result = decimal(value, label) * 100
    if result != result.to_integral_value():
        raise GateError(f'{label} has fractions smaller than one paisa.')
    return int(result)


def numbers(text):
    return [Decimal(x.replace(',', '')) for x in re.findall(r'(?<![\w.-])\d+(?:,\d{3})*(?:\.\d+)?(?![\w.-])', text)]


def check_quote(e: Evidence, documents):
    if not e.quote.strip() or e.quote not in documents[e.document_id]:
        raise GateError(f'An evidence quote is not present verbatim in {e.document_id}.')
    if re.fullmatch(r'M\d+', e.reference):
        matching = [line for line in documents['context'].splitlines() if line.startswith(e.reference + ' |')]
        if e.document_id != 'context' or not any(e.quote in line for line in matching):
            raise GateError('Message evidence does not match its supplied message reference.')


def validate(analysis: Analysis, invoice_text: str, context_text: str, setup: dict):
    docs = {'invoice': invoice_text, 'context': context_text}
    inv = analysis.invoice
    critical = ['vendor_name', 'vendor_id', 'invoice_ref', 'order_ref', 'currency', 'account', 'purpose', 'discount', 'tax', 'total']
    for name in critical:
        evidence = getattr(inv.field_evidence, name)
        if not evidence or any(e.document_id != 'invoice' for e in evidence):
            raise GateError(f'Missing invoice evidence for {name}.')
        for e in evidence:
            check_quote(e, docs)
        quotes = '\n'.join(e.quote for e in evidence)
        value = getattr(inv, name)
        if name in {'discount', 'tax', 'total'}:
            amount = decimal(value, name)
            no_tax = name == 'tax' and amount == 0 and 'no separate tax line' in quotes.lower()
            if amount not in numbers(quotes) and not no_tax:
                raise GateError(f'The {name} amount is unsupported by its quote.')
        elif value not in quotes:
            raise GateError(f'The extracted {name} is unsupported by its quote.')
    for name in critical:
        group = getattr(inv.field_evidence, name)
        for e in group:
            check_quote(e, docs)
    line_total = 0
    for line in inv.lines:
        for e in line.evidence:
            if e.document_id != 'invoice':
                raise GateError('Invoice lines need invoice evidence.')
            check_quote(e, docs)
        quotes = '\n'.join(e.quote for e in line.evidence)
        q = decimal(line.quantity, 'Quantity')
        unit = paisa(line.unit_price, 'Unit price')
        amount = paisa(line.amount, 'Line amount')
        if q <= 0 or q * unit != amount:
            raise GateError('Quantity × unit price does not equal the printed line amount.')
        if line.pricing_basis == 'lump_sum' and q != 1:
            raise GateError('A flat charge must use quantity one.')
        required = [decimal(line.amount, 'Line amount'), decimal(line.unit_price, 'Unit price')]
        if line.pricing_basis == 'unit':
            required.append(q)
        if any(value not in numbers(quotes) for value in required) or line.description not in quotes:
            raise GateError('An invoice line description or amount lacks source support.')
        line_total += amount
    total = paisa(inv.total, 'Total')
    if total <= 0 or line_total - paisa(inv.discount, 'Discount') + paisa(inv.tax, 'Tax') != total:
        raise GateError('Invoice lines, discount and tax do not equal the printed total.')
    for finding in analysis.findings:
        for e in finding.evidence:
            check_quote(e, docs)
    if inv.currency != setup['currency']:
        raise GateError('Only the configured PKR demo currency is supported.')
    if inv.invoice_ref not in context_text or inv.order_ref not in context_text or setup['authorized_buyer']['id'] not in context_text:
        raise GateError('Context must identify this invoice/order and the supplied authorized buyer.')
    issues = []
    if inv.account != setup['approved_vendor']['account'] or inv.vendor_id != setup['approved_vendor']['vendor_id'] or inv.vendor_name != setup['approved_vendor']['name']:
        issues.append('Vendor or destination differs from the independent approved demo setup. Obtain independent confirmation before rechecking.')
    if any(f.status == 'ISSUE' for f in analysis.findings) or issues:
        state = 'HOLD'
    elif any(f.status == 'UNCLEAR' for f in analysis.findings) or analysis.clarification_needed:
        state = 'REVIEW'
    else:
        state = 'AWAITING_OWNER'
    return {'state': state, 'amount_minor': total, 'gate_messages': issues}
