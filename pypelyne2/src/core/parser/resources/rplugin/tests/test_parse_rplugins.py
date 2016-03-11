# import unittest
# import random
import pypelyne2.src.core.parser.resources.rplugin.parse_rplugins as parse_rplugins


plugins = parse_rplugins.get_rplugins()

for plugin in plugins:
    print
    print
    print 'processing {0}'.format(plugin)
    print dir(plugin)
    for attribute in dir(plugin):
        print '%s == %s' % (attribute, getattr(plugin, attribute))
