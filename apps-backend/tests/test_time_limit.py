import os
import signal
import time

import pytest

from app import time_limit
from app.time_limit import TimeLimitExceeded, run_with_time_limit


def test_returns_the_result():
    assert run_with_time_limit(10, lambda a, b: [a, b], 1, "two") == [1, "two"]


def test_runs_in_another_process():
    assert run_with_time_limit(10, os.getpid) != os.getpid()


def test_stops_work_that_takes_too_long(tmp_path):
    marker = tmp_path / "finished"

    def slow():
        time.sleep(5)
        marker.touch()

    start = time.monotonic()
    with pytest.raises(TimeLimitExceeded):
        run_with_time_limit(0.2, slow)

    assert time.monotonic() - start < 2
    time.sleep(0.1)
    assert not marker.exists()


def test_reports_an_exception():
    def fail():
        raise ValueError("bad score")

    # The exit code depends on whether the child exits before it's killed.
    with pytest.raises(RuntimeError, match="Failed in a child process"):
        run_with_time_limit(10, fail)


def test_reports_a_child_that_dies():
    with pytest.raises(RuntimeError, match="exit code 3"):
        run_with_time_limit(10, os._exit, 3)


def test_the_child_stops_itself_if_its_parent_is_gone(monkeypatch):
    """As if the parent were killed while waiting: nothing kills the child."""
    monkeypatch.setattr(time_limit, "_ALARM_MARGIN", 0)
    receiver, sender = time_limit._fork.Pipe(duplex=False)
    child = time_limit._fork.Process(target=time_limit._run, args=(sender, time.sleep, (30,), 0.5))

    child.start()
    child.join(10)

    assert child.exitcode == -signal.SIGALRM
