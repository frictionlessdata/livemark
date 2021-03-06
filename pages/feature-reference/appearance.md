# Appearance

## Brand

This feature adds a project name at the top left corner:

```yaml image
path: ../../assets/brand.png
width: unset
height: unset
class: border
```

> livemark.yaml

```yaml
brand:
  text: Livemark
```

## Notes

By default, this feature shows a last updated datetime and a link to Livemark:

```yaml image
path: ../../assets/notes.png
width: unset
height: unset
class: border
```

> livemark.yaml

```yaml
notes:
  format: %Y-%m-%d
```

## Rating

Based on the "Github" feature setting it will show a repository's star rating:

```yaml image
path: ../../assets/rating.png
width: unset
height: unset
class: border
```

> livemark.yaml

```yaml
rating:
  type: start
```

## About

This feature adds information about the project or the page to the top right corner:

```yaml image
path: ../../assets/about.png
width: unset
height: unset
class: border
```

> livemark.yaml

```yaml
about:
  text: Livemark is a Python static site generator...
```

## Display

This feature gives an ability to print a page, increase/decrease font size readability, and use a "Back to top" button:

```yaml image
path: ../../assets/display.png
width: unset
height: unset
class: border
```

## Mobile

This feature provides a mobile version of the site:

```yaml image
path: ../../assets/mobile.png
width: unset
height: unset
class: border
```

## Source

This features shows a Markdown source of a section on the "Source" heading button, which is available on hover. It is really useful to show the underlying source code for data visualisations:

```yaml image
path: ../../assets/source.png
width: 100%
height: unset
class: border
```

## News

This adds news to the top of the site:

```yaml image
path: ../../assets/news.png
width: 100%
height: unset
class: border
```

> livemark.yaml

```yaml
news:
  text: It's test news
```
