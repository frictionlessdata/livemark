---
title: Livemark
header:
  title: Livemark
status:
  type: star
  user: frictionlessdata
  repo: livemark
navigation:
  selector: h2, h3
scroll:
  speed: 10
reference:
  links:
    - name: Website
      path: https://frictionlessdata.io/
    - name: Discord
      path: https://discord.com/channels/695635777199145130/695635777199145133
    - name: Twitter
      path: https://twitter.com/frictionlessd8a
---

# Livemark

[![Build](https://img.shields.io/github/workflow/status/frictionlessdata/livemark/general/main)](https://github.com/frictionlessdata/livemark/actions)
[![Coverage](https://img.shields.io/codecov/c/github/frictionlessdata/livemark/main)](https://codecov.io/gh/frictionlessdata/livemark)
[![Registry](https://img.shields.io/pypi/v/livemark.svg)](https://pypi.python.org/pypi/livemark)
[![Codebase](https://img.shields.io/badge/codebase-github-brightgreen)](https://github.com/frictionlessdata/livemark)
[![Support](https://img.shields.io/badge/support-discord-brightgreen)](https://discord.com/channels/695635777199145130/695635777199145133)

> This document is completely [written and published](https://raw.githubusercontent.com/frictionlessdata/livemark/main/index.md) in Livemark notation

Livemark is a static site generator that extends Markdown with interactive charts, tables, scripts, and more.

## Install

Livemark is a Python library and it can be installed with PIP:

```bash
$ pip install livemark
```

After installation, you can use a command-line interface:

```bash
# Build a single document
$ livemark build '<path=index.md>'

# Start a livereload server
$ livemark start
```

When you build/start Livemark it takes your `index.md` (or a provided file) and generates a corresponding HTML file. It extends markdown as explained in the sections below.

## Logic

> https://jinja.palletsprojects.com/en/3.0.x/templates/

Livemark preprocesses your document using the Jinja templating language. Inside templates, you can use [Frictionless Framework](https://framework.frictionlessdata.io/) as a `frictionless` variable to work with tabular data. This is a high-level preprocessing so you can combine Logic with other syntax, such as Table or Chart:

{% raw %}
```markup
{% for car in frictionless.extract('data/cars.csv', layout={"limitRows": 5}) %}
- {{ car.brand }} {{ car.model }}: ${{ car.price }}
{% endfor %}
```
{% endraw %}

{% for car in frictionless.extract('data/cars.csv', layout={"limitRows": 5}) %}
- {{ car.brand }} {{ car.model }}: ${{ car.price }}
{% endfor %}

## Table

> https://handsontable.com/docs/9.0.0/tutorial-introduction.html

Livemark supports CSV table rendering using Handsontable, which you can see in the example below (replace the single quotes with back ticks). The `data` property will be read by [Frictionless Framework](https://framework.frictionlessdata.io/) so in addition to Handsontable options you can pass a [file path](https://raw.githubusercontent.com/frictionlessdata/livemark/main/data/cars.csv) or a resource descriptor in a Frictionless format:

```yaml
'''table
data: data/cars.csv
maxRows: 10
filters: true
dropdownMenu: true
columnSorting:
  initialConfig:
    column: 2
    sortOrder: desc
width: 600
'''
```

```table
data: data/cars.csv
maxRows: 10
filters: true
dropdownMenu: true
columnSorting:
  initialConfig:
    column: 2
    sortOrder: desc
width: 600
```

## Chart

> https://vega.github.io/vega-lite/

Livemark supports Vega Lite visualisations rendering (to try this example, replace the single quotes with back ticks):

```yaml
'''chart
data:
  url: data/cars.csv
mark: circle
selection:
  brush:
    type: interval
# other options are omitted
width: 500
height: 300
'''
```

```chart
data:
  url: data/cars.csv
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
width: 500
height: 300
```

## Script

> https://www.python.org/

Livemark supports Python/Bash script execution inside Markdown. We think of this as a lightweight version of Jupiter Notebooks. Sometimes, a declarative Logic/Table/Chart is not enough for presenting data so you might also want to include scripts:

```script
from pprint import pprint
from frictionless import Resource, transform, steps

brands = transform(
    Resource("data/cars.csv"),
    steps=[
        steps.table_normalize(),
        steps.table_aggregate(group_name="brand", aggregation={"price": ("price", max)}),
        steps.row_sort(field_names=["price"], reverse=True),
        steps.row_slice(head=5),
    ],
)
pprint(brands.read_rows())
```

## Markup

> https://getbootstrap.com/docs/4.6/getting-started/introduction/

With Livemark you can use HTML inside Markdown with Bootstrap 4 support. Here is an example of creating a responsive grid of cards (note that if we set a `markdown` class we can use markdown inside html):

```html
<div class="w-50">
<div class="container">
<div class="row">
<div class="col-sm">
  <div class="markdown">![Package](data/data-package.png)</div>
  <div class="text-center">
  <p><strong>Data Package</strong></p>
  <p>A simple container format for describing a coherent collection of data in a single package.</p>
  </div>
</div>
<!-- other columns are omitted -->
</div>
</div>
</div>
```

<div style="max-width: 600px">
<div class="container">
<div class="row">
<div class="col-sm">
  <div class="markdown">![Package](data/data-package.png)</div>
  <div class="text-center">
  <p><strong>Data Package</strong></p>
  <p>A simple container format for describing a coherent collection of data in a single package.</p>
  </div>
</div>
<div class="col-sm markdown">
  <div class="markdown">![Resource](data/data-resource.png)</div>
  <div class="text-center">
  <p><strong>Data Resource</strong></p>
  <p>A simple format to describe and package a single data resource such as a individual table or file.</p>
  </div>
</div>
<div class="col-sm markdown">
  <div class="markdown">![Schema](data/table-schema.png)</div>
  <div class="text-center">
  <p><strong>Table Schema</strong></p>
  <p>A simple format to declare a schema for tabular data. The schema is designed to be expressible in JSON.</p>
  </div>
</div>
</div>
</div>
</div>

## Content

> https://guides.github.com/features/mastering-markdown/

Livemark supports Github Flavoured Markdown so you can use familiar notation:

![Sidebar](data/content.png)

## Sidebar

> https://tscanlin.github.io/tocbot/

Livemark provides an automatically generated table of contents:

![Sidebar](data/sidebar.png)

## Scroll

> https://azrsix.github.io/ue-scroll-js/

Livemark provides a scroll-to-top button when you scroll down your document:

![Scroll](data/scroll.png)

## Layout

> https://github.com/frictionlessdata/livemark/blob/main/livemark/assets/templates/layout.html

It's possible to customize the layout. You will need to save it first:

```bash
$ livemark layout > layout.html
```

Then, you can update the layout as a whole or use Jinja's inheritance. For example, let's use Tailwind instead of Bootstrap and some custom styles:

> layout.html

{% raw %}
```html
{% extends "layout.html" %}.

{% block markup %}
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

## Publish

> https://pages.github.com/

Livemark generates a static HTML document so you can publish it using any static page hosting. A common option for hosting is to use Github Pages - go to "Settings->Pages" in your repository and choose your main branch in the source menu:

![Github](data/github.png)
