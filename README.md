# AccordPay — BroGrammers

An invoice review prototype for fictional DEMO FUNDS. Exactly three language checks: included costs charged again, actual extra approval, and later corrections/cancellations. AI interprets wording; ordinary code validates evidence/money and executes one atomic demo transfer after explicit owner confirmation.

## Submission materials

- Repository: https://github.com/AliHassan012/AccordPay
- Presentation: [AccordPay Demo](submission/AccordPay_Demo.pptx)
- PDF test inputs: [12 invoice/contract pairs](delivery/INVOICES_AND_CONTRACTS_12/)
- Deployment instructions: [Render Free setup](DEPLOYMENT.md)
- Hosted URL: pending deployment and smoke test.

The presentation includes current development evidence and labels the older evaluation as historical. Earlier walkthrough videos use the former product name and clearly labelled saved AI replays. They remain local optional submission materials, not proof of current live analysis.

## Windows: run the app

1. Open the app folder (the repository root after downloading from GitHub) in File Explorer.
2. On this laptop dependencies are installed. Double-click **start.cmd**.
3. Leave its terminal window open. Open **http://127.0.0.1:8000** in a browser.
4. Click **D03**, then **Analyze with live AI**. Review the quotes and saved exact payment details.
5. Click **Open owner review**, enter the passcode you set privately, and confirm or reject.
6. A confirmed supported D03 transfers PKR 25,000 of fictional funds: owner 500,000 → 475,000; vendor 0 → 25,000. Repeating approval gives the same receipt.
7. Try **D07** for a corrected charge (HOLD), and **D04** for tentative approval (REVIEW). Both block payment.

For a fresh Windows computer with Python 3.12 available, double-click **setup.cmd** first. It creates an isolated `.venv`, installs the exact versions in `requirements.txt`, and creates `.env` without overwriting an existing one. The script also detects this Codex laptop's bundled Python. On a computer without Python, install Python 3.12 from python.org and enable its PATH option before setup. No Node/React build is needed.

Equivalent commands from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe init_env.py
.\.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000 --no-access-log
```

## Private settings

Open **.env** in this folder. Enter the Gemini key after `GEMINI_API_KEY=` and a password you choose after `DEMO_OWNER_PASSCODE=`. Never paste either into chat, screenshots, HTML or a repository. Save with Ctrl+S. Private values reload on each analysis/owner decision. Model, session-secret, database-path and hosting-origin changes should be followed by a server restart.

`GEMINI_MODEL` selects one actual Gemini model. Development began with `gemini-3.5-flash-lite`; malformed output/message-reference failures justified comparison with `gemini-3.8-flash`. The latest PDF troubleshooting switched back to Flash-Lite after verifying new development cases. Read BUILD_STATUS.md for current evidence. The provider uses the official `google-genai` Interactions API, a simplified supported JSON Schema, and full local Pydantic validation. Low thinking is configured. The historical evaluation freeze is preserved separately; it does not cover the latest development revision.

If analysis fails, read the specific message. A timeout or unavailable message means Gemini did not complete the request; wait briefly and click Edit / recheck inputs once. Analysis can take up to two minutes. A 429 message means check project limits in Google AI Studio. A rejected-key/access message means check the private key and project permissions. Do not paste keys into chat. Errors block payment. Refreshing an old result shows its saved error; use recheck to make a new request.

If the contract/chat has no matching invoice or order reference, the app immediately shows REVIEW with "No matching context found for this invoice in the contract/chat". Upload the matching documents or include the correct reference. This check does not call Gemini. Matching references still need live analysis and the existing approval/payment checks.

All three findings need original quotes. Critical fields and invoice arithmetic must pass code checks. An API error, malformed response or unsupported evidence blocks owner readiness; there is no preset answer fallback. The provider timeout is 120 seconds; an independent subprocess limit stops the entire operation after 125 seconds, including stalled SDK cleanup.

Current local model: `gemini-3.5-flash-lite`. It passed live development checks on PDF pairs 04 (REVIEW), 02 (AWAITING_OWNER), and 06 (HOLD) in about 5–6 seconds after the previous model timed out. This is a new development configuration; historical reserved evaluation scores apply only to the original frozen model/prompt. The prompt now explicitly preserves source punctuation in quotes and excludes separately printed dates from message-line citations. Exact evidence validation remains required. Old saved ERROR pages remain saved results: use **Edit / recheck inputs** and Analyze again to make a fresh request.

The original project's free daily allowance was exhausted. A privately supplied replacement key subsequently passed a real request and the complete browser D03 transfer; D07 HOLD and D04 REVIEW also worked. Failures and slow calls still occur and block payment; recheck the saved inputs if needed. BUILD_STATUS.md records current evidence. Changing hosting or GitHub login does not solve provider quota. Do not present old saved results as new live calls.

## Inputs and demo inbox

Paste one invoice and one short buyer-maintained deal/messages record, or upload UTF-8 TXT / selectable-text PDF. Use text OR a file for each input. Limit each file to 2 MB, PDF to 20 pages, and each extracted input to 40,000 characters. No OCR or scanned-PDF support. Filenames are never used as saved filesystem paths. Raw inputs and analysis are stored in SQLite.

Examples D01–D09 contain raw development documents only. Selection loads text; clicking Analyze makes a fresh live request. Saved review pages are labelled replays. Reserved cases/answer keys are excluded from app assets and Docker. The **Demo inbox** contains actual stored in-app notices; it does not send real email.

## Verify and reset

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe verify_live.py D01
```

