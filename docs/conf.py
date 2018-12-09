import os
import sys

sys.path.insert(0, os.path.abspath(".."))


extensions = ["sphinx.ext.autodoc", "sphinx.ext.todo"]

templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"

project = "cli_ui"
copyright = "2017, Kontrol SAS"
author = "Kontrol SAS"
version = "0.1.0"
release = "0.1.0"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

pygments_style = "sphinx"

todo_include_todos = True


html_theme = "alabaster"
html_copy_source = True
html_show_sourcelink = False
