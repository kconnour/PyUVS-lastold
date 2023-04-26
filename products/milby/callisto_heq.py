import numpy as np

from products import graphics


arr = np.load('/home/kyle/Downloads/x207-to-plot.npy')
heq_arr = graphics.histogram_equalize_grayscale_image(arr).astype('int')
print(arr.shape, heq_arr.shape)
#np.save('/home/kyle/x207-to-plot-heq.npy', heq_arr)
