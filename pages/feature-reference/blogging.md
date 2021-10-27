# Blogging

## Blog

Blog is an essential part of many websites and Livemark provides it as well. To activate the blog feature:
- create a `blog` folder in the project's root directory
- add an article there, e.g. `blog/2021-09-01-article.md`
- add a blog index to the pages, e.g. `- path: blog/index`

It's possible to customize an article using frontmatter:

> blog/2021-09-01-article.md

```yaml
blog:
  author: John Doe
  image: ../assets/example.png
```

See [Blog](../../blog/index.html) as an example.

## Comments

To enable comments for a specific article you need to provide frontmatter with Disqus id and a canonical website link:

> article.md

```yaml
comments:
  code: livemark
  link: https://livemark.frictionlessdata.io
```

It's possible to enable comments for all the pages using project config:

> livemark.yaml

```yaml
comments:
  code: livemark
  link: https://livemark.frictionlessdata.io
```

See [Forum](../forum.html) as an example.
