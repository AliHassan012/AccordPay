from pathlib import Path
import secrets

root = Path(__file__).resolve().parent
target = root / '.env'
if not target.exists():
    text = (root / '.env.example').read_text(encoding='utf-8')
    text = text.replace('SESSION_SECRET=\n', 'SESSION_SECRET=' + secrets.token_urlsafe(48) + '\n')
    target.write_text(text, encoding='utf-8')
    print('Created private .env. Fill GEMINI_API_KEY and DEMO_OWNER_PASSCODE privately.')
else:
    print('Existing private .env preserved.')
