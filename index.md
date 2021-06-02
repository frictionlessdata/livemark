---
title: Livemark
---

# Livemark

[![Build](https://img.shields.io/github/workflow/status/frictionlessdata/livemark/general/main)](https://github.com/frictionlessdata/livemark/actions)
[![Coverage](https://img.shields.io/codecov/c/github/frictionlessdata/livemark/main)](https://codecov.io/gh/frictionlessdata/livemark)
[![Registry](https://img.shields.io/pypi/v/livemark.svg)](https://pypi.python.org/pypi/livemark)
[![Codebase](https://img.shields.io/badge/codebase-github-brightgreen)](https://github.com/frictionlessdata/livemark)
[![Support](https://img.shields.io/badge/support-discord-brightgreen)](https://discord.com/channels/695635777199145130/695635777199145133)

Publish articles written in extended Markdown at ease.

## Table

> https://github.com/derekeder/csv-to-html-table

Livemark supports CSV tables rendering (replace single quote to back tickes):

```
'''table
data/country-codes.csv
'''
```

```table
data/country-codes.csv
```

## Chart

> https://github.com/derekeder/csv-to-html-table

Livemark supports Vega Lite visualisations rendering (replace single quote to back tickes):

```
'''chart
data:
  url: "data/cars.csv"
mark: circle
selection:
  brush:
    type: interval
encoding:
  x:
    type: quantitative
    field: kmpl
    scale:
     domain: [12,25]
  y:
    type: quantitative
    field: price
    scale:
     domain: [100,900]
  color:
    condition:
      selection: brush
      field: type
      type: nominal
    value: grey
  size:
    type: quantitative
    field: bhp
width: 450
height: 300
'''
```

```chart
data:
  url: "data/cars.csv"
mark: circle
selection:
  brush:
    type: interval
encoding:
  x:
    type: quantitative
    field: kmpl
    scale:
     domain: [12,25]
  y:
    type: quantitative
    field: price
    scale:
     domain: [100,900]
  color:
    condition:
      selection: brush
      field: type
      type: nominal
    value: grey
  size:
    type: quantitative
    field: bhp
width: 450
height: 300
```

## Logic

> https://jinja.palletsprojects.com/en/3.0.x/templates/

Livemark preprosecces your document using Jinja templating language:

{% raw %}
```
{% for number in [1, 2, 3] %}
- number: {{ number }}
{% endfor %}
```
{% endraw %}

{% for number in [1, 2, 3] %}
- number: {{ number }}
{% endfor %}

## Style

> https://getbootstrap.com/docs/4.6/getting-started/introduction/

With Livemark you can use HTML inside Markdown with Bootstrap 4 support. Here is an example of creating a "hero" element:

```html
<div class="jumbotron">
<h1 class="display-4">Hello, world!</h1>
<p class="lead">This is a simple hero unit.</p>
<hr class="my-4">
<p>It uses Bootstrap 4.</p>
<a class="btn btn-primary btn-lg" href="#" role="button">Learn more</a>
</div>
```

<div class="jumbotron">
<h1 class="display-4">Hello, world!</h1>
<p class="lead">This is a simple hero unit.</p>
<hr class="my-4">
<p>It uses Bootstrap 4.</p>
<a class="btn btn-primary btn-lg" href="#" role="button">Learn more</a>
</div>

Note that, an HTML block can't contain blank lines and if you need to use markdown inside HTML it will only work if you set `class="markdown"`:

```html
<div class="markdown">
**This text is highlighted**
</div>
```

<div class="markdown">
**This text is highlighted**
</div>

## Layout

> https://github.com/frictionlessdata/livemark/blob/main/livemark/assets/templates/layout.html

It's possible to customize the layout. You need to save it first:

```bash
$ livemark layout > layout.html
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

<script src="static/jquery.min.js"></script>
<script src="static/popper.min.js"></script>
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
