# AccordPay: Railway trial setup

## 1. Check access first

Open https://railway.com and sign in with GitHub as AliHassan012. Complete signup yourself. Stay on the trial: do not add a card or upgrade to Hobby for this attempt. Open https://railway.com/verify and connect GitHub to request trial verification. Check whether Railway reports Full Trial or Limited Trial. Limited Trial restricts outbound internet, so successful Gemini access is not guaranteed. If verification fails or a card is required, stop and report the exact message instead of paying.

Railway offers new eligible users $5 of trial credit for up to 30 days or until spent; afterwards the Free plan has $1/month credit. This is usage credit, not a promise this app will run free indefinitely.
Official reference: https://docs.railway.com/pricing/free-trial

## 2. Connect the repository after verification

Click New Project > Deploy from GitHub repo. Select AliHassan012/AccordPay and branch main. If GitHub installation permissions are requested, grant access to this repository only where possible. Repository root is the app root; leave Root Directory empty. Railway detects the existing Dockerfile automatically. Leave build/start overrides empty: the Dockerfile installs requirements and starts Uvicorn on Railway's PORT. One instance/worker only. Set health check path to /health.

Docker reference: https://docs.railway.com/builds/dockerfiles

## 3. Private service variables

Open the AccordPay service > Variables. Enter values privately in Railway; never put them into GitHub or chat. On the laptop, the existing values are in prototype/.env (right-click > Open with > Notepad).

| Name | Value |
|---|---|
| GEMINI_API_KEY | Copy your private Gemini key from .env |
| DEMO_OWNER_PASSCODE | Copy your chosen demo passcode from .env |
| SESSION_SECRET | Copy the existing random SESSION_SECRET from .env |
| GEMINI_MODEL | gemini-3.5-flash-lite |
| COOKIE_SECURE | true |
| DATABASE_PATH | /app/runtime/demo.sqlite3 |

Generate the public URL under Settings > Networking > Generate Domain. Add BASE_URL as that exact https:// URL with no trailing slash, then apply/redeploy. BASE_URL must match the final domain before owner confirmation is tested. Do not add a second instance or scale horizontally with local SQLite.

Networking reference: https://docs.railway.com/networking/public-networking

## 4. Storage limitation and verification

The path above is writable by the existing container user but is not persistent without a volume. Redeployment/replacement can reset saved reviews, balances and receipts. Keep the local app as a backup. A volume can retain SQLite, but must be configured separately, checked against remaining trial credits and verified for container-user write permissions. Do not claim hosted restart persistence before that actual test. Do not mount a volume over /app or copy the laptop database to GitHub.

Volume reference: https://docs.railway.com/volumes

After deploy: open the assigned domain and /health. Run one fresh supported invoice, inspect evidence, then verify owner review and one fictional receipt. Test HOLD and REVIEW blocking. Record actual results and storage behavior in BUILD_STATUS.md, and add the verified URL to README/SUBMISSION_CHECKLIST. All inputs/accounts/money remain fictional. A successful build alone is not a working AI/approval demo.

## Current state

Repository preparation complete; Railway account access/verification, build, public domain, private variables, real hosted Gemini call and hosted payment smoke test are pending. Docker is unavailable locally, so container execution remains untested. No Railway service or paid plan has been created by the builder.
