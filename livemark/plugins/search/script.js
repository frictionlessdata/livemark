document.addEventListener("DOMContentLoaded", function () {
  const searchItems = {
    {% for item in items %}
      '{{ item.link }}': {
          'name': '{{ item.name }}',
          'link': '{{ item.link }}',
          'text': {{ item.text | striptags | tojson }},
      },
    {% endfor %}
  };
  const searchIndex = lunr(function () {
    this.ref("link")
    this.field("name", { boost: 10 })
    this.field("text")
    for (const item of Object.values(searchItems)) {
      this.add(item)
    }
  });
  const searchOutput = document.getElementById('livemark-search-output')
  const searchInput = document.getElementById('livemark-search-input')
  searchInput.addEventListener('input', (event) => {
    const query = event.target.value
    searchOutput.innerHTML = ''
    searchOutput.style.display = 'none'
    if (query.length < 3) return
    const results = searchIndex.search(query)
    if (!results.length) return
    const elements = []
    for (const result of results) {
      const item = searchItems[result.ref]
      elements.push(`<li><a href="${item.link}?q=${query}">${item.name}</a></li>`)
    }
    searchOutput.innerHTML = `<ul>\n${elements.join('\n')}\n</ul>`
    searchOutput.style.display = 'block'
  })
});
