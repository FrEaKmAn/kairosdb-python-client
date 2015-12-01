from kairosdbclient.exceptions import MetricException
from .aggregators import aggregators
from kairosdbclient.rest.aggregators import Aggregator
from kairosdbclient.rest.groupers import groupers, GroupBy


class Metric(object):
    def __init__(self, name):
        self.name = name

        self.tags = {}
        self.aggregators = []
        self.group_bys = []
        self.limit = None
        self.ttl_time = 0
        self.exclude_tags = False
        self.order = None

    def tag(self, **kwargs):
        self.tags.clear()

        for name, values in kwargs.items():
            if isinstance(values, str):
                values = [values]

            self.tags[name] = values

        return self

    def aggregate(self, *args, **kwargs):
        self.aggregators = []

        for aggregator in args:
            if not isinstance(aggregator, Aggregator):
                raise MetricException(
                    "Invalid aggregator type: %s, must be one of %s." % (type(aggregator), aggregators))

            self.aggregators.append(aggregator)

        for name, aggregator_args in kwargs.items():
            if name not in aggregators:
                raise MetricException("Invalid aggregation method: %s." % name)

            aggregator = aggregators[name]
            self.aggregators.append(aggregator.from_arguments(aggregator_args))

        return self

    def group_by(self, *args, **kwargs):
        self.group_bys = []

        for grouper in args:
            if not isinstance(grouper, GroupBy):
                raise MetricException(
                    "Invalid group by type: %s, must be one of %s." % (type(grouper), groupers))

            self.group_bys.append(grouper)

        for name, grouper_args in kwargs.items():
            if name not in groupers:
                raise MetricException("Invalid group by: %s." % name)

            grouper = groupers[name]
            self.group_bys.append(grouper.from_arguments(grouper_args))

        return self

    def limit_to(self, limit):
        if not isinstance(limit, int):
            limit = int(limit)

        self.limit = limit

        return self

    def exclude_tag(self, exclude=True):
        self.exclude_tags = exclude

        return self

    def order_direction(self, order):
        if order not in ['asc', 'desc']:
            raise MetricException("Invalid order direction: %s" % order)

        self.order = order

        return self

    def order_asc(self):
        return self.order_direction('asc')

    def order_desc(self):
        return self.order_direction('desc')

    def ttl(self, ttl_time=0):
        self.ttl_time = ttl_time

        return self

    def format(self):
        request = {
            'name': self.name,
        }

        if self.tags:
            request['tags'] = self.tags

        if self.limit:
            request['limit'] = self.limit

        if self.ttl_time:
            request['ttl'] = self.ttl_time

        if self.exclude_tags:
            request['exclude_tags'] = self.exclude_tags

        if self.order:
            request['order'] = self.order

        if self.group_bys:
            request['group_by'] = map(lambda g: g.format(), self.group_bys)

        if self.aggregators:
            request['aggregators'] = map(lambda a: a.format(), self.aggregators)

        return request

    def __repr__(self):
        from pprint import pformat

        return pformat(vars(self), indent=4)


class SingleMetric(object):
    def __init__(self, callback, start, end, metrics):
        self.callback = callback

        self.start = start
        self.end = end

        self.metrics = []

        if isinstance(metrics, str):
            metrics = [metrics]

        for metric in metrics:
            self.metrics.append(Metric(metric))

    def tag(self, **kwargs):
        for metric in self.metrics:
            metric.tag(**kwargs)

        return self

    def aggregate(self, *args, **kwargs):
        for metric in self.metrics:
            metric.aggregate(*args, **kwargs)

        return self

    def group_by(self, *args, **kwargs):
        for metric in self.metrics:
            metric.group_by(*args, **kwargs)

        return self

    def ttl(self, ttl_time=0):
        for metric in self.metrics:
            metric.ttl(ttl_time)

        return self

    def order_asc(self):
        for metric in self.metrics:
            metric.order_asc()

        return self

    def order_desc(self):
        for metric in self.metrics:
            metric.order_desc()

        return self

    def limit_to(self, limit):
        for metric in self.metrics:
            metric.limit_to(limit)

        return self

    def exclude_tag(self, exclude=True):
        for metric in self.metrics:
            metric.exclude_tags(exclude)

        return self

    def query(self):
        return self.callback(self.start, self.end, self.metrics)
