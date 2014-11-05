Retry Twisted web requests
==========================

This extends the excellent [txretry](https://github.com/terrycojones/txretry)
by Terry Jones with error handling for common twisted.web.client errors and
simple but opinionated functions to quickly get you started.

Example usage:

```python

import treq
from txwebretry import retry3_exponential as retry3
from txwebretry import retry5_immediate as retry5

# Retry up to 3 times with exponential backoff
retry3(treq.get, 'http://localhost:8080/index.html')

# Retry up to 5 times without delay
retry5(treq.get, 'http://localhost:8080/index.html')

```
