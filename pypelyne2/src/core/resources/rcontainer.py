class RContainer(object):

    """Documentation for class Container(object)."""

    def __init__(self, d):

        """__init__.

        Args:
            d (dict): dictionary with the attributes for self"""

        super(RContainer, self).__init__()
        self.__dict__ = d
