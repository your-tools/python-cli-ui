import re
from typing import Any, Iterator, Optional

import pytest

import cli_ui


class MessageRecorder:
    """Helper class to tests emitted messages"""

    def __init__(self) -> None:
        cli_ui._MESSAGES = []
        self.idx_find_next: int = 0

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
        for idx, message in enumerate(cli_ui._MESSAGES):
            if re.search(regexp, message):
                if isinstance(message, str):
                    self.idx_find_next = idx + 1
                    return message
        return None

    def find_right_after(self, pattern: str) -> Optional[str]:
        """Same as 'find', but only check the message that is right after
        the one found last time. if no message was found before, the 1st
        message in buffer is checked

        :param pattern: regular expression pattern to use
                        when looking for recorded message

        This is particulary usefull when we want to match only consecutive message.
        Calling this function can be repeated for further consecutive message match.
        """
        if len(cli_ui._MESSAGES) > self.idx_find_next:
            regexp = re.compile(pattern)
            message = cli_ui._MESSAGES[self.idx_find_next]
            if re.search(regexp, message):
                if isinstance(message, str):
                    self.idx_find_next += 1
                    return message
        return None


@pytest.fixture
def message_recorder(request: Any) -> Iterator[MessageRecorder]:
    recorder = MessageRecorder()
    recorder.start()
    yield recorder
    recorder.stop()
