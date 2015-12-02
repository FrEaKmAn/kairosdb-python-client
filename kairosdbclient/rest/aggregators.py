from abc import abstractmethod
from kairosdbclient.exceptions import AggregatorException
from kairosdbclient.timeunits import TIME_UNITS, parse_time


class Aggregator(object):
    def __init__(self,):
        if not hasattr(self, 'name'):
            raise AggregatorException("Aggregator has to have a name attribute.")

    @abstractmethod
    def _validate_params(self):
        pass

    @classmethod
    @abstractmethod
    def from_arguments(cls, self):
        pass

    def format(self):
        return {
            'name': getattr(self, 'name')
        }

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.format() == other.format()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4)


class RangeAggregator(Aggregator):
    def __init__(self, value, unit, align_sampling=False, align_start_time=False, start_time=0, time_zone=None):
        super(RangeAggregator, self).__init__()

        self.value = value
        self.unit = unit
        self.align_sampling = align_sampling
        self.align_start_time = align_start_time
        self.start_time = start_time
        self.time_zone = time_zone

        self._validate_params()

    def _validate_params(self):
        if not isinstance(self.value, int):
            raise AggregatorException("Invalid time type: %s, must be instance of int." % type(self.value))

        if self.value < 0:
            raise AggregatorException("Invalid time value: %d, must be 0 or greater." % self.value)

        if self.unit.lower() not in TIME_UNITS:
            raise AggregatorException("Invalid time unit: %s." % self.unit)

        if not isinstance(self.start_time, int):
            raise AggregatorException("Invalid start_time type: %s, must be instance of int." % type(self.start_time))

        if self.start_time < 0:
            raise AggregatorException("Invalid start_time: %d, must be 0 or greater." % self.start_time)

    @classmethod
    def _parse_dict_arguments(cls, args):
        if 'value' not in args:
                raise AggregatorException("Missing value in args: %s" % args)

        if 'unit' not in args:
            raise AggregatorException("Missing unit in args: %s" % args)

        return {
            'value': args['value'],
            'unit': args['unit'],
            'align_sampling': args.pop('align_sampling', False),
            'align_start_time': args.pop('align_start_time', False),
            'start_time': args.pop('start_time', 0),
            'time_zone': args.pop('time_zone', None)
        }

    @classmethod
    def from_arguments(cls, args):
        if isinstance(args, dict):
            return cls(**cls._parse_dict_arguments(args))
        elif isinstance(args, (list, tuple)):
            if not len(args) is 2:
                raise AggregatorException("Invalid args length: %d, must be a 2 (value, unit)." % len(args))

            value, unit = args
            return cls(value, unit)
        elif isinstance(args, str):
            try:
                value, unit = parse_time(args)
                return cls(value, unit)
            except ValueError as e:
                raise AggregatorException(e)
        else:
            raise AggregatorException("Invalid args type: %s, must be a dict, list, tuple or str." % type(args))

    def format(self):
        request = {
            'name': getattr(self, 'name'),
            'sampling': {
                'value': self.value,
                'unit': self.unit
            },
            'align_start_time': self.align_start_time,
            'align_sampling': self.align_sampling
        }

        if self.start_time:
            request['start_time'] = self.start_time

        if self.time_zone:
            request['time_zone'] = self.time_zone

        return request


