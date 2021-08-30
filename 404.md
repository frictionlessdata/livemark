# Not Found

> The page is not found

Return to the <a href="/">home</a> page.

```html markup
<script>
const items = JSON.parse('{{ document.get_plugin('redirect').items | tojson }}');
for (const item of items) {
  if (`/${item.prev}.html` === location.pathname) {
    location.href = `/${item.next}.html`;
  }
}
</script>
```
