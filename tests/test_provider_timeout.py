import sys
import time
import pytest
from analyzer import _run_bounded, ProviderFailure

def test_hung_provider_process_is_terminated():
    started = time.monotonic()
    with pytest.raises(ProviderFailure, match='time limit'):
        _run_bounded([sys.executable, '-c', 'import time; time.sleep(30)'], '{}', timeout=.25)
    assert time.monotonic() - started < 5


@pytest.mark.parametrize('status,code', [(429,'quota'),(401,'key'),(403,'access'),(402,'billing'),(404,'model'),(400,'request'),(503,'unavailable')])
def test_provider_status_is_actionable_without_exposing_raw_error(status,code):
    from analyzer import provider_failure
    class APIError(Exception):
        status_code=status
    result=provider_failure(APIError('private-test-secret https://example.invalid/?key=private-test-secret'))
    assert result.code==code
    assert 'private-test-secret' not in str(result)
    assert 'Payment is blocked' in str(result)


def test_worker_quota_is_preserved_but_untrusted_stderr_is_not(monkeypatch):
    import analyzer
    from subprocess import CompletedProcess
    monkeypatch.setattr(analyzer,'_run_bounded',lambda *args:CompletedProcess([],1,'','{"failure":"quota"}'))
    with pytest.raises(ProviderFailure,match='429'):
        analyzer.analyze('invoice','contract')
    monkeypatch.setattr(analyzer,'_run_bounded',lambda *args:CompletedProcess([],1,'','secret-from-sdk'))
    with pytest.raises(ProviderFailure) as caught:
        analyzer.analyze('invoice','contract')
    assert 'secret-from-sdk' not in str(caught.value)


def test_timeout_and_connection_errors_have_distinct_actions():
    from analyzer import provider_failure
    APITimeoutError=type('APITimeoutError',(Exception,),{})
    APIConnectionError=type('APIConnectionError',(Exception,),{})
    assert provider_failure(APITimeoutError()).code=='timeout'
    assert provider_failure(APIConnectionError()).code=='network'
