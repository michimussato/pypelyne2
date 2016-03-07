import pypelyne2.src.modules.core.parser.output.parse_outputs as parse_outputs


outputs = parse_outputs.get_outputs()

# print len(containers)

for output in outputs:
    print
    print
    print 'processing {0}'.format(output)
    print dir(output)

    for attr in dir(output):
        print '%s == %s' % (attr, getattr(output, attr))
