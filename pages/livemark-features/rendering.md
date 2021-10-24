# Rendering

Currently, Livemark supports two rendering target: HTML and Markdown.

## HTML

To build a document as an HTML (all the commands belows are equal):

```bash
$ livemark build
$ livemark build index.md
$ livemark build index.md --target index.html
```

In-general, most of Livemark features are only applicable to the HTML rendering target.

## Markdown

To build a document as a Markdown:

```bash
$ livemark build source.md --target target.md
```

Note that for the markdown rendering only a limited set of plugins are supported such as `script`. To get all from Livemark it's better to reder documents as HTML.


---

You can [write your own](../plugin-system/writing-plugin.html) renderer using Plugin System or use an [external one](../plugin-system/adding-plugin.html).
