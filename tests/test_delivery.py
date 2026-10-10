import sys
from pathlib import Path
import pytest
from conftest import ready
from store import Store
import reset_demo


def test_reset_archives_previous_state_and_restores_fictional_balances(tmp_path, sample, monkeypatch):
    root=tmp_path/'prototype'; runtime=root/'runtime';runtime.mkdir(parents=True)
    path=runtime/'demo.sqlite3';store=Store(path);row=ready(store,sample)
    store.decide(row['id'],row['version'],row['current_token'],'test-owner','test-owner')
    monkeypatch.setattr(reset_demo,'ROOT',root)
    monkeypatch.setattr(reset_demo,'database_path',lambda:path)
    monkeypatch.setattr(sys,'argv',['reset_demo.py','--confirm'])
    reset_demo.main()
    assert Store(path).balances() == {'owner':50000000,'vendor':0}
    archives=list((runtime/'backups').glob('*.sqlite3'))
    assert len(archives) == 1
    assert Store(archives[0]).balances() == {'owner':47500000,'vendor':2500000}

def test_reset_refuses_database_outside_named_runtime(tmp_path, monkeypatch):
    root=tmp_path/'prototype';root.mkdir()
    outside=tmp_path/'outside.sqlite3';outside.write_text('preserve')
    monkeypatch.setattr(reset_demo,'ROOT',root)
    monkeypatch.setattr(reset_demo,'database_path',lambda:outside)
    monkeypatch.setattr(sys,'argv',['reset_demo.py','--confirm'])
    with pytest.raises(SystemExit): reset_demo.main()
    assert outside.read_text() == 'preserve'
