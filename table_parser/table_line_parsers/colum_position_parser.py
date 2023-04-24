from enum import Enum

from ..abstract_line_parser import AbstractLineParser


class CellAlignment(Enum):
    LEFT = 1
    RIGHT = 2


class ColumnPositionParser(AbstractLineParser):
    """
    Parser for tables that has alignment by table headers. This means that the start (or end) position of the header
    column is equal to the start (or end) position of the cell text for each row.
    """
    def __init__(self, alignment: CellAlignment = CellAlignment.LEFT, gap: int = 2):
        self.__gap = gap
        self.__alignment = alignment
        self.__column_indexes = []

    def parse_line(self, text_line: str) -> list:
        if not self.__column_indexes:
            self.__find_indexes(text_line)
        if max(self.__column_indexes[-1]) > len(text_line):
            return []
        return [text_line[cell_index[0]: cell_index[1] + 1 if cell_index[1] >= 0 else len(text_line)] for
                cell_index in self.__column_indexes]

    def __find_indexes(self, text_line: str):
        self.__column_indexes = []
        line_len = len(text_line)
        separator = ' ' * self.__gap
        last_position = 0
        find_separator = True
        for position in range(line_len):
            if text_line[position] != ' ':  # it space
                if find_separator and self.__alignment == CellAlignment.LEFT:
                    self.__column_indexes.append([position, -1])
                    if len(self.__column_indexes) > 1:
                        self.__column_indexes[-2][1] = position - 1
                    last_position = position
                find_separator = False

            elif position + self.__gap < line_len \
                    and text_line[position: position + self.__gap] == separator \
                    or position == line_len:
                if not find_separator and self.__alignment == CellAlignment.RIGHT:
                    self.__column_indexes.append([last_position, position])
                    last_position = position
                find_separator = True


if __name__ == '__main__':
    print(ColumnPositionParser(alignment=CellAlignment.LEFT, gap=3).parse_line(
        '   Destination/Mask   Nexthop         Flag TimeStamp     Interface              TunnelID   '))
