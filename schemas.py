from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Evidence(StrictModel):
    document_id: Literal['invoice', 'context']
    reference: str = Field(min_length=1, max_length=160, description='For a message, its exact ID (M1, M2, etc). Each quote must belong to THAT message only. Otherwise use Invoice or Deal record.')
    quote: str = Field(min_length=1, max_length=4000)


class Line(StrictModel):
    description: str = Field(min_length=1, max_length=300)
    pricing_basis: Literal['unit', 'lump_sum']
    quantity: str = Field(description='Positive plain decimal string, e.g. 2. Use 1 for a flat/lump-sum charge.')
    unit_price: str = Field(description='Money as digits and optional decimal point only, e.g. 10000. No commas/currency/text.')
    amount: str = Field(description='Printed line amount as plain decimal string, e.g. 20000. Do not recompute or repair.')
    evidence: list[Evidence] = Field(min_length=1)


class FieldEvidence(StrictModel):
    vendor_name: list[Evidence] = Field(min_length=1)
    vendor_id: list[Evidence] = Field(min_length=1)
    invoice_ref: list[Evidence] = Field(min_length=1)
    order_ref: list[Evidence] = Field(min_length=1)
    currency: list[Evidence] = Field(min_length=1)
    account: list[Evidence] = Field(min_length=1)
    purpose: list[Evidence] = Field(min_length=1)
    discount: list[Evidence] = Field(min_length=1)
    tax: list[Evidence] = Field(min_length=1)
    total: list[Evidence] = Field(min_length=1)


class Invoice(StrictModel):
    vendor_name: str = Field(min_length=1)
    vendor_id: str = Field(min_length=1)
    invoice_ref: str = Field(min_length=1)
    order_ref: str = Field(min_length=1)
    currency: str = Field(min_length=1)
    account: str = Field(min_length=1)
    purpose: str = Field(min_length=1, max_length=300)
    lines: list[Line] = Field(min_length=1, max_length=30)
    discount: str = Field(description='Plain decimal string only. An explicit zero discount is "0".')
    tax: str = Field(description='Plain decimal string only. If invoice explicitly says no separate tax line, return "0", NOT that sentence. Put the sentence in field_evidence.tax.')
    total: str = Field(description='Printed total as a plain decimal string, e.g. "25000". No commas or currency.')
    field_evidence: FieldEvidence


class Finding(StrictModel):
    check: Literal['COST_COVERAGE', 'APPROVAL_MEANING', 'LATEST_UPDATE']
    status: Literal['SUPPORTED', 'ISSUE', 'UNCLEAR']
    explanation: str = Field(min_length=1, max_length=2000)
    evidence: list[Evidence] = Field(min_length=1)


class Analysis(StrictModel):
    invoice: Invoice
    findings: list[Finding] = Field(min_length=3, max_length=3)
    clarification_needed: list[str]

    @model_validator(mode='after')
    def three_unique_checks(self):
        if {x.check for x in self.findings} != {'COST_COVERAGE', 'APPROVAL_MEANING', 'LATEST_UPDATE'}:
            raise ValueError('Exactly the three distinct required checks must be present.')
        return self
