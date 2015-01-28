''' txwebretry - retry mechanisms for web requests.

Utilities for automatically retrying web requests made with twisted.web.client.

Usage:

>>> # GET localhost:8080 up to 3 times with exponential backoff
>>> d = retry3_exponential(treq.get, 'http://localhost:8080')

>>> # GET localhost:8080 up to 5 times without delay
>>> d = retry5_immediate(treq.get, 'http://localhost:8080')

'''


from itertools import repeat
from twisted.web.client import ResponseFailed
from twisted.internet.error import ConnectionRefusedError, ConnectingCancelledError
from txretry.retry import RetryingCall, simpleBackoffIterator

class Retry(object):
    ''' Defines a context for making retrying calls. '''

    web_errors = [ResponseFailed, ConnectionRefusedError, ConnectingCancelledError]

    def __init__(self, backoff_func, *backoff_args, **backoff_kwargs):
        self.backoff_func = backoff_func
        self.backoff_args = backoff_args
        self.backoff_kwargs = backoff_kwargs

    def __call__(self, f, *args, **kwargs):
        retrying_call = RetryingCall(f, *args, **kwargs)
        return retrying_call.start(
                backoffIterator=self._backoff_iterator(),
                failureTester=self._test_failure)

    def _backoff_iterator(self):
        return self.backoff_func(*self.backoff_args, **self.backoff_kwargs)

    def _test_failure(self, failure):
        if not failure.check(*self.web_errors):
            return failure


def ImmediateRetry(attempts=3):
    ''' Returns a Retry context that will retry calls immediately. '''

    return Retry(repeat, 0, attempts)


def ExponentialBackoffRetry(attempts=3):
    ''' Returns a Retry context that will retry calls using exponential
    backoff. '''

    return Retry(simpleBackoffIterator, attempts)


# For convenience

retry3_exponential = ExponentialBackoffRetry(3)
retry5_exponential = ExponentialBackoffRetry(5)
retry10_exponential = ExponentialBackoffRetry(10)

retry3_immediate = ImmediateRetry(3)
retry5_immediate = ImmediateRetry(5)
retry10_immediate = ImmediateRetry(10)
