from typing import Any, Iterator, Optional
import cli_ui
import re

import pytest


class MessageRecorder:
    def __init__(self) -> None:
        cli_ui.CONFIG["record"] = True
        cli_ui._MESSAGES = list()

    def stop(self) -> None:
        cli_ui.CONFIG["record"] = False
        cli_ui._MESSAGES = list()

    def reset(self) -> None:
        cli_ui._MESSAGES = list()

    def find(self, pattern: str) -> Optional[str]:
        regexp = re.compile(pattern)
        for message in cli_ui._MESSAGES:
            if re.search(regexp, message):
                return message
        return None


@pytest.fixture
def message_recorder(request: Any) -> Iterator[MessageRecorder]:
    """ Start recording messages

    *Methods*

    * `stop()`: stop recording
    * `reset()`: clear the list of recorded messages.
    * `find(regex)` find a message in the list matching the given regular
       expression

    """
    recorder = MessageRecorder()
    yield recorder
    recorder.stop()
