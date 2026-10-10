# AccordPay: Render Free deployment

Repository: https://github.com/AliHassan012/AccordPay

Render Free can run this Python/FastAPI demo. Its filesystem is temporary: saved reviews, fictional balances and receipts disappear on restart, redeploy or idle spin-down. Free services sleep after 15 minutes without traffic; waking takes about one minute. Keep the local app as the reliable rehearsal backup. This free deployment does not satisfy restart persistence for the hosted database; local SQLite persistence is tested. Use a paid persistent disk later if retaining hosted history is required.

Official limitations: https://render.com/docs/free

## Beginner steps

1. Create or sign in to a Render account at https://dashboard.render.com. Complete any account/terms steps yourself.
2. Select New > Web Service. Connect GitHub and select AliHassan012/AccordPay, or use its public repository URL.
3. Name: accordpay. Branch: main. Root directory: leave empty. Runtime: Python 3.
4. Build command: pip install -r requirements.txt
5. Start command: uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1 --no-access-log
6. Instance type: Free. Do not select a paid plan or add a paid disk.
7. Enter private environment variables in Render, never in GitHub:
   - GEMINI_API_KEY: your Gemini key
   - DEMO_OWNER_PASSCODE: your chosen demo owner passcode
   - SESSION_SECRET: a randomly generated secret (use Render Generate)
   - GEMINI_MODEL: gemini-3.5-flash-lite
   - COOKIE_SECURE: true
   - DATABASE_PATH: runtime/demo.sqlite3
   - PYTHON_VERSION: 3.12.14
   - BASE_URL: the exact assigned HTTPS URL, without a trailing slash
8. Deploy. If Render only reveals its assigned URL after deployment, then set BASE_URL to that exact URL and redeploy. The owner flow must not be tested until BASE_URL is correct.
9. Visit /health on the assigned URL; verify the page opens. Test a supported invoice through owner review and one fictional transfer. Then test HOLD and REVIEW. Check the receipt/history. Never claim hosted restart persistence on the Free plan.
10. Put the verified URL into README and SUBMISSION_CHECKLIST.md before final submission.

The app sends documents to Gemini only when Analyze is clicked and references match. Gemini usage/quota is separate from free hosting. Public visitors can consume the configured API quota by submitting inputs; use a demo-only key with suitable provider limits and only fictional data. The owner passcode stays server-side. No real bank transfer or real email occurs.

## Deployment state

Prepared, not deployed. No destination/service was created, no public URL is claimed, and Docker build remains untested where Docker is unavailable.
