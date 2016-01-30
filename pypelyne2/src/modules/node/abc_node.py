import abc


class Node(object):
    # difference between:

    # class PlugIn(metaclass=abc.ABCMeta):

    # and

    # class PlugIn(object):
    # __metaclass__ = abc.ABCMeta

    # ???
    """
    Abstract Node object

    """
    __metaclass__ = abc.ABCMeta

    # @abc.abstractmethod
    # def something(self):
    #     pass

    @abc.abstractproperty
    def get_users(self):
        """parses and returns user object list"""
        pass

    @abc.abstractproperty
    def get_tasks(self):
        """parses and returns task object list"""
        pass

    @abc.abstractproperty
    def get_thumbnail_icon(self):
        """returns a thumbnail and its extension in a dict"""
        pass