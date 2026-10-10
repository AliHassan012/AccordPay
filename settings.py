import json
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent


def settings():
    # Reload private local values so saving .env does not require a restart.
    load_dotenv(ROOT / '.env', override=True)
    return {
        'key': os.getenv('GEMINI_API_KEY', '').strip(),
        'passcode': os.getenv('DEMO_OWNER_PASSCODE', '').strip(),
        'model': os.getenv('GEMINI_MODEL', 'gemini-3.5-flash-lite').strip(),
        'base_url': os.getenv('BASE_URL', 'http://127.0.0.1:8000').rstrip('/'),
        'cookie_secure': os.getenv('COOKIE_SECURE', 'false').lower() == 'true',
    }


def database_path():
    load_dotenv(ROOT / '.env', override=True)
    value = Path(os.getenv('DATABASE_PATH', 'runtime/demo.sqlite3'))
    return value if value.is_absolute() else ROOT / value


def trusted_setup():
    return json.loads((ROOT / 'assets' / 'shared_company_setup.json').read_text(encoding='utf-8'))


def session_secret():
    load_dotenv(ROOT / '.env', override=True)
    return os.getenv('SESSION_SECRET') or secrets.token_urlsafe(48)
