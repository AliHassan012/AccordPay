## Railway preparation — 10 October 2026

Render deployment repeatedly requested a card despite the user selecting Free $0/month. User chose to try Railway. Added RAILWAY_SETUP.md with GitHub trial verification, existing Dockerfile deployment, private variables, domain/BASE_URL, health check and honest ephemeral SQLite limitation. Railway eligibility and full outbound access depend on account verification; no unrestricted Gemini access or perpetual free hosting promised. No app, model, prompt, money gate, credential or local balance change. Existing Dockerfile preserved. Docker/railway CLIs are unavailable locally; container execution and Railway hosted flow remain UNTESTED. Official Railway docs reviewed, including current trial $5/up to30 days and restricted Limited Trial. Next: user signs in with GitHub and reports Full Trial or Limited Trial before we configure the hosted service. Deployed URL remains pending.

## AccordPay GitHub submission checkpoint — 10 October 2026

- User selected AccordPay and authorized publication to https://github.com/AliHassan012/AccordPay. Product branding updated in app, templates, README, startup check and demo script. Original documents and prior presentations retained.
- Published app at repository root, with source, exact requirements, Windows setup/start/reset scripts, tests, 24 fictional invoice/contract PDFs, deployment instructions and submission checklist. Clean checkout: submission/AccordPay. Private .env, virtual environment, runtime SQLite/uploads and evaluation data were excluded. Private-value scan: 91 deliverable files checked, zero matches or forbidden files.
- GitHub connector reads succeeded but the first Contents write returned 403 Resource not accessible by integration. CLI gh login is expired. Git Credential Manager dry-run succeeded, and normal git push uploaded main successfully. Remote main matched local commit b03ae6e before this documentation update. No force push or unrelated repository change.
- Exact repository package tests: 66 PASS in 6.06 seconds, one existing dependency warning. No new provider request or fictional transfer during repository publication.
- Updated five-slide submission/AccordPay_Demo.pptx imported from prior deck, preserving design. All five rendered slides visually inspected; final structural/layout/font/import checks PASS with zero findings. PowerPoint opening and timed human rehearsal still UNTESTED. Historical receipt screenshot remains visibly from earlier product branding, documented in notes. Latest slide distinguishes current three PDF development checks and historical evaluation.
- Two optional MP4 walkthroughs uploaded under submission/videos. They retain the old product name, edited scenes and clearly labelled saved AI replays; not presented as current live AI screen recordings. Existing walkthrough provenance README included. Optional journey video not created.
- Free-host recommendation: Render Free can run this app without a database rewrite, but its SQLite state is lost after restart/redeploy/spin-down. DEPLOYMENT.md gives exact setup and disclosure. Vercel supports FastAPI but local SQLite is unsuitable for shared persistent approvals/receipts; an external database migration would be required. No hosted service created or deployed link claimed.
- Browser branding checkpoint: previous local server was stopped; started the existing app again without resetting SQLite. Fresh browser tab shows AccordPay and persisted owner PKR475,000/vendor PKR25,000. Screenshot runtime/screenshots/accordpay-branding.png retained locally; no new AI call or payment.
- Unfinished: choose/sign in to hosting, deploy and test the public URL; remaining nine PDF live cases, fresh independent evaluation, teammate evidence review and five-minute rehearsal. Organizer deadline is Saturday night, 10 October 2026; exact cutoff not supplied. Next action: user chooses hosting account; configure private values in that host, verify supported/HOLD/REVIEW flows, then add the verified deployed URL to submission docs.

## Current checkpoint: Pair 04 timeout repair — 10 October 2026

