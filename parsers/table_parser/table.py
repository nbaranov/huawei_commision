from typing import Callable


class Table:
    """
    Encapsulates logic work with a tables. It immutable object, any modify functions must return new Table instance.
    """
    def __init__(self, head, body):
        self.__head = {head[i]: i for i in range(len(head))}
        self.__body = body

    @property
    def head(self) -> list:
        return list(self.__head.keys())

    @property
    def body(self) -> list:
        return self.__body

    def get_column(self, column_name: str) -> list:
        column_index = self.__head[column_name]
        return [row[column_index] for row in self.__body]

    def get_simple_table(self):
        return [{k: row[v] for k, v in self.__head.items()} for row in self.__body]

    def get_pivot_table(self):
        return {row[0]: {k: row[v] for k, v in list(self.__head.items())[1:]} for row in self.__body}

    def filter(self, column_name: str, filter_func: Callable[[str], bool]) -> 'Table':
        """
Validate rows use filter_function.
        :param column_name: The name of the column in which to check the cell for each row
        :param filter_func: A validate function that apply to every cell in column
        :return: Filtered Table instance
        """
        column_index = self.__head[column_name]
        new_body = [row for row in self.__body if filter_func(row[column_index])]
        return Table(list(self.__head.keys()), new_body)
