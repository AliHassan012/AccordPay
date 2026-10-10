import hashlib
import hmac
import json
import secrets
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from schemas import Analysis
from gates import validate, GateError
from settings import database_path, trusted_setup


class PaymentBlocked(ValueError):
    pass


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def fingerprint(invoice, context, analysis):
    return digest(json.dumps({'invoice': invoice, 'context': context, 'analysis': analysis}, sort_keys=True, ensure_ascii=False))


class Store:
    def __init__(self, path=None, setup=None):
        self.path = Path(path or database_path())
        self.setup = setup or trusted_setup()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS balances (name TEXT PRIMARY KEY, amount INTEGER NOT NULL CHECK(amount >= 0));
            CREATE TABLE IF NOT EXISTS requests (
              id TEXT PRIMARY KEY, version INTEGER NOT NULL, status TEXT NOT NULL,
              current_token TEXT, created REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS snapshots (
              request_id TEXT NOT NULL, version INTEGER NOT NULL,
              invoice TEXT NOT NULL, context TEXT NOT NULL, analysis TEXT,
              amount_minor INTEGER, gate_messages TEXT NOT NULL, error TEXT,
              snapshot_hash TEXT NOT NULL, model TEXT NOT NULL, prompt_version TEXT NOT NULL,
              created REAL NOT NULL, PRIMARY KEY(request_id,version));
            CREATE TABLE IF NOT EXISTS approvals (
              token_hash TEXT PRIMARY KEY, request_id TEXT NOT NULL, version INTEGER NOT NULL,
              snapshot_hash TEXT NOT NULL, expires REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS transfers (
              id TEXT PRIMARY KEY, request_id TEXT NOT NULL UNIQUE, version INTEGER NOT NULL,
              vendor_id TEXT NOT NULL, invoice_ref TEXT NOT NULL, account TEXT NOT NULL,
              amount_minor INTEGER NOT NULL CHECK(amount_minor > 0), purpose TEXT NOT NULL,
              currency TEXT NOT NULL, owner_after INTEGER NOT NULL, vendor_after INTEGER NOT NULL,
              created REAL NOT NULL, UNIQUE(vendor_id,invoice_ref));
            CREATE TABLE IF NOT EXISTS notices (
              id INTEGER PRIMARY KEY, request_id TEXT NOT NULL, version INTEGER NOT NULL,
              kind TEXT NOT NULL, message TEXT NOT NULL, created REAL NOT NULL);
            CREATE TRIGGER IF NOT EXISTS immutable_snapshot_update BEFORE UPDATE ON snapshots
              BEGIN SELECT RAISE(ABORT, 'Saved snapshots are immutable'); END;
            CREATE TRIGGER IF NOT EXISTS immutable_snapshot_delete BEFORE DELETE ON snapshots
              BEGIN SELECT RAISE(ABORT, 'Saved snapshots are immutable'); END;
            ''')
            db.execute('INSERT OR IGNORE INTO balances VALUES (?,?)', ('owner', self.setup['demo_owner_balance_minor_units']))
            db.execute('INSERT OR IGNORE INTO balances VALUES (?,?)', ('vendor', self.setup['demo_vendor_balance_minor_units']))

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=20, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA busy_timeout=20000')
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def transaction(self):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                yield db
                db.commit()
            except Exception:
                db.rollback()
                raise

    def begin(self, request_id=None):
        with self.transaction() as db:
            if request_id:
                row = db.execute('SELECT * FROM requests WHERE id=?', (request_id,)).fetchone()
                if not row:
                    raise PaymentBlocked('Request not found.')
                if row['status'] == 'PAID':
                    raise PaymentBlocked('A paid request cannot be edited. Create a new unpaid invoice instead.')
                version = row['version'] + 1
                db.execute('UPDATE requests SET version=?, status=?, current_token=NULL WHERE id=?', (version, 'ANALYZING', request_id))
            else:
                request_id, version = secrets.token_urlsafe(18), 1
                db.execute('INSERT INTO requests VALUES (?,?,?,NULL,?)', (request_id, version, 'ANALYZING', time.time()))
        return request_id, version

    def finish(self, request_id, version, invoice, context, analysis, result, model, prompt_version, error=None):
        payload = analysis.model_dump() if analysis else None
        hash_value = fingerprint(invoice, context, payload)
        state = result['state']
        with self.transaction() as db:
            row = db.execute('SELECT * FROM requests WHERE id=?', (request_id,)).fetchone()
            if row['version'] != version or row['status'] != 'ANALYZING':
                raise PaymentBlocked('This analysis was superseded. Open the newest request version.')
            if state == 'AWAITING_OWNER' and analysis:
                inv = analysis.invoice
                if inv.invoice_ref in self.setup['prior_paid_invoices'] or db.execute('SELECT 1 FROM transfers WHERE vendor_id=? AND invoice_ref=?', (inv.vendor_id, inv.invoice_ref)).fetchone():
                    state = 'HOLD'
                    result['gate_messages'] = result.get('gate_messages', []) + ['This vendor invoice has already been paid.']
            db.execute('INSERT INTO snapshots VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (
                request_id, version, invoice, context,
                json.dumps(payload, ensure_ascii=False) if payload else None,
                result.get('amount_minor'), json.dumps(result.get('gate_messages', [])), error,
                hash_value, model, prompt_version, time.time()))
            token = None
            if state == 'AWAITING_OWNER':
                token = secrets.token_urlsafe(32)
                db.execute('INSERT INTO approvals VALUES (?,?,?,?,?)', (digest(token), request_id, version, hash_value, time.time() + 15 * 60))
            db.execute('UPDATE requests SET status=?,current_token=? WHERE id=?', (state, token, request_id))
            message = 'Owner review needed. Opening the link does not pay.' if state == 'AWAITING_OWNER' else 'Payment blocked. Review the findings, evidence and clarification.'
            db.execute('INSERT INTO notices(request_id,version,kind,message,created) VALUES (?,?,?,?,?)', (request_id, version, state, message, time.time()))
        return self.get(request_id)

    def get(self, request_id):
        with self.connection() as db:
            row = db.execute('SELECT r.*,s.invoice,s.context,s.analysis,s.amount_minor,s.gate_messages,s.error,s.snapshot_hash,s.model,s.prompt_version FROM requests r LEFT JOIN snapshots s ON s.request_id=r.id AND s.version=r.version WHERE r.id=?', (request_id,)).fetchone()
            if not row:
                return None
            result = dict(row)
            result['analysis'] = json.loads(result['analysis']) if result['analysis'] else None
            result['gate_messages'] = json.loads(result['gate_messages'] or '[]')
            receipt = db.execute('SELECT * FROM transfers WHERE request_id=?', (request_id,)).fetchone()
            result['receipt'] = dict(receipt) if receipt else None
            return result

    def balances(self):
        with self.connection() as db:
            return {r['name']: r['amount'] for r in db.execute('SELECT * FROM balances')}

    def history(self):
        with self.connection() as db:
            return [dict(r) for r in db.execute('SELECT * FROM transfers ORDER BY created DESC')]

    def inbox(self):
        with self.connection() as db:
            return [dict(r) for r in db.execute('SELECT n.*,r.status,r.current_token FROM notices n JOIN requests r ON r.id=n.request_id ORDER BY n.created DESC')]

    def receipt(self, receipt_id):
        with self.connection() as db:
            row = db.execute('SELECT * FROM transfers WHERE id=?', (receipt_id,)).fetchone()
            return dict(row) if row else None

    def verify_token(self, request_id, token, version):
        with self.connection() as db:
            row = db.execute('SELECT * FROM approvals WHERE token_hash=?', (digest(token),)).fetchone()
            req = db.execute('SELECT * FROM requests WHERE id=?', (request_id,)).fetchone()
            if not row or not req or row['request_id'] != request_id or row['version'] != version or req['version'] != version:
                raise PaymentBlocked('Invalid or outdated owner link. Open the current review.')
            if req['status'] != 'PAID' and row['expires'] < time.time():
                raise PaymentBlocked('Owner link expired. Reanalyze the saved inputs to obtain a new link.')

    def decide(self, request_id, version, token, passcode, expected_passcode, action='approve', fail_after_debit=False):
        if not expected_passcode or not passcode or not hmac.compare_digest(passcode.encode(), expected_passcode.encode()):
            raise PaymentBlocked('Owner passcode is missing or incorrect. No funds moved.')
        if action not in {'approve', 'reject'}:
            raise PaymentBlocked('Unknown owner decision.')
        with self.transaction() as db:
            req = db.execute('SELECT * FROM requests WHERE id=?', (request_id,)).fetchone()
            auth = db.execute('SELECT * FROM approvals WHERE token_hash=?', (digest(token),)).fetchone()
            if not req or not auth or auth['request_id'] != request_id or auth['version'] != version or req['version'] != version:
                raise PaymentBlocked('Invalid or outdated approval. No funds moved.')
            previous = db.execute('SELECT * FROM transfers WHERE request_id=?', (request_id,)).fetchone()
            if req['status'] == 'PAID' and previous:
                if action != 'approve':
                    raise PaymentBlocked('This request has already been paid; it cannot be rejected.')
                return dict(previous)
            if auth['expires'] < time.time():
                raise PaymentBlocked('Approval expired. Reanalyze before another owner review.')
            if req['status'] != 'AWAITING_OWNER':
                raise PaymentBlocked('This request is not ready for owner approval. No funds moved.')
            snap = db.execute('SELECT * FROM snapshots WHERE request_id=? AND version=?', (request_id, version)).fetchone()
            if not snap or auth['snapshot_hash'] != snap['snapshot_hash']:
                raise PaymentBlocked('The saved request no longer matches this approval.')
            payload = json.loads(snap['analysis']) if snap['analysis'] else None
            if fingerprint(snap['invoice'], snap['context'], payload) != snap['snapshot_hash']:
                raise PaymentBlocked('Saved request integrity check failed.')
            try:
                analysis = Analysis.model_validate(payload)
                checked = validate(analysis, snap['invoice'], snap['context'], self.setup)
            except (ValueError, GateError):
                raise PaymentBlocked('Saved evidence or money validation failed. No funds moved.') from None
            if checked['state'] != 'AWAITING_OWNER' or checked['amount_minor'] != snap['amount_minor']:
                raise PaymentBlocked('Saved request no longer passes payment checks.')
            inv = analysis.invoice
            if inv.invoice_ref in self.setup['prior_paid_invoices'] or db.execute('SELECT 1 FROM transfers WHERE vendor_id=? AND invoice_ref=?', (inv.vendor_id, inv.invoice_ref)).fetchone():
                raise PaymentBlocked('This vendor invoice has already been paid.')
            if action == 'reject':
                db.execute('UPDATE requests SET status=? WHERE id=?', ('REJECTED', request_id))
                return None
            owner = db.execute('SELECT amount FROM balances WHERE name=?', ('owner',)).fetchone()['amount']
            vendor = db.execute('SELECT amount FROM balances WHERE name=?', ('vendor',)).fetchone()['amount']
            amount = checked['amount_minor']
            if owner < amount:
                raise PaymentBlocked('Insufficient demo funds. No balances changed.')
            db.execute('UPDATE balances SET amount=amount-? WHERE name=?', (amount, 'owner'))
            if fail_after_debit:
                # Test-only dependency argument, never reachable from an HTTP form.
                raise RuntimeError('Controlled transfer fault for rollback verification')
            db.execute('UPDATE balances SET amount=amount+? WHERE name=?', (amount, 'vendor'))
            receipt_id = 'DEMO-' + secrets.token_hex(8).upper()
            db.execute('INSERT INTO transfers VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (receipt_id, request_id, version, inv.vendor_id, inv.invoice_ref, inv.account, amount, inv.purpose, inv.currency, owner-amount, vendor+amount, time.time()))
            db.execute('UPDATE requests SET status=? WHERE id=?', ('PAID', request_id))
            receipt = dict(db.execute('SELECT * FROM transfers WHERE id=?', (receipt_id,)).fetchone())
        return receipt
