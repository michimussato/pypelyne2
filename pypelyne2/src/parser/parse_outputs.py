import os
import json
import logging

import operator

import pypelyne2.src.modules.output.output as class_output
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_outputs():
    logging.info('parsing outputs')

    with open(SETTINGS.OUTPUTS_FILE, 'r') as f:
        json_object = json.load(f)

    outputs = [output for output in json_object if output['output_enable']]

    for output in outputs:
        if output[u'icon'] is not None:
            try:
                output[u'icon'] = os.path.join(SETTINGS.OUTPUTS_ICONS, output[u'icon'])
            except Exception, e:
                logging.error(e)
                output[u'icon'] = None

    return sorted(outputs,
                  key=operator.itemgetter(SETTINGS.SORT_OUTPUTS),
                  reverse=SETTINGS.SORT_OUTPUTS_REVERSE)


def get_outputs():
    output_objects = []
    outputs = parse_outputs()
    for output in outputs:
        new_output_object = class_output.Output(output)
        output_objects.append(new_output_object)

    return output_objects
