from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Type, Union, IO

Dict, Type

import argparse
import datetime
import difflib
import functools
import getpass
import inspect
import io
import os
import sys
import time
import traceback

import colorama
import unidecode
import tabulate

ConfigValue = Union[None, bool, str]
FileObj = IO[str]

# Global variable to store configuration

CONFIG = {
    "verbose": os.environ.get("VERBOSE"),
    "quiet": False,
    "color": "auto",
    "title": "auto",
    "timestamp": False,
    "record": False,  # used for testing
}  # type: Dict[str, ConfigValue]


# used for testing
_MESSAGES = list()

# so that we don't re-compute this variable over
# and over again:
_ENABLE_XTERM_TITLE = None

# should we call colorama.init()?
_INITIALIZED = False


# Tokens can be strings, or Color, UnicodeSequence or Symbol instances,
# or anything that can be converted to string.
Token = Any


def setup(
    *,
    verbose: bool = False,
    quiet: bool = False,
    color: str = "auto",
    title: str = "auto",
    timestamp: bool = False
) -> None:
    """ Configure behavior of message functions.

    :param verbose: Whether :func:`debug` messages should get printed
    :param quiet: Hide every message except :func:`warning`, :func:`error`, and
                  :func:`fatal`
    :param color: Choices: 'auto', 'always', or 'never'. Whether to color output.
                  By default ('auto'), only use color when output is a terminal.
    :param title: Ditto for setting terminal title
    :param timestamp: Whether to prefix every message with a time stamp
    """
    _setup(verbose=verbose, quiet=quiet, color=color, title=title, timestamp=timestamp)


def _setup(**kwargs: ConfigValue) -> None:
    for key, value in kwargs.items():
        CONFIG[key] = value


class Color:
    """Represent an ANSI escape sequence """

    def __init__(self, code: str):
        self.code = code


# fmt: off
reset     = Color(colorama.Style.RESET_ALL)
bold      = Color(colorama.Style.BRIGHT)
faint     = Color(colorama.Style.DIM)
# for some reason those are not in colorama
standout  = Color('\x1b[3m')
underline = Color('\x1b[4m')
blink     = Color('\x1b[5m')
overline  = Color('\x1b[6m')

black   = Color(colorama.Fore.BLACK)
red     = Color(colorama.Fore.RED)
green   = Color(colorama.Fore.GREEN)
yellow  = Color(colorama.Fore.YELLOW)
blue    = Color(colorama.Fore.BLUE)
magenta = Color(colorama.Fore.MAGENTA)
cyan    = Color(colorama.Fore.CYAN)
white   = Color(colorama.Fore.WHITE)

# backward compatibility:
brown = yellow      # used by ui.warning
lightgray = white  # used by ui.debug
darkred = red
darkgreen = green
darkblue = blue
purple = magenta
fuscia = magenta
fuschia = magenta
turquoise = cyan
darkgray = black
darkteal = cyan
darkyellow = yellow
# fmt: on


# Other nice-to-have characters:
class UnicodeSequence:
    """ Represent a sequence containing a color followed by a Unicode symbol """

    def __init__(self, color: Color, as_unicode: str, as_ascii: str):
        if os.name == "nt":
            self.as_string = as_ascii
        else:
            self.as_string = as_unicode
        self.color = color

    def tuple(self) -> Tuple[Token, ...]:
        return (reset, self.color, self.as_string, reset)


ellipsis = UnicodeSequence(reset, "…", "...")
check = UnicodeSequence(green, "✓", "ok")
cross = UnicodeSequence(red, "❌", "ko")


class Symbol(UnicodeSequence):
    def __init__(self, as_unicode: str, as_ascii: str):
        super().__init__(reset, as_unicode, as_ascii)

    def tuple(self) -> Tuple[Token, ...]:
        return (self.as_string,)


def using_colorama() -> bool:
    if os.name == "nt":
        if "TERM" not in os.environ:
            return True
        if os.environ["TERM"] == "cygwin":
            return True
        return False
    else:
        return False


def config_color(fileobj: FileObj) -> bool:
    if CONFIG["color"] == "never":
        return False
    if CONFIG["color"] == "always":
        return True
    if os.name == "nt":
        # sys.isatty() is False on mintty, so
        # let there be colors by default. (when running on windows,
        # people can use --color=never)
        # Note that on Windows, when run from cmd.exe,
        # console.init() does the right thing if sys.stdout is redirected
        return True
    else:
        return fileobj.isatty()


