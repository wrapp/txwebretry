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
from twisted.internet.error import ConnectionRefusedError
from txretry.retry import RetryingCall, simpleBackoffIterator


class Retry(object):
    ''' Defines a context for making retrying calls. '''

    web_errors = [ResponseFailed, ConnectionRefusedError]

    def __init__(self, backoff_iterator):
        self.backoff_iterator = backoff_iterator

    def __call__(self, f, *args, **kwargs):
        retrying_call = RetryingCall(f, *args, **kwargs)
        return retrying_call.start(
                backoffIterator=self.backoff_iterator,
                failureTester=self._test_failure)

    def _test_failure(self, failure):
        return failure.check(self.web_errors)


def ImmediateRetry(retries=3):
    ''' Returns a Retry context that will retry calls immediately. '''


    backoff_iterator = repeat(0, retries)
    return Retry(backoff_iterator)


def ExponentialBackoffRetry(retries=3):
    ''' Returns a Retry context that will retry calls using exponential
    backoff. '''

    backoff_iterator = simpleBackoffIterator(retries)
    return Retry(backoff_iterator)


# For convenience
retry3_exponential = ExponentialBackoffRetry(3)
retry5_exponential = ExponentialBackoffRetry(5)
retry3_immediate = ImmediateRetry(3)
retry5_immediate = ImmediateRetry(5)
