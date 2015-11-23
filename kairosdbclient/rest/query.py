class Metric(object):
    def __init__(self, name):
        self.name = name

        self.tags = {}
        self.aggregators = []
        self.group_bys = []
        self.limit = None

    def tag(self, **kwargs):
        self.tags = kwargs
        return self

    def aggregate(self, **kwargs):
        self.aggregators = []

        for method, params in kwargs.items():
            align_start_time = params.pop('align_start_time', False)
            align_sampling = params.pop('align_sampling', False)

            if type(params) is dict:
                time = params['value']
                unit = params['unit']
            else:
                time, unit = params

            self.aggregators.append({
                'name': method,
                'sampling': {
                    'value': time,
                    'unit': unit
                },
                'align_start_time': align_start_time,
                'align_sampling': align_sampling
            })

        return self

    def group_by(self, tags=None):
        self.group_bys = []

        if tags:
            self.group_bys.append({'name': 'tag', 'tags': tags})

        return self

    def limit(self, limit):
        self.limit = limit
        return self

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

    def aggregate(self, **kwargs):
        for metric in self.metrics:
            metric.aggregate(**kwargs)

        return self

    def group_by(self, tags=None):
        for metric in self.metrics:
            metric.group_by(tags=tags)

        return self

    def query(self):
        return self.callback(self.start, self.end, self.metrics)
