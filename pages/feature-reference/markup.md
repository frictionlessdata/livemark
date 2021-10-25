# Markup

> https://getbootstrap.com/docs/5.0/getting-started/introduction/

With Livemark you can use HTML inside Markdown with Bootstrap support. Here is an example of creating a responsive grid of cards (note that if we set a `livemark-markdown` class we can use markdown inside html):

```html
'''html markup
<div class="w-50">
<div class="container">
<div class="row">
<div class="col-sm">
  <div class="markdown">![Package](../../assets/data-package.png)</div>
  <div class="text-center">
  <p><strong>Data Package</strong></p>
  <p>A simple container format for describing a coherent collection of data in a single package.</p>
  </div>
</div>
<!-- other columns are omitted -->
</div>
</div>
</div>
'''
```

```html markup
<div style="max-width: 600px">
<div class="container">
<div class="row">
<div class="col-sm">
  <div class="livemark-markdown">![Package](../../assets/data-package.png)</div>
  <div class="text-center">
  <p><strong>Data Package</strong></p>
  <p>A simple container format for describing a coherent collection of data in a single package.</p>
  </div>
</div>
<div class="col-sm">
  <div class="livemark-markdown">![Resource](../../assets/data-resource.png)</div>
  <div class="text-center">
  <p><strong>Data Resource</strong></p>
  <p>A simple format to describe and package a single data resource such as a individual table or file.</p>
  </div>
</div>
<div class="col-sm">
  <div class="livemark-markdown">![Schema](../../assets/table-schema.png)</div>
  <div class="text-center">
  <p><strong>Table Schema</strong></p>
  <p>A simple format to declare a schema for tabular data. The schema is designed to be expressible in JSON.</p>
  </div>
</div>
</div>
</div>
</div>
```
