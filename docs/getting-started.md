# Getting Started

## Installation

Livemark is a Python library and it can be installed with pip (or [pipx](https://pypa.github.io/pipx/)):

```bash
$ pip install livemark
```

After installation, you can start writing your document (eg an `index.md` file) using the extended Markdown syntax described in the next sections.

## Usage

You can then use the command-line interface to build the output HTML file:

```bash
# Build a single document
$ livemark build
```

Or start a livereload server to automatically reload the output page as you modify the input Markdown document:

```bash
# Start a livereload server
$ livemark start
```

Both commands assume that an `index.md` file is present in the same folder the command is being run on. If that's not the case you can pass the path to the input Markdown file as the first parameter:

```bash
$ livemark build path/to/your/file.md
$ livemark start path/to/your/file.md
```
