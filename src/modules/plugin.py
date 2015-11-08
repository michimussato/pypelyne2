class PlugIn(object):
    def __init__(self, d):
        super(PlugIn, self).__init__()
        self.__dict__ = d
        self.dict_x32 = None
        self.dict_x64 = None
