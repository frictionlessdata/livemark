# Software Education

Livemark is perfectly suited for writing education materials as it uses code execution model in markdown documents. This means that as an author you only need to write code snippet inputs while outputs will be automatically inserted into your articles. It solves a range of problems with testing and having your code examples up-to-date.

## Example

Note that this project is under development:

> https://frictionlessdata.github.io/learning-python/

```yaml image
path: ../../assets/education.png
width: 100%
height: unset
class: border
```

## Quick Start

> Start from [Github Template](https://github.com/frictionlessdata/livemark-project) if you want the quickest setup

Livemark requires only a few steps from zero to a published project:

First of all, create:
- `livemark.yaml`
- `index.md`
- `pages/data.md` (for example)

Fill in your configuration file:

> livemark.yaml

```yaml
brand:
  text: My Project
about:
  text: My project is for data journalism
site:
  favicon: assets/favicon.ico
github:
  user: <user>
  repo: <repo>
topics:
  selector: h2
links:
  items:
    - name: About Me
      path: https://personal.site
pages:
  items:
    - name: Introduction
      path: index
    - path: pages/data
```

Run a livereload server locally:

```bash
$ livemark start
```

When you are ready to publish your work, commit the changes and push it to Github. The only missing part now is enabling Github Pages:

> https://guides.github.com/features/pages/

```yaml image
path: ../../assets/deploy.png
width: 75%
height: unset
class: border
```

After this step your documentation portal will be up and running.
