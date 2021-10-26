# Configuration

Livemark doesn't require any configuration by default. If you haven't started your first project yet you can skip this section. On the other hand, this knowledge will help you later so we recommend reading it in-advance.

## Project

To configure the whole project, you can use `livemark.yaml` file in the project root directory. This file need to be written in YAML syntax:

> livemark.yaml

```yaml
site:
  title: Global Title
```

## Document

Every document can be configured using a frontmatter. Document's config has a high priority over the project config.

> index.md

```md
---
site:
  title: My Title
---

# My Document
```
