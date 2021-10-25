# Script

> https://www.python.org/

Livemark supports Python/Bash script execution inside Markdown. We think of this as a lightweight version of Jupiter Notebooks. Sometimes, a declarative Logic/Table/Chart is not enough for presenting data so you might also want to include scripts:

```python script
from pprint import pprint
from frictionless import Resource, transform, steps

brands = transform(
    Resource("data/cars.csv"),
    steps=[
        steps.table_normalize(),
        steps.table_aggregate(group_name="brand", aggregation={"price": ("price", max)}),
        steps.row_sort(field_names=["price"], reverse=True),
        steps.row_slice(head=5),
    ],
)
pprint(brands.read_rows())
```
