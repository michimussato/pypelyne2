import pypelyne2.src.core.parser.resources.routput.parse_routputs as parse_routputs


outputs = parse_routputs.get_routputs()

# print len(containers)

for output in outputs:
    print
    print
    print 'processing {0}'.format(output)
    print dir(output)

    for attr in dir(output):
        print '%s == %s' % (attr, getattr(output, attr))
