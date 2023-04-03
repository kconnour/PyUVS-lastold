import matplotlib.pyplot as plt
import numpy as np

from gcm.ames import AmesSimulation
from gcm.pcm import PlanetaryClimateModelSimulation


if __name__ == '__main__':
    ames_mars_year = 30
    ames = AmesSimulation(2, ames_mars_year)

    ames_dust = ames.get_dust_visible_column_optical_depth()
    ames_ice = ames.get_ice_visible_column_optical_depth()

    ames_x, ames_y = np.meshgrid(ames.get_longitude_edges(), ames.get_latitude_edges())

    lat_min = -90
    lat_max = 90
    lon_min = 0
    lon_max = 360
    ice_vmin = 0
    ice_vmax = 1
    dust_vmin = 0
    dust_vmax = 1

    fig, ax = plt.subplots(4, 6, figsize=(12, 6))
    fig.suptitle(f'Ames visible dust optical depth (MY{ames_mars_year}, sol 364--369)')

    for lt in range(24):
        pcm = ax[lt // 6, lt % 6].pcolormesh(ames_x, ames_y, ames_dust[1, (lt+8) % 24], cmap='cividis', vmin=dust_vmin, vmax=dust_vmax)
        ax[lt // 6, lt % 6].set_xlim(lon_min, lon_max)
        ax[lt // 6, lt % 6].set_ylim(lat_min, lat_max)
        ax[lt // 6, lt % 6].set_xticks([])
        ax[lt // 6, lt % 6].set_yticks([])
    fig.colorbar(pcm, ax=ax[:, -1])
    plt.savefig(f'/media/kyle/iuvs/images/gcm/ames_dust_diurnal_evolution_simulation2-my{ames_mars_year}.png', dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(4, 6, figsize=(12, 6))
    fig.suptitle(f'Ames visible ice optical depth (MY{ames_mars_year}, sol 364--369)')

    for lt in range(24):
        pcm = ax[lt // 6, lt % 6].pcolormesh(ames_x, ames_y, ames_ice[1, (lt+8) % 24], cmap='viridis', vmin=ice_vmin, vmax=ice_vmax)
        ax[lt // 6, lt % 6].set_xlim(lon_min, lon_max)
        ax[lt // 6, lt % 6].set_ylim(lat_min, lat_max)
        ax[lt // 6, lt % 6].set_xticks([])
        ax[lt // 6, lt % 6].set_yticks([])
    fig.colorbar(pcm, ax=ax[:, -1])
    plt.savefig(f'/media/kyle/iuvs/images/gcm/ames_ice_diurnal_evolution_simulation2-my{ames_mars_year}.png', dpi=300)
    plt.close(fig)

    for pcm_mars_year in [33, 34, 35]:
        pcm = PlanetaryClimateModelSimulation(2, pcm_mars_year)

        pcm_dust = pcm.get_dust_ultraviolet_column_optical_depth()
        pcm_ice = pcm.get_ice_ultraviolet_column_optical_depth()

        pcm_x, pcm_y = np.meshgrid(pcm.get_longitude_edges(), pcm.get_latitude_edges())

        lat_min = -90
        lat_max = 90
        lon_min = 0
        lon_max = 360

        fig, ax = plt.subplots(4, 6, figsize=(12, 6))
        fig.suptitle(f'PCM UV dust optical depth (MY{pcm_mars_year}, sol 366)')

        for lt in range(24):
            pcm = ax[lt // 6, lt % 6].pcolormesh(pcm_x, pcm_y, pcm_dust[367, (lt+8) % 24], cmap='cividis', vmin=dust_vmin, vmax=dust_vmax)
            ax[lt // 6, lt % 6].set_xlim(lon_min, lon_max)
            ax[lt // 6, lt % 6].set_ylim(lat_min, lat_max)
            ax[lt // 6, lt % 6].set_xticks([])
            ax[lt // 6, lt % 6].set_yticks([])
        fig.colorbar(pcm, ax=ax[:, -1])
        plt.savefig(f'/media/kyle/iuvs/images/gcm/pcm_dust_diurnal_evolution_simulation2-my{pcm_mars_year}.png', dpi=300)
        plt.close(fig)

        fig, ax = plt.subplots(4, 6, figsize=(12, 6))
        fig.suptitle(f'PCM UV ice optical depth (MY{pcm_mars_year}, sol 366)')

        for lt in range(24):
            pcm = ax[lt // 6, lt % 6].pcolormesh(pcm_x, pcm_y, pcm_ice[366, (lt+8) % 24], cmap='viridis', vmin=ice_vmin, vmax=ice_vmax)
            ax[lt // 6, lt % 6].set_xlim(lon_min, lon_max)
            ax[lt // 6, lt % 6].set_ylim(lat_min, lat_max)
            ax[lt // 6, lt % 6].set_xticks([])
            ax[lt // 6, lt % 6].set_yticks([])
        fig.colorbar(pcm, ax=ax[:, -1])
        plt.savefig(f'/media/kyle/iuvs/images/gcm/pcm_ice_diurnal_evolution_simulation2-my{pcm_mars_year}.png', dpi=300)
        plt.close(fig)
