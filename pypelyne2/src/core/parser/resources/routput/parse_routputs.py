import json
import logging
import operator
import os

import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.core.resources.routput as routput


def parse_routputs():

    """Parses the pypelyne2.src.conf.settings.OUTPUTS_FILE file and returns a sorted list of dicts.

    Parameters
    ----------


    Examples
    --------


    Returns
    -------
    list
        a sorted list of output dicts.

    """

    logging.info('parsing outputs')

    with open(SETTINGS.OUTPUTS_FILE, 'r') as f:
        json_object = json.load(f)

    outputs = [output for output in json_object if output['output_enable']]

    # for output in outputs:
    #     output['entity_type'] = 'output'

    for output in outputs:
        # output[u'node_id_source'] = None
        output[u'version_id_list'] = set()
        # output[u'version_id_live'] = None
        if output[u'icon'] is not None:
            try:
                output[u'icon'] = os.path.join(SETTINGS.OUTPUTS_ICONS, output[u'icon'])
            except Exception, e:
                logging.error(e)
                output[u'icon'] = None

    return sorted(outputs,
                  key=operator.itemgetter(SETTINGS.SORT_OUTPUTS),
                  reverse=SETTINGS.SORT_OUTPUTS_REVERSE)


def get_routputs():

    """Get all Output() objects in a list

    Parameters
    ----------


    Returns
    -------
    list
        list of pypelyne2.src.modules.output.output.Output() objects

    """

    output_objects = []
    outputs = parse_routputs()
    for output in outputs:
        new_output_object = routput.ROutput(output)
        output_objects.append(new_output_object)

    return output_objects
