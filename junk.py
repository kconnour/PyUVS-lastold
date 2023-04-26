from pathlib import Path
from astropy.io import fits
from h5py import File
import numpy as np
import matplotlib.pyplot as plt


files = sorted(Path('/media/kyle/iuvs/production/orbit17300/').glob('*apoapse*orbit17300*muv*.gz'))
print(len(files))
for f in files:
    print(f)
    hdul = fits.open(f)

raise SystemExit(9)

f = File('/media/kyle/iuvs/data/orbit04400/orbit04465.hdf5')
sn = f['apoapse/integration/swath_number'][:]
ma = f['apoapse/integration/mirror_angle'][:]
dayside = f['apoapse/muv/integration/dayside_integrations'][:]
good_ints = np.logical_and(dayside, sn==0)
mask = good_ints[dayside]

br = f['apoapse/muv/dayside/detector/brightness'][mask]

fig, ax = plt.subplots()
ax.imshow(br[..., -1])
plt.savefig('/home/kyle/br.png')
