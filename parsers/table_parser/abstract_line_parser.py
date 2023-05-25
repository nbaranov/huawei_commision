from abc import ABCMeta, abstractmethod


class AbstractLineParser(metaclass=ABCMeta):

    @abstractmethod
    def parse_line(self, text_line: str) -> list:
        pass
