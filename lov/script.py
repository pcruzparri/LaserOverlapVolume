import numpy as np
import matplotlib.pyplot as plt


from pyvista import Plotter
from laser import *
from layers import *


# Laser setup
l1_size = 200
l1_fwhm = 20
l1_id = 100


l1 = Laser(size=l1_size, fwhm=l1_fwhm, initial_depth=l1_id)
lasers = [l1]


# Layers setup

layers = Layers(lasers=lasers)
layers.add_layer(0, 200, (-15, 0, 0))
layers.add_layer(0, 100, (15, 0, 30))


plotter = Plotter()
plotter.add_mesh(layers.lasers[0].arr3d[:, :, :l1_size//2])
plotter.show_grid()
plotter.show()
