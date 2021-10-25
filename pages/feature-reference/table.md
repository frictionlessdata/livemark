# Table

> https://datatables.net/manual/index

Livemark supports CSV table rendering using DataTables, which you can see in the example below (replace the single quotes with back ticks). The `data` property will be read at the build stage so in addition to DataTables options you can pass a [file path](https://raw.githubusercontent.com/frictionlessdata/livemark/main/data/cars.csv) as `data` property (CSV/Excel/JSON are supported). Use `columns` property to customize fields or their order:

```yaml
'''yaml table
data: data/cars.csv
width: 600
order:
  - [3, 'desc']
columns:
  - data: type
  - data: brand
  - data: model
  - data: price
  - data: kmpl
  - data: bhp
'''
```

```yaml table
data: data/cars.csv
width: 600
order:
  - [3, 'desc']
columns:
  - data: type
  - data: brand
  - data: model
  - data: price
  - data: kmpl
  - data: bhp
```