- Current local model: **gemini-3.5-flash-lite**, low thinking, prompt/schema/config version **b306d6ae5ed5793b**. Private .env model setting and .env.example updated; existing credentials preserved. Settings reload on the next request, so no restart was required.
- Diagnosis: configured gemini-3.8-flash timed out even on a minimal real request (21.1 seconds with a 20-second diagnostic bound). Flash-Lite access was confirmed by a real metadata request. This demonstrates latency failure, not proof of exhausted quota or invalid credentials.
- Initial Flash-Lite Pair04 response took 5.3 seconds but failed exact invoice evidence because it removed commas from an amount quote. A subsequent 5.7-second response preserved commas but included the separately printed date in an M3 quote, failing message-line validation. Both were safely blocked. Prompt now explicitly separates numeric extraction formatting from verbatim quote formatting, and excludes preceding dates from M-number citations. Validators, schema, arithmetic, owner verification and transfer logic were not weakened.
- Final real PDF development checks: Pair04 **REVIEW**, 6.1 seconds, approval UNCLEAR; Pair02 **AWAITING_OWNER**, 5.0 seconds; Pair06 **HOLD**, 5.0 seconds, latest cancellation ISSUE. All three passed existing evidence and money gates with no gate messages. Actual outputs saved in runtime/pair04-fast-model-quote-fix.json, pair02-fast-model-quote-fix.json and pair06-fast-model-quote-fix.json. These cases have been used for development, not held-out evaluation.
- Actual browser recheck of the user's saved Invoice04/Contract04 request zh0n4t9-vMDlcQnAG9AdTHir completed successfully: version2 REVIEW, PKR15,000, three findings visible, exact M3 tentative wording shown, clarification requested, no payable owner link. Previous version1 timeout remains saved. Screenshot: runtime/screenshots/pair04-timeout-fixed.png. The live click returned in about 13 seconds (browser interaction wall time, not provider-only latency).
- Regression command: .venv/Scripts/python.exe -m pytest -q --basetemp=runtime/pytest-fast-model-check: **66 PASS in 6.28 seconds**, one existing Starlette/httpx deprecation warning. No transfer performed during this repair. Persisted owner PKR475,000/vendor PKR25,000, one prior transfer.
- Original frozen prompt saved before editing at runtime/prompt-before-timeout-fix.txt. Original evaluation scores/configuration remain historical and do not validate this new model/prompt. README documents the current model and correct 120-second provider / 125-second subprocess limits.
- Unfinished: full 12-pair live run and fresh independent evaluation of this revision, teammate review of quote meaning, hosted deployment and public destination remain pending. Three targeted live checks and the browser success do not guarantee all future API requests will succeed. Next: test remaining matching PDF pairs and review their evidence; on an old ERROR page use Edit / recheck inputs and click Analyze once.

# BUILD_STATUS — Before You Pay

## Missing contract/chat context check - 10 October 2026

Added context_reference_check in gates.py, called by app.py before the provider. Clearly labelled invoice/order references are read from invoice text and looked for as complete references in the contract/chat, without relying on uploaded filenames. If neither appears, a saved REVIEW explains "No matching context found for this invoice in the contract/chat", identifies the invoice/order, asks for matching records and blocks payment. Unreadable/ambiguous references also require clarification. A matching reference only permits existing Gemini analysis and payment gates to continue; it does not establish approval or semantic relevance. The three main language checks remain unchanged.

Actual validation: full suite 66 PASS after repairing initial punctuation-boundary and test whitespace issues. Tests cover missing context, similar reference prefixes, order-only linkage, unknown layout, actual Invoice_07.pdf + Contract_01.pdf without calling a provider, and all 12 matching pairs passing linkage alone. Matching-pair AI outcomes are not claimed. The app restarted (PID26540). Browser upload from the user's exact AICON/demo-data/INVOICES_AND_CONTRACTS_12 folder produced saved request cViNV9L7q4uGF8xo0ZO5f6gL: REVIEW with the requested message, no owner approval link, no Gemini call. Screenshot runtime/screenshots/no-matching-context.png. Existing balances preserved. Review footer now distinguishes a saved precheck result from AI analysis; intake no longer claims every submission calls Gemini. Provider availability for linked requests remains unresolved as recorded below. Next action: retry the mismatched pair or use Edit / recheck inputs; old saved timeout results retain their history until rechecked.

## Gemini error diagnosis and clearer failures - 10 October 2026

User reported the generic live-analysis error while uploading the PDF test data. Rechecked the latest saved fictional request: Interactions raised APITimeoutError at the original 60-second limit; repeating with 120 seconds also timed out. A separate model metadata request succeeded with the current private key/model, confirming current authentication/model access. A diagnostic GenerateContent call using the same input/schema/model returned a ServerError after 120.3 seconds. This alternate route was diagnostic only; production remains Interactions. Successful live analysis retry is NOT verified. Current provider generation availability is the remaining blocker; no evidence that a new key is needed, and no new quota exhaustion was observed.

