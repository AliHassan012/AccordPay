# AccordPay: earlier demo walkthroughs

These videos were recorded before the AccordPay rename and show the former product name. They use explicitly labelled saved AI replays. They are optional supporting walkthroughs, not continuous live screen recordings of the current model.

- `payment_approved.mp4`: about 2 minutes 3 seconds. Documents, saved AI answer, approval proof, inbox notice, owner review, masked password, actual fictional transfer, receipt and history.
- `payment_not_approved.mp4`: about 1 minute 47 seconds. Documents, saved AI answer, correction proof, HOLD, unavailable payment, warning notice and unchanged balances.

Both are 1920 x 1080 MP4 files with simple English voice and captions. They are edited walkthroughs made from actual browser screens, not continuous screen recordings.

The main app's live D03 analysis passed during this task and its owner-confirmed fictional payment committed receipt DEMO-72D8CC797DFB4BA7. Two live D07 attempts timed out and blocked payment. These failures are retained in the main app's saved records.

Final filming used a separate local recording copy with clearly labelled replays of real saved AI answers: D03 from the successful current-task request and D07 from runtime/live-checks/D07.json. No new live AI call is claimed in the videos. The recording button says Review saved AI result. The main application source was not changed.

The recording copy ran actual app validation, owner password verification and fictional payment code against recording-demo.sqlite3. One D03 transfer committed receipt DEMO-C86DDF466C5A8976. D07 ended HOLD and has no transfer or receipt. Final balances are owner PKR475,000/vendor PKR25,000; one total transfer. See workflow_verification.json.

Initial D07 replay returned REVIEW because browser line endings differed from the original text-file source. Its original snapshot is retained. The recording-only helper restores original text-file line endings without changing AI quotes or product evidence checks. Rechecking produced the recorded HOLD result.

Notices are stored in the demo inbox. No real email, separate payment email or real-bank transfer happened. The password is masked and not included in narration or video files.

Every composed scene was visually inspected. FFprobe verified H.264 video, AAC audio, 1080p dimensions and durations. Each complete MP4 decoded without error using FFmpeg. video_validation.json contains results.

Supporting frames, narration, contact sheets and scripts are retained for editing. The two MP4 files are the deliverables.
