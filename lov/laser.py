__all__ = ['Laser']

import numpy as np
from scipy.ndimage import rotate as r, shift as s
import warnings
from utils import *


class Laser:
    def __init__(self, size, fwhm, center=None, initial_angles=(), initial_depth=0, initial_shifts=(), **kwargs):
        self.size = size
        self.fwhm = fwhm
        self.center = center
        self.angles = initial_angles if initial_angles else (0, 0, 0)
        self.depth = initial_depth if initial_depth else 1
        self.shifts = initial_shifts if initial_shifts else (0, 0, 0)
        self.arr3d = None
        self.make3d(self.depth, **kwargs)

    def get_arr3d(self):
        return self.arr3d

    def make3d(self, depth, **kwargs):
        self.depth = depth
        self.arr3d = np.array([makeGaussian(self.size, self.fwhm, self.center, **kwargs)]*depth)
        self.rotate(self.angles)
        self.shift(self.shifts)

    def rotate(self, angles):
        self.angles = angles
        for rot_ind, rot in enumerate(self.angles):
            self.arr3d = r(self.arr3d, rot, axes=(rot_ind, (rot_ind+1)%3), reshape=False, mode='nearest')

    def shift(self, shifts):
        self.shifts = shifts
        self.arr3d = s(self.arr3d, shifts)

    