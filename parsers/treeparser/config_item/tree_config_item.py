import re
from abc import ABC
from datetime import datetime
from functools import reduce
from typing import Any, Callable, Optional, TypeVar, List

from .abc import AbcTreeConfigItem

SelfTreeConfig = TypeVar("SelfTreeConfig", bound="TreeConfigItem")


class TreeConfigItem(AbcTreeConfigItem):
    """This class implement store level, childrens and parents of current item.
    Also, this contains logic for find items by any parameters.
    Extend this class for define how parse and store config line.
    """

    def __init__(self, parent=None, level: int = 0):
        self.__level = level
        self.__childrens = []
        self.__parent = parent

    def add_children(self, children: SelfTreeConfig):
        self.__childrens.append(children)

    def find_config(self, validator: Callable[[str], bool], level_min: int = 0, level_max: int = 0) -> list:
        """Completely scanning tree and find all items, that is valid by validator function.
        :param validator: Function that validate item by get_config string
        :param level_min: Limit search deep by minimum level
        :param level_max: Limit search deep by maximum level
        :return: list of find items.
        """
        result = []
        if validator(self.get_config()) \
                and (not level_min or self.__level >= level_min) \
                and (not level_max or self.__level <= level_max):
            result.append(self)
        children_find = list(map(lambda conf: conf.find_config(
            validator, level_min, level_max), self.childrens))
        if children_find:
            result.extend(reduce(lambda x, y: x + y, children_find))
        return result

    def follow_path(self, path: list, extractor: Optional[Callable[[SelfTreeConfig], str]] = None) -> Any:
        """Follow by path as list of strings, and return found value of None. Use extractor for returning string value of item,
        or in another case it return tree item instance.
        :param path: list of strings that will compare with string getted from get_config, implemented in your
        AbstractTreeConfigItem implementation.
        :param extractor: A function that convert tree item to string
        :return: Item or string, found in the path or None in case path isn't exists.
        """
        if path and path[0] == self.get_config():
            if len(path) > 1:
                remaining_items = path[1:]
                children_search_result = [children.follow_path(remaining_items, extractor)
                                          for children in self.__childrens]
                childrens_find = tuple(filter(lambda x: x is not None, children_search_result))
                return childrens_find[0] if childrens_find else None
            else:
                return extractor(self) if extractor else self
        return None

    def find_parent(self, level: int) -> SelfTreeConfig:
        """Find parent item for level
        :param level: For this level it find parent item
        :return: Instance of TreeConfigItem that have level higher(number is less) than getting from param
        """
        if self.__level >= level:
            return self.__parent.find_parent(level)
        else:
            if level == self.__level + 1 or not self.__childrens or self.__childrens[-1].level >= level:
                return self
            else:
                return self.__childrens[-1]

    def chain_to_root(self) -> list:
        """It creates list of items, that every item is parent for previous in order by level from root item to item that called this function.
        :return: list of instance TreeConfigItem
        """
        return self.__parent.chain_to_root() + [self] if self.__parent is not None else [self]

    @property
    def level(self) -> int:
        return self.__level

    @property
    def parent(self) -> int:
        return self.__parent

    @property
    def childrens(self) -> list:
        return self.__childrens


class SimpleConfigItem(TreeConfigItem):
    """This instance store config as simple text line.
    """

    def __init__(self, config: str, parent=None, level: int = 0):
        super().__init__(parent, level)
        self.__config = config

    def parse_children_in_line(self, config_line: str, level: int):
        self.add_children(SimpleConfigItem(config_line, self, level))

    def get_config(self) -> str:
        return self.__config

    def __str__(self):
        return f'tree level: {self.level}, indent: {self.level - 1 if self.level != 0 else self.level}, line: {self.__config}'


