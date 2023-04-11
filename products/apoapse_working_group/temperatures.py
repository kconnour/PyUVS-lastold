import numpy as np
import matplotlib.pyplot as plt
from h5py import File
import pyuvs as pu


viridis = plt.get_cmap('viridis')


def make_block_plot(block: int) -> None:
    fig, ax = plt.subplots()
    ob = pu.orbit.make_orbit_code(block)

    for orbit in range(block, block+100):
        print(orbit)
        orbit_block = pu.orbit.make_orbit_block(orbit)
        orbit_code = pu.orbit.make_orbit_code(orbit)

        file = File(f'/media/kyle/iuvs/data/{orbit_block}/{orbit_code}.hdf5')
        temperature = file['apoapse/muv/integration/detector_temperature'][:]

        orbs = np.ones(temperature.shape) * orbit

        points = np.linspace(0, 1, num=temperature.shape[0])
        color = [viridis(f) for f in points]

        ax.scatter(orbs, temperature, color=color)

    ax.set_xlim(block, block+100)
    ax.set_ylim(-25, -18)
    ax.set_xlabel('Orbit number')
    ax.set_ylabel('Detector temperature [degrees C]')
    plt.savefig(f'/media/kyle/iuvs/apoapse-working-group/temperature-{ob}.png')


for i in range(3000, 17000, 100):
    make_block_plot(i)
