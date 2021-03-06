# Writing a Plugin

> Start quickly with [Livemark Plugin](https://github.com/frictionlessdata/livemark-plugin) Github Template

## Overview

Livemark provides a plugin interface to help write new plugins. There are 4 main hooks a plugin author can use to alter the rendering process. All of them take an corresponding object that can be updated:

- `Pluing.process_project(project)`
- `pluing.process_document(document)`
- `pluing.process_snippet(snippet)`
- `pluing.process_markup(markup)`

## Example

This plugin simply adds a string to H1 tags on every page in the project:

```python
from livemark import Plugin


class CustomPlugin(Plugin):
    identity = "custom"

    # Process

    def process_markup(self, markup):
        markup.add_markup("<span>(template)<span>", target="h1")
```

## References

To help you write a plugin, explore core plugins, architecture, and API References:
- [Core Plugins](https://github.com/frictionlessdata/livemark/tree/main/livemark/plugins)
- [Architecture](architecture.html)
- [API Reference](reference.html)
