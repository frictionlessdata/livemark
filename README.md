# Livermark

[![Build](https://img.shields.io/github/workflow/status/frictionlessdata/livemark/general/main)](https://github.com/frictionlessdata/livemark/actions)
[![Coverage](https://img.shields.io/codecov/c/github/frictionlessdata/livemark/main)](https://codecov.io/gh/frictionlessdata/livemark)
[![Registry](https://img.shields.io/pypi/v/livemark.svg)](https://pypi.python.org/pypi/livemark)
[![Codebase](https://img.shields.io/badge/codebase-github-brightgreen)](https://github.com/frictionlessdata/livemark)
[![Support](https://img.shields.io/badge/support-discord-brightgreen)](https://discord.com/channels/695635777199145130/695635777199145133)

> This software is in the early stages and not well-tested

Livemark is a static page generator that extends Markdown with interactive charts, tables, scripts, and more.

## Purpose

- **Improved writing experience**: You can write data articles the way use usually do but with support of interactive charts, tables, live development server, and many more.
- **Static site generator**: Livemark is fully predictable as it only operates with static files. It create an HTML file from your Mardown file.

## Features

- Open Source (MIT)
- Full markdown compatibility
- Markdown extensions such as tables and charts
- Simple command-line interface
- Live development server

## Example

> Take a look at the [DEMO](https://frictionlessdata.github.io/livemark/) article

```bash
# Build a single document
$ livemark build '<path=index.md>'

# Start a livereload server
$ livemark start
```

## Documentation

Please visit our documentation portal:
- https://frictionlessdata.github.io/livemark/
