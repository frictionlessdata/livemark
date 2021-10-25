# Adapters

## Infinity

It's an exerimental feature that adds an ability to create infinity scroll listings using an HTML class `livemark-infinity`:

{% raw %}
```html
'''html markup
<div class="livemark-infinity">
  {% for number in range(1, 1001) %}
  <div>{{ number }}</div>
  {% endfor %}
</div>
'''
```
{% endraw %}

## Pagination

It's an exerimental feature that adds an ability to create paginations using an HTML class `livemark-pagination`:

{% raw %}
```html
'''html markup
<div class="livemark-pagination">
  {% for number in range(1, 1001) %}
  <div>{{ number }}</div>
  {% endfor %}
</div>
'''
```
{% endraw %}
