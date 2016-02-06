import os
import uuid
import logging
import random
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.parser.parse_users as parse_users
import pypelyne2.src.parser.parse_tasks as parse_tasks


class NodeCore(object):
    def __init__(self, node_id=None, name_string=None, task_type=None):
        super(NodeCore, self).__init__()
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
        self.uuid = node_id or str(uuid.uuid4())
        self.name_string = name_string or self.uuid
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

    @property
    def get_thumbnail_icon(self):

        thumbnail_dict = {}

        thumbnail = self.preview_icon_path or SETTINGS.ICON_THUMBNAIL_DEFAULT

        try:
            thumbnail = self.preview_icon_path or os.path.join(SETTINGS.ICONS_DIR, 'rand_img', random.choice(SETTINGS.ICON_THUMBNAIL_PLACEHOLDER))
        except IndexError, e:
            logging.info('no thumbnail for node found: {0}'.format(e))
        finally:
            extension = os.path.splitext(thumbnail)[1]
            if extension not in SETTINGS.ICON_FORMATS:
                logging.warning('bad thumbnail: {0} (using default)'.format(thumbnail))
                thumbnail = SETTINGS.ICON_THUMBNAIL_DEFAULT

        thumbnail_dict[u'thumbnail'] = thumbnail
        thumbnail_dict[u'extension'] = extension

        return thumbnail_dict
