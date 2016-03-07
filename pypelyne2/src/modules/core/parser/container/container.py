class Container(object):

    """Documentation for class Container(object)."""

    def __init__(self, d):

        """__init__.

        Args:
            d (dict): dictionary with the attributes for self"""

        super(Container, self).__init__()
        self.__dict__ = d
