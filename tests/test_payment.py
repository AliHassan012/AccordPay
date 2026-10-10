from concurrent.futures import ThreadPoolExecutor
import sqlite3
import pytest
from conftest import ready
from store import Store, PaymentBlocked

PASSCODE = 'test-owner-only'

def pay(store, row, **kwargs):
    return store.decide(row['id'], row['version'], row['current_token'], PASSCODE, PASSCODE, **kwargs)

def unchanged(store):
    assert store.balances() == {'owner': 50000000, 'vendor': 0}
    assert store.history() == []

def test_transfer_persists_and_repeated_approval_has_same_receipt(store, sample):
    row = ready(store, sample)
    receipt = pay(store, row)
    assert receipt['amount_minor'] == 2500000
    assert store.balances() == {'owner': 47500000, 'vendor': 2500000}
    reopened = Store(store.path, store.setup)
    assert reopened.balances() == store.balances()
    assert pay(reopened, row)['id'] == receipt['id']
    assert len(reopened.history()) == 1

def test_concurrent_repeat_has_exactly_one_transfer(store, sample):
    row = ready(store, sample)
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda _: pay(store, row), range(6)))
    assert len({x['id'] for x in results}) == 1
    assert store.balances() == {'owner': 47500000, 'vendor': 2500000}
    assert len(store.history()) == 1

def test_rejection_is_final_and_does_not_move_funds(store, sample):
    row = ready(store, sample)
    assert pay(store, row, action='reject') is None
    assert store.get(row['id'])['status'] == 'REJECTED'
    with pytest.raises(PaymentBlocked):
        pay(store, row)
    unchanged(store)

@pytest.mark.parametrize('passcode,token', [('', None), ('wrong', None), (PASSCODE, 'wrong-token')])
def test_owner_verification_cannot_be_bypassed(store, sample, passcode, token):
    row = ready(store, sample)
    with pytest.raises(PaymentBlocked):
        store.decide(row['id'], row['version'], token or row['current_token'], passcode, PASSCODE)
    unchanged(store)

@pytest.mark.parametrize('state', ['HOLD','REVIEW','ERROR','REJECTED','ANALYZING'])
def test_state_blocking_is_server_side(store, sample, state):
    row = ready(store, sample)
    with store.connection() as db:
        db.execute('UPDATE requests SET status=? WHERE id=?', (state, row['id']))
    with pytest.raises(PaymentBlocked):
        pay(store, row)
    unchanged(store)

def test_expired_approval_cannot_pay(store, sample):
    row = ready(store, sample)
    with store.connection() as db:
        db.execute('UPDATE approvals SET expires=0')
    with pytest.raises(PaymentBlocked, match='expired'):
        pay(store, row)
    unchanged(store)

def test_edit_invalidates_previous_approval_before_new_analysis(store, sample):
    row = ready(store, sample)
    request_id, version = store.begin(row['id'])
    assert version == 2
    with pytest.raises(PaymentBlocked):
        pay(store, row)
    with pytest.raises(PaymentBlocked):
        store.verify_token(row['id'], row['current_token'], 1)
    unchanged(store)

def test_insufficient_funds_changes_nothing(store, sample):
    row = ready(store, sample)
    with store.connection() as db:
        db.execute('UPDATE balances SET amount=10000 WHERE name=?', ('owner',))
    with pytest.raises(PaymentBlocked, match='Insufficient'):
        pay(store, row)
    assert store.balances() == {'owner': 10000, 'vendor': 0}
    assert not store.history()
    assert store.get(row['id'])['status'] == 'AWAITING_OWNER'

def test_fault_between_debit_and_credit_rolls_back_everything(store, sample):
    row = ready(store, sample)
    with pytest.raises(RuntimeError):
        pay(store, row, fail_after_debit=True)
    unchanged(store)
    assert store.get(row['id'])['status'] == 'AWAITING_OWNER'
    assert pay(store, row)['amount_minor'] == 2500000

def test_duplicate_invoice_in_another_request_cannot_pay_twice(store, sample):
    first, second = ready(store, sample), ready(store, sample)
    pay(store, first)
    with pytest.raises(PaymentBlocked, match='already been paid'):
        pay(store, second)
    third = ready(store, sample)
    assert third['status'] == 'HOLD'
    assert len(store.history()) == 1

def test_changed_trusted_account_blocks_old_approval(store, sample):
    row = ready(store, sample)
    store.setup['approved_vendor']['account'] = 'DEMO-DIFFERENT-ACCOUNT'
    with pytest.raises(PaymentBlocked):
        pay(store, row)
    unchanged(store)

def test_saved_snapshot_is_immutable_and_approval_is_bound_to_hash(store, sample):
    row = ready(store, sample)
    with store.connection() as db:
        with pytest.raises(sqlite3.IntegrityError, match='immutable'):
            db.execute('UPDATE snapshots SET amount_minor=1')
        db.execute('UPDATE approvals SET snapshot_hash=?', ('tampered',))
    with pytest.raises(PaymentBlocked):
        pay(store, row)
    unchanged(store)
