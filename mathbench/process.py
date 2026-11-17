"""Run workers with a wall time limit and clean up their process groups."""
import os
import signal
import subprocess
import tempfile

from .registry import ROOT


def run_process(args, env, timeout):
    with tempfile.TemporaryFile() as errors:
        proc = subprocess.Popen(args, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL, stderr=errors, start_new_session=True)
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            raise TimeoutError("Wall time limit exceeded")
        finally:
            # Stop descendants even when the immediate child has exited.
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if proc.returncode:
            errors.seek(0)
            message = errors.read(8192).decode(errors="replace")
            raise RuntimeError(message[-3000:] or "Worker failed")
