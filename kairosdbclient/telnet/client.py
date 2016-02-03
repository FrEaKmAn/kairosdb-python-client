import socket
from kairosdbclient.exceptions import RequestException
from kairosdbclient.telnet.commands.put import PutCommand


class KairosDBTelnetClient(object):
    def __init__(self, host='127.0.0.1', port=4242):
        self.host = host
        self.port = port

    def _make_request(self, command):
        messages = command.format()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((self.host, self.port))
            for message in messages:
                s.sendall(message)

            s.close()
        except socket.error, ex:
            raise RequestException(ex)
        finally:
            s.close()

    def save(self, data_points):
        self._make_request(PutCommand(data_points))