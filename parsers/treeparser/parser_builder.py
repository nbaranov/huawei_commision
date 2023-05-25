from typing import Callable

from .config_item.abc import AbcTreeConfigItem


class ConfigParserBuilder:
    """
    This builder configure ConfigParser. After set all parameters, call build() for get 'ConfigParser' instance.
    """

    class __ConfigParser:
        """
        Class for fill your implementation of TreeConfigItem as tree structure.
        Use the builder to define what text segment is a config.
        """

        def __init__(self):
            self._line_separator = '\n'
            self._list_validators = []
            self._level_chars = ''
            self._root_item = None

        def __get_line_attributes(self, line: str) -> dict:
            result = {}
            if not all(map(lambda v: v(line), self._list_validators)):
                return result
            result['line'] = line.lstrip(self._level_chars)
            result['level'] = len(line) - len(result['line']) + 1
            return result

        def parse_config(self, config_text: str = ''):
            """
            It does parse text by line and fill tree in _root_item.
            :param config_text: text formatted as a tree structure
            :return: the root element that contains(or not) the same children elements
            """
            current_parent_item = self._root_item
            for config_line in filter(None, config_text.split(self._line_separator)):
                line_attributes = self.__get_line_attributes(config_line)
                if line_attributes:
                    current_parent_item = current_parent_item.find_parent(line_attributes['level'])
                    current_parent_item.parse_children_in_line(line_attributes['line'], line_attributes['level'])
            return self._root_item

    def __init__(self):
        self.__list_validators = []
        self.__list_level_chars = []
        self.__build_instance = ConfigParserBuilder.__ConfigParser()

    def set_line_separator(self, line_separator: str):
        self.__build_instance._line_separator = line_separator
        return self

    def set_root_item(self, root_item: AbcTreeConfigItem):
        self.__build_instance._root_item = root_item
        return self

    def add_line_validator(self, validator: Callable[[str], bool]):
        self.__list_validators.append(validator)
        return self

    def add_level_char(self, level_char: str):
        self.__list_level_chars.append(level_char)
        return self

    def build(self):
        if self.__build_instance._root_item is None:
            raise ValueError('Root item is not set!')
        self.__build_instance._level_chars = ''.join(self.__list_level_chars)
        self.__build_instance._list_validators = self.__list_validators
        return self.__build_instance