Changes: analyzer.py maps provider HTTP codes, connection/timeouts and invalid output to fixed actionable messages. analyzer_worker.py transports only an allowlisted failure category, never raw SDK exception text. Parent preserves that category instead of discarding it. HTTP timeout is now 120 seconds with a 125-second subprocess cap. intake.html explains the two-minute wait and single-click workflow. No prompt/model/schema, owner gate or transfer logic changes. Existing failed snapshots retain their original messages; rechecking creates a new version.

Verification: reviewed local full suite 59 PASS; provider subset 10 PASS after defensive category-type handling. Earlier restricted full runs stalled on Windows sandbox behavior; those identified test processes were stopped and are not counted as passes. Uvicorn restarted with the updated code (PID30552), home screen and unchanged balances (owner475,000/vendor25,000) verified in the browser. Diagnostics made no transfers. Exact next action: use Edit / recheck inputs once after a short wait; if the new timeout/unavailable message persists, retry when Gemini service responds. Historical successful runs and evaluation scores are preserved and not claimed as current availability checks.

## Simplified PDF delivery - supersedes the earlier dataset pack

Following the user's correction, the current dataset is `delivery/INVOICES_AND_CONTRACTS_12.zip`, with the same unzipped folder beside it. Exactly 24 PDFs in one flat folder: Invoice_01.pdf through Invoice_12.pdf and Contract_01.pdf through Contract_12.pdf. No Excel, guide, results log or answer key in this delivery. Contracts contain structured parties/order/price/inclusions/payment terms plus the dated authorization/amendment record needed by the app's three language checks. Each pair has matching new INV-PDF12 / ORDER-PDF12 references. Earlier pack preserved but superseded.

Actual checks: all 24 PDFs are single-page selectable-text documents below 2 MB; matching references and complete M-reference lines verified using pypdf. All 24 pages rendered with Poppler and visually reviewed. ZIP integrity PASS, exactly 24 files. Case 11 deliberately has an incorrect invoice total; case 12 deliberately has a changed account. Coverage also includes clear approvals, included costs charged again, tentative approval, refusal, later cancellation/correction, wrong-order approval, supplier assertion and fulfilled approval conditions. No Gemini requests made for this pack; website results remain UNTESTED. No app/prompt/payment changes. Files excluded from Docker runtime. Next action: upload an invoice and the contract bearing the same number to the website.

## Two MP4 walkthroughs - 10 October 2026

- User requested an approved-payment video and a not-approved-payment video. Main app source, prompt and provider configuration unchanged.
- Current-task live D03 passed; browser owner approval committed DEMO-72D8CC797DFB4BA7, owner PKR475,000/vendor PKR25,000. Two current-task live D07 attempts timed out and blocked payment; saved versions retained. No new successful D07 live check is claimed.
- Final filming uses an isolated recording copy, visibly labelled VIDEO DEMO: SAVED AI REPLAY. D03 replays the genuine current-task saved result; D07 replays the earlier genuine runtime/live-checks/D07.json result. The button says Review saved AI result. This is an edited walkthrough, not a new live-AI recording.
- Actual app validation, owner confirmation and fictional transfer ran against separate output/demo_videos/recording-demo.sqlite3. D03 PAID with receipt DEMO-C86DDF466C5A8976; D07 HOLD with no transfer. Saved records verified one transfer, owner PKR475,000/vendor PKR25,000. Recording copy restarted during filming; paid state persisted.
- Initial D07 replay returned REVIEW because browser line endings differed from the original saved source. That snapshot is retained. Recording-only helper restores original text-file line endings; product gates and saved AI quotes are unchanged. Version2 passes evidence validation and returns HOLD.
- Deliverables: output/demo_videos/payment_approved.mp4 and payment_not_approved.mp4, 1080p with simple English narration/captions. Scenes visually inspected; complete MP4 playback decoded successfully. Provenance and checks are in output/demo_videos/README.md, workflow_verification.json and video_validation.json.
- Videos explicitly show demo inbox notices. No real email or real money transfer happened. Owner password is masked.

## Added dataset delivery - 10 October 2026, 17:53 Pakistan time

User-requested new 12-case synthetic pack: `delivery/TEST_CASES_12/`, packaged as `delivery/TEST_CASES_12.zip`. Contains 12 distinct project folders, each with one invoice PDF and one deal/messages PDF, plus `Case_Index.xlsx`, `START_HERE.pdf`, and separate `reviewer_only/Expected_Results.pdf`. Unique invoice/order references use INV-T12 / ORDER-T12. English and Roman Urdu messages use the existing fictional vendor V001 and buyer OWNER-01. Coverage: base purchase, approved optional fee, included cost billed again, tentative wording, refusal, cancellation, corrected amount, wrong order, supplier assertion, satisfied condition, arithmetic mismatch and changed account.

