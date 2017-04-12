import datetime
import io
import re
from unittest import mock

import ui

import pytest

RED = "\x1b[31;1m"
GREEN = "\x1b[32;1m"
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
BEGIN_TITLE = "\x1b]0;"
END_TITLE = "\x07"


def assert_equal_strings(a, b):
    return a.split() == b.split()


@pytest.fixture
def smart_tty():
    res = io.StringIO()
    res.isatty = lambda: True
    return res


@pytest.fixture
def dumb_tty():
    res = io.StringIO()
    res.isatty = lambda: False
    return res


@pytest.fixture
def toggle_timestamp():
    ui.CONFIG["timestamp"] = True
    yield
    ui.CONFIG["timestamp"] = False


def test_info_stdout_is_a_tty(smart_tty):
    ui.info(ui.red, "this is red", ui.reset,
            ui.green, "this is green",
            fileobj=smart_tty)
    expected = (RED + "this is red " + RESET +
                GREEN + "this is green" + RESET + "\n")
    actual = smart_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_update_title(smart_tty):
    ui.info("Something", ui.bold, "bold", fileobj=smart_tty, update_title=True)
    expected = (BEGIN_TITLE + "Something bold" + END_TITLE +
                "Something " + BOLD + "bold" + RESET + "\n")
    actual = smart_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_info_stdout_is_not_a_tty(dumb_tty):
    ui.info(ui.red, "this is red", ui.reset,
            ui.green, "this is green",
            fileobj=dumb_tty)
    expected = "this is red this is green\n"
    actual = dumb_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_info_characters(smart_tty):
    ui.info("Doing stuff", ui.ellipsis, "sucess", ui.check, fileobj=smart_tty)
    actual = smart_tty.getvalue()
    expected = "Doing stuff " + RESET + "…" + " sucess " + GREEN + "✓"
    assert_equal_strings(actual, expected)


def test_timestamp(dumb_tty, toggle_timestamp):
    ui.info("message", fileobj=dumb_tty)
    actual = dumb_tty.getvalue()
    match = re.match("\[(.*)\]", actual)
    assert match
    assert datetime.datetime.strptime(match.groups()[0], "%Y-%m-%d %H:%M:%S")


def test_record_message(messages):
    ui.info_1("This is foo")
    assert messages.find("foo")
    messages.reset()
    ui.info_1("This is bar")
    assert not messages.find("foo")


def test_read_input():
    with mock.patch('builtins.input') as m:
        m.side_effect = ["foo"]
        actual = ui.read_input()
        assert actual == "foo"


def test_ask_string():
    with mock.patch('builtins.input') as m:
        m.side_effect = ["sugar!", ""]
        res = ui.ask_string("coffee with what?")
        assert res == "sugar!"
        res = ui.ask_string("coffee with what?", default="milk")
        assert res == "milk"


def test_ask_yes_no():
    """ Test that you can answer with several types of common answers """
    with mock.patch('builtins.input') as m:
        m.side_effect = ["y", "yes", "Yes", "n", "no", "No"]
        expected_res  = [True, True, True, False, False, False]
        for res in expected_res:
            actual = ui.ask_yes_no("coffee?")
            assert actual == res


def test_ask_yes_no_default():
    """ Test that just pressing enter returns the default value """
    with mock.patch('builtins.input') as m:
        m.side_effect = ["", ""]
        assert ui.ask_yes_no("coffee?", default=True)  is True
        assert ui.ask_yes_no("coffee?", default=False) is False


def test_ask_yes_no_wrong_input():
    """ Test that we keep asking when answer does not make sense """
    with mock.patch('builtins.input') as m:
        m.side_effect = ["coffee!", "n"]
        assert ui.ask_yes_no("tea?") is False
        assert m.call_count == 2


def test_ask_choice():
    fruits = ["apple", "banana", "orange"]
    with mock.patch('builtins.input') as m:
        m.side_effect = ["nan", "2"]
        actual = ui.ask_choice("Select a fruit", fruits)
        assert actual == "banana"
        assert m.call_count == 2


def test_ask_choice_default():
    fruits = ["apple", "banana", "orange"]
    with mock.patch('builtins.input') as m:
        m.side_effect = [""]
        actual = ui.ask_choice("Select a fruit", fruits)
        assert actual == "apple"
