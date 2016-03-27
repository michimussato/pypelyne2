import pypelyne2.src.core.entities.entity as entity


class EntityProject(entity.Entity):

    """Documentation for class Project(object)."""

    def __init__(self, d, entity_identifier):

        """__init__.

        Args:
            d (dict): dictionary with the attributes for self"""

        self.__dict__ = d

        super(EntityProject, self).__init__(entity_identifier)


    # @property
    # def containers(self):
    #     return
