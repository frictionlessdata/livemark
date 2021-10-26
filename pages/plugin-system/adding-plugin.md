# Adding a Plugin

## Overview

When you work on your Livemark project there are different options of adding a plugin to the building process:
- installing an external plugin
- adding a custom plugin

## External Plugin

You can install an external plugin, for example:

```bash
$ pip install livemark-ckan
```

And activate it in `livemark.yaml` file:

```yaml
ckan: true # or a plugin config
```

## Custom Plugin

You can [Write a Plugin](write-plugin.html) and put it into `plugin.py` module or export from `plugins` package in your project root. You don't need to activate it in `livemark.yaml`. For example, you can take a look how it works in the [Livemark Project Template](https://github.com/frictionlessdata/livemark-project).

It's also possible to add a plugin programmatically:

```python
from livemark import system

system.register(CustomPlugin)
```
