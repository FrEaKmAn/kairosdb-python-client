from kairosdbclient.rest.apirequests.base import Request


class DeleteMetricDataPointsRequest(Request):
    uri = 'datapoints/delete'
    resource = None
    success_status_code = 204
    request_method = 'DELETE'

    def __init__(self, data_points):
        super(DeleteMetricDataPointsRequest, self).__init__()

        if not isinstance(data_points, (list, tuple)):
            data_points = [data_points]

        self._data_points = data_points

    def payload(self):
        return [data_point.format() for data_point in self._data_points]