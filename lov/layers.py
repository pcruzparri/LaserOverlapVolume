__all__ = ['Layers']


from laser import *
import numpy as np
from functools import reduce

class Layers:
    def __init__(self, lasers):
        self.lasers = lasers
        assert not np.any(np.array([len(l.arr3d) for l in self.lasers]) != len(self.lasers[0].arr3d)),\
            'The initialization lasers are not of the same length.'
        self.depths = [len(self.lasers[0].arr3d)]
        self.overlaped = self.overlap()

    def add_layer(self, laser_index, depth, angles):
        prev_layers = self.lasers[laser_index]
        new_layer = Laser(prev_layers.size, 
                          prev_layers.fwhm,
                          initial_depth=depth, 
                          initial_angles=angles)
        prev_arr = prev_layers.arr3d
        new_arr = new_layer.arr3d
        stitch1 = np.ndarray.flatten(
            np.array(
                np.where(prev_arr[len(prev_arr)-1, :, :]==np.max(prev_arr[len(prev_arr)-1, :, :]))
                )
            )
        stitch2 = np.ndarray.flatten(
            np.array(
                np.where(new_arr[0, :, :]==np.max(new_arr[0, :, :]))
                )
            )
        new_layer.shift([0]+list(stitch1-stitch2))
        self.lasers[laser_index].arr3d = np.vstack((prev_arr, new_layer.arr3d))
        # TODO: need to align by similar intensity if max not on both, maybe...

    def overlap(self):
        return reduce(np.multiply, [l.arr3d for l in self.lasers])

    def replace_layer(self):
        pass
    def check_continuity(self):
        pass  
