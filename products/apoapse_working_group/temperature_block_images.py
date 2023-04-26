from pathlib import Path

from h5py import File
import matplotlib.pyplot as plt
import numpy as np

import pyuvs as pu


viridis = plt.get_cmap('viridis')


def make_temperature_block_plot(data_block: int) -> None:
    fig, axes = plt.subplots(10, 10, figsize=(25, 15))

    axes[9, 0].set_xlabel('Ephemeris time')
    axes[9, 0].set_ylabel('Detector temperature [degrees C]')

    def fill_subplot_with_image(orbit: int):
        print(orbit)
        orbit_block = pu.orbit.make_orbit_block(orbit)
        orbit_code = pu.orbit.make_orbit_code(orbit)
        floor = pu.orbit.make_orbit_floor(orbit)

        ax = axes[int(orbit//10 - floor/10), orbit % 10]

        file = File(f'/media/kyle/iuvs/data/{orbit_block}/{orbit_code}.hdf5')
        et = file['apoapse/integration/ephemeris_time'][:]
        temperature = file['apoapse/muv/integration/detector_temperature'][:]

        points = np.linspace(0, 1, num=temperature.shape[0])
        color = [viridis(f) for f in points]

        ax.scatter(et, temperature, color=color)

        ax.set_ylim(-25, -18)
        ax.set_xticks([])
        ax.set_title(f'{orbit}', pad=0)

    for orb in range(data_block, data_block + 100):
        fill_subplot_with_image(orb)

    filename = f'{pu.orbit.make_orbit_block(data_block)}-temperatures.png'
    plt.savefig(save_location / filename, dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    save_location = Path('/media/kyle/iuvs/apoapse-working-group/')
    for i in range(3000, 17000, 100):
        make_temperature_block_plot(i)
