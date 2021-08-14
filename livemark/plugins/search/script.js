document.addEventListener("DOMContentLoaded", function () {
  const prepare = () => {
    const searchParams = new URLSearchParams(window.location.search);
    // TODO: sync search parameter name (q) with cards/modal plugin
    const query = searchParams.get('q') || ''
    if (query.length >= 3) {
      searchInput.value = query
    }
  }
  const search = () => {
    unhighlight()
    query = searchInput.value
    searchOutput.innerHTML = ''
    searchOutput.style.visibility = 'hidden'
    const searchParams = new URLSearchParams(window.location.search);
    if (query.length < 3) return
    const results = searchIndex.search(query)
    if (!results.length) return
    searchParams.set('q', query)
    const newRelativePathQuery = window.location.pathname + '?' + searchParams.toString();
    history.pushState(null, '', newRelativePathQuery);
    const elements = []
    for (const result of results) {
      const item = searchList[result.ref]
      const cls = window.location.pathname === item.link ? 'class="active"' : ''
      elements.push(`<li ${cls}><a href="${item.link}?q=${query}">${item.name}</a></li>`)
    }
    searchOutput.innerHTML = `<ul>\n${elements.join('\n')}\n</ul>`
    searchOutput.style.visibility = 'visible'
    highlight()
  }
  const highlight = () => {
    const stem = lunr.stemmer(new lunr.Token(query)).str
    $('#livemark-main').highlight(stem, {className: 'livemark-search-found'});
    setTimeout(() => {
      $(window).scrollTo($('.livemark-search-found').first(), 1000)
    }, 1000)
  }
  const unhighlight = () => {
    $('#livemark-main').unhighlight({className: 'livemark-search-found'});
  }
  const searchList = {
    {% for item in list %}
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
    for (const item of Object.values(searchList)) {
      this.add(item)
    }
  });
  const searchOutput = document.getElementById('livemark-search-output')
  const searchInput = document.getElementById('livemark-search-input')
  searchInput.addEventListener('input', search)
  prepare()
  search()
});
