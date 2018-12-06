import cli_ui
import re

import pytest


class MessageRecorder():
    def __init__(self):
        cli_ui.CONFIG["record"] = True
        cli_ui._MESSAGES = list()

    def stop(self):
        cli_ui.CONFIG["record"] = False
        cli_ui._MESSAGES = list()

    def reset(self):
        cli_ui._MESSAGES = list()

    def find(self, pattern):
        regexp = re.compile(pattern)
        for message in cli_ui._MESSAGES:
            if re.search(regexp, message):
                return message


@pytest.fixture()
def message_recorder(request):
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
