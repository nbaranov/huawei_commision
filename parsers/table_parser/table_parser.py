from .exceptions import TableParseException
from .table import Table
from .abstract_line_parser import AbstractLineParser


class TableParser:
    """Used to parse text line by line to create a table. For work use implementation of AbstractLineParser
    for parse every line to separate columns. Also clears the cell text from some junk."""
    def __init__(self, line_parser: AbstractLineParser):
        self.line_parser = line_parser

    def parse(self, table_text: str | list, head_lines: int = 1) -> Table:
        list_lines = table_text.split('\n') if isinstance(table_text, str) else table_text
        raw_table_rows = list(map(self.line_parser.parse_line, list_lines))
        clear_table_rows = self.__clear_rows(raw_table_rows)
        # check table is not empty and number of column is same
        if not clear_table_rows or any(map(lambda x: len(x) != len(clear_table_rows[0]), clear_table_rows[1:])):
            raise TableParseException('Can\'t parse this text!')

        table_head = clear_table_rows[0] if head_lines == 1 else self.__merge_rows(clear_table_rows[head_lines:])
        table_body = clear_table_rows[head_lines:]
        return Table(table_head, table_body)

    def __merge_rows(self, rows: list) -> list:
        result = []
        for i in range(len(rows)):
            head_merged_str = ' '.join((row[i] for row in rows))
            result.append(head_merged_str)
        return result

    def __clear_rows(self, raw_table_rows: list) -> list:
        return [list(map(lambda x: x.strip(), row)) for row in raw_table_rows if row]
