# Others

## Cleanup

This feature provides an ability to spicify a list of Bash command to be run after the document building:

> livemark.yaml

```yaml
cleanup:
  - rm table.csv
```

## Counter

This feature currently support a Google Analytics counter that can be added to all the project pages:

> livemark.yaml

```yaml
counter:
  type: google
  code: G-<code>
```

## Github

Some plugins rely on Github repository information that is provided by this feature. Be default, it will be inferred automatically from you local `.git` directory. It's also possible to configure it manually:

> livemark.yaml

```yaml
github:
  user: frictionlessdata
  repo: livemark
```

## Prepare

This feature provides an ability to spicify a list of Bash command to be run before the document building:

> livemark.yaml

```yaml
prepare:
  - cp data/table.csv table.csv
```

## Redirect

Using Github Pages as a hosting it's possible to setup a redirect table:

> livemark.yaml

```yaml
redirect:
  items:
    - prev: getting-started
      next: pages/installation
```

Under the hood, Livemark will create a `404.html` file and use a client-side redirect.