def write_title_string(mystr: str, fileobj: FileObj) -> None:
    if using_colorama():
        # By-pass colorama bug:
        # colorama/win32.py, line 154
        #   return _SetConsoleTitleW(title)
        # ctypes.ArgumentError: argument 1: <class 'TypeError'>: wrong type
        return
    mystr = "\x1b]0;%s\x07" % mystr
    fileobj.write(mystr)
    fileobj.flush()


def process_tokens(
    tokens: Sequence[Token], *, end: str = "\n", sep: str = " "
) -> Tuple[str, str]:
    """ Returns two strings from a list of tokens.
    One containing ASCII escape codes, the other
    only the 'normal' characters

    """
    # Flatten the list of tokens in case some of them are of
    # class UnicodeSequence:
    flat_tokens = list()  # type: List[Token]
    for token in tokens:
        if isinstance(token, UnicodeSequence):
            flat_tokens.extend(token.tuple())
        else:
            flat_tokens.append(token)

    with_color = _process_tokens(flat_tokens, end=end, sep=sep, color=True)
    without_color = _process_tokens(flat_tokens, end=end, sep=sep, color=False)
    return (with_color, without_color)


def _process_tokens(
    tokens: Sequence[Token], *, end: str = "\n", sep: str = " ", color: bool = True
) -> str:
    res = ""

    if CONFIG["timestamp"]:
        now = datetime.datetime.now()
        res += now.strftime("[%Y-%m-%d %H:%M:%S] ")

    for i, token in enumerate(tokens):
        if isinstance(token, Color):
            if color:
                res += token.code
        else:
            res += str(token)
            if i != len(tokens) - 1:
                res += sep
    res += end
    if color:
        res += reset.code
    return res


def write_and_flush(fileobj: FileObj, to_write: str) -> None:
    try:
        fileobj.write(to_write)
    except UnicodeEncodeError:
        # Maybe the file descritor does not support the full Unicode
        # set, like stdout on Windows.
        # Use the unidecode library
        # to make sure we only have ascii, while still keeping
        # as much info as we can
        fileobj.write(unidecode.unidecode(to_write))
    fileobj.flush()


def message(
    *tokens: Token,
    end: str = "\n",
    sep: str = " ",
    fileobj: FileObj = sys.stdout,
    update_title: bool = False
) -> None:
    """ Helper method for error, warning, info, debug

    """
    if using_colorama():
        global _INITIALIZED
        if not _INITIALIZED:
            colorama.init()
            _INITIALIZED = True
    with_color, without_color = process_tokens(tokens, end=end, sep=sep)
    if CONFIG["record"]:
        _MESSAGES.append(without_color)
    if update_title and with_color:
        write_title_string(without_color, fileobj)
    to_write = with_color if config_color(fileobj) else without_color
    write_and_flush(fileobj, to_write)


def fatal(*tokens: Token, **kwargs: Any) -> None:
    """ Print an error message and call ``sys.exit`` """
    error(*tokens, **kwargs)
    sys.exit(1)


def error(*tokens: Token, **kwargs: Any) -> None:
    """ Print an error message """
    tokens = [bold, red, "Error:"] + list(tokens)  # type: ignore
    kwargs["fileobj"] = sys.stderr
    message(*tokens, **kwargs)


def warning(*tokens: Token, **kwargs: Any) -> None:
    """ Print a warning message """
    tokens = [brown, "Warning:"] + list(tokens)  # type: ignore
    kwargs["fileobj"] = sys.stderr
    message(*tokens, **kwargs)


def info(*tokens: Token, **kwargs: Any) -> None:
    r""" Print an informative message

    :param tokens: list of `ui` constants or strings, like ``(cli_ui.red, 'this is an error')``
    :param sep: separator, defaults to ``' '``
    :param end: token to place at the end, defaults to ``'\n'``
    :param fileobj: file-like object to print the output, defaults to ``sys.stdout``
    :param update_title: whether to update the title of the terminal window
    """
    if CONFIG["quiet"]:
        return
    message(*tokens, **kwargs)


def info_section(*tokens: Token, **kwargs: Any) -> None:
    """ Print an underlined section name """
    # We need to know the length of the section:
    process_tokens_kwargs = kwargs.copy()
    process_tokens_kwargs["color"] = False
    no_color = _process_tokens(tokens, **process_tokens_kwargs)
    info(*tokens, **kwargs)
    info("-" * len(no_color), end="\n\n")


def info_1(*tokens: Token, **kwargs: Any) -> None:
    """ Print an important informative message """
    info(bold, blue, "::", reset, *tokens, **kwargs)


def info_2(*tokens: Token, **kwargs: Any) -> None:
    """ Print an not so important informative message """
    info(bold, blue, "=>", reset, *tokens, **kwargs)


