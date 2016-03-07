import uuid


class Entity(object):
    def __init__(self, entity_uuid=None):

        # super(Entity, self).__init__()
        # the unique uuid of the entity (static once created)
        # str: 'uuid'
        self.entity_uuid = entity_uuid or str(uuid.uuid4())

        # print self.entity_uuid

        # the name of the entity (not necessarily unique, not static)
        # str: string
        self.entity_string = str()

        # the type of the entity (task node, container node, output)
        # str: string (container, task, output, version)
        self.entity_type = str()

        # where does the entity live on disk
        # str: string (path)
        self.entity_location = str()

        # who created this entity
        # dict: {user: uuid, date: date, comment: 'some explanation'}
        self.entity_creator = dict()

        # the history of modifications to the entity
        # list: [{index or uuid: index or uuid, date: date, user: uuid, comment: 'some explanation'},
        #        {index or uuid: index or uuid, date: date, user: uuid, comment: 'some explanation'}]
        self.entity_modifications = []

    # @property
    # def modifications(self):
    #     return self.entity_modifications
    #
    # @property
    # def creator(self):
    #     return self.entity_creator
