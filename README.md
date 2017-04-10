# python-cli-ui

This repository contains a small Python module I've been using
in several projects.

## Demo:

```python
info_1("Info 1")
time.sleep(0.5)
info_2("Info 2")
time.sleep(0.5)
info_3("Info 3")
time.sleep(0.5)
list_of_things = ["foo", "bar", "baz"]
for i, thing in enumerate(list_of_things):
    time.sleep(0.5)
    info_count(i, len(list_of_things), thing)
info_progress("Done",  5, 20)
time.sleep(0.5)
info_progress("Done", 10, 20)
time.sleep(0.5)
info_progress("Done", 20, 20)
time.sleep(0.5)
info("\n", check, "all done")
```

https://asciinema.org/a/112368


## Usage

Install the dependencies in `requirements.txt`, copy/paste the `ui.py` file and
use it in your code.

## Testing

Tests are written using `pytest`.

You can check what messages are displayed in your own tests using the
`messages` fixture in the `conftest.py` file

## FAQ

### Why not publish on pypi ?

* I'm lazy
* The code is really small
* It's better for you to integrate the `ui.py` file directly in
  you project: that way you can tweak it however you like, and
  there's no need for a "centralized" project

I can change my mind, though, and I'm also willing to accept pull requests.

### Python2 support?

* Maybe. I've start using Python2 altogether last year, but the code _should_ be
  more or less compatible.

### Windows support?

* Yes! Should work in `mintty` and `cmd.exe` at least.
