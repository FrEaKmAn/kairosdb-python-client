from kairosdbclient.telnet.commands.base import Command


class PutCommand(Command):
    def __init__(self, data_points):
        self._data_points = data_points

    def format(self):
        messages = []
        for data_point in self._data_points:
            metric_name = data_point['metric']

            messages.append("put %s\n" % (metric_name, ))