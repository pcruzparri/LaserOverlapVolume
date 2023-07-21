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
        self.lasers[laser_index].append(new_layer)
        self.depths[laser_index].append(depth)
        self._stitch(laser_index, (-1, -2))
        #self.lasers[laser_index].arr3d = np.vstack((prev_arr, new_layer.arr3d))
        # TODO: need to align by similar intensity if max not on both, maybe...

    def add_laser(self, laser):
        self.lasers.append([laser])
        self.depths.append([laser.depth])

    def _stitch(self, laser_index, layer_indices):
        assert min(layer_indices)+1 == max(layer_indices) and len(layer_indices)==2, 'Layers are not continuous, ' \
                                                                                    'or too many layers provided'
        prev_arr = self.lasers[laser_index][min(layer_indices)].arr3d
        next_arr = self.lasers[laser_index][max(layer_indices)].arr3d
        stitch1 = np.ndarray.flatten(
            np.array(
                np.where(prev_arr[len(prev_arr) - 1, :, :] == np.max(prev_arr[len(prev_arr) - 1, :, :]))
            )
        )
        stitch2 = np.ndarray.flatten(
            np.array(
                np.where(next_arr[0, :, :] == np.max(next_arr[0, :, :]))
            )
        )
        coord_shift = list(stitch2 - stitch1) if layer_indices[0] < layer_indices[1] else list(stitch1 - stitch2)
        self.lasers[laser_index][layer_indices[0]].shift([0] + coord_shift)

    def set_focus(self, center):
        lasers_to_focus = []
        for laser in self.lasers:
            arr = np.vstack(list(map(lambda x: x.arr3d, laser)))
            arrmax = np.ndarray.flatten(
                np.array(
                    np.where(arr[center[0], :, :] == np.max(arr[center[0], :, :]))
                )
            )
            center = np.array(center)
            print(arrmax, center)
            coord_shift = list(arrmax - center[1:]) if arrmax[1] < center[1] else list(center[1:] - arrmax)

            for layer in laser:
                layer.shift([0] + coord_shift)

    def stack(self):
        return np.array([np.vstack(list(map(lambda x: x.arr3d, l))) for l in self.lasers])

    def layers_multiply(self):
        return reduce(np.multiply, self.stack())

    def layers_sum(self):
        return reduce(np.add, self.stack())

    def replace_layer(self, new_laser_layer, laser_index, layer_index):
        self.lasers[laser_index][layer_index] = new_laser_layer

    def check_continuity(self):
        pass  
