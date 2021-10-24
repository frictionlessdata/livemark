---
site:
  description: The page is not found
---

# Not Found

> The page is not found

Return to the <a href="/">home</a> page.

```html markup
<script>
for (const item of JSON.parse('{{ document.get_plugin('redirect').items | tojson }}')) {
  if (`/${item.prev}.html` === location.pathname) {
    location.href = `/${item.next}.html`;
  }
}
</script>
```
