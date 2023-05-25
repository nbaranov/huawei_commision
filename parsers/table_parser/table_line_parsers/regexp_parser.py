import re

from ..abstract_line_parser import AbstractLineParser


class RegexpLineParser(AbstractLineParser):
    """For this parser, every cell must be matched the regular expression pattern."""

    def __init__(self, pattern: str):
        self.__pattern = re.compile(pattern)

    def parse_line(self, text_line: str) -> list:
        matches = self.__pattern.finditer(text_line)
        return list(map(lambda x: x.group(0), matches)) if matches else []


if __name__ == '__main__':
    print(RegexpLineParser(pattern='[^\s]+(\s+|$)').parse_line(
        '   Destination/Mask   Nexthop         Flag TimeStamp     Interface              TunnelID   '))
