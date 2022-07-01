# Starting a Project

> Start quickly with [Livemark Project](https://github.com/frictionlessdata/livemark-project) Github Template

Project is the most important concept in Livemark along side with Document. You create a project that contains one or more documents and optional [configuration](../configuration.html) file.

## Prepare

Consider you're starting a new project called `my-project`:

```bash
$ mkdir my-project
$ cd my-project
```

Create a virtual environment (optional):

```bash
$ python3 -m venv .python
$ source .python/bin/activate
```

## Bootstrap

Livemark requires only a few steps from zero to a published project:

First of all, create:
- `index.md`
- `livemark.yaml`

Draft the main page (**this step is required**):

> index.md

```md
# My Project

It will be great here
```

Fill in your configuration file:

> livemark.yaml

```yaml
brand:
  text: My Project
site:
  favicon: assets/favicon.ico
```

## Preview

Now we're ready to start a livereload server:

> http://localhost:7000

```bash
$ livemark start
```