class PropertyConfigItem(TreeConfigItem):
    """
    This instance store config as key and value, and use key as identifier.
    Line of this config can contain multiple children elements, separated by __config_separator.
    """

    def __init__(self, key: str = 'root', value: str = None, parent=None, level: int = 0):
        super().__init__(parent, level)
        self.__value = value
        self.__key = key
        self.__key_value_separators = (':', ' is ')
        self.__config_separator = ','
        self.__value_pattern = '([-+]?\d+(\.\d+)?)\s*([^\d\s]+)?'

    def __validate_items(self, line_separated: list):
        current_item = 0
        while len(line_separated) > current_item and len(line_separated) != 1:
            if not any(map(lambda x: x in line_separated[current_item], self.__key_value_separators)):
                if current_item == 0:
                    line_separated[1] = line_separated[0] + \
                                        self.__config_separator + line_separated[1]
                    del line_separated[0]
                else:
                    line_separated[current_item - 1] = line_separated[current_item - 1] \
                                                       + self.__config_separator \
                                                       + line_separated[current_item]
                    del line_separated[current_item]
            else:
                current_item += 1
        return line_separated

    def parse_children_in_line(self, config_line: str, level: int):
        line_separated = self.__validate_items(
            config_line.split(self.__config_separator))
        for conf_item in line_separated:
            separators = {conf_item.find(separator): separator for separator in self.__key_value_separators
                          if separator in conf_item}
            if not separators:
                conf_list = [conf_item, None]
            else:
                min_pos = min(separators.keys())
                conf_list = [conf_item[0:min_pos],
                             conf_item[min_pos + len(separators[min_pos]):]]
                conf_list[1] = conf_list[1].strip()
            self.add_children(
                PropertyConfigItem(key=conf_list[0].strip(), value=conf_list[1], parent=self, level=level))

    def get_config(self):
        return self.__key

    @property
    def name(self) -> str:
        return self.__key

    @property
    def value(self) -> str:
        return self.__value

    @property
    def number_value(self) -> Optional[float | int]:
        match = re.search(self.__value_pattern, self.__value)
        if match:
            num_value = match.group(1)
            return float(num_value) if '.' in num_value else int(num_value)

    @property
    def notation_value(self) -> Optional[str]:
        match = re.search(self.__value_pattern, self.__value)
        if match:
            num_value = match.group(3)
            return num_value

    def parse_date(self, custom_pattern: str = None, custom_date_mask: str = None) -> Optional[datetime]:
        DATE_PATTERN = '\d{4}(-\d\d){2} (\d{2}:?){3}'
        DATE_MASK = "%Y-%m-%d %H:%M:%S"
        matches = re.search(custom_pattern or DATE_PATTERN, self.__value)
        if matches:
            return datetime.strptime(matches.group(0), custom_date_mask or DATE_MASK) if matches else None

    def __str__(self):
        return f'tree level: {self.level}, indent: {self.level - 1 if self.level != 0 else self.level}, line: {self.__key} = {self.__value}'


class PivotTableConfigItem(TreeConfigItem):
    def __init__(self, body: List[str], column_parse_function: Callable[[str], list], header: dict = None, parent=None,
                 level: int = 0):
        super().__init__(parent, level)
        self.__column_parse_function = column_parse_function
        self.__header = header
        self.__body = body

    def parse_children_in_line(self, config_line: str, level: int):
        row = self.__column_parse_function((' ' * (level - 1)) + config_line)
        if not row:
            return
        row = list(map(lambda x: x.strip(), row))
        if self.__header and len(row) < len(self.__header):
            row.append([''] * (len(self.__header) - len(row)))
        if self.__header:
            self.add_children(PivotTableConfigItem(body=row, column_parse_function=self.__column_parse_function,
                                                   header=self.__header, parent=self, level=level))
        else:
            self.__header = {row[cell_id]: cell_id for cell_id in range(len(row))}

    def get_config(self) -> str:
        return self.__body[0] if self.__body else None

    def get_value(self, column_name: str) -> Optional[str]:
        return self.__body[self.__header[column_name]] if column_name in self.__header else None

    @property
    def body(self) -> List[str]:
        return self.__body

    @property
    def header(self) -> dict:
        return self.__header
