# python-cli-ui

[![Python](https://img.shields.io/pypi/pyversions/cli-ui.svg)](https://pypi.org/project/cli-ui)
[![PyPI](https://img.shields.io/pypi/v/cli-ui.svg)](https://pypi.org/project/cli-ui/)
[![License](https://img.shields.io/github/license/your-tools/python-cli-ui.svg)](https://github.com/your-tools/python-cli-ui/blob/main/LICENSE)

Tools for nice user interfaces in the terminal.

## Note

This project was originally hosted on the [TankerHQ](https://github.com/TankerHQ) organization, which was my employer from 2016 to 2021. They kindly agreed to give back ownership of this project to me. Thanks!

## Features

- **Colored output**: Easy to use color constants and formatting
- **User input**: Ask questions, get choices, passwords
- **Progress indication**: Show progress with dots, counters, and progress bars  
- **Tables**: Display data in nicely formatted tables
- **Timers**: Time operations with context managers or decorators
- **Cross-platform**: Works on Linux, macOS, and Windows

## Installation

```bash
pip install cli-ui
```

## Quick Start

```python
import cli_ui

# Coloring
cli_ui.info(
    "This is", cli_ui.red, "red", cli_ui.reset,
    "and this is", cli_ui.bold, "bold"
)

# User input
with_sugar = cli_ui.ask_yes_no("With sugar?", default=False)

fruits = ["apple", "orange", "banana"]
selected_fruit = cli_ui.ask_choice("Choose a fruit", choices=fruits)

# Progress
list_of_things = ["foo", "bar", "baz"]
for i, thing in enumerate(list_of_things):
    cli_ui.info_count(i, len(list_of_things), thing)

# Tables
headers = ["name", "score"]
data = [
    [("John", cli_ui.bold), (10, cli_ui.green)],
    [("Jane", cli_ui.bold), (5, cli_ui.green)],
]
cli_ui.info_table(data, headers=headers)
```

## API Overview

### Colors and Formatting

Available colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
Available formatting: `bold`, `faint`, `standout`, `underline`, `blink`, `overline`, `reset`

### Information Functions

- `info(*tokens, **kwargs)` - Print informative message
- `info_1(*tokens, **kwargs)` - Important info with "::" prefix
- `info_2(*tokens, **kwargs)` - Secondary info with "=>" prefix  
- `info_3(*tokens, **kwargs)` - Detailed info with "*" prefix
- `info_section(*tokens, **kwargs)` - Section header with underline
- `debug(*tokens, **kwargs)` - Debug message (only shown if verbose=True)

### Error Functions

- `warning(*tokens, **kwargs)` - Print warning message
- `error(*tokens, **kwargs)` - Print error message  
- `fatal(*tokens, exit_code=1, **kwargs)` - Print error and exit

### Progress Functions

- `dot(last=False, fileobj=sys.stdout)` - Print progress dot
- `info_count(i, n, *rest, **kwargs)` - Show counter with message
- `info_progress(prefix, value, max_value)` - Show percentage progress

### User Input Functions

- `ask_string(*question, default=None)` - Ask for string input
- `ask_password(*question)` - Ask for password (hidden input)
- `ask_yes_no(*question, default=False)` - Ask yes/no question
- `ask_choice(*prompt, choices, func_desc=None, sort=True)` - Choose from list
- `select_choices(*prompt, choices, func_desc=None, sort=True)` - Select multiple

### Table Functions

- `info_table(data, headers=(), fileobj=sys.stdout)` - Display formatted table

### Utility Functions

- `indent(text, num=2)` - Indent text by number of spaces
- `tabs(num)` - Generate tab spacing
- `did_you_mean(message, user_input, choices)` - Suggest corrections

### Configuration

```python
cli_ui.setup(
    verbose=False,    # Show debug messages
    quiet=False,      # Hide info messages  
    color="auto",     # Color mode: "auto", "always", "never"
    title="auto",     # Terminal title updates
    timestamp=False   # Add timestamps to messages
)
```

### Timer Context Manager

```python
# As context manager
with cli_ui.Timer("doing something"):
    do_something()

# As decorator
@cli_ui.Timer("processing")
def process_data():
    # ... processing code
    pass
```

## Testing Support

For testing code that uses cli-ui:

```python
from cli_ui.tests import MessageRecorder

def test_my_function(message_recorder):
    message_recorder.start()
    my_function()  # calls cli_ui.info("something")
    assert message_recorder.find("something")
    message_recorder.stop()
```

## Examples

See the `examples/` directory for:
- Basic usage examples
- Threading examples  
- Async/await examples

## Requirements

- Python 3.7+
- colorama>=0.4.1
- tabulate>=0.8.3
- unidecode>=1.0.23

## License

BSD 3-Clause License. See LICENSE file for details.

## Contributing

Contributions welcome! Please see the contributing guidelines in the repository.