// TODO: wrap in a function on domloaded
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
  this.ref("link");
  this.field("name", { boost: 10 });
  this.field("text");
  for (const item of Object.values(searchItems)) {
    this.add(item);
  }
});
