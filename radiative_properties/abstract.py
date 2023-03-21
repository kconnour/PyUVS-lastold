import abc


class AbstractRadiativeProperties(metaclass=abc.ABCMeta):
    """An object defining an interface that all radiative properties must implement.

    This is not designed to be directly instantiated.

    """
    @abc.abstractmethod
    def get_particle_sizes(self):
        pass

    @abc.abstractmethod
    def get_wavelengths(self):
        pass

    @abc.abstractmethod
    def get_scattering_cross_sections(self):
        pass

    @abc.abstractmethod
    def get_extinction_cross_sections(self):
        pass

    @abc.abstractmethod
    def get_asymmetry_parameters(self):
        pass
