import uuid
import logging
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class Entity(object):
    def __init__(self, entity_uuid=None):

        # super(Entity, self).__init__()
        # the unique uuid of the entity (static once created)
        # str: 'uuid'
        try:
            uuid_obj = uuid.UUID(entity_uuid, version=4)
        except Exception, e:
            uuid_obj = uuid.uuid4()
            # print 'not valid uuid, creating random. {0}'.format(e)
            logging.info('not a valid uuid, creating a new one. {0}'.format(e))

        self.entity_uuid = uuid_obj

        # the name of the entity (not necessarily unique, not static)
        # str: string
        self.entity_string = str()

        # the type of the entity (task node, container node, output)
        # str: string (container, task, output, version)
        self.entity_type = None

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
