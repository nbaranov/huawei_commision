from typing import Optional

from .huawei import HuaweiFactory


def _get_factory(parser_type: str) -> Optional[HuaweiFactory]:
    if parser_type == 'huawei':
        return HuaweiFactory()
    else:
        raise IndexError('Unsupported type')
