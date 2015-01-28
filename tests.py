from itertools import repeat
from txwebretry import Retry
from twisted.web.client import getPage

from nose.tools import assert_raises
from nose.twistedtools import deferred
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ConnectionRefusedError
from mock import patch


@deferred()
@inlineCallbacks
def test_retry_connection_refused():
    num_attempts = 3
    retry = Retry(repeat, 0, num_attempts)
    with _patch_test_failure(retry) as m:
        with assert_raises(ConnectionRefusedError):
            yield retry(getPage, 'http://localhost:19999')

    # Should retry 3 times
    actual_attempts = len(m.call_args_list)
    assert actual_attempts == num_attempts, actual_attempts


@deferred()
@inlineCallbacks
def test_retry_non_web_error():
    def fail():
        1 / 0

    num_attempts = 3
    retry = Retry(repeat, 0, num_attempts)
    with _patch_test_failure(retry) as m:
        with assert_raises(ZeroDivisionError):
            yield retry(fail)

    # Should not retry
    actual_attempts = len(m.call_args_list)
    assert actual_attempts == 1, actual_attempts


def _patch_test_failure(retry):
    ''' Wraps the Retry._test_failure method in a Mock. '''
    return patch.object(retry, '_test_failure',
            side_effect=retry._test_failure)
