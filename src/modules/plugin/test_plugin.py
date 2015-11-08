# usage:

import src.parser.parse_plugins as parse_plugins

plugins = parse_plugins.get_plugins()

attributes = dir(plugins[0])
for attribute in attributes:
    print '%s = %s' % (attribute, getattr(plugins[1], attribute))
