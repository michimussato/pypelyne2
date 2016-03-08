import pypelyne2.src.modules.core.parser.entities.role.parse_roles as parse_roles


roles = parse_roles.get_roles()

for role in roles:
    print
    print
    print 'processing {0}'.format(role)
    print dir(role)
    for attribute in dir(role):
        print '%s == %s' % (attribute, getattr(role, attribute))
