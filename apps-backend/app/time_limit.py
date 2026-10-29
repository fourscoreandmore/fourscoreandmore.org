"""Run slow work in a child process, so that it can be stopped.

music21 can take a long time over a large or unusual score, and Python can't
interrupt a thread, so run_with_time_limit forks a child, waits for its result
and kills it if it takes too long. Forking copies the parent, imports and app
config included, so the child starts at once. That's safe because Gunicorn's
sync workers have a single thread.

The child also sets an alarm, a little later than the parent would kill it,
so it stops itself if the parent is killed first (e.g. by the OOM killer).
"""
import logging
import math
import multiprocessing
import signal

_fork = multiprocessing.get_context("fork")

# Seconds after the time limit at which the child's alarm stops it.
_ALARM_MARGIN = 5


class TimeLimitExceeded(Exception):
    pass


def _run(sender, func, args, seconds):
    # SIGALRM's default action ends the process.
    signal.alarm(math.ceil(seconds) + _ALARM_MARGIN)
    try:
        result = (True, func(*args))
    except BaseException:
        logging.exception("Failed in a child process")
        result = (False, None)
    sender.send(result)
    sender.close()


def run_with_time_limit(seconds, func, *args):
    """Return func(*args), run in a child process.

    Raises TimeLimitExceeded if it takes more than seconds, and RuntimeError if
    it raises an exception (which the child logs) or the child dies.
    """
    receiver, sender = _fork.Pipe(duplex=False)
    child = _fork.Process(target=_run, args=(sender, func, args, seconds), daemon=True)
    child.start()
    sender.close()
    try:
        if not receiver.poll(seconds):
            raise TimeLimitExceeded(f"Took more than {seconds} seconds")
        try:
            succeeded, result = receiver.recv()
        except EOFError:
            succeeded = False
    finally:
        if child.is_alive():
            child.kill()
        child.join()
        receiver.close()
    if not succeeded:
        raise RuntimeError(f"Failed in a child process (exit code {child.exitcode})")
    return result
