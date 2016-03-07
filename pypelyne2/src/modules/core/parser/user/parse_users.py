import json
import logging
import operator
import os
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.core.entities.user as class_user


def parse_users():

    """Parses all json files in pypelyne2.src.conf.settings.USERS_FILES folder and returns a sorted list of dicts.

    Parameters
    ----------


    Examples
    --------


    Returns
    -------
    list
        a sorted list of user dicts.

    """

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

    """Get all User() objects in a list

    Parameters
    ----------


    Returns
    -------
    list
        list of pypelyne2.src.modules.user.user.User() objects

    """

    user_objects = []
    users = parse_users()
    for user in users:
        new_user_object = class_user.User(user)
        # print dir(new_user_object)
        user_objects.append(new_user_object)

    return user_objects
