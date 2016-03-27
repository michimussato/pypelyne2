import pypelyne2.src.core.entities.entity as entity


class EntityTask(entity.Entity):
    def __init__(self, d, entity_identifier, rtask, rplugin):

        self.__dict__ = d

        super(EntityTask, self).__init__(entity_identifier)

        self.rtask = rtask
        self.rplugin = rplugin
