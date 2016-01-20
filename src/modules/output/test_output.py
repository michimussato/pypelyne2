# usage:

import src.parser.parse_outputs as parse_outputs

outputs = parse_outputs.get_outputs()

attributes = dir(outputs[0])
for attribute in attributes:
    print '%s = %s' % (attribute, getattr(outputs[1], attribute))
