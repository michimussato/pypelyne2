import os
import json
import logging
import pypelyne2.src.modules.user.user as class_user
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_users():
    user_list = []

    for user_file in SETTINGS.USERS_FILES:

        logging.info('processing user source file: {0}'.format(user_file))
        with open(os.path.join(SETTINGS.USERS_DIR, user_file), 'r') as f:
            user_object = json.load(f)

        # print user_object

        user_dict = {}
        department_roles_list = []
        project_roles_list = []

        for department_role in user_object[u'department_roles']:
            department_roles_list.append(department_role.copy())

        for project in user_object[u'project_roles']:
            for role in project[u'roles']:
                role[u'project'] = project[u'project']

            project_roles_list.append(role.copy())

        # print department_roles_list
        # print project_roles_list

        user_dict[u'department_roles'] = user_object[u'department_roles']
        user_dict[u'project_roles'] = user_object[u'project_roles']
        user_dict[u'password'] = user_object[u'password']
        user_dict[u'icon'] = user_object[u'icon']
        user_dict[u'id'] = user_object[u'id']
        user_dict[u'name_login'] = user_object[u'name_login']
        user_dict[u'name_full'] = user_object[u'name_full']
        # user_dict[u''] = user_object[u'']
        # user_dict[u''] = user_object[u'']
        # user_dict[u''] = user_object[u'']
        # user_dict[u''] = user_object[u'']

        # print user_object

        user_list.append(user_dict.copy())
        #
        # print user_list

    # # logging.info('parsing tasks')
    #
    # with open(SETTINGS.TASKS_FILE, 'r') as f:
    #     json_object = json.load(f)
    # # f.close()
    #
    # tasks = [task for task in json_object if task['task_enable']]

    # print user_list
    return user_list


def get_users():
    user_objects = []
    users = parse_users()
    for user in users:
        new_user_object = class_user.User(user)
        user_objects.append(new_user_object)
        # print new_user_object

    return user_objects
