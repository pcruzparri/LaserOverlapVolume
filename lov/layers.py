__all__ = ['Layers']


from laser import *
import numpy as np
from functools import reduce


class Layers:
    def __init__(self, lasers):
        self.lasers = [[l] for l in lasers]
        """assert not np.any(np.array([len(l.arr3d) for l in self.lasers]) != len(self.lasers[0].arr3d)),\
            'The initialization lasers are not of the same length.'"""
        self.depths = [[li.depth for li in lj] for lj in self.lasers]

    def add_layer(self, laser_index, depth, angles):
        prev_layer = self.lasers[laser_index][-1]
        new_layer = Laser(prev_layer.size,
                          prev_layer.fwhm,
                          initial_depth=depth, 
                          initial_angles=angles)
        prev_arr = prev_layer.arr3d
        new_arr = new_layer.arr3d
        stitch1 = np.ndarray.flatten(
            np.array(
                np.where(prev_arr[len(prev_arr)-1, :, :] == np.max(prev_arr[len(prev_arr)-1, :, :]))
                )
            )
        stitch2 = np.ndarray.flatten(
            np.array(
                np.where(new_arr[0, :, :] == np.max(new_arr[0, :, :]))
                )
            )
        new_layer.shift([0]+list(stitch1-stitch2))
        self.lasers[laser_index].append(new_layer)
        #self.lasers[laser_index].arr3d = np.vstack((prev_arr, new_layer.arr3d))
        # TODO: need to align by similar intensity if max not on both, maybe...

    def stack(self):
        return np.array([np.vstack(list(map(lambda x: x.arr3d, l))) for l in self.lasers])

    def layers_multiply(self):
        return reduce(np.multiply, self.stack())

    def layers_sum(self):
        return reduce(np.add, self.stack())

    def replace_layer(self, laser_index, layer_index):
        pass
    def check_continuity(self):
        pass  
