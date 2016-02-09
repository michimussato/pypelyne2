import json
import logging
import operator
import pypelyne2.src.modules.role.role as class_role
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_roles():

    """Parses the pypelyne2.src.conf.settings.SETTINGS.ROLES_FILE file and returns a sorted list of dicts.

    Parameters
    ----------


    Examples
    --------


    Returns
    -------
    list
        a sorted list of role dicts.

    """

    logging.info('parsing roles')

    with open(SETTINGS.ROLES_FILE, 'r') as f:
        json_object = json.load(f)
    # f.close()

    roles = [role for role in json_object if role['role_enable']]

    return sorted(roles,
                  key=operator.itemgetter(SETTINGS.SORT_ROLES),
                  reverse=SETTINGS.SORT_ROLES_REVERSE)


def get_roles():

    """Get all Role() objects in a list

    Parameters
    ----------


    Returns
    -------
    list
        list of pypelyne2.src.modules.role.role.Role() objects

    """

    role_objects = []
    roles = parse_roles()
    print roles
    for role in roles:
        new_role_object = class_role.Role(role)
        role_objects.append(new_role_object)

    return role_objects