Actual document checks: all 24 inputs are single-page selectable-text PDFs below the upload limit; required invoice fields and complete single-line M-reference messages verified with pypdf. Embedded TrueType fonts verified in all 26 PDFs. All 28 PDF pages rendered with Poppler and visually inspected. Both Excel sheets rendered and visually inspected; typed invoice amounts match source data, 12 results rows remain blank, two table filters/two dropdowns/frozen log headings verified in saved XLSX. Formula-error scan matched 0 entries. ZIP integrity PASS, exactly 27 deliverable files; authoring scripts/QA files excluded. Builder evidence is in runtime/dataset-build/qa/delivery-checks.json.

C11 is intentionally the only arithmetic mismatch (printed 27,000 versus calculated 25,000). C12 intentionally changes destination from trusted account A to account B. Reviewer expectations are manual design targets: 3 AWAITING_OWNER, 5 HOLD, 4 REVIEW. Actual Gemini runs on this pack: 0; new-case app outcomes, teammate interpretation review and native Microsoft Excel opening remain UNTESTED. No new API key or permission requested and no quota consumed. App prompt, model and payment logic unchanged. Pack and reviewer key excluded from Docker runtime. Next action: team uploads matching pairs, compares quotes/meaning to the separate reviewer key, and records observed states in Run log. Earlier implementation and evaluation evidence below is preserved.

Implementation checkpoint last updated: 10 October 2026, approximately 16:25 Pakistan time
Elapsed build time: approximately 2 hours 40 minutes of wall time since initial implementation, including interruptions. Earlier checkpoints below are historical.
Current model: gemini-3.8-flash, low thinking. Frozen prompt/schema version 9063daea71c2844e.
Current milestone: local prototype ready for teammate rehearsal. 50 local tests PASS; live D03 payment/receipt/persistence, D07 HOLD and D04 REVIEW PASS. Repeat evaluation8/9 matched,1 failed safely. Nothing published.

## Replacement-key checkpoint — 10 October, approximately 16:20 Pakistan time

- User privately saved a replacement key. Real `verify_live.py D03` succeeded: gemini-3.8-flash, frozen9063daea71c2844e, AWAITING_OWNER, PKR25,000. No private values printed.
- Full running browser flow D03: raw inputs -> live findings -> owner summary -> private passcode POST -> committed receipt DEMO-315C44933A5AB649. Request cA06YGy-H7chDikYGSoZ2B1Y/version1.
- Actual SQLite verification: one transfer, owner47,500,000 paisa, vendor2,500,000 paisa. Owner-link GET remained display only. Reopened completed owner page displayed PAID and linked the same receipt, with no payable form. Sequential/concurrent repeated POST protection remains covered by the passing50-test suite.
- Actual live browser D07 returned HOLD with M2 quote correcting5,000 to3,000 and no owner payment link. Screenshot runtime/screenshots/hold-live.jpg. Receipt proof runtime/screenshots/receipt-live.jpg. D04 browser REVIEW currently running.
- Original reserved results retained unchanged. Automatic approval review rejected the initial repeat as broader external document export; user then explicitly approved repeating all nine fictional cases to Gemini. Repeat running separately in evaluation-repeat-new-key/ with unchanged prompt/schema/model/config. It is a repeat after original scoring, not a fresh unseen set. No score claimed yet.
- Next: finish D04, verify paid state after actual app restart, score the full repeat only after all9 files exist, update deck/results, and leave the app ready for team rehearsal. Teammate meaning review, backup recording and hosting still pending.

D04 first browser attempt returned ERROR with no payment; same saved inputs retried as version2 returned REVIEW with the exact tentative M2 quote and clarification request, no owner link. Screenshot runtime/screenshots/review-live.jpg. Actual server restarted using start.cmd (PID27324); history and receipt still showed exactly one transfer and balances475,000/25,000. Paid receipt survived restart. Full AI-to-owner-to-stored-demo-transfer browser path is now PASS. Human teammate acceptance/rehearsal still pending.

### Final local handoff

