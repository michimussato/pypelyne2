import pypelyne2.src.core.parser.entities.department.parse_departments as parse_departments


departments = parse_departments.get_departments()

# print len(containers)

for department in departments:
    print department

for attr in dir(departments[0]):
    print attr, '=', getattr(departments[0], attr)
