import abc


class Pypelyne(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_projects(self,
                     project_status=None,
                     project_client=None,
                     project_name_pattern=None,
                     project_type=None,
                     project_fps=None,
                     project_resolution=None,
                     project_due_by=None,
                     project_uuid=None):
        """
        :param project_status: str()
        :param project_client: str()
        :param project_name_pattern: str()
        :param project_type:
        :param project_fps:
        :param project_resolution:
        :param project_due_by:

        :returns all matching projects
        """
        pass

    @abc.abstractmethod
    def set_project(self,
                    project):
        """

        :param project:
        :return:
        """


    @abc.abstractmethod
    def load_entities(self,
                      project):
        """
        :param project: Project()

        load all entities of a project.
        """
        pass

    @abc.abstractmethod
    def get_children(self,
                     entity):
        """
        :param entity: entity

        :returns all direct children of an entity.
        None if entity has no children.
        """
        pass

    @abc.abstractmethod
    def get_inputs(self,
                   entity):
        """
        :param entity: entity (container or task)

        :returns list of EntityOutput all incoming outputs of an entity.
        None if entity has no incoming outputs.

        entity must be container or task.
        """
        pass
