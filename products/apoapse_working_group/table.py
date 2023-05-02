import numpy as np
import pandas as pd
from h5py import File
import pyuvs as pu

start_orbit = 3000
end_orbit = 17000

n_orbits = end_orbit - start_orbit


orbits = np.arange(n_orbits) + start_orbit

app = np.empty((n_orbits,))
spatial_binning = np.empty((n_orbits,))
spectral_binning = np.empty((n_orbits,))
int_time = np.empty((n_orbits,))
mcp_volt = np.empty((n_orbits,))
mcp_gain = np.empty((n_orbits,))
temperature_mean = np.empty((n_orbits,))
#temperature_range = np.empty((n_orbits,))
temperature_min = np.empty((n_orbits,))
temperature_max = np.empty((n_orbits,))


for c, orbit in enumerate(range(start_orbit, end_orbit)):
    print(orbit)
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    file = File(f'/media/kyle/iuvs/data/{orbit_block}/{orbit_code}.hdf5')
    try:
        app[c] = file['apoapse/instrument_geometry/app_flip'][0]
    except IndexError:
        app[c] = np.nan

    try:
        spatial_binning[c] = file['apoapse/muv/dayside/detector/raw'][:].shape[1]
    except IndexError:
        spatial_binning[c] = np.nan

    try:
        spectral_binning[c] = file['apoapse/muv/dayside/detector/raw'][:].shape[2]
    except IndexError:
        spectral_binning[c] = np.nan

    try:
        int_time[c] = file['apoapse/integration/integration_time'][:][0]
    except IndexError:
        int_time[c] = np.nan

    try:
        mcp_volt[c] = file['apoapse/muv/integration/mcp_voltage'][:][0]
    except IndexError:
        mcp_volt[c] = np.nan

    try:
        mcp_gain[c] = file['apoapse/muv/integration/mcp_voltage_gain'][:][0]
    except IndexError:
        mcp_gain[c] = np.nan

    try:
        t = file['apoapse/muv/integration/detector_temperature'][:]
        temperature_mean[c] = np.mean(t)
    except:
        temperature_mean[c] = np.nan

    '''try:
        t = file['apoapse/muv/integration/detector_temperature'][:]
        temperature_range[c] = np.ptp(t)
    except:
        temperature_range[c] = np.nan'''

    try:
        t = file['apoapse/muv/integration/detector_temperature'][:]
        temperature_min[c] = np.nanmin(t)
    except:
        temperature_min[c] = np.nan

    try:
        t = file['apoapse/muv/integration/detector_temperature'][:]
        temperature_max[c] = np.nanmax(t)
    except:
        temperature_max[c] = np.nan


data = {'Orbit': orbits,
        'APP flip': app,
        'Spatial binning': spatial_binning,
        'Spectral binning': spectral_binning,
        'Integration time': int_time,
        'MCP voltage': mcp_volt,
        'MCP gain': mcp_gain,
        'MUV detector temperature mean': temperature_mean,
        #'Temperature range': temperature_range
        'MUV detector temperature max': temperature_max,
        'MUV detector temperature min': temperature_min
        }


df = pd.DataFrame(data)

df.to_csv('/media/kyle/iuvs/apoapse-working-group/reddening-table.csv', index=False)
