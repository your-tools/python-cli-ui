# python-cli-ui

This repository contains a small Python module I've been using
in several projects.

## Demo:

Run `python3 ui.py` and be amazed!

Or just watch the [asciinema recording](https://asciinema.org/a/112368)


## Usage

Install the dependencies in `requirements.txt`, copy/paste the `ui.py` file and
use it in your code.

## Testing

Tests are written using `pytest`.

You can check what messages are displayed in your own tests using the
`messages` fixture in the `conftest.py` file

## FAQ

### Documentation?

Use the source, Luke!

I'm too lazy to write a proper documentation, and it would always be outdated
anyway ...


### Why not publish on pypi?

* I'm lazy (again)
* The code is really small
* It's better for you to integrate the `ui.py` file directly in
  you project: that way you can tweak it however you like, and
  there's no need for a "centralized" project

I can change my mind, though, and I'm also willing to accept pull requests.

### Python2 support?

* No. If you need this, feel free to create your own fork :)

### Windows support?

* Yes! Should work in `mintty` and `cmd.exe` at least.
