from kairosdbclient.exceptions import ResponseException
from kairosdbclient.rest.resources.base import Resource


class MetricDataPoints(Resource):
    def __init__(self, response):
        self.queries = map(ResultMetric, response.json()['queries'])

    def __iter__(self):
        for query in self.queries:
            yield query

    def __getitem__(self, index):
        return self.queries[index]

    def __len__(self):
        return len(self.queries)


class ResultMetric(object):
    def __init__(self, query):
        self.sample_size = query['sample_size']
        self.results = query['results']

    def as_data_frame(self, time_zone, columns=None):
        # columns are in format 'AIP': {'name': ['AIP']}

        def get_column_key(tags):
            key = None
            if columns:
                for column_key, column_tags in columns.items():
                    if column_tags == tags:
                        if key:
                            raise ValueError("Multiple keys: %s." % key)

                        key = column_key

                if not key:
                    return str(key)

            return key

        try:
            from pandas import DataFrame, Series, concat, to_datetime

            series = []
            for result in self.results:
                identifier = get_column_key(result['tags'])

                if result['values']:
                    times, values = zip(*result['values'])
                    ts = Series(values, index=to_datetime(times, unit='ms'), name=identifier)
                    ts.index = ts.index.tz_localize('UTC').tz_convert(time_zone)

                    series.append(ts)

            if not series:
                return None

            return concat(series, axis=1)
        except ImportError:
            raise ResponseException("You have to first install pandas to be able to generate DataFrame.")

    def __iter__(self):
        for result in self.results:
            yield result

    def __getitem__(self, index):
        return self.results[index]

    def __len__(self):
        return len(self.results)