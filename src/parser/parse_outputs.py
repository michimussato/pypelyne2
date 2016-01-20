import json
import logging
import src.modules.output.output as class_output
import src.conf.settings.SETTINGS as SETTINGS


def parse_outputs():
    logging.info('parsing outputs')

    with open(SETTINGS.OUTPUTS_FILE, 'r') as f:
        json_object = json.load(f)

    outputs = [output for output in json_object if output['output_enable']]

    return outputs


def get_outputs():
    output_objects = []
    outputs = parse_outputs()
    for output in outputs:
        new_output_object = class_output.Output(output)
        output_objects.append(new_output_object)

    return output_objects