def info_3(*tokens: Token, **kwargs: Any) -> None:
    """ Print an even less important informative message """
    info(bold, blue, "*", reset, *tokens, **kwargs)


def dot(*, last: bool = False, fileobj: Any = None) -> None:
    """ Print a dot without a newline unless it is the last one.

    Useful when you want to display a progress with very little
    knowledge.

    :param last: whether this is the last dot (will insert a newline)
    """
    end = "\n" if last else ""
    info(".", end=end, fileobj=fileobj)


def info_count(i: int, n: int, *rest: Token, **kwargs: Any) -> None:
    """ Display a counter before the rest of the message.

    ``rest`` and ``kwargs`` are passed to :func:`info`

    Current index should start at 0 and end at ``n-1``, like in ``enumerate()``

    :param i: current index
    :param n: total number of items
    """
    num_digits = len(str(n))
    counter_format = "(%{}d/%d)".format(num_digits)
    counter_str = counter_format % (i + 1, n)
    info(green, "*", reset, counter_str, reset, *rest, **kwargs)


def info_progress(prefix: str, value: float, max_value: float) -> None:
    """ Display info progress in percent.

    :param value: the current value
    :param max_value: the max value
    :param prefix: the prefix message to print


    """
    if sys.stdout.isatty():
        percent = float(value) / max_value * 100
        sys.stdout.write(prefix + ": %.0f%%\r" % percent)
        sys.stdout.flush()


def debug(*tokens: Token, **kwargs: Any) -> None:
    """ Print a debug message.

    Messages are shown only when ``CONFIG["verbose"]`` is true
    """
    if not CONFIG["verbose"] or CONFIG["record"]:
        return
    message(*tokens, **kwargs)


def indent_iterable(elems: Sequence[str], num: int = 2) -> List[str]:
    """Indent an iterable."""
    return [" " * num + l for l in elems]


def indent(text: str, num: int = 2) -> str:
    """Indent a piece of text."""
    lines = text.splitlines()
    return "\n".join(indent_iterable(lines, num=num))


def tabs(num: int) -> str:
    """ Compute a blank tab

    """
    return "  " * num


def info_table(
    data: Any, *, headers: Optional[List[str]] = None, fileobj: Any = None
) -> None:
    if not fileobj:
        fileobj = sys.stdout
    colored_data = list()
    plain_data = list()
    for row in data:
        colored_row = list()
        plain_row = list()
        for item in row:
            colored_str, plain_str = process_tokens(item, end="")
            colored_row.append(colored_str)
            plain_row.append(plain_str)
        colored_data.append(colored_row)
        plain_data.append(plain_row)
    if config_color(fileobj):
        data_for_tabulate = colored_data
    else:
        data_for_tabulate = plain_data

    res = tabulate.tabulate(data_for_tabulate, headers=headers)
    res += "\n"
    write_and_flush(fileobj, res)


def message_for_exception(exception: Exception, message: str) -> Sequence[Token]:
    """ Returns a tuple suitable for cli_ui.error()
    from the given exception.
    (Traceback will be part of the message, after
    the ``message`` argument)

    Useful when the exception occurs in an other thread
    than the main one.

    """
    tb = sys.exc_info()[2]
    buffer = io.StringIO()
    traceback.print_tb(tb, file=io)  # type: ignore
    # fmt: off
    return (
        red, message + "\n",
        exception.__class__.__name__,
        str(exception), "\n",
        reset, buffer.getvalue()
    )
    # fmt: on


def read_input() -> str:
    """ Read input from the user

    """
    info(green, "> ", end="")
    return input()


def read_password() -> str:
    """ Read a password from the user

    """
    info(green, "> ", end="")
    return getpass.getpass(prompt="")


def get_ask_tokens(tokens: Sequence[Token]) -> List[Token]:
    return [green, "::", reset] + list(tokens) + [reset]


def ask_string(*question: Token, default: Optional[str] = None) -> Optional[str]:
    """Ask the user to enter a string.
    """
    tokens = get_ask_tokens(question)
    if default:
        tokens.append("(%s)" % default)
    info(*tokens)
    answer = read_input()
    if not answer:
        return default
    return answer


def ask_password(*question: Token) -> str:
    """Ask the user to enter a password.
    """
    tokens = get_ask_tokens(question)
    info(*tokens)
    answer = read_password()
    return answer


FuncDesc = Callable[[Any], str]


