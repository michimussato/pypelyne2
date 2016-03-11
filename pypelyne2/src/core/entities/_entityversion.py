import pypelyne2.src.core.entities.entity as entity


class EntityVersion(entity.Entity):
    def __init__(self):
        super(EntityVersion, self).__init__()

        # overrides of base class
        self.entity_type = 'version'

        self.entity_version_parent_output = str()

        # publishing dates
        # list:
        self.entity_version_published = bool(False)

        # the version status
        # str: 'in progress', 'for review', 'client', 'approved', 'revise'
        self.entity_version_status = str()

        # comment
        # list: [{date: comment}]
        self.entity_version_comments = list()
