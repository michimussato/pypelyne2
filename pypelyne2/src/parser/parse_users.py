import os
import json
import logging

import operator

import pypelyne2.src.modules.user.user as class_user
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_users():
    user_list = []

    for user_file in SETTINGS.USERS_FILES:

        logging.info('processing user source file: {0}'.format(user_file))
        with open(os.path.join(SETTINGS.USERS_DIR, user_file), 'r') as f:
            user_object = json.load(f)

        user_list.append(user_object)

    return sorted(user_list,
                  key=operator.itemgetter(SETTINGS.SORT_USERS),
                  reverse=SETTINGS.SORT_USERS_REVERSE)


def get_users():
    user_objects = []
    users = parse_users()
    for user in users:
        new_user_object = class_user.User(user)
        user_objects.append(new_user_object)

    return user_objects