Explicitly approved repeat completed all9 cases and was scored separately afterwards.8/9 exact dispositions;3 correct readiness;0 unsafe readiness;0 unnecessary HOLD/REVIEW;1 provider/output failure (E09 stayed ERROR). Results in evaluation-repeat-new-key/SCORE.json. Original2/9 matched with7 failures retained. This is a labelled repeat after earlier gold scoring, not fresh unseen validation. Prompt/schema/model/config unchanged; no evaluation-answer tuning. Nine synthetic examples and unresolved model failures do not establish production reliability.

Actual reset verified after stopping the app: previous fictional SQLite state archived under runtime/backups/, current owner500,000/vendor0/no transfers. start.cmd relaunched the app (PID376); fresh balances visibly verified in browser. Reset prevents paid D03 duplicate protection from blocking the team's next demonstration. Saved receipt/hold/review screenshots remain as historical proof. One-click reset-demo.cmd added with explicit stop-app/archive instructions; underlying reset command tested, batch UI itself UNTESTED.

Final presentation delivery/Before_You_Pay_v3.pptx includes actual receipt and both evaluation results, with notes distinguishing repeat evaluation and current reset state. Package/layout/first-party import validation PASS with0 findings; all5 slide previews visually inspected. PowerPoint opening and timed human rehearsal UNTESTED. Private-credential scan of source/docs/scripts/templates/static returned no matches. No raw evaluation answers in runtime app assets or Docker; both evaluation result folders ignored by Git/Docker.

Remaining: Asad checks whether quotes support meaning; Adil and Moeez complete their own beginner walkthrough and time the5-minute demo; record an honest backup video; supply/authorize repository and hosting destination, then build-test Docker and run hosted smoke/persistence checks. No new key required for this completed local verification. Avoid unnecessary AI reruns before rehearsal; quota remains finite.

## Current checkpoint (supersedes historical table below)

| Feature | Files | Actual result | Status / next action |
|---|---|---|---|
| Setup / private settings / local app | setup.cmd, start.cmd, .env | Dependencies installed, real key accepted; start.cmd actually launched Uvicorn and browser reopened after restart | PASS on this laptop; fresh-machine setup UNTESTED |
| Live three-check analysis | analyzer.py, schemas.py, prompt.txt, gates.py | Earlier development run all9 expected states; new key real browser D03/D07/D04 expected states | PASS for observed calls; intermittent failures recorded |
| Payment protection | store.py, tests/ | 50 tests PASS; real browser D03 transfer, same receipt on completed owner page, paid state survived actual app restart | PASS; teammate acceptance pending |
| Intake / uploads / notices | app.py, templates/, tests/test_http.py | TXT/readable PDF, upload limits, escaped text and actual SQLite demo inbox tested. Browser inbox/history visible | PASS automated checks; teammate walkthrough pending |
| Provider time limit | analyzer.py, analyzer_worker.py, tests/test_provider_timeout.py | Hanging process terminated in regression; actual browser request returned blocked ERROR at limit | PASS; 65-second independent bound added without prompt tuning |
| Reserved run | evaluate_reserved.py, score_reserved.py, evaluation-results/, evaluation-repeat-new-key/ | Original2/9 matched,7 failures. Explicit repeat8/9 matched,1 failure;3 correct readiness,0 unsafe readiness | Partial reliability result; original retained, repeated synthetic set |
| Deployment preparation | Dockerfile, .dockerignore, README.md | Source whitelist and persistent SQLite instructions prepared. Docker absent, no destination supplied | Container UNTESTED; publishing deliberately pending |
| Team delivery | DEMO_SCRIPT.md, delivery/Before_You_Pay_v3.pptx | Updated5-slide PPTX validated and previews inspected, actual receipt and results included | Deck PASS; PowerPoint opening, recording and teammate rehearsal UNTESTED |

### Historical quota failure and repairs

The key authenticated a read-only models request (HTTP200, configured model listed). A minimal documented generateContent request then returned HTTP429 RESOURCE_EXHAUSTED: free daily requests for gemini-3.8-flash exhausted (provider reports limit20). This is a confirmed quota blocker; it does not prove every earlier timeout had the same cause. GenerateContent was briefly tested diagnostically and reverted; the final application retains Interactions and the original frozen prompt/schema/model/config.

