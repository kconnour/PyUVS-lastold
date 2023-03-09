import abc

from h5py import File


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
    def get_scattering_cross_section(self):
        pass

    @abc.abstractmethod
    def get_absorption_cross_section(self):
        pass

    @abc.abstractmethod
    def get_extinction_cross_section(self):
        pass

    @abc.abstractmethod
    def get_asymmetry_parameter(self):
        pass


class WolffRadiativeProperties(AbstractRadiativeProperties):
    def __init__(self, file: File):
        self.file = file

    def get_particle_sizes(self):
        return self.file['particle_sizes'][:]

    def get_wavelengths(self):
        return self.file['wavelengths'][:]

    def get_scattering_angles(self):
        return self.file['scattering_angles'][:]

    def get_scattering_cross_section(self):
        return self.file['scattering_cross_section'][:]

    def get_absorption_cross_section(self):
        csca = self.file['scattering_cross_section'][:]
        cext = self.file['extinction_cross_section'][:]
        return cext - csca

    def get_extinction_cross_section(self):
        return self.file['extinction_cross_section'][:]

    def get_asymmetry_parameter(self):
        return self.file['asymmetry_parameter'][:]
