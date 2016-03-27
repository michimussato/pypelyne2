import os
import uuid
import logging
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class Entity(object):
    def __init__(self, entity_identifier=None):

        # super(Entity, self).__init__()
        # the unique uuid of the entity (static once created)
        # str: 'uuid'
        try:
            logging.info('validating uuid identifier ({0})'.format(entity_identifier))
            identifier = uuid.UUID(entity_identifier, version=4)
            logging.info('entity has a valid uuid v4')
        except Exception, e:
            identifier = uuid.uuid4()
            logging.warning('not a valid uuid identifier, creating a new one. {0}'.format(e))

        self.identifier = identifier

        # the name of the entity (not necessarily unique, not static)
        # str: string

        if not bool(len(self.entity_name)) or self.entity_name is None:

            self.entity_name = str(self.identifier)

        # # the type of the entity (task node, container node, output)
        # # str: string (container, task, output, version)
        # self.entity_type = self.entity_type or 'undefined'

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

        # all entities can be tagged
        self.entity_tags = set()

    @property
    def thumbnail_path(self):
        # print type(self.identifier)
        # print dir(self.identifier)
        # print self.identifier
        path = os.path.join(SETTINGS.WORKDATA_DIR_DEFAULT, str(self.identifier), 'thumbnails', self.thumbnail)

        if os.path.exists(path):
            return path
        else:
            return None
