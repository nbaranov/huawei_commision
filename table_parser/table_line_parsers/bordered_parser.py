from ..exceptions import WrongBorderChar
from ..abstract_line_parser import AbstractLineParser


class BorderedTableParser(AbstractLineParser):
    """
    Parser for tables that has some special symbol as column separator  like '|' or ';'.
    """
    def __init__(self, border_symbol: str, out_border: bool = False):
        self.__out_border = out_border
        self.__border_symbol = border_symbol
        if len(self.__border_symbol) != 1 or self.__border_symbol == ' ':
            raise WrongBorderChar('Must contain single symbol and not equal "space"')

    def parse_line(self, text_line: str) -> list:
        line = text_line.strip(' ' + self.__border_symbol) if self.__out_border else text_line.strip()
        return line.split(self.__border_symbol) if line and self.__border_symbol in line else []


if __name__ == '__main__':
    print(BorderedTableParser(border_symbol='#', out_border=True).parse_line(
        '   #Destination/Mask #  Nexthop    #     Flag TimeStamp   #  Interface      #       TunnelID   #'))