The reserved runner originally stalled on E08. Interrupted that attempt, recorded it as ERROR, preserved E01-E07, and explicitly finished only E09 with the independent time limit. E06's recorded1196.92 seconds includes the interruption period; not a reliable provider latency estimate. No reserved retry counted as unseen. Gold was accessed only by separate scoring after all nine attempt records existed. No prompt tuned from these answers. Meaning review remains PENDING for all cases.

Browser D03 version2 was live-supported, but its15-minute token expired during the limit interruption. An actual owner POST correctly blocked it; history still showed owner500,000/vendor0 and no transfers. Later D03 attempts failed safely. One request interrupted by server restart may remain ANALYZING; edit/recheck creates a new version. No successful browser receipt is claimed. Prior successful CLI D03 result was overwritten by a later blocked diagnostic; the actual successful browser snapshot remains in SQLite. verify_live.py now archives previous attempts before replacement.

Next: wait for provider quota reset or user-enabled billing, then run fresh D03/D07/D04 browser analyses, approve D03 once, repeat and verify stored475,000/25,000 balances after restart. Asad reviews quote meaning; teammates complete and time the five-minute rehearsal. Supply a deployment destination only when ready to publish. No real email, money, hosting, or GitHub push occurred.

Final regression after restoring Interactions: `pytest -q` 50 PASS in5.54s, one dependency warning. Prompt hash confirmed9063daea71c2844e. Actual restarted database:0 transfers, owner50,000,000 paisa/vendor0. Screenshots:runtime/screenshots/intake.jpg, ready-review.jpg (earlier supported saved D03), blocked-provider.jpg (actual failed latest request). Local browser left open at intake. No reset needed to undo transfers because none occurred in this live database; reset command tested on an isolated database and archives state deliberately.

Deck build repairs: initial font policy failure corrected using the documented typeface property; missing bundled-import configuration supplied; first screenshot path embedding rendered a placeholder and was replaced by embedded image bytes. Final v2 validation reports0 findings and all five visual previews checked. Superseded deck archived under runtime/deck-build/. The deck's speaker notes explicitly distinguish controlled payment tests from unfinished live browser transfer. Human rehearsal/backup recording remain pending.

## Historical facts and milestone evidence

| Milestone / feature | Implementation | Actual check and observed result | State |
|---|---|---|---|
| 1: isolated environment and dependencies | .venv, requirements.txt | Installed via pip; exact installed versions frozen. Python 3.12.14 / google-genai 2.29.0. | PASS |
| 1: private settings | .env, .env.example | Private key/passcode saved by user; values not printed. Key accepted by real provider request. | PASS |
| 1: app startup | app.py, start.cmd | `.venv\Scripts\python.exe -m pytest -q tests/test_startup.py`: 1 passed, 1 dependency deprecation warning. | PASS |
| 1: local browser | app.py | Uvicorn on http://127.0.0.1:8000; browser tab 2 visibly shows setup screen. | PASS |
| 1: real Gemini call | analyzer.py, verify_live.py | SDK interactions.create signature inspected. `verify_live.py D01`: AWAITING_OWNER, PKR 20,000, real structured request; original evidence/arithmetic gates passed. See runtime/live-checks/D01.json. | PASS |
| 2: schema, evidence and money checks | schemas.py, prompt.txt, gates.py | Source written; live interpretation and gate tests not yet run. | UNTESTED |
| 3: saved owner review and transfer | store.py | Source written; payment-state tests not yet run. | UNTESTED |
| 4: full human flow/uploads | pending | Not implemented or tested. | NOT STARTED |
| 5: notices/deployment | pending | GitHub token invalid; hosting/destination not supplied. Local development continues independently. | NOT STARTED |
| 6: payment tests and reserved evaluation | pending | Reserved raw cases and expected_answers.json remain unopened; evaluation not run. | NOT STARTED |
| 7: rehearsal/submission | pending | No deployed URL, PPTX, recording, or rehearsal. | NOT STARTED |

## Failures and fixes

- Initial venv failed: sandbox temporary-directory permission error. Fixed by assigning TEMP/TMP inside prototype/runtime/tmp.
- Initial pip install failed: sandbox DNS could not reach PyPI. The same install succeeded with reviewed network access.
- Sandboxed pytest and server stalled before output. Startup test/server succeeded outside sandbox. No passing result claimed for the stalled commands.
- Starlette emits a TestClient/httpx deprecation warning; startup test still passed. Address if it affects subsequent checks.
- A Gemini key was posted into chat. User instructed to revoke/replace it and enter replacement privately. Posted key was not written to project files.

