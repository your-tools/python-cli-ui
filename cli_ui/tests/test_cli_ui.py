from typing import Iterator
import datetime
import io
import operator
import re
from unittest import mock

import colorama.ansi
import colorama
import pytest

import cli_ui
from cli_ui.tests.conftest import MessageRecorder


def assert_equal_strings(a: str, b: str) -> bool:
    return a.split() == b.split()


class SmartTTY(io.StringIO):
    def __init__(self) -> None:
        super().__init__()

    def isatty(self) -> bool:
        return True


class DumbTTY(io.StringIO):
    def __init__(self) -> None:
        super().__init__()

    def isatty(self) -> bool:
        return False


@pytest.fixture
def smart_tty() -> SmartTTY:
    return SmartTTY()


@pytest.fixture
def dumb_tty() -> DumbTTY:
    return DumbTTY()


@pytest.fixture
def toggle_timestamp() -> Iterator[None]:
    cli_ui.CONFIG["timestamp"] = True
    yield
    cli_ui.CONFIG["timestamp"] = False


def test_info_stdout_is_a_tty(smart_tty: io.StringIO) -> None:
    # fmt: off
    cli_ui.info(
        cli_ui.red, "this is red", cli_ui.reset,
        cli_ui.green, "this is green",
        fileobj=smart_tty
    )
    # fmt: on
    expected = (
        colorama.Fore.RED
        + "this is red "
        + colorama.Style.RESET_ALL
        + colorama.Fore.GREEN
        + "this is green"
        + colorama.Style.RESET_ALL
        + "\n"
    )
    actual = smart_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_update_title(smart_tty: SmartTTY) -> None:
    # fmt: off
    cli_ui.info(
        "Something", cli_ui.bold, "bold",
        fileobj=smart_tty,
        update_title=True
    )
    # fmt: on
    expected = (
        colorama.ansi.set_title("Something bold")
        + "Something "
        + colorama.Style.BRIGHT
        + "bold"
        + colorama.Style.RESET_ALL
        + "\n"
    )
    actual = smart_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_info_stdout_is_not_a_tty(dumb_tty: DumbTTY) -> None:
    # fmt: off
    cli_ui.info(
        cli_ui.red, "this is red", cli_ui.reset,
        cli_ui.green, "this is green",
        fileobj=dumb_tty
    )
    # fmt: on
    expected = "this is red this is green\n"
    actual = dumb_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_info_characters(smart_tty: SmartTTY) -> None:
    cli_ui.info(
        "Doing stuff", cli_ui.ellipsis, "sucess", cli_ui.check, fileobj=smart_tty
    )
    actual = smart_tty.getvalue()
    expected = (
        "Doing stuff "
        + colorama.Style.RESET_ALL
        + "…"
        + " sucess "
        + colorama.Fore.GREEN
        + "✓"
    )
    assert_equal_strings(actual, expected)


def test_timestamp(dumb_tty: DumbTTY, toggle_timestamp: None) -> None:
    cli_ui.info("message", fileobj=dumb_tty)
    actual = dumb_tty.getvalue()
    match = re.match(r"\[(.*)\]", actual)
    assert match
    assert datetime.datetime.strptime(match.groups()[0], "%Y-%m-%d %H:%M:%S")


def test_record_message(message_recorder: MessageRecorder) -> None:
    cli_ui.info_1("This is foo")
    assert message_recorder.find("foo")
    message_recorder.reset()
    cli_ui.info_1("This is bar")
    assert not message_recorder.find("foo")


def test_read_input() -> None:
    with mock.patch("builtins.input") as m:
        m.side_effect = ["foo"]
        actual = cli_ui.read_input()
        assert actual == "foo"


def test_read_password() -> None:
    with mock.patch("getpass.getpass") as m:
        m.side_effect = ["bar"]
        actual = cli_ui.read_password()
        assert actual == "bar"


