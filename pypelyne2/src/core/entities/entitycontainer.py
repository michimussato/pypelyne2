import pypelyne2.src.core.entities.entity as entity


class EntityContainer(entity.Entity):
    def __init__(self, d, entity_identifier, rcontainer):

        self.__dict__ = d

        super(EntityContainer, self).__init__(entity_identifier)

        self.rcontainer = rcontainer
