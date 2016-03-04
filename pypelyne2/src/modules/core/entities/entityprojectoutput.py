import pypelyne2.src.modules.core.entities.entityproject as entityproject


class EntityProjectOutput(entityproject.EntityProject):
    # delivery entity
    def __init__(self,
                 override_entity_project_fps=False,
                 override_entity_project_width=False,
                 override_entity_project_height=False,
                 override_entity_project_units=False,
                 override_entity_project_anamorphic=False,
                 override_entity_project_scaling=False):
        super(EntityProjectOutput, self).__init__()

        # overrides of base classes
        self.entity_type = 'delivery'

        # frames per second
        # float:
        self.entity_project_output_fps = override_entity_project_fps or self.entity_project_fps

        # the width and the height of the project output
        self.entity_project_output_width = override_entity_project_width or self.entity_project_width
        self.entity_project_output_height = override_entity_project_height or self.entity_project_height

        # the units of width and height
        # str(): pixel, mm, inch,
        self.entity_project_output_units = override_entity_project_units or self.entity_project_units

        self.entity_project_output_anamorphic = override_entity_project_anamorphic or self.entity_project_anamorphic
        # self.entity_project_output_client = None
        self.entity_project_output_scaling = override_entity_project_scaling or self.entity_project_scaling
