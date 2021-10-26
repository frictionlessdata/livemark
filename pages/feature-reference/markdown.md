# Markdown

Livemark extends Markdown with variety of features. Usually, a codeblock syntax is used for new functionality. For example, adding a `script` word to a Python snippet's header will make it a Livemark script.

## Task

Livemark allows you to include Python and Bash tasks in your markdown documents and run them using `livemark run` command. This functionality is really useful for a data-driven project where you can share the whole process of getting and transforming your data in a markdown document preserving an ability to run those scripts. It's also used for Contribution Guides and similar documents. It will be rendered as a code block with the command to run it added:

```
'''python task id=example
print('It is a task')
'''
```

```python task id=example
print('It is a task')
```

You can run it using:

```bash
$ livemark run example
```
```
It is a task
```

## Logic

> https://jinja.palletsprojects.com/en/3.0.x/templates/

Livemark process your document using the Jinja templating language. Inside templates, you can use [Frictionless Framework](https://framework.frictionlessdata.io/) as a `frictionless` variable to work with tabular data. It's a high-level data preprocessing so you can combine Logic with other syntax, such as Table or Chart:

{% raw %}
```
{% for car in frictionless.extract('data/cars.csv', layout={"limitRows": 5}) %}
- {{ car.brand }} {{ car.model }}: ${{ car.price }}
{% endfor %}
```
{% endraw %}

{% for car in frictionless.extract('data/cars.csv', layout={"limitRows": 5}) %}
- {{ car.brand }} {{ car.model }}: ${{ car.price }}
{% endfor %}

## Table

> https://datatables.net/manual/index

Livemark supports CSV table rendering using DataTables, which you can see in the example below (replace the single quotes with back ticks). The `data` property will be read at the build stage so in addition to DataTables options you can pass a [file path](https://raw.githubusercontent.com/frictionlessdata/livemark/main/data/cars.csv) as `data` property (CSV/Excel/JSON are supported). Use `columns` property to customize fields or their order:

```yaml
'''yaml table
data: data/cars.csv
width: 600
order:
  - [3, 'desc']
columns:
  - data: type
  - data: brand
  - data: model
  - data: price
  - data: kmpl
  - data: bhp
'''
```

```yaml table
data: data/cars.csv
width: 600
order:
  - [3, 'desc']
columns:
  - data: type
  - data: brand
  - data: model
  - data: price
  - data: kmpl
  - data: bhp
```

## Chart

> https://vega.github.io/vega-lite/

Livemark supports Vega Lite visualisations rendering (to try this example, replace the single quotes with back ticks):

```yaml
'''yaml chart
data:
  url: ../../data/cars.csv
mark: circle
selection:
  brush:
    type: interval
# other options are omitted
width: 500
height: 300
'''
```

```yaml chart
data:
  url: ../../data/cars.csv
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

Livemark supports Python/Bash script execution inside Markdown. We think of this as a lightweight version of Jupyter Notebooks. Sometimes, a declarative Logic/Table/Chart is not enough for presenting data so you might also want to include the scripts:

```python script
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

> https://getbootstrap.com/docs/5.0/getting-started/introduction/

With Livemark you can use HTML inside Markdown with Bootstrap support. Here is an example of creating a responsive grid of cards (note that if we set a `livemark-markdown` class we can use markdown inside html):

```html
'''html markup
<div class="w-50">
<div class="container">
<div class="row">
<div class="col-sm">
  <div class="markdown">![Package](../../assets/data-package.png)</div>
  <div class="text-center">
  <p><strong>Data Package</strong></p>
  <p>A simple container format for describing a coherent collection of data in a single package.</p>
  </div>
</div>
<!-- other columns are omitted -->
</div>
</div>
</div>
'''
```

```html markup
<div style="max-width: 600px">
<div class="container">
<div class="row">
<div class="col-sm">
  <div class="livemark-markdown">![Package](../../assets/data-package.png)</div>
  <div class="text-center">
  <p><strong>Data Package</strong></p>
  <p>A simple container format for describing a coherent collection of data in a single package.</p>
  </div>
</div>
<div class="col-sm">
  <div class="livemark-markdown">![Resource](../../assets/data-resource.png)</div>
  <div class="text-center">
  <p><strong>Data Resource</strong></p>
  <p>A simple format to describe and package a single data resource such as a individual table or file.</p>
  </div>
</div>
<div class="col-sm">
  <div class="livemark-markdown">![Schema](../../assets/table-schema.png)</div>
  <div class="text-center">
  <p><strong>Table Schema</strong></p>
  <p>A simple format to declare a schema for tabular data. The schema is designed to be expressible in JSON.</p>
  </div>
</div>
</div>
</div>
</div>
```

## Map

> https://geojson.org/

Livemark supports GeoJson visualisations rendering (to try this example, replace the single quotes with back ticks):

```yaml
'''yaml map
data: data/france.json
'''
```

```yaml map
data: data/france.json
```

## Audio

This feature renders an audio file or a SoundCloud track:

```
'''yaml audio
path: https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3
width: 50%
'''
```

```yaml image
path: ../../assets/soundcloud.png
width: 50%
height: unset
class: border
```

## File

This feature adds a file from the disc with a given code syntax:

```
'''python file
livemark/__init__.py
'''
```

```python file
livemark/__init__.py
```

## Image

This feature adds an image with an ability to customize dimensions and CSS class:

```yaml image
path: ../../assets/example.png
width: 50%
height: unset
class: border
```

## Remark

This feature for adding a remark is being developed at the moment.

## Package

This feature renders a Frictionless Data Package:

```
'''yaml package
descriptor: https://raw.githubusercontent.com/fjuniorr/cicd-gh-pages-rmarkdown/main/datapackage.json
'''
```

```yaml image
path: ../../assets/package.png
width: 50%
height: unset
class: border
```

## Reference

This includes a Python function or class reference (in active development):

```
'''yaml reference
path: livemark.Document
'''
```

```yaml reference
path: livemark.Document
```

## Notebook

This feature for including Jupyter Notebooks is being developed at the moment.

## Report

This renders an interactive Validation Report, using the Frictionless Framework:

```
'''yaml report
descriptor: data/invalid.report.json
'''
```

```yaml image
path: ../../assets/report.png
width: 100%
height: unset
class: border
```

## Resource

This feature for including Data Resource is being developed at the moment.

## Schema

It renders an interactive Table Schema, using the Frictionless Framework:

```
'''yaml schema
descriptor: data/cars.schema.json
'''
```

```yaml image
path: ../../assets/schema.png
width: 100%
height: unset
class: border
```

## Video

This feature renders a video file or a YouTube video:

```
'''yaml video/youtube
code: NMg-eCbO6L0
'''
```

```yaml image
path: ../../assets/youtube.png
width: 50%
height: unset
class: border
```

## Pipeline

This feature for including Transformation Pipelines is being developed at the moment.
