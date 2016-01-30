import abc


class PlugIn(object):
    # difference between:

    # class PlugIn(metaclass=abc.ABCMeta):

    # and

    # class PlugIn(object):
    # __metaclass__ = abc.ABCMeta

    # ???
    """
    Abstract PlugIn object

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def x32(self):
        """returns an x32 version PlugIn object version of the general PlugIn object"""
        pass

    @abc.abstractproperty
    def x64(self):
        """returns an x64 version PlugIn object version of the general PlugIn object"""
        pass

    @abc.abstractproperty
    def agnostic(self):
        """returns an arch agnostic PlugIn object version of the general PlugIn object"""
        pass

    # def __eq__(self, other):
    #     return (self.name == other.name) and (self.asset_type == other.asset_type)
    #
    # def __repr__(self):
    #     return "Asset('{0}', asset_type='{1}')".format(self.name, self.asset_type)
    #
    # @abc.abstractproperty
    # def name(self):
    #     """Name of the asset, e.g. creature01"""
    #     pass
    #
    # @abc.abstractproperty
    # def asset_type(self):
    #     """Asset type e.g. camera, comp, light."""
    #     pass
    #
    # @abc.abstractmethod
    # def create_component(self, name, path):
    #     """Create a Component with the given name and path."""
    #     pass
    #
    # @abc.abstractmethod
    # def components(self, name=None, path=None):
    #     """List of components available for this asset."""
    #     pass
