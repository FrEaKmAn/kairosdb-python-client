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
client.query(1448019560000, 1448019565000, metrics=[
    Metric('my.test.metric').tag(host=['amazon', 'azure']).group_by(tags=['host']).aggregate(sum=(1, 'hours'))
])
```

or shorter

```python
client[1448019560000:1448019565000, 'my.test.metric'].tag(host=['amazon', 'azure']).group_by(tags=['host']).aggregate(sum=(1, 'hours')).query()
```