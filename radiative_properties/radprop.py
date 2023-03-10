import abc

from astropy.io import fits

from radiative_properties.wolff import RadiativeProperties


class AbstractRadiativeProperties(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_particle_sizes(self):
        pass

    @abc.abstractmethod
    def get_wavelengths(self):
        pass

    @abc.abstractmethod
    def get_scattering_angles(self):
        pass

    @abc.abstractmethod
    def get_scattering_cross_sections(self):
        pass

    @abc.abstractmethod
    def get_absorption_cross_sections(self):
        pass

    @abc.abstractmethod
    def get_extinction_cross_sections(self):
        pass

    @abc.abstractmethod
    def get_asymmetry_parameters(self):
        pass


class WolffRadiativeProperties(AbstractRadiativeProperties):
    def __init__(self, path: str):
        hdul = fits.open(path)
        self.radprop = RadiativeProperties(hdul)

    def get_particle_sizes(self):
        return self.radprop.get_particle_sizes()

    def get_wavelengths(self):
        return self.radprop.get_wavelengths()

    def get_scattering_angles(self):
        return self.radprop.get_scattering_angles()

    def get_scattering_cross_sections(self):
        return self.radprop.get_scattering_cross_section()

    def get_absorption_cross_sections(self):
        csca = self.get_scattering_cross_sections()
        cext = self.get_extinction_cross_sections()
        return cext - csca

    def get_extinction_cross_sections(self):
        return self.radprop.get_extinction_cross_section()

    def get_asymmetry_parameters(self):
        return self.radprop.get_asymmetry_parameter()