class PercentileAggregator(RangeAggregator):
    name = 'percentile'

    def __init__(self, value, unit, percentile, align_sampling=False, align_start_time=False, start_time=0, time_zone=None):
        self.percentile = percentile  # TODO, calling super __init__ should be first

        super(PercentileAggregator, self).__init__(value, unit, align_sampling, align_start_time, start_time, time_zone)

        self._validate_params()

    @classmethod
    def _parse_dict_arguments(cls, args):
        super_args = super(PercentileAggregator, cls)._parse_dict_arguments(args)

        if 'percentile' not in args:
            raise AggregatorException("Missing percentile in args: %s." % args)

        super_args['percentile'] = args['percentile']
        return super_args

    @classmethod
    def from_arguments(cls, args):
        if isinstance(args, dict):
            return cls(**cls._parse_dict_arguments(args))
        elif isinstance(args, (list, tuple)):
            if len(args) is not 3:
                raise AggregatorException("Invalid args length: %d, must be a 3 (value, unit, percentile)." % len(args))

            value, unit, percentile = args
            return cls(value, unit, percentile)
        else:
            raise AggregatorException("Invalid args type: %s, must be a dict, list or tuple." % type(args))

    def _validate_params(self):
        super(PercentileAggregator, self)._validate_params()

        if not isinstance(self.percentile, (int, float)):
            raise AggregatorException("Invalid percentile type: %s, must be int or float." % type(self.percentile))

        if not 0 < self.percentile <= 1:
            raise AggregatorException("Invalid percentile: %d, must be 0 < x <= 1." % self.percentile)

    def format(self):
        request = super(PercentileAggregator, self).format()
        request['percentile'] = self.percentile

        return request


class DivAggregator(Aggregator):
    name = 'div'

    def __init__(self, divisor):
        super(DivAggregator, self).__init__()

        self.divisor = divisor

        self._validate_params()

    @classmethod
    def _parse_dict_arguments(cls, args):
        if 'divisor' not in args:
                raise AggregatorException("Missing divisor in args: %s." % args)

        return {
            'divisor': args['divisor']
        }

    @classmethod
    def from_arguments(cls, args):
        if isinstance(args, dict):
            return cls(**cls._parse_dict_arguments(args))
        if isinstance(args, (int, float)):
            return cls(args)
        else:
            raise AggregatorException("Invalid args type: %s, must be a dict, int or float." % type(args))

    def _validate_params(self):
        if not isinstance(self.divisor, (int, float)):
            raise AggregatorException("Invalid divisor type: %s, must be int or float." % type(self.divisor))

    def format(self):
        request = super(DivAggregator, self).format()
        request['divisor'] = self.divisor

        return request


class DiffAggregator(Aggregator):
    name = 'diff'

    @classmethod
    def from_arguments(cls, args):
        return cls()

    def _validate_params(self):
        pass


# TODO confused with combining unit and sampling
class RateAggregator(Aggregator):
    name = 'rate'

    def __init__(self, unit, time_zone=None):
        self.unit = unit
        self.time_zone = time_zone

        super(RateAggregator, self).__init__()

        self._validate_params()

    @classmethod
    def _parse_dict_arguments(cls, args):
        if 'unit' not in args:
                raise AggregatorException("Missing unit in args: %s." % args)

        return {
            'unit': args['unit'],
            'time_zone': args.pop('time_zone', None)
        }

    @classmethod
    def from_arguments(cls, args):
        if isinstance(args, dict):
            return cls(**cls._parse_dict_arguments(args))
        elif isinstance(args, str):
            return cls(args)
        else:
            raise AggregatorException("Invalid args type: %s, must be a dict or str." % type(args))

    def _validate_params(self):
        if self.unit not in TIME_UNITS:
            raise AggregatorException("Invalid unit: %s." % self.unit)

    def format(self):
        request = super(RateAggregator, self).format()
        request['unit'] = self.unit

        if self.time_zone:
            request['time_zone'] = self.time_zone

        return request


class SamplerAggregator(Aggregator):
    name = 'sampler'

    def __init__(self, unit, time_zone=None):
        self.unit = unit
        self.time_zone = time_zone

        super(SamplerAggregator, self).__init__()

        self._validate_params()

    @classmethod
    def _parse_dict_arguments(cls, args):
        if 'unit' not in args:
                raise AggregatorException("Missing unit in args: %s." % args)

        return {
            'unit': args['unit'],
            'time_zone': args.pop('time_zone', None)
        }

    @classmethod
    def from_arguments(cls, args):
        if isinstance(args, dict):
            return cls(**cls._parse_dict_arguments(args))
        elif isinstance(args, str):
            return cls(args)
        else:
            raise AggregatorException("Invalid args type: %s, must be a dict or str." % type(args))

    def _validate_params(self):
        if self.unit not in TIME_UNITS:
            raise AggregatorException("Invalid unit: %s." % self.unit)

    def format(self):
        request = super(SamplerAggregator, self).format()
        request['unit'] = self.unit

        if self.time_zone:
            request['time_zone'] = self.time_zone

        return request


