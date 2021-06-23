# Configuration

## Document

Livemark document can be configured using a frontmatter:

> index.md

```md
---
title: My Title
---

# My Document
```

## Project

For the whole project, you can use `livemark.yaml` file in the project root directory. It will be merge to the document configuration with lower priority:

> livemark.yaml

```yaml
title: Global Title
```
