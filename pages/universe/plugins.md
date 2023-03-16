# Plugins

```html markup
<div class="plugins">
  {% for row in frictionless.Resource('data/plugins.csv').read_rows() %}
  <div class="item">
    <div class="item-content">
      <h3>
        <a href="https://github.com/{{ row.user}}/{{row.repo }}" target="_blank" style="color: black"> {{ row.repo }}
        </a>
      </h3>
      <p>{{ row.description or 'Description is not provided'}}</p>
      <p>
        <a class="item-content-link" href="https://github.com/{{ row.user}}/{{row.repo }}" target="_blank">
          Github <span class="fa fa-external-link-alt"></span>
        </a>
      </p>
    </div>
    <div class="item-stars">
      <span class="fa-stack fa-2x">
        <i class="fas fa-stack-2x fa-star fa-inverse item-stars-icon"></i>
        <i class="fas fa-stack-1x item-stars-count">{{ row.stars }}</i>
      </span>
    </div>
  </div>
  {% endfor %}
</div>
```
