import signal
from contextlib import contextmanager
import time
from random import randint


@contextmanager
def timeout(sec):
    # Register a function to raise a TimeoutError on the signal
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after given time
    signal.alarm(sec)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    print("Couldn't solve!")
    raise TimeoutError


class SolverDFS:
    def __init__(self, game):
        self.game = game    # puzzle handler
        self.timeout_duration = 10   # time (in seconds) after solve function will terminate

    def solve_with_timeout(self):
        with timeout(self.timeout_duration):
            self.solve()

    def solve(self):
        while True:
            x, y = randint(1,4), randint(1, 4)
            self.game.board[x, y] = 1
            print(x, y, self.game.board[x, y])
            time.sleep(1)
