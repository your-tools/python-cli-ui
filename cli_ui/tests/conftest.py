import re
from typing import Any, Iterator, Optional

import pytest

import cli_ui


class MessageRecorder:
    """Helper class to tests emitted messages"""

    def __init__(self) -> None:
        cli_ui._MESSAGES = []

    def start(self) -> None:
        """Start recording messages"""
        cli_ui.CONFIG["record"] = True

    def stop(self) -> None:
        """Stop recording messages"""
        cli_ui.CONFIG["record"] = False
        cli_ui._MESSAGES = []

    def reset(self) -> None:
        """Reset the list"""
        cli_ui._MESSAGES = []

    def find(self, pattern: str) -> Optional[str]:
        """Find a message in the list of recorded message

        :param pattern: regular expression pattern to use
                        when looking for recorded message
        """
        regexp = re.compile(pattern)
        for message in cli_ui._MESSAGES:
            if re.search(regexp, message):
                return message
        return None


@pytest.fixture
def message_recorder(request: Any) -> Iterator[MessageRecorder]:
    recorder = MessageRecorder()
    recorder.start()
    yield recorder
    recorder.stop()
