import random

import pypelyne2.src.modules.core.entities.entity as entity
import pypelyne2.src.modules.core.parser.parse_outputs as parse_outputs


class EntityTaskOutput(entity.Entity):
    def __init__(self, output_object=None):
        super(EntityTaskOutput, self).__init__()

        # overrides of base class
        self.entity_type = 'output'

        # these are the the output versions
        # list: [uuid, uuid, uuid]
        self.entity_task_output_versions = []

        # this is the currently published version
        # str: 'uuid'
        self.entity_task_output_published = str()

        self.entity_task_output_object = output_object or parse_outputs.get_outputs()[random.randint(0, len(
            parse_outputs.get_outputs()) - 1)].rand_arch



