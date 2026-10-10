"""One genuine structured analysis, using ONLY raw development documents."""
import json
import sys
from datetime import datetime, timezone
from analyzer import analyze, prompt_version, ProviderFailure
from gates import validate, GateError
from settings import ROOT, settings, trusted_setup


def main():
    case = sys.argv[1] if len(sys.argv) > 1 else 'D01'
    if case not in [f'D{i:02}' for i in range(1, 10)]:
        raise SystemExit('Use a development case D01-D09.')
    path = ROOT / 'assets' / 'development' / case
    invoice = (path / 'invoice.txt').read_text(encoding='utf-8')
    context = (path / 'deal_and_messages.txt').read_text(encoding='utf-8')
    cfg = settings()
    record = {'case': case, 'model': cfg['model'], 'prompt_version': prompt_version(), 'time_utc': datetime.now(timezone.utc).isoformat(), 'live_call': False}
    try:
        output = analyze(invoice, context)
        record['live_call'] = True
        record['analysis'] = output.model_dump()
        record.update(validate(output, invoice, context, trusted_setup()))
        record['result'] = 'PASS'
        print(f'LIVE {case}: {record["state"]}, PKR {record["amount_minor"]/100:.2f}; model={cfg["model"]}')
    except (ProviderFailure, GateError) as exc:
        record.update(result='BLOCKED', error=str(exc))
        print('BLOCKED:', str(exc))
    out = ROOT / 'runtime' / 'live-checks'
    out.mkdir(parents=True, exist_ok=True)
    previous = out / f'{case}.json'
    if previous.exists():
        archive = out / 'attempts'
        archive.mkdir(exist_ok=True)
        previous.rename(archive / (case + '-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.json'))
    (out / f'{case}.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0 if record['result'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
