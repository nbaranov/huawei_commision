from abc import ABCMeta, abstractmethod


class AbcTreeConfigItem(metaclass=ABCMeta):

    @abstractmethod
    def parse_children_in_line(self, config_line: str, level: int):
        """Config_line contains childrens elements for this instance. This function create all childrens from config_line and append
        to list use add_children.
        :param config_line: String that contains information for create new TreeConfigItem
        :param level: Level for this items
        """
        pass

    @abstractmethod
    def get_config(self) -> str:
        """String that can identify this item.
        """
        pass

    @abstractmethod
    def find_parent(self, level: int):
        pass
