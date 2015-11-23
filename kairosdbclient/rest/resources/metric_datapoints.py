from kairosdbclient.rest.resources.base import Resource


class MetricDataPoints(Resource):
    def __init__(self, response):
        self.queries = response.json()['queries']

    def __iter__(self):
        for query in self.queries:
            yield query

    def __getitem__(self, index):
        return self.queries[index]

    def __len__(self):
        return len(self.queries)

    """
    def __len__(self):
        counter = count()
        deque(izip(self.queries, counter), maxlen=0)

        return next(counter)
    """