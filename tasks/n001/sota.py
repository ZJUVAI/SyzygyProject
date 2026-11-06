"""Return the published 367-word C7^5 construction for exact replay."""

from .human import run_human


def run_code():
    """Load the task-local transcription of Polak and Schrijver's witness."""
    return run_human()
