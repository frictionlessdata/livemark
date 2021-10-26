# Architecture

```yaml remark
type: warning
text: This article is work-in-progress
```

## Overview

In a nutshell, Livemark is just a text processor. It takes a Markdown document and outputs an HTML document. It also possible to ouput different formats but the main Livemark's specialization is Markdown-to-HTML conversion.

## Plugins

Livemark's core only provides an abstract classes like Project, Document, or Snippet. The actual work is done by various plugins like HtmlPlugin, SitePlugin, or TablePlugin. You can find their description in the Livemark Markdown and Livemark Features sections.

## Build

On the figure below we present the Livemark's building flow schematically: a Markdown document containing various snippets being converted to an HTML document containing various markup blocks by Livemark and its plugins:

```yaml image
path: ../../assets/flow.png
width: 100%
height: unset
```
