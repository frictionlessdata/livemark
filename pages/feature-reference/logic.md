# Logic

> https://jinja.palletsprojects.com/en/3.0.x/templates/

Livemark process your document using the Jinja templating language. Inside templates, you can use [Frictionless Framework](https://framework.frictionlessdata.io/) as a `frictionless` variable to work with tabular data. It's a high-level preprocessing so you can combine Logic with other syntax, such as Table or Chart:

{% raw %}
```
{% for car in frictionless.extract('data/cars.csv', layout={"limitRows": 5}) %}
- {{ car.brand }} {{ car.model }}: ${{ car.price }}
{% endfor %}
```
{% endraw %}

{% for car in frictionless.extract('data/cars.csv', layout={"limitRows": 5}) %}
- {{ car.brand }} {{ car.model }}: ${{ car.price }}
{% endfor %}
