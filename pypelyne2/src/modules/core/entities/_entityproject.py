import pypelyne2.src.modules.core.entities.entity as entity


class EntityProject(entity.Entity):
    def __init__(self):
        super(EntityProject, self).__init__()

        # a project should have the following information
        #
        # - project id/uuid
        # - project codename
        # - project abbreviation
        # - client
        # - due
        # - progress
        # - type
        #   - feature
        #   - short
        #   - spot
        #   - print
        # - output
        #   - format
        #     - encoding
        #     - fps
        #     - height
        #     - width
        #     - aspect ratio
        #     - pixel aspect ratio
        #       - anamorphic

        # overrides of base classes
        self.entity_type = 'project'

        # frames per second
        # float:
        self.entity_project_fps = float()

        # the width and the height of the project output
        self.entity_project_width = float()
        self.entity_project_height = float()

        # the units of width and height
        # str(): pixel, mm, inch,
        self.entity_project_units = str()

        self.entity_project_anamorphic = False
        self.entity_project_client = None
        self.entity_project_scaling = None
