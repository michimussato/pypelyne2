class Department(object):
    def __init__(self, d):
        super(Department, self).__init__()
        self.__dict__ = d
