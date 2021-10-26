# Building a Website

Livemark is a very simple static site generator design-wise. It takes your Markdown documents as input and outputs HTML documents. The result can be deployed as it is to any static site hosting.

## Build

You can then use the command-line interface to build the output HTML file:

```bash
# Build a single document (index.md by default)
$ livemark build
```

Or start a livereload server to automatically reload the output page as you modify the input Markdown document:

```bash
# Start a livereload server
$ livemark start
```

Both commands will create an `index.md` file if it's not present in the same folder the command is being run on. If that's not the case you can pass the path to the input Markdown file as the first parameter:

```bash
$ livemark build path/to/your/file.md
$ livemark start path/to/your/file.md
```

## Publish

> https://pages.github.com/

Livemark generates a static HTML document so you can publish it using any static page hosting. A common option for hosting is to use Github Pages - go to "Settings->Pages" in your repository and choose your main branch in the source menu:

```yaml image
path: ../../assets/deploy.png
width: 75%
height: unset
class: border
```
