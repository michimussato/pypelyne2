class Container(object):
    def __init__(self, d):
        super(Container, self).__init__()
        self.__dict__ = d