Tests use controlled model stubs for payment/gate/HTTP tests; they are not live-AI accuracy evidence. `verify_live.py` sends only raw development documents to Gemini and saves actual results under runtime/live-checks/. Check BUILD_STATUS.md for observed tests, live failures and browser evidence. A file's existence is not a passed test.

To reset: press **Ctrl+C** in the app terminal, then double-click **reset-demo.cmd** and follow its message. Or run:

```powershell
.\.venv\Scripts\python.exe reset_demo.py --confirm
```

Previous fictional state is archived under runtime/backups/. Reset restores owner PKR 500,000 and vendor PKR 0, clears current history, and verifies the result. Restart start.cmd. Reset is a local command, never a public endpoint. Do not reset while a teammate is approving a request.

## Payment protections

Owner POST requires the private passcode, signed-session CSRF check, random request/version-bound token and unexpired approval (15 minutes). GET never pays. New input analysis invalidates old approval. The server rereads immutable saved data and revalidates quotes/arithmetic/trusted account before any transfer; browser amount/account fields cannot override it. One SQLite transaction rechecks funds and duplicate vendor/invoice, debits, credits, writes a unique receipt and marks PAID. Any failure rolls back. Retry of a completed request returns the same receipt.

The in-app browser's opaque Origin:null is supported only for loopback local development after signed-session CSRF validation. Hosted null/foreign origins are rejected. HTTPS hosting requires `COOKIE_SECURE=true` and the exact public `BASE_URL`.

## Deployment preparation — nothing published yet

There is no required GitHub/hosting access for local use. To publish later, first supply/authorize the exact destination. Then:

1. Use the repository root as the build root. Commit source, assets and tests; `.gitignore` excludes `.env`, runtime databases, virtual environment, and results. Inspect the staged files before any push. Never publish the parent handoff's evaluation-only folder.
2. Deploy a single Python web-service instance or the included Dockerfile. Python build command: `pip install -r requirements.txt`. Start: `uvicorn app:app --host 0.0.0.0 --port $PORT --no-access-log` (use port 8000 if the host supplies no PORT).
3. Set server-only secrets `GEMINI_API_KEY`, `DEMO_OWNER_PASSCODE`, `SESSION_SECRET`. Configure `GEMINI_MODEL`, exact HTTPS `BASE_URL`, `COOKIE_SECURE=true`, and `DATABASE_PATH` on a writable path. Never commit private `.env`.
4. Use persistent storage for SQLite (Docker default `/data/demo.sqlite3`, mount `/data`). If hosting storage is ephemeral, requests/balances/receipts can disappear on restart. Disclose that and keep the local backup. Use one worker/instance; no distributed SQLite writes.
5. Open `/health`, then test live D03 analyze → owner → receipt and D07 HOLD from another browser. Verify persisted balances after restart. A URL alone does not establish a working deployment.

Docker files are prepared but must be build-tested where Docker is available. Public URL/repository destination and hosted smoke test remain pending until authorized. No real-bank transfer, identity authentication, production fraud validation or numeric security probability is claimed.

## Team

Ali starts the app and controls private setup. Asad reviews whether exact quotes actually support meaning. Adil tests owner decision/repeat clicks/balances. Moeez checks clarity and rehearses. See DEMO_SCRIPT.md; PPTX and a backup recording must use the actual verified app/results.
