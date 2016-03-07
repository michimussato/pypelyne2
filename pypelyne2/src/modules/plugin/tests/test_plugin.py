import pypelyne2.src.parser.parse_plugins as parse_plugins


plugins = parse_plugins.get_plugins()

for plugin in plugins:
    print
    print
    print 'processing {0}'.format(plugin)
    print dir(plugin)
    for attribute in dir(plugin):
        print '%s = %s' % (attribute, getattr(plugin, attribute))
