import numpy as np
import matplotlib.pyplot as plt


from pyvista import Plotter
from laser import *
from layers import *


# Laser setup
l1_fwhm = 20
l2_fwhm = 20
l3_fwhm = 20
size = 100
layer1_depth = 50

l1 = Laser(size=size,
           fwhm=l1_fwhm,
           initial_depth=layer1_depth,
           initial_angles=[30, 0, 0],
           initial_shifts=(0, -40, 0))
l2 = Laser(size=size,
           fwhm=l2_fwhm,
           initial_depth=layer1_depth,
           initial_angles=[-15, 0, 0],
           initial_shifts=[0, 40, 0])
lasers = [l1, l2]


# Layers setup
layer2_depth = 100
layer3_depth = 100
layers = Layers(lasers=lasers)
layers.add_layer(0, layer2_depth, (10, 0, 0))
layers.add_layer(0, layer3_depth, (30, 0, 0))
layers.add_layer(1, layer2_depth, (-5, 0, 0))
layers.add_layer(1, layer3_depth, (-15, 0, 0))

# Add new laser and its layers
'''l3 = Laser(size=size,
           fwhm=l2_fwhm,
           initial_depth=layer1_depth,
           initial_angles=[0, 0, 0],
           initial_shifts=[0, 0, 0])
layers.add_laser(l3),
layers.add_layer(2, layer2_depth, (0, 0, 0))
layers.add_layer(2, layer3_depth, (0, 0, 0))'''

sum_out = layers.layers_sum()
layers.set_focus((130, size//2, size//2))
print('overlap volume' + np.sum(layers.layers_multiply())

opacity = [0,0.5,1,1]
plotter = Plotter(shape=(1, 2))
plotter.set_background('gray')
plotter.subplot(0, 0)
plotter.add_volume(np.where(sum_out >= 1, 1, sum_out),
                   cmap='Greens',
                   blending='maximum',
                   opacity=opacity)
plotter.show_grid()

layers.set_focus((150, size//2, size//2))
plotter.subplot(0, 1)
plotter.add_volume(layers.layers_sum(),
                   cmap='Greens',
                   blending='maximum',
                   opacity=opacity)
#plotter.add_volume_clip_plane(p)
plotter.show_grid()
plotter.show()

