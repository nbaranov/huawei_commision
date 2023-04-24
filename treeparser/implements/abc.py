from abc import ABCMeta, abstractmethod


class AbcVendorFactory(metaclass=ABCMeta):
    """Class for configure ConfigParser via builder. Override configure method for create special configure of
    ConfigParser and use it quickly. After all, add your implementation to _get_factory function under some name."""
    @abstractmethod
    def configure(self, builder):
        pass