def test_ask_string() -> None:
    with mock.patch("builtins.input") as m:
        m.side_effect = ["sugar!", ""]
        res = cli_ui.ask_string("coffee with what?")
        assert res == "sugar!"
        res = cli_ui.ask_string("coffee with what?", default="milk")
        assert res == "milk"


def test_ask_colored_message() -> None:
    with mock.patch("builtins.input") as m:
        m.side_effect = ["y"]
        res = cli_ui.ask_yes_no(
            "Deploy to", cli_ui.bold, "prod", cli_ui.reset, "?", default=False
        )
        assert res


def test_ask_password() -> None:
    with mock.patch("getpass.getpass") as m:
        m.side_effect = ["chocolate!", ""]
        res = cli_ui.ask_password("guilty pleasure?")
        assert res == "chocolate!"


def test_empty_password() -> None:
    with mock.patch("getpass.getpass") as m:
        m.side_effect = [""]
        actual = cli_ui.ask_password(
            "Please enter your password or just press enter to skip"
        )
        assert actual == ""


def test_ask_yes_no() -> None:
    """ Test that you can answer with several types of common answers """
    with mock.patch("builtins.input") as m:
        m.side_effect = ["y", "yes", "Yes", "n", "no", "No"]
        expected_res = [True, True, True, False, False, False]
        for res in expected_res:
            actual = cli_ui.ask_yes_no("coffee?")
            assert actual == res


def test_ask_yes_no_default() -> None:
    """ Test that just pressing enter returns the default value """
    with mock.patch("builtins.input") as m:
        m.side_effect = ["", ""]
        assert cli_ui.ask_yes_no("coffee?", default=True) is True
        assert cli_ui.ask_yes_no("coffee?", default=False) is False


def test_ask_yes_no_wrong_input() -> None:
    """ Test that we keep asking when answer does not make sense """
    with mock.patch("builtins.input") as m:
        m.side_effect = ["coffee!", "n"]
        assert cli_ui.ask_yes_no("tea?") is False
        assert m.call_count == 2


def test_ask_choice() -> None:
    class Fruit:
        def __init__(self, name: str, price: int):
            self.name = name
            self.price = price

    def func_desc(fruit: Fruit) -> str:
        return fruit.name

    fruits = [Fruit("apple", 42), Fruit("banana", 10), Fruit("orange", 12)]
    with mock.patch("builtins.input") as m:
        m.side_effect = ["nan", "5", "2"]
        actual = cli_ui.ask_choice(
            "Select a fruit", choices=fruits, func_desc=operator.attrgetter("name")
        )
        assert actual.name == "banana"
        assert actual.price == 10
        assert m.call_count == 3


def test_ask_choice_empty_input() -> None:
    with mock.patch("builtins.input") as m:
        m.side_effect = [""]
        res = cli_ui.ask_choice("Select a animal", choices=["cat", "dog", "cow"])
        assert res is None


def test_ask_choice_ctrl_c() -> None:
    with pytest.raises(KeyboardInterrupt):
        with mock.patch("builtins.input") as m:
            m.side_effect = KeyboardInterrupt
            cli_ui.ask_choice("Select a animal", choices=["cat", "dog", "cow"])


def test_quiet(message_recorder: MessageRecorder) -> None:
    cli_ui.setup(quiet=True)
    cli_ui.info("info")
    cli_ui.error("error")
    assert message_recorder.find("error")
    assert not message_recorder.find("info")


def test_color_always(dumb_tty: DumbTTY) -> None:
    cli_ui.setup(color="always")
    cli_ui.info(cli_ui.red, "this is red", fileobj=dumb_tty)
    assert colorama.Fore.RED in dumb_tty.getvalue()


def test_color_never(smart_tty: SmartTTY) -> None:
    cli_ui.setup(color="never")
    cli_ui.info(cli_ui.red, "this is red", fileobj=smart_tty)
    assert colorama.Fore.RED not in smart_tty.getvalue()
