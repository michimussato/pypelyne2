# import pypelyne2.src.modules.api.abc_plugin as plugin
# http://www.sphinx-doc.org/en/stable/ext/example_numpy.html#example-numpy
import logging
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# class PlugIn(plugin.PlugIn):
class PlugIn(object):

    """Documentation for class PlugIn(object)

    Note
    ----


    Attributes
    ----------

    """

    def __init__(self, d):

        """__init__

        Note
        ----
        We're using d to set __dict__. We also keeping an unmodified copy
        of d in a private variable _parsed_json_original. It can be
        accessed by calling using the property plugin_dict which in turn returns
        a 1 to 1 copy of d.


        Parameters
        ----------
        d : dict
            dictionary with the attributes for self

        """

        super(PlugIn, self).__init__()

        self.__dict__ = d.copy()

        self._parsed_json_original = d.copy()

    @property
    def plugin_dict(self):

        """plugin_dict

        Note
        ----


        Returns
        -------
        dict
            unmodified copy of the original d

        """

        return self._parsed_json_original.copy()

    @property
    def x32(self):

        """x32

        Note
        ----


        Returns
        -------
        object
            Assembles a 32bits object version of self and returns the new object.

        """

        # this try/except statement is only here for testing
        # i.e. test_containerui collects a random plugin
        # if this plugin has no executable_x32, it'll
        # error. to prevent this, it tries to get the
        # x64 equivalent. this is not supposed to happen
        # if pypelyne is human controlled.

        try:

            dict_x32 = self.plugin_dict
            dict_x32[u'executable'] = dict_x32[u'executable_x32']
            dict_x32[u'flags'] = dict_x32[u'flags_x32']
            dict_x32[u'label'] = dict_x32[u'label_x32']
            dict_x32[u'architecture'] = 'x32'

            return PlugIn(dict_x32)

        except KeyError, e:

            logging.warning('are we in testing mode? ({0})'.format(e))

            self.x64

    @property
    def x64(self):

        """x64

        Note
        ----


        Returns
        -------
        object
            Assembles a 64bits object version of self and returns the new object.

        """

        try:

            dict_x64 = self.plugin_dict
            dict_x64[u'executable'] = dict_x64[u'executable_x64']
            dict_x64[u'flags'] = dict_x64[u'flags_x64']
            dict_x64[u'label'] = dict_x64[u'label_x64']
            dict_x64[u'architecture'] = 'x64'

            return PlugIn(dict_x64)

        except KeyError, e:

            logging.warning('are we in testing mode? ({0})'.format(e))

            self.agnostic

    @property
    def agnostic(self):

        """agnostic

        Note
        ----


        Returns
        -------
        object
            Assembles an architecture agnostic object version of self and returns the new object.

        """

        dict_agnostic = self.plugin_dict
        # dict_agnostic[u'executable'] = dict_agnostic[u'executable_x64']
        # dict_agnostic[u'flags'] = dict_agnostic[u'flags_x64']
        # dict_agnostic[u'label'] = dict_agnostic[u'label_x64']
        dict_agnostic[u'architecture'] = None
        return PlugIn(dict_agnostic)

    @property
    def submitter(self):

        """submitter

        Returns
        -------
        object
            Assembles a submitter object version of self and returns the new object."""

        dict_submitter = self.plugin_dict
        dict_submitter[u'executable'] = dict_submitter[u'executable']
        dict_submitter[u'flags'] = dict_submitter[u'flags']
        dict_submitter[u'label'] = dict_submitter[u'label']
        dict_submitter[u'architecture'] = None
        return PlugIn(dict_submitter)