def ask_choice(
    *prompt: Token, choices: List[Any], func_desc: Optional[FuncDesc] = None
) -> Any:
    """Ask the user to choose from a list of choices.

    :return: the selected choice

    ``func_desc`` will be called on every list item for displaying
    and sorting the list. If not given, will default to
    the identity function.

    Will loop until:
        * the user enters a valid index
        * or hits ``ctrl-c``
        * or leaves the prompt empty

    In the last two cases, None will be returned
    """
    if func_desc is None:
        func_desc = lambda x: str(x)
    tokens = get_ask_tokens(prompt)
    info(*tokens)
    choices.sort(key=func_desc)
    for i, choice in enumerate(choices, start=1):
        choice_desc = func_desc(choice)
        info("  ", blue, "%i" % i, reset, choice_desc)
    keep_asking = True
    res = None
    while keep_asking:
        answer = read_input()
        if not answer:
            return None
        try:
            index = int(answer)
        except ValueError:
            info("Please enter a valid number")
            continue
        if index not in range(1, len(choices) + 1):
            info(str(index), "is out of range")
            continue
        res = choices[index - 1]
        keep_asking = False

    return res


def ask_yes_no(*question: Token, default: bool = False) -> bool:
    """Ask the user to answer by yes or no"""
    while True:
        tokens = [green, "::", reset] + list(question) + [reset]
        if default:
            tokens.append("(Y/n)")
        else:
            tokens.append("(y/N)")
        info(*tokens)
        answer = read_input()
        if answer.lower() in ["y", "yes"]:
            return True
        if answer.lower() in ["n", "no"]:
            return False
        if not answer:
            return default
        warning("Please answer by 'y' (yes) or 'n' (no) ")


AnyFunc = Callable[..., Any]


class Timer:
    """ Display time taken when executing a list of statements.

    """

    def __init__(self, description: str):
        self.description = description
        self.start_time = datetime.datetime.now()
        self.stop_time = datetime.datetime.now()
        self.elapsed_time = 0

    def __call__(self, func: AnyFunc, *args: Any, **kwargs: Any) -> AnyFunc:
        @functools.wraps(func)
        def res(*args: Any, **kwargs: Any) -> Any:
            self.start()
            ret = func(*args, **kwargs)
            self.stop()
            return ret

        return res

    def __enter__(self) -> "Timer":
        self.start()
        return self

    def __exit__(self, *unused: Any) -> None:
        self.stop()

    def start(self) -> None:
        """ Start the timer """
        self.start_time = datetime.datetime.now()

    def stop(self) -> None:
        """ Stop the timer and emit a nice log """
        end_time = datetime.datetime.now()
        elapsed_time = end_time - self.start_time
        elapsed_seconds = elapsed_time.seconds
        hours, remainder = divmod(int(elapsed_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        as_str = "%sh %sm %ss %dms" % (
            hours,
            minutes,
            seconds,
            elapsed_time.microseconds / 1000,
        )
        info("%s took %s" % (self.description, as_str))


def did_you_mean(message: str, user_input: str, choices: Sequence[str]) -> str:
    """ Given a list of choices and an invalid user input, display the closest
    items in the list that match the input.

    """
    if not choices:
        return message
    else:
        result = {
            difflib.SequenceMatcher(a=user_input, b=choice).ratio(): choice
            for choice in choices
        }
        message += "\nDid you mean: %s?" % result[max(result)]
        return message


def main_test_colors() -> None:
    this_module = sys.modules[__name__]
    for name, value in inspect.getmembers(this_module):
        if isinstance(value, Color):
            info(value, name)


def main_demo() -> None:
    info("OK", check)
    up = Symbol("👍", "+1")
    info("I like it", blue, up)
    info_section(bold, "python-cli demo")
    # Monkey-patch message() so that we sleep after
    # each call
    global message
    old_message = message

    def new_message(*args: Any, **kwargs: Any) -> None:
        old_message(*args, **kwargs)
        time.sleep(1)

    message = new_message

    info_1("Important info")
    info_2("Secondary info")
    info("This is", red, "red")
    info("this is", bold, "bold")
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        info_count(i, len(list_of_things), thing)
    info_progress("Done", 5, 20)
    info_progress("Done", 10, 20)
    info_progress("Done", 20, 20)
    info("\n", check, "all done")

    # stop monkey patching
    message = old_message
    fruits = ["apple", "orange", "banana"]
    answer = ask_choice("Choose a fruit", choices=fruits)
    info("You chose:", answer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["test_colors", "demo"])
    args = parser.parse_args()
    if args.action == "demo":
        main_demo()
    elif args.action == "test_colors":
        main_test_colors()


if __name__ == "__main__":
    main()
