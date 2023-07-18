import numpy as np
import matplotlib.pyplot as plt


from pyvista import Plotter
from laser import *
from layers import *


# Laser setup
l1_fwhm = 20
l2_fwhm = 20
size = 200
initial_depth = 100

l1 = Laser(size=size,
           fwhm=l1_fwhm,
           initial_depth=initial_depth,
           initial_angles=[30, 0, 0],
           initial_shifts=(0, -50, 0))
l2 = Laser(size=size,
           fwhm=l2_fwhm,
           initial_depth=initial_depth,
           initial_angles=[-30, 0, 0],
           initial_shifts=[0, 50, 0])
lasers = [l1, l2]


# Layers setup

layers = Layers(lasers=lasers)
layers.add_layer(0, 200, (15, 0, 0))
layers.add_layer(0, 100, (25, 0, 0))
layers.add_layer(1, 200, (-15, 0, 0))
layers.add_layer(1, 100, (-25, 0, 0))


plotter = Plotter()
plotter.add_volume(layers.lasers[0].arr3d, cmap='Reds')
plotter.add_volume(layers.lasers[1].arr3d, cmap='Blues')
plotter.show_grid()
plotter.show()
