# Chart

> https://vega.github.io/vega-lite/

Livemark supports Vega Lite visualisations rendering (to try this example, replace the single quotes with back ticks):

```yaml
'''yaml chart
data:
  url: ../../data/cars.csv
mark: circle
selection:
  brush:
    type: interval
# other options are omitted
width: 500
height: 300
'''
```

```yaml chart
data:
  url: ../../data/cars.csv
mark: circle
selection:
  brush:
    type: interval
encoding:
  x:
    type: quantitative
    field: kmpl
    scale:
     domain: [12,25]
  y:
    type: quantitative
    field: price
    scale:
     domain: [100,900]
  color:
    condition:
      selection: brush
      field: type
      type: nominal
    value: grey
  size:
    type: quantitative
    field: bhp
width: 500
height: 300
```
