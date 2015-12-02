# kairosdb-python-client

Python client for KairosDB. Very alpha stage! [![Build Status](https://travis-ci.org/FrEaKmAn/kairosdb-python-client.svg)](https://travis-ci.org/FrEaKmAn/kairosdb-python-client)

## Installation

TODO


## Getting Started

TODO

## Examples

### Query data points

To query datapoints, we create a query

```python
client = KairosDBRestClient()
client.query(1448019060000, 1448019560000, metrics=[
    Metric('my.test.metric').tag(host=['amazon', 'azure']).group_by(tags=['host']).aggregate(avg=(1, 'hours'))
])
```

or shorter

```python
client[1448019060000:1448019560000:avg(1,'hours'), 'my.test.metric'].tag(host=['amazon', 'azure']).group_by(tags=['host']).query()
```