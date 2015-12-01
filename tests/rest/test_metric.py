import unittest
from kairosdbclient.exceptions import MetricException
from kairosdbclient.rest.aggregators import SumAggregator
from kairosdbclient.rest.groupers import TagGroupBy, TimeGroupBy, ValueGroupBy
from kairosdbclient.rest.metric import Metric


class TestMetricName(unittest.TestCase):
    def test_metric_name(self):
        metric = Metric('metric.name')

        self.assertEqual(metric.name, 'metric.name')


class TestMetricTag(unittest.TestCase):
    def setUp(self):
        self.metric = Metric('metric.name')

    def test_metric_tag(self):
        self.metric.tag(host=['azure', 'amazon'], server=['server1'])

        self.assertEqual(self.metric.tags, {'host': ['azure', 'amazon'], 'server': ['server1']})

    def test_metric_tag_as_str(self):
        self.metric.tag(host='azure')

        self.assertEqual(self.metric.tags, {'host': ['azure']})


class TestMetricGroupBy(unittest.TestCase):
    def setUp(self):
        self.metric = Metric('metric.name')

    def test_group_by_tag(self):
        self.metric.group_by(tags=['host'])

        self.assertEqual(self.metric.group_bys, [TagGroupBy(['host'])])

    def test_group_by_time(self):
        self.metric.group_by(time=(1, 'milliseconds', 2))

        self.assertEqual(self.metric.group_bys, [TimeGroupBy(1, 'milliseconds', 2)])

    def test_group_by_value(self):
        self.metric.group_by(value=1)

        self.assertEqual(self.metric.group_bys, [ValueGroupBy(1)])

    def test_group_by_as_args(self):
        groupers = [TagGroupBy(['host']), TimeGroupBy(1, 'milliseconds', 2), ValueGroupBy(1)]
        self.metric.group_by(*groupers)

        self.assertEqual(self.metric.group_bys, groupers)

    def test_should_fail_if_invalid_method(self):
        with self.assertRaises(MetricException):
            self.metric.group_by(invalid=1)

    def test_should_fail_if_invalid_grouper(self):
        with self.assertRaises(MetricException):
            self.metric.group_by('grouper')


class TestMetricLimit(unittest.TestCase):
    def setUp(self):
        self.metric = Metric('metric.name')

    def test_limit(self):
        self.metric.limit_to(100)

        self.assertEqual(self.metric.limit, 100)

    def test_should_fail_if_limit_not_number(self):
        with self.assertRaises(ValueError):
            self.metric.limit_to('not_a_number')


class TestMetricOrder(unittest.TestCase):
    def setUp(self):
        self.metric = Metric('metric.name')

    def test_order_asc(self):
        self.metric.order_asc()

        self.assertEqual(self.metric.order, 'asc')

    def test_order_desc(self):
        self.metric.order_desc()

        self.assertEqual(self.metric.order, 'desc')

    def test_order_direction(self):
        self.metric.order_direction('asc')

        self.assertEqual(self.metric.order, 'asc')

    def test_should_fail_if_invalid_direction(self):
        with self.assertRaises(MetricException):
            self.metric.order_direction('invalid')


class TestMetricAggregate(unittest.TestCase):
    def setUp(self):
        self.metric = Metric('metric.name')

    def test_aggregate(self):
        self.metric.aggregate(sum=(1, 'days'))

        self.assertEqual(self.metric.aggregators, [SumAggregator(1, 'days')])

    def test_aggregate_as_args(self):
        aggregator = SumAggregator(1, 'days')
        self.metric.aggregate(aggregator)

        self.assertEqual(self.metric.aggregators, [aggregator])

    def test_should_fail_if_invalid_method(self):
        with self.assertRaises(MetricException):
            self.metric.aggregate(invalid=(1, 'days'))

    def test_should_fail_if_invalid_aggregator(self):
        with self.assertRaises(MetricException):
            self.metric.aggregate('invalid_aggregator')