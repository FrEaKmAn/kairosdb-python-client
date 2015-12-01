from abc import abstractmethod
from kairosdbclient.exceptions import GroupByException
from kairosdbclient.timeunits import TIME_UNITS


class GroupBy(object):
    @abstractmethod
    def format(self):
        pass

    @classmethod
    @abstractmethod
    def from_arguments(cls, args):
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.format() == other.format()

    def __ne__(self, other):
        return not self.__eq__(other)


class TagGroupBy(GroupBy):
    name = 'tags'

    def __init__(self, tags):
        self.tags = tags

        self._validate_params()

    def _validate_params(self):
        if not isinstance(self.tags, (list, tuple)):
            raise GroupByException("Invalid args type: %s, must be a list or tuple." % type(self.tags))

    @classmethod
    def from_arguments(cls, args):
        return cls(args)

    def format(self):
        return {
            'name': 'tag',
            'tags': self.tags
        }


class TimeGroupBy(GroupBy):
    name = 'time'

    def __init__(self, range_value, range_unit, group_count):
        self.range_value = range_value
        self.range_unit = range_unit
        self.group_count = group_count

        self._validate_params()

    def _validate_params(self):
        if not isinstance(self.range_value, int):
            raise GroupByException("Invalid range_value type: %s, must be int." % type(self.range_value))

        if self.range_value <= 0:
            raise GroupByException("Invalid range_value value: %d, must be greater than 0." % self.range_value)

        if self.range_unit not in TIME_UNITS:
            raise GroupByException(
                "Invalid range_unit value: %s, must be valid time unit: %s." % (self.range_unit, TIME_UNITS))

        if not isinstance(self.group_count, int):
            raise GroupByException("Invalid group_count type: %s, must be int." % type(self.group_count))

        if self.group_count <= 0:
            raise GroupByException("Invalid group_count value: %d, must be greater than 0." % self.group_count)

    @classmethod
    def from_arguments(cls, args):
        if not isinstance(args, (list, tuple)):
            raise GroupByException("Invalid args type: %s, must be a list or tuple." % type(args))

        if not len(args) is 3:
            raise GroupByException(
                "Invalid args length: %d, must be a 3 (range_value, range_unit, group_count)." % len(args))

        range_value, range_unit, group_count = args
        return cls(range_value, range_unit, group_count)

    def format(self):
        return {
            'name': self.name,
            'group_count': self.group_count,
            'range_size': {
                'value': self.range_value,
                'unit': self.range_unit
            }
        }


class ValueGroupBy(GroupBy):
    name = 'value'

    def __init__(self, range_size):
        self.range_size = range_size

        self._validate_params()

    def _validate_params(self):
        if not isinstance(self.range_size, int):
            raise GroupByException("Invalid range_size type: %s, must be int." % type(self.range_size))

        if self.range_size <= 0:
            raise GroupByException("Invalid range_size value: %d, must be greater than 0." % self.range_size)

    def format(self):
        return {
            'name': 'value',
            'range_size': self.range_size
        }

    @classmethod
    def from_arguments(cls, args):
        return cls(args)


groupers = {
    TagGroupBy.name: TagGroupBy,
    TimeGroupBy.name: TimeGroupBy,
    ValueGroupBy.name: ValueGroupBy
}