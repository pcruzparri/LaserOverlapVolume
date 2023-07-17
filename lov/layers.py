__all__ = ['Layers']


from laser import *
import numpy as np

class Layers:
    def __init__(self, lasers):
        self.lasers = lasers
        self.together = np.sum(lasers)

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
        
        aligned = new_layer.shift([0]+list(stitch1-stitch2))
        self.lasers[laser_index].arr3d = np.vstack((prev_arr, new_arr))

    def replace_layer(self):
        pass
    def check_continuity(self):
        pass  
