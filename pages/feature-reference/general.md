# General

## Site

To build a website (all the commands belows are equal):

```bash
$ livemark build
$ livemark build index.md
$ livemark build index.md --target index.html
```

Configuration, for example:

```yaml
site:
  favicon: assets/favicon.ico
  styles:
    - style.css
```

## HTML

To build just a document without the site:

```python
from livemark import Project

project = Project('source.md', target='target.md', config={"site": False})
project.document.build()
```

## Markdown

To build a document as a Markdown:

```bash
$ livemark build source.md --target target.md
```

Note that for the markdown rendering only a limited set of plugins are supported such as `script`. To get all from Livemark it's better to reder documents as HTML.