class ScaleAggregator(Aggregator):
    name = 'scale'

    def __init__(self, factor):
        self.factor = factor

        super(ScaleAggregator, self).__init__()

        self._validate_params()

    @classmethod
    def _parse_dict_arguments(cls, args):
        if 'factor' not in args:
                raise AggregatorException("Missing factor in args: %s." % args)

        return {
            'factor': args['factor']
        }

    @classmethod
    def from_arguments(cls, args):
        if isinstance(args, dict):
            return cls(**cls._parse_dict_arguments(args))
        if isinstance(args, (int, float)):
            return cls(args)
        else:
            raise AggregatorException("Invalid args type: %s, must be a dict, int or float." % type(args))

    def _validate_params(self):
        if not isinstance(self.factor, (int, float)):
            raise AggregatorException("Invalid factor type: %s, must be int or float." % type(self.factor))

    def format(self):
        request = super(ScaleAggregator, self).format()
        request['factor'] = self.factor

        return request


class TrimAggregator(Aggregator):
    name = 'trim'

    def __init__(self, trim):
        self.trim = trim

        super(TrimAggregator, self).__init__()

        self._validate_params()

    @classmethod
    def _parse_dict_arguments(cls, args):
        if 'trim' not in args:
                raise AggregatorException("Missing trim in args: %s." % args)

        return {
            'trim': args['trim']
        }

    @classmethod
    def from_arguments(cls, args):
        if isinstance(args, dict):
            return cls(**cls._parse_dict_arguments(args))
        if isinstance(args, str):
            return cls(args)
        else:
            raise AggregatorException("Invalid args type: %s, must be a dict or str." % type(args))

    def _validate_params(self):
        if not isinstance(self.trim, str):
            raise AggregatorException("Invalid trim type: %s, must be str." % type(self.trim))

        if self.trim.lower() not in ['first', 'last', 'both']:
            raise AggregatorException("Invalid trim: %s, must be first, last or both." % self.trim)

    def format(self):
        request = super(TrimAggregator, self).format()
        request['trim'] = self.trim

        return request


class AvgAggregator(RangeAggregator):
    name = 'avg'


class SumAggregator(RangeAggregator):
    name = 'sum'


class StdAggregator(RangeAggregator):
    name = 'dev'


class CountAggregator(RangeAggregator):
    name = 'count'


class FirstAggregator(RangeAggregator):
    name = 'first'


class GapsAggregator(RangeAggregator):
    name = 'gaps'


class LastAggregator(RangeAggregator):
    name = 'last'


class LeastSquaresAggregator(RangeAggregator):
    name = 'least_squares'


class MaxAggregator(RangeAggregator):
    name = 'max'


class MinAggregator(RangeAggregator):
    name = 'min'


def avg(value, unit):
    return AvgAggregator(value, unit)


aggregators = {
    AvgAggregator.name: AvgAggregator,
    StdAggregator.name: StdAggregator,
    CountAggregator.name: CountAggregator,
    FirstAggregator.name: FirstAggregator,
    GapsAggregator.name: GapsAggregator,
    LastAggregator.name: LastAggregator,
    LeastSquaresAggregator.name: LeastSquaresAggregator,
    MaxAggregator.name: MaxAggregator,
    MinAggregator.name: MinAggregator,
    PercentileAggregator.name: PercentileAggregator,
    SumAggregator.name: SumAggregator,
    DiffAggregator.name: DiffAggregator,
    DivAggregator.name: DivAggregator,
    RateAggregator.name: RateAggregator,
    SamplerAggregator.name: SamplerAggregator,
    ScaleAggregator.name: ScaleAggregator,
    TrimAggregator.name: TrimAggregator
}