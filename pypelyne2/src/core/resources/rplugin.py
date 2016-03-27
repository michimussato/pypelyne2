# http://www.sphinx-doc.org/en/stable/ext/example_numpy.html#example-numpy
import logging


class RPlugin(object):

    """Documentation for class Plugin(object)

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

        super(RPlugin, self).__init__()

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

        if self.plugin_dict[u'type'] == 'standalone' and not self.plugin_dict[u'architecture_agnostic']:
            dict_x32 = self.plugin_dict
            dict_x32[u'executable'] = dict_x32[u'executable_x32']
            dict_x32[u'flags'] = dict_x32[u'flags_x32']
            dict_x32[u'label'] = dict_x32[u'label_x32']
            dict_x32[u'architecture'] = 'x32'

            return RPlugin(dict_x32)

        else:

            logging.warning('plugin {0} has no x32 represention ({1}/{2})'.format(self,
                                                                                  self.plugin_dict[u'label'],
                                                                                  self.plugin_dict[u'type']))

            return None

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
        if self.plugin_dict[u'type'] == 'standalone' and not self.plugin_dict[u'architecture_agnostic']:
            dict_x64 = self.plugin_dict
            dict_x64[u'executable'] = dict_x64[u'executable_x64']
            dict_x64[u'flags'] = dict_x64[u'flags_x64']
            dict_x64[u'label'] = dict_x64[u'label_x64']
            dict_x64[u'architecture'] = 'x64'

            return RPlugin(dict_x64)

        else:

            logging.warning('plugin {0} has no x64 represention ({1}/{2})'.format(self,
                                                                                  self.plugin_dict[u'label'],
                                                                                  self.plugin_dict[u'type']))

            return None

    @property
    def rand_arch(self):

        if self.plugin_dict[u'type'] == 'standalone':

            if 'executable_x32' in self.plugin_dict or 'executable_x64' in self.plugin_dict:

                dict_rand_arch = self.plugin_dict
                if dict_rand_arch[u'executable_x32'] is not None:
                    self.x32

                elif dict_rand_arch[u'executable_x64'] is not None:
                    self.x64

                # return Plugin(dict_rand_arch)

            # else:
            #
            #     logging.error('plugin {0} has neither executable_x32 nor executable_x64 key'.format(self))

        else:

            logging.warning('plugin {0} has no rand_arch represention ({1}/{2})'.format(self,
                                                                                        self.plugin_dict[u'label'],
                                                                                        self.plugin_dict[u'type']))

            return None

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

        # print 'blabla'

        if 'architecture_agnostic' in self.plugin_dict and self.plugin_dict[u'architecture_agnostic']:

            # if self.plugin_dict[u'architecture_agnostic']:

            dict_agnostic = self.plugin_dict
            # dict_agnostic[u'executable'] = dict_agnostic[u'executable_x64']
            # dict_agnostic[u'flags'] = dict_agnostic[u'flags_x64']
            # dict_agnostic[u'label'] = dict_agnostic[u'label_x64']
            dict_agnostic[u'architecture'] = None

            # print 'blabla'

            return RPlugin(dict_agnostic)

        else:

            # print self.plugin_dict

            logging.warning('plugin {0} has no agnostic represention ({1}/{2})'.format(self,
                                                                                       self.plugin_dict[u'label'],
                                                                                       self.plugin_dict[u'type']))

            return None

    @property
    def submitter(self):

        """submitter

        Returns
        -------
        object
            Assembles a submitter object version of self and returns the new object."""

        if self.plugin_dict[u'type'] == 'submitter':

            dict_submitter = self.plugin_dict
            # print dict_submitter
            dict_submitter[u'executable'] = dict_submitter[u'executable']
            dict_submitter[u'flags'] = dict_submitter[u'flags']
            dict_submitter[u'label'] = dict_submitter[u'label']
            dict_submitter[u'architecture'] = None

            return RPlugin(dict_submitter)

        else:

            logging.warning('plugin {0} has no submitter represention ({1}/{2})'.format(self,
                                                                                        self.plugin_dict[u'label'],
                                                                                        self.plugin_dict[u'type']))

            return None
