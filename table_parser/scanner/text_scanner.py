from typing import Callable

from ..abstract_line_parser import AbstractLineParser
from ..table_parser import TableParser
from ..table import Table


class TableScanner:
    """
    Scans multiline text and looks for table-like structures.
    In order for multiple text strings to be identified as a table, they must contain
    a symbol separator in same position several time.
    """

    def __init__(self, column_separator_symbol: str = ' ', columns_count_min: int = 3,
                 rows_count_min: int = 2, column_width_min: int = 3, validators: list[Callable[[str], bool]] = None):
        if len(column_separator_symbol) != 1:
            raise ValueError('column_separator_symbol must be single symbol')
        if columns_count_min < 2:
            raise ValueError('columns_count_min must be greater then 2')
        if rows_count_min < 2:
            raise ValueError('rows_count_min must be greater then 2')
        if column_width_min < 1:
            raise ValueError('column_width_min must be greater then 0')

        self.__column_width_min = column_width_min
        self.__column_separator_symbol = column_separator_symbol
        self.__columns_count_min = columns_count_min
        self.__rows_count_min = rows_count_min
        self.__validators = validators

    def scan(self, text: str) -> list[Table]:
        tables = []
        text_lines = self.__to_text_lines(text)
        table_start_line_num = 0
        last_mask = self.__create_mask(text_lines[0])
        for text_line_num in range(1, len(text_lines)):
            current_line_mask = self.__create_mask(text_lines[text_line_num])
            and_mask = last_mask & current_line_mask
            if self.__count_columns(and_mask) < self.__columns_count_min:
                if text_line_num - table_start_line_num >= self.__rows_count_min:
                    tables.append(self.__create_table(text_lines, table_start_line_num, text_line_num - 1, last_mask))
                last_mask = current_line_mask
                table_start_line_num = text_line_num
            else:
                last_mask = and_mask
        if len(text_lines) - table_start_line_num >= self.__rows_count_min:
            tables.append(self.__create_table(text_lines, table_start_line_num, len(text_lines) - 1, last_mask))
        return tables

    def __to_text_lines(self, text: str) -> list:
        text_lines = text.split('\n')
        return [line for line in text_lines if self.__line_validate(line)]

    def __line_validate(self, text_line: str) -> bool:
        return all([validator(text_line) for validator in self.__validators]) if self.__validators else True

    def __create_table(self, text_lines: list, start_line_index: int, end_line_index: int, mask: set) -> Table:
        parser = _MaskParser(list(mask), self.__column_width_min)
        table_parser = TableParser(parser)
        return table_parser.parse(text_lines[start_line_index: end_line_index + 1])

    def __create_mask(self, text_line: str):
        return set([symbol_pos
                    for symbol_pos in range(len(text_line))
                    if text_line[symbol_pos] == self.__column_separator_symbol])

    def __count_columns(self, mask: set):
        result = 0
        mask_list = sorted(list(mask))
        for mask_index in range(len(mask)):
            if mask_index and mask_list[mask_index] - mask_list[mask_index - 1] >= self.__column_width_min - 1 \
                    and mask_list[mask_index] != 0:
                result += 1
        return result + 1


class _MaskParser(AbstractLineParser):
    def __init__(self, mask: list, column_width_min: int):
        self.__mask = []
        sorted_mask = sorted(mask)
        mask_size = len(sorted_mask)
        for mask_index in range(mask_size):  # remove all sequences in mask
            if mask_index == mask_size - 1 \
                    or sorted_mask[mask_index + 1] - sorted_mask[mask_index] - 1 >= column_width_min \
                    and sorted_mask[mask_index]:
                self.__mask.append(sorted_mask[mask_index])

    def parse_line(self, text_line: str) -> list:
        result = []
        last_pos = 0
        for line_index in self.__mask:
            result.append(text_line[last_pos: line_index])
            last_pos = line_index
        result.append(text_line[last_pos:])
        return result
