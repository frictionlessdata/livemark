# General

General Livemark features are listed on this page. They are related to document processing and rendering. See other reference sections for more specific features like [Table](markdown.html#table) or [Search](navigation.html#search).

## Site

To build a website (all the commands below are equal):

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

The site will include following client-side software:

- Bootstrap 5
- Font Awesome 5
- Lodash 4
- jQuery 3

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

Note that for the markdown rendering only a limited set of plugins are supported such as `script`. To use all of Livemark's features, it's better to render documents as HTML.
