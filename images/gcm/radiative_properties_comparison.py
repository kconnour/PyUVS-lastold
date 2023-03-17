import matplotlib.pyplot as plt
import numpy as np

from radiative_properties.wolff import WolffRadiativeProperties
from radiative_properties.ames import AmesRadiativeProperties


fig, ax = plt.subplots(2, 3, figsize=(9, 6))

wolff_dust = WolffRadiativeProperties('dust', 1)
wolff_particle_sizes = wolff_dust.get_particle_sizes()
wolff_wavelengths = wolff_dust.get_wavelengths()
wolff_csca = wolff_dust.get_scattering_cross_sections()
wolff_cext = wolff_dust.get_extinction_cross_sections()

wolff_particle_size_edges = np.concatenate(([0.05], (wolff_particle_sizes[1:] + wolff_particle_sizes[:-1])/2, [5.875]))
wolff_wavelength_edges = np.concatenate(([0.15], (wolff_wavelengths[1:] + wolff_wavelengths[:-1])/2, [50.1]))
wolff_x, wolff_y = np.meshgrid(wolff_wavelength_edges, wolff_particle_size_edges)

ames_dust = AmesRadiativeProperties('dust', 1)
ames_particle_sizes = ames_dust.get_particle_sizes()
ames_wavelengths = ames_dust.get_wavelengths()
ames_csca = (ames_dust.get_scattering_cross_sections().T * np.pi * ames_particle_sizes**2).T
ames_cext = ames_dust.get_extinction_cross_sections() # (ames_dust.get_extinction_cross_sections().T * np.pi * ames_particle_sizes**2).T

ames_particle_size_edges = np.concatenate(([0.18], (ames_particle_sizes[1:] + ames_particle_sizes[:-1])/2, [1000]))
ames_wavelength_edges = np.concatenate(([0.06], (ames_wavelengths[1:] + ames_wavelengths[:-1])/2, [64]))
ames_x, ames_y = np.meshgrid(ames_wavelength_edges, ames_particle_size_edges)

for i in range(2):
    for j in range(3):
        if i == 0 and j == 0:
            pcm = ax[0, 0].pcolormesh(wolff_x, wolff_y, np.log(wolff_csca), cmap='plasma', vmin=0, vmax=5)
            ax[0, 0].set_title('Log Wolff Csca')
        elif i == 0 and j == 1:
            pcm = ax[0, 1].pcolormesh(wolff_x, wolff_y, np.log(wolff_cext), cmap='plasma', vmin=0, vmax=5)
            ax[0, 1].set_title('Log Wolff Cext')
        elif i == 0 and j == 2:
            pcm = ax[0, 2].pcolormesh(wolff_x, wolff_y, wolff_csca / wolff_cext, cmap='plasma', vmin=0, vmax=1)
            ax[0, 2].set_title('Wolff SSA')
        elif i == 1 and j == 0:
            pcm = ax[1, 0].pcolormesh(ames_x, ames_y, np.log(ames_csca), cmap='plasma', vmin=0, vmax=5)
            ax[1, 0].set_title('Log Ames Csca')
            ax[1, 0].set_ylabel('Particle size [microns]')
            ax[1, 0].set_xlabel('Wavelength [microns]')
        elif i == 1 and j == 1:
            pcm = ax[1, 1].pcolormesh(ames_x, ames_y, ames_cext, cmap='jet', vmin=0, vmax=3.6)
            ax[1, 1].set_title('Log Ames Cext')
        elif i == 1 and j == 2:
            pcm = ax[1, 2].pcolormesh(ames_x, ames_y, ames_csca / ames_cext, cmap='plasma', vmin=0, vmax=1)
            ax[1, 2].set_title('Ames SSA')

        ax[i, j].set_xlim(0, 2)
        ax[i, j].set_ylim(0, 5)
        ax[i, j].set_facecolor('gray')

        fig.colorbar(pcm, ax=ax[i, j])

