import pypelyne2.src.modules.api.plugin as plugin


class PlugIn(plugin.PlugIn):
    def __init__(self, d):
        super(PlugIn, self).__init__()
        self.__dict__ = d.copy()

    @property
    def x32(self):
        dict_x32 = self.__dict__
        dict_x32[u'executable'] = dict_x32[u'executable_x32']
        dict_x32[u'flags'] = dict_x32[u'flags_x32']
        dict_x32[u'label'] = dict_x32[u'label_x32']
        dict_x32[u'architecture'] = 'x32'
        return PlugIn(dict_x32)

    @property
    def x64(self):
        dict_x64 = self.__dict__
        dict_x64[u'executable'] = dict_x64[u'executable_x64']
        dict_x64[u'flags'] = dict_x64[u'flags_x64']
        dict_x64[u'label'] = dict_x64[u'label_x64']
        dict_x64[u'architecture'] = 'x64'
        return PlugIn(dict_x64)

    @property
    def agnostic(self):
        dict_agnostic = self.__dict__
        # dict_agnostic[u'executable'] = dict_agnostic[u'executable_x64']
        # dict_agnostic[u'flags'] = dict_agnostic[u'flags_x64']
        # dict_agnostic[u'label'] = dict_agnostic[u'label_x64']
        dict_agnostic[u'architecture'] = None
        return PlugIn(dict_agnostic)

    @property
    def submitter(self):
        dict_submitter = self.__dict__
        dict_submitter[u'executable'] = dict_submitter[u'executable']
        dict_submitter[u'flags'] = dict_submitter[u'flags']
        dict_submitter[u'label'] = dict_submitter[u'label']
        dict_submitter[u'architecture'] = None
        return PlugIn(dict_submitter)
