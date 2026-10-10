"""Local command only. Archive previous demo database before restoring balances."""
import argparse
import shutil
from datetime import datetime, timezone
from settings import ROOT, database_path
from store import Store


def main():
    parser = argparse.ArgumentParser(description='Reset fictional balances/history. Stop the app first.')
    parser.add_argument('--confirm', action='store_true', help='Confirm archiving previous fictional demo state.')
    args = parser.parse_args()
    if not args.confirm:
        parser.error('Stop the app, then run reset_demo.py --confirm. Existing database will be archived.')
    path = database_path().resolve()
    runtime = (ROOT / 'runtime').resolve()
    if not path.is_relative_to(runtime):
        raise SystemExit('Reset only supports a database inside prototype/runtime. Hosted/custom databases require separate maintenance.')
    if path.exists():
        archive = runtime / 'backups'
        archive.mkdir(exist_ok=True)
        name = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.sqlite3'
        shutil.move(str(path), str(archive / name))
        print('Previous fictional state archived under runtime/backups/.')
    store = Store(path)
    assert store.balances() == {'owner': 50000000, 'vendor': 0}
    assert store.history() == []
    print('Reset verified: owner PKR 500,000; vendor PKR 0; no transfers.')


if __name__ == '__main__':
    main()
