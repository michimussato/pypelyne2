import logging
import os

import pypelyne2.src.modules.core.entities.uuidobject as uuidobject
import pypelyne2.src.parser.parse_users as parse_users

import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.core.parser.resources.task.parse_tasks as parse_tasks


class NodeCore(uuidobject.UuidObject):
    def __init__(self, node_id=None, name_string=None, task_type=None):
        super(NodeCore, self).__init__(object_type='node', object_id=node_id)
        # self.container = False
        self.dirty = False
        self._users = []
        self._tasks = []

        # TODO:
        self.task_type = task_type

        # self._thumbnail_icon = None
        # nodes living inside self as children
        # self.child_items = []
        # self.siblings = []
        # the parent container of self
        self.parent_container = None
        # the output ports
        self.outputs = []
        # the input ports
        self.inputs = []
        self.task = None
        self.tool = None
        # if self.uuid is None:

        # self.uuid = node_id or str(uuid.uuid4())
        self.name_string = name_string or self.object_id
        # self.icon = None
        # self.dependenies_req = None
        # self.dependenies_opt = None
        # self.creator = None
        # self.modificators = None

    # def is_container(self):
    #     return bool(self.child_items)

    @property
    def get_users(self):
        logging.info('getting users...')
        if not bool(self._users):
            logging.info('no users cache found')
            self._users = parse_users.get_users()
        return self._users

    @property
    def get_tasks(self):
        logging.info('getting tasks...')
        if not bool(self._tasks):
            logging.info('no tasks cache found')
            self._tasks = parse_tasks.get_tasks()
        return self._tasks

    def get_thumbnail_icon(self, icon_path=None):

        thumbnail_dict = {}

        if icon_path is None or os.path.splitext(icon_path)[1] not in SETTINGS.ICON_FORMATS:
            logging.info('using default thumbnail')
            # thumbnail = self.plugin.icon
            thumbnail_dict[u'thumbnail'] = self.plugin.icon
            thumbnail_dict[u'extension'] = None
            self.preview_icon_path = None
        else:
            try:
                # thumbnail = icon_path
                self.preview_icon_path = icon_path
                extension = os.path.splitext(self.preview_icon_path)[1]
                thumbnail_dict[u'thumbnail'] = self.preview_icon_path
                thumbnail_dict[u'extension'] = extension
            except IndexError, e:
                logging.info('no thumbnail for node found: {0}'.format(e))
                # thumbnail = self.plugin.icon
                # extension = None
                thumbnail_dict[u'thumbnail'] = self.plugin.icon
                thumbnail_dict[u'extension'] = None
                self.preview_icon_path = None
            # finally:
            #
            #     # if extension not in SETTINGS.ICON_FORMATS:
            #     #     logging.warning('bad thumbnail: {0} (using default)'.format(self.preview_icon_path))
            #     #     # thumbnail = SETTINGS.ICON_THUMBNAIL_DEFAULT



        return thumbnail_dict
