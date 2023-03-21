import abc


class AbstractSimulation(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_surface_pressure(self):
        pass

    @abc.abstractmethod
    def get_surface_temperature(self):
        pass

    @abc.abstractmethod
    def get_atmospheric_pressure(self):
        pass

    @abc.abstractmethod
    def get_atmospheric_temperature(self):
        pass