## Scope and next action

Use only copied raw development text and independent shared setup. Demo inbox by default; no real email, publishing or real money. A09 asynchronous payment adapter is OUT OF SCOPE (immediate SQLite transfer).

Next: receive private setup, run genuine D01 structured analysis, then validate development outcomes. In parallel, finish simple screens and test saved approval/atomic transfers. Milestone 1 core checks PASS. Fresh-machine setup.cmd remains UNTESTED; startup test is not a deployment check.

## Live integration repair evidence

- Minimal real Gemini request succeeded; small structured D01 extraction returned total 20000.
- Full schema initially rejected with provider 400 invalid_request. Explicit fields/inline references alone still failed.
- Restricting provider schema to basic type/properties/items/required/enum accepted; strict Pydantic constraints still validated locally.
- Full D01 structured analysis passed at 2026-10-10T09:26:03.746759+00:00 UTC, prompt b84aa817b6d47534. No model switch or preset result.

## Milestones 2–4 verification checkpoint

- `pytest -q`: 44 passed in 4.61s; after local opaque-origin regression added, 45 passed in 4.29s. One Starlette/httpx deprecation warning. Tests use controlled model stubs only for deterministic gates/HTTP behavior, not claimed live interpretation.
- Atomic transfer verified: 2,500,000 paisa debit/credit; sequential and six concurrent calls give one receipt; state persists after reopening SQLite.
- Owner verification, GET no-payment, rejection, expired/stale/changed approvals, wrong account, duplicate invoice, insufficient funds, rollback, CSRF and form amount tampering verified.
- Screens, pasted text/TXT, empty PDF/oversize/type handling, escaped source text, and demo inbox HTTP checks pass. Full browser transfer still UNTESTED.
- Browser intake visibly verified and screenshot saved runtime/screenshots/intake.jpg. In-app browser sends Origin:null with no referrer; strict origin check initially blocked legitimate local forms. Fixed local-only opaque origin AFTER signed-session CSRF verification; hosted null/foreign origin and missing CSRF remain blocked (test added).
- Initial live development run: D04/D08/D09 false HOLD, D05 wrong quote/message reference. Prompt clarified cost coverage vs approval absence and per-message evidence.
- Subsequent Flash-Lite development run: D01/D02/D03/D04/D05/D09 expected states; D06/D07 wrong message references, D08 malformed structured output. These are blocked outcomes, not successful checks. Archived in runtime/development-flash-lite/.
- Trying configured gemini-3.8-flash as allowed by development failures. Default-thinking D01 timed out, D02 returned HOLD; interrupted further default run. Testing documented low thinking with bounded retries; results pending.
- No reserved evaluation inputs/answers have been read yet. No publishing or SMTP.

Next: finish provider comparison, validate full live browser payment/HOLD/REVIEW flow, then freeze prompt/schema/model and run reserved scoring separately.

## Final development configuration checkpoint

- gemini-3.8-flash with documented low thinking, bounded provider timeout/retries passed all nine development dispositions at frozen version 9063daea71c2844e. D01/D03 AWAITING_OWNER; D02/D05/D06/D07 HOLD; D04/D08/D09 REVIEW. Real outputs in runtime/live-checks/. Quote/field/arithmetic gates passed for those calls; teammate meaning review still pending.
- Full suite expanded: first 46 PASS / 1 FAIL on readable-PDF mock quote whitespace; corrected the test provider to quote actual extracted input without weakening evidence validation. `pytest -q` then 47 PASS in 4.04s, one dependency deprecation warning.
- PROMPT_FREEZE.json written before any reserved prediction; generation config and schema included in hash. No reserved expected answers read. Nine-case raw evaluation currently running separately.
- Browser D03 intake submits correctly, but its live request timed out and was correctly saved as ERROR with no owner link/no payment. Full successful browser path is STILL NOT VERIFIED. This is an observed provider failure, not completion.
- Dockerfile, .dockerignore, README, Windows setup/start scripts, local archival reset, demo script prepared. Docker executable unavailable; container build UNTESTED. Publishing/deployed URL NOT DONE by instruction; destination not provided.
- SMTP cut by default; actual SQLite demo inbox implemented, no real email sent.
