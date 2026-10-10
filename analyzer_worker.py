"""Private subprocess transport. Documents enter via stdin, never command arguments."""
import json
import sys
from analyzer import _analyze_live, ProviderFailure

if __name__ == '__main__':
    try:
        payload = json.load(sys.stdin)
        result = _analyze_live(payload['invoice'], payload['context'])
        sys.stdout.write(result.model_dump_json())
    except ProviderFailure as exc:
        # Only an allowlisted category crosses the subprocess boundary.
        sys.stderr.write(json.dumps({'failure': exc.code}))
        sys.exit(1)
