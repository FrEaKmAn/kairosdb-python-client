import unittest
from kairosdbclient.exceptions import GroupByException
from kairosdbclient.rest.groupers import TagGroupBy, TimeGroupBy, ValueGroupBy


class TagGroupByTest(unittest.TestCase):
    def test_from_arguments(self):
        group_by = TagGroupBy.from_arguments(['host', 'cpu'])

        self.assertEqual(group_by.tags, ['host', 'cpu'])

    def test_should_fail_if_arguments_are_not_list(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid args type: <type 'str'>, must be a list or tuple."):
            TagGroupBy.from_arguments('not_a_list')

    def test_format(self):
        group_by = TagGroupBy(['host', 'cpu'])

        self.assertEqual(group_by.format(), {'name': 'tag',
                                             'tags': ['host', 'cpu']})


class TimeGroupByTest(unittest.TestCase):
    def test_from_arguments(self):
        group_by = TimeGroupBy.from_arguments((2, 'days', 500))

        self.assertEqual(group_by.range_value, 2)
        self.assertEqual(group_by.range_unit, 'days')
        self.assertEqual(group_by.group_count, 500)

    def test_should_fail_if_arguments_are_not_list(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid args type: <type 'str'>, must be a list or tuple."):
            TimeGroupBy.from_arguments('not_a_list')

    def test_should_fail_if_invalid_length_of_arguments(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid args length: 2, must be a 3 .*"):
            TimeGroupBy.from_arguments(('invalid', 'length'))

    def test_should_fail_if_range_value_is_equal_zero(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid range_value value: 0, must be greater than 0."):
            TimeGroupBy(0, 'days', 500)

    def test_should_fail_if_range_value_is_below_zero(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid range_value value: -1, must be greater than 0."):
            TimeGroupBy(-1, 'days', 500)

    def test_should_fail_if_range_value_not_int(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid range_value type: <type 'str'>, must be int."):
            TimeGroupBy('not_int', 'days', 500)

    def test_should_fail_if_invalid_range_unit(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid range_unit value: invalid_unit, must be .*"):
            TimeGroupBy(1, 'invalid_unit', 500)

    def test_should_fail_if_group_count_not_int(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid group_count type: <type 'str'>, must be int."):
            TimeGroupBy(1, 'days', 'not_int')

    def test_should_fail_if_group_count_is_equal_zero(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid group_count value: 0, must be greater than 0."):
            TimeGroupBy(1, 'days', 0)

    def test_should_fail_if_group_count_is_below_zero(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid group_count value: -1, must be greater than 0."):
            TimeGroupBy(1, 'days', -1)

    def test_format(self):
        group_by = TimeGroupBy(1, 'days', 500)

        self.assertEqual(group_by.format(), {'name': 'time',
                                             'group_count': 500,
                                             'range_size': {
                                                 'value': 1,
                                                 'unit': 'days'
                                             }})


class ValueGroupByTest(unittest.TestCase):
    def test_from_arguments(self):
        group_by = ValueGroupBy.from_arguments(500)

        self.assertEqual(group_by.range_size, 500)

    def test_should_fail_if_range_size_not_int(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid range_size type: <type 'str'>, must be int."):
            ValueGroupBy.from_arguments('not_int')

    def test_should_fail_if_range_size_equal_zero(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid range_size value: 0, must be greater than 0."):
            ValueGroupBy.from_arguments(0)

    def test_should_fail_if_range_size_below_zero(self):
        with self.assertRaisesRegexp(GroupByException, "Invalid range_size value: -1, must be greater than 0."):
            ValueGroupBy.from_arguments(-1)

    def test_format(self):
        group_by = ValueGroupBy(500)

        self.assertEqual(group_by.format(), {'name': 'value',
                                             'range_size': 500})