plt.savefig('/media/kyle/iuvs/images/gcm/dust_wolff1_vs_ames1-jet.png', dpi=200)
plt.close(fig)

fig, ax = plt.subplots(2, 3, figsize=(9, 6))

wolff_dust = WolffRadiativeProperties('ice', 1)
wolff_particle_sizes = wolff_dust.get_particle_sizes()
wolff_wavelengths = wolff_dust.get_wavelengths()
wolff_csca = wolff_dust.get_scattering_cross_sections()
wolff_cext = wolff_dust.get_extinction_cross_sections()

wolff_particle_size_edges = np.concatenate(([0.05], (wolff_particle_sizes[1:] + wolff_particle_sizes[:-1])/2, [5.875]))
wolff_wavelength_edges = np.concatenate(([0.15], (wolff_wavelengths[1:] + wolff_wavelengths[:-1])/2, [50.1]))
wolff_x, wolff_y = np.meshgrid(wolff_wavelength_edges, wolff_particle_size_edges)

ames_dust = AmesRadiativeProperties('ice', 1)
ames_particle_sizes = ames_dust.get_particle_sizes()
ames_wavelengths = ames_dust.get_wavelengths()
ames_csca = (ames_dust.get_scattering_cross_sections().T * np.pi * ames_particle_sizes**2).T
ames_cext = (ames_dust.get_extinction_cross_sections().T * np.pi * ames_particle_sizes**2).T

ames_particle_size_edges = np.concatenate(([0.18], (ames_particle_sizes[1:] + ames_particle_sizes[:-1])/2, [1000]))
ames_wavelength_edges = np.concatenate(([0.098], (ames_wavelengths[1:] + ames_wavelengths[:-1])/2, [50.5]))
ames_x, ames_y = np.meshgrid(ames_wavelength_edges, ames_particle_size_edges)

for i in range(2):
    for j in range(3):
        if i == 0 and j == 0:
            pcm = ax[0, 0].pcolormesh(wolff_x, wolff_y, np.log(wolff_csca), cmap='plasma', vmin=0, vmax=5)
            ax[0, 0].set_title('Log Wolff Csca')
        elif i == 0 and j == 1:
            pcm = ax[0, 1].pcolormesh(wolff_x, wolff_y, np.log(wolff_cext), cmap='plasma', vmin=0, vmax=5)
            ax[0, 1].set_title('Log Wolff Cext')
        elif i == 0 and j == 2:
            pcm = ax[0, 2].pcolormesh(wolff_x, wolff_y, wolff_csca / wolff_cext, cmap='plasma', vmin=0, vmax=1)
            ax[0, 2].set_title('Wolff SSA')
        elif i == 1 and j == 0:
            pcm = ax[1, 0].pcolormesh(ames_x, ames_y, np.log(ames_csca), cmap='plasma', vmin=0, vmax=5)
            ax[1, 0].set_title('Log Ames Csca')
            ax[1, 0].set_ylabel('Particle size [microns]')
            ax[1, 0].set_xlabel('Wavelength [microns]')
        elif i == 1 and j == 1:
            pcm = ax[1, 1].pcolormesh(ames_x, ames_y, np.log(ames_cext), cmap='plasma', vmin=0, vmax=5)
            ax[1, 1].set_title('Log Ames Cext')
        elif i == 1 and j == 2:
            pcm = ax[1, 2].pcolormesh(ames_x, ames_y, ames_csca / ames_cext, cmap='plasma', vmin=0, vmax=1)
            ax[1, 2].set_title('Ames SSA')

        ax[i, j].set_xlim(0, 1)
        ax[i, j].set_ylim(0, 5)
        ax[i, j].set_facecolor('gray')

        fig.colorbar(pcm, ax=ax[i, j])

plt.savefig('/media/kyle/iuvs/images/gcm/ice_wolff1_vs_ames1.png', dpi=200)
