import pypelyne2.src.core.entities.entity as entity


class EntityOutput(entity.Entity):
    def __init__(self, d, entity_identifier, routput):

        self.__dict__ = d

        super(EntityOutput, self).__init__(entity_identifier)

        self.routput = routput
