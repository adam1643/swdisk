import time

DEFAULT_TIMEOUT = 30


def timer(event, timeout):
    if timeout == 0:
        return
    time.sleep(timeout)
    event.set()
