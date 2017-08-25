import ui
import re

import pytest

class MessageRecorder():
    def __init__(self):
        ui.CONFIG["record"] = True
        ui._MESSAGES = list()

    def stop(self):
        ui.CONFIG["record"] = False
        ui._MESSAGES = list()

    def reset(self):
        ui._MESSAGES = list()

    def find(self, pattern):
        regexp = re.compile(pattern)
        for message in ui._MESSAGES:
            if re.search(regexp, message):
                return message

@pytest.fixture()
def messages(request):
    recorder = MessageRecorder()
    request.addfinalizer(recorder.stop)
    return recorder
