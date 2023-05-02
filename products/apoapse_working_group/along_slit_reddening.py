from pathlib import Path

from h5py import File
import numpy as np
import matplotlib.pyplot as plt

import pyuvs as pu


rainbow = plt.get_cmap('rainbow')
points = np.linspace(0, 1, num=15)
color = [rainbow(f) for f in points]


def plot_along_slit_reddening(orbit: int) -> None:
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    f = File(file_path / orbit_block / f'{orbit_code}.hdf5')

    dayside = f['apoapse/muv/integration/dayside_integrations'][:]
    opportunity_swaths = f['apoapse/integration/opportunity_classification'][:]
    dayside_science_integrations = np.logical_and(dayside, ~opportunity_swaths)

    if np.sum(dayside_science_integrations) == 0:
        return

    brightness = f['apoapse/muv/dayside/detector/brightness'][~opportunity_swaths[dayside]]
    swath_number = f['apoapse/integration/swath_number'][:][dayside_science_integrations]
    app_flip = f['apoapse/instrument_geometry/app_flip'][0]

    if brightness.shape[2] not in [15, 19, 20]:
        return
    if brightness.shape[2] in [19, 20]:
        brightness = brightness[..., 1:16]

    fig, axes = plt.subplots(1, len(np.unique(swath_number)))

    for c, sn in enumerate(np.unique(swath_number)):
        ax = axes[c]

        kr = brightness[swath_number == sn]
        n_integrations = kr.shape[0]
        kr = kr[int(n_integrations*0.25):int(n_integrations*0.75), ...]
        average_spectrum = np.mean(np.mean(kr, axis=0), axis=0)

        along_slit_spectrum = np.mean(kr / average_spectrum, axis=0)

        slit = np.arange(kr.shape[1]) + 0.5 if not app_flip else np.linspace(kr.shape[1]-1, 0, num=kr.shape[1]) + 0.5
        for wavelength in range(15):
            ax.plot(slit, along_slit_spectrum[:, wavelength], color=color[wavelength])

        ax.set_ylim(0.5, 1.5)

    plt.savefig(save_location / f'{orbit_code}.png')
    plt.close(fig)


if __name__ == '__main__':
    file_path = Path('/media/kyle/iuvs/data/')
    save_location = Path('/media/kyle/iuvs/apoapse-working-group/along_slit_colors')

    for orb in range(11200, 11300):
        print(orb)
        plot_along_slit_reddening(orb)
