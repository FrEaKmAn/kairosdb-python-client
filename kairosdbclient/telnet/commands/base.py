from abc import abstractmethod


class Command(object):

    @abstractmethod
    def format(self):
        pass