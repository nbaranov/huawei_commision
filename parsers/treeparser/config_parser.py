from .implements import _get_factory

from .parser_builder import ConfigParserBuilder


def tree_parser(parser_type: str, root_item):
    parce_builder = ConfigParserBuilder()
    factory_instance = _get_factory(parser_type)
    factory_instance.configure(parce_builder)
    parce_builder.set_root_item(root_item)
    return parce_builder.build()
