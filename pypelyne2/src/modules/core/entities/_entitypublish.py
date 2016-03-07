import pypelyne2.src.modules.core.entities.entity as entity


class EntityPublish(entity.Entity):
    def __init__(self):
        super(EntityPublish, self).__init__()

        # overrides of base class
        self.entity_type = 'publish'

