import unittest
from kairosdbclient.rest.aggregators import *


class RangeAggregatorTest(unittest.TestCase):
    def setUp(self):
        RangeAggregator.name = 'abstract_name'

    def test_from_arguments_as_list(self):
        aggregator = RangeAggregator.from_arguments((2, 'days'))

        self.assertEqual(aggregator.value, 2)
        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.align_sampling, False)
        self.assertEqual(aggregator.align_start_time, False)
        self.assertEqual(aggregator.start_time, 0)
        self.assertEqual(aggregator.time_zone, None)

    def test_should_fail_if_from_arguments_has_invalid_list_length(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid args length: 1, must be a 2 \(value, unit\)."):
            RangeAggregator.from_arguments(['invalid_length'])

    def test_from_arguments_as_dict(self):
        aggregator = RangeAggregator.from_arguments({'value': 2,
                                                     'unit': 'days',
                                                     'align_sampling': True,
                                                     'align_start_time': True,
                                                     'start_time': 100,
                                                     'time_zone': 'Europe/Ljubljana'})

        self.assertEqual(aggregator.value, 2)
        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.align_sampling, True)
        self.assertEqual(aggregator.align_start_time, True)
        self.assertEqual(aggregator.start_time, 100)
        self.assertEqual(aggregator.time_zone, 'Europe/Ljubljana')

    def test_should_fail_if_from_arguments_has_empty_dict(self):
        with self.assertRaises(AggregatorException):
            RangeAggregator.from_arguments({})

    def test_from_arguments_as_str(self):
        aggregator = RangeAggregator.from_arguments('2days')

        self.assertEqual(aggregator.value, 2)
        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.align_sampling, False)
        self.assertEqual(aggregator.align_start_time, False)
        self.assertEqual(aggregator.start_time, 0)
        self.assertEqual(aggregator.time_zone, None)

    def test_should_fail_if_from_arguments_str_has_invalid_unit(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid time unit: invalidunit"):
            RangeAggregator.from_arguments('2invalidunit')

    def test_format(self):
        aggregator = RangeAggregator(value=2, unit='days')

        self.assertEqual(aggregator.format(), {'name': 'abstract_name',
                                               'sampling': {'value': 2, 'unit': 'days'},
                                               'align_sampling': False,
                                               'align_start_time': False})

    def test_format_with_all_parameters(self):
        aggregator = RangeAggregator(value=2,
                                     unit='days',
                                     align_sampling=True,
                                     align_start_time=True,
                                     start_time=10,
                                     time_zone='Europe/Ljubljana')

        self.assertEqual(aggregator.format(), {'name': 'abstract_name',
                                               'sampling': {'value': 2, 'unit': 'days'},
                                               'align_sampling': True,
                                               'align_start_time': True,
                                               'start_time': 10,
                                               'time_zone': 'Europe/Ljubljana'})

    def test_should_fail_if_from_parameters_is_invalid_type(self):
        with self.assertRaisesRegexp(AggregatorException,
                                     "Invalid args type: <type 'int'>, must be a dict, list, tuple or str."):
            RangeAggregator.from_arguments(1)

    def test_should_fail_if_value_not_int(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid time type: <type 'str'>, must be instance of int."):
            RangeAggregator(value='not_int', unit='days')

    def test_should_fail_if_value_less_than_zero(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid time value: -1, must be 0 or greater."):
            RangeAggregator(value=-1, unit='days')

    def test_should_fail_if_invalid_unit(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid time unit: invalid_unit"):
            RangeAggregator(value=2, unit='invalid_unit')

    def test_should_fail_if_start_time_not_int(self):
        with self.assertRaisesRegexp(AggregatorException,
                                     "Invalid start_time type: <type 'str'>, must be instance of int."):
            RangeAggregator(value=2, unit='days', start_time='not_int')

    def test_should_fail_if_start_time_less_than_zero(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid start_time: -1, must be 0 or greater."):
            RangeAggregator(value=2, unit='days', start_time=-1)


class PercentileAggregatorTest(unittest.TestCase):
    def test_from_arguments_as_list(self):
        aggregator = PercentileAggregator.from_arguments((2, 'days', 0.5))

        self.assertEqual(aggregator.value, 2)
        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.percentile, 0.5)

    def test_should_fail_if_from_arguments_has_invalid_list_length(self):
        with self.assertRaisesRegexp(AggregatorException,
                                     "Invalid args length: 1, must be a 3 \(value, unit, percentile\)."):
            PercentileAggregator.from_arguments(['invalid_length'])

    def test_from_arguments_as_dict(self):
        aggregator = PercentileAggregator.from_arguments({'value': 2,
                                                          'unit': 'days',
                                                          'percentile': 0.5})

        self.assertEqual(aggregator.value, 2)
        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.percentile, 0.5)

    def test_format(self):
        aggregator = PercentileAggregator(value=2, unit='days', percentile=0.5)

        self.assertEqual(aggregator.format(), {'name': 'percentile',
                                               'sampling': {'value': 2, 'unit': 'days'},
                                               'percentile': 0.5,
                                               'align_sampling': False,
                                               'align_start_time': False})

    def test_should_fail_if_percentile_not_number(self):
        with self.assertRaisesRegexp(AggregatorException,
                                     "Invalid percentile type: <type 'str'>, must be int or float."):
            PercentileAggregator(2, 'days', 'not_number')

    def test_should_fail_if_percentile_zero(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid percentile: 0, must be 0 < x <= 1."):
            PercentileAggregator(2, 'days', 0)

    def test_should_fail_if_percentile_less_than_zero(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid percentile: -50, must be 0 < x <= 1."):
            PercentileAggregator(2, 'days', -50)

    def test_should_fail_if_percentile_greater_than_one(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid percentile: 50, must be 0 < x <= 1."):
            PercentileAggregator(2, 'days', 50)


class DivideAggregatorTest(unittest.TestCase):
    def test_from_arguments_as_dict(self):
        aggregator = DivAggregator.from_arguments({'divisor': 5})

        self.assertEqual(aggregator.divisor, 5)

    def test_from_arguments_as_number(self):
        aggregator = DivAggregator.from_arguments(5)

        self.assertEqual(aggregator.divisor, 5)

    def test_format(self):
        aggregator = DivAggregator(5)

        self.assertEqual(aggregator.format(), {'name': 'div',
                                               'divisor': 5})

    def test_should_fail_if_from_arguments_has_empty_dict(self):
        with self.assertRaisesRegexp(AggregatorException, "Missing divisor in args: {}."):
            DivAggregator.from_arguments({})

    def test_should_fail_if_divisor_not_number(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid divisor type: <type 'str'>, must be int or float."):
            DivAggregator('not_number')


class RateAggregatorTest(unittest.TestCase):
    def test_from_arguments_as_dict(self):
        aggregator = RateAggregator.from_arguments({'unit': 'days',
                                                    'time_zone': 'Europe/Ljubljana'})

        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.time_zone, 'Europe/Ljubljana')

    def test_from_arguments_as_str(self):
        aggregator = RateAggregator.from_arguments('days')

        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.time_zone, None)

    def test_should_fail_if_from_arguments_has_empty_dict(self):
        with self.assertRaises(AggregatorException):
            RateAggregator.from_arguments({})

    def test_should_fail_if_from_parameters_is_invalid_type(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid args type: <type 'int'>, must be a dict or str."):
            RateAggregator.from_arguments(1)

    def test_should_fail_is_invalid_unit(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid unit: invalid_unit."):
            RateAggregator('invalid_unit')


class SamplerAggregatorTest(unittest.TestCase):
    def test_from_arguments_as_dict(self):
        aggregator = SamplerAggregator.from_arguments({'unit': 'days',
                                                       'time_zone': 'Europe/Ljubljana'})

        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.time_zone, 'Europe/Ljubljana')

    def test_from_arguments_as_str(self):
        aggregator = SamplerAggregator.from_arguments('days')

        self.assertEqual(aggregator.unit, 'days')
        self.assertEqual(aggregator.time_zone, None)

    def test_should_fail_if_from_arguments_has_empty_dict(self):
        with self.assertRaises(AggregatorException):
            SamplerAggregator.from_arguments({})

    def test_should_fail_if_from_parameters_is_invalid_type(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid args type: <type 'int'>, must be a dict or str."):
            SamplerAggregator.from_arguments(1)

    def test_should_fail_is_invalid_unit(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid unit: invalid_unit."):
            SamplerAggregator('invalid_unit')


class ScaleAggregatorTest(unittest.TestCase):
    def test_from_arguments_as_dict(self):
        aggregator = ScaleAggregator.from_arguments({'factor': 5})

        self.assertEqual(aggregator.factor, 5)

    def test_from_arguments_as_number(self):
        aggregator = ScaleAggregator.from_arguments(5)

        self.assertEqual(aggregator.factor, 5)

    def test_format(self):
        aggregator = ScaleAggregator(5)

        self.assertEqual(aggregator.format(), {'name': 'scale',
                                               'factor': 5})

    def test_should_fail_if_from_arguments_has_empty_dict(self):
        with self.assertRaisesRegexp(AggregatorException, "Missing factor in args: {}."):
            ScaleAggregator.from_arguments({})

    def test_should_fail_if_factor_not_number(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid factor type: <type 'str'>, must be int or float."):
            ScaleAggregator('not_number')


class TrimAggregatorTest(unittest.TestCase):
    def test_from_arguments_as_dict(self):
        aggregator = TrimAggregator.from_arguments({'trim': 'both'})

        self.assertEqual(aggregator.trim, 'both')

    def test_from_arguments_as_str(self):
        aggregator = TrimAggregator.from_arguments('both')

        self.assertEqual(aggregator.trim, 'both')

    def test_format(self):
        aggregator = TrimAggregator('both')

        self.assertEqual(aggregator.format(), {'name': 'trim',
                                               'trim': 'both'})

    def test_should_fail_if_from_arguments_has_empty_dict(self):
        with self.assertRaisesRegexp(AggregatorException, "Missing trim in args: {}."):
            TrimAggregator.from_arguments({})

    def test_should_fail_if_trim_not_str(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid trim type: <type 'int'>, must be str."):
            TrimAggregator(1)

    def test_should_fail_if_invalid_trim(self):
        with self.assertRaisesRegexp(AggregatorException, "Invalid trim: invalid, must be first, last or both."):
            TrimAggregator('invalid')