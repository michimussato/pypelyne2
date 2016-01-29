import json
import logging
import operator
import pypelyne2.src.modules.department.department as class_department
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_departments():
    logging.info('parsing departments')

    with open(SETTINGS.DEPARTMENTS_FILE, 'r') as f:
        json_object = json.load(f)
    # f.close()

    departments = [department for department in json_object if department['department_enable']]

    return sorted(departments,
                  key=operator.itemgetter(SETTINGS.SORT_DEPARTMENTS),
                  reverse=SETTINGS.SORT_DEPARTMENTS_REVERSE)


def get_departments():
    department_objects = []
    departments = parse_departments()
    print departments
    for department in departments:
        new_department_object = class_department.Department(department)
        department_objects.append(new_department_object)

    return department_objects
