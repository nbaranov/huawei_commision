from .abc import AbcVendorFactory


class HuaweiFactory(AbcVendorFactory):
    def configure(self, builder):
        builder.add_level_char(' ') \
            .add_line_validator(lambda x: x != '#') \
            .add_line_validator(lambda x: not x.startswith('!')) \
            .add_line_validator(lambda x: x.count('=') < 10 and x.count('-') < 10) \
            .add_line_validator(lambda x: x.strip())
