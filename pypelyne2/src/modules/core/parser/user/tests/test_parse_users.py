import pypelyne2.src.modules.core.parser.user.parse_users as parse_users


users = parse_users.get_users()

for user in users:
    print
    print
    print 'processing {0}'.format(user)
    print dir(user)
    for attribute in dir(user):
        print '%s == %s' % (attribute, getattr(user, attribute))
