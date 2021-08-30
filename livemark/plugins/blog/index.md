# Blog

{% for item in document.get_plugin('blog').items %}
<p>
  <h2><a href="/{{ item.document.path }}.html">{{ item.document.name }}</a></h2>
  {{ document.description }}
</p>
{% endfor %}
