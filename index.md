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

## Table

> https://github.com/derekeder/csv-to-html-table

Livemark supports CSV tables rendering (replace single quotes to back ticks):

```
'''table
data/country-codes.csv
'''
```

```table
data/country-codes.csv
```

## Chart

> https://vega.github.io/vega-lite/

Livemark supports Vega Lite visualisations rendering (replace single quotes to back ticks):

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

## Code

> https://prismjs.com/

Syntax highlithing is proviced by PrismJS (replace single quotes to back ticks):

```
'''python
# This program adds two numbers

num1 = 1.5
num2 = 6.3

# Add two numbers
sum = num1 + num2

# Display the sum
print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))
'''
```

```python
# This program adds two numbers

num1 = 1.5
num2 = 6.3

# Add two numbers
sum = num1 + num2

# Display the sum
print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))
```

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

Then, you can update the layout as whole or use Jinja's inheritance. For example, let's use Tailwind instead of Bootstrap and some custom styles:

> layout.html

{% raw %}
```html
{% extends "layout.html" %}.

{% block style %}
<link rel="stylesheet" href="static/tailwind.css">
<link rel="stylesheet" href="static/custom.css">
{% endblock %}
```
{% endraw %}

Then link your new layout in markdown documents:

> article.md

```md
---
layout: layout.html
---
# My Article

This article uses a custom layout
```
