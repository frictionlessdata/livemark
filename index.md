---
title: Livemark
---

# Livemark

[![Build](https://img.shields.io/github/workflow/status/frictionlessdata/livemark/general/main)](https://github.com/frictionlessdata/livemark/actions)
[![Coverage](https://img.shields.io/codecov/c/github/frictionlessdata/livemark/main)](https://codecov.io/gh/frictionlessdata/livemark)
[![Registry](https://img.shields.io/pypi/v/livemark.svg)](https://pypi.python.org/pypi/livemark)
[![Codebase](https://img.shields.io/badge/codebase-github-brightgreen)](https://github.com/frictionlessdata/livemark)
[![Support](https://img.shields.io/badge/support-discord-brightgreen)](https://discord.com/channels/695635777199145130/695635777199145133)

It's a test article

<div>
**test**
</div>

```python
print('Hello World')
```

## Style

Example with a grid:

<div class="container">
<div class="row">
<div class="col-sm">
One of three columns
</div>
<div class="col-sm">
One of three columns
</div>
<div class="col-sm">
One of three columns
</div>
</div>
</div>

## Logic

Example with a list:

{% for number in [1, 2, 3] %}
- number: {{ number }}
{% endfor %}

## Table

## Chart

## Layout

It's possible to customize the layout.

You need to save it first:

```bash
livemark layout > layout.html
```

Then, for example, switch to local static files:

> layout.html

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="static/bootstrap.min.css">
<link rel="stylesheet" href="static/github-markdown.css">
<link rel="stylesheet" href="static/prism.css">
<title>{{ title }}</title>
</head>
<body>

<div class="container">
<div class="markdown-body m-5 px-lg-5">
{{ content }}
</div>
</div>

<script src="static/bootstrap.min.js"></script>
<script src="static/prism-core.min.js"></script>
<script src="static/prism-autoloader.min.js"></script>
</body>
</html>
```

And use your new layout in markdown documents:

> article.md

```md
---
layout: layout.html
---
# My Article

This article uses a custom layout
```
