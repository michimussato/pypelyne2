class Department(object):

    """Documentation for class Department(object)."""

    def __init__(self, d):

        """__init__.

        Args:
            d (dict): dictionary with the attributes for self"""

        super(Department, self).__init__()
        self.__dict__ = d
