__all__ = ['Laser']

import numpy as np
from scipy.ndimage import rotate, shift as r, s
import warnings
from .utils import *


class Laser:
    def __init__(self, size, fwhm, center=None, initial_angles=(), initial_depth=0, amp=1, norm=False):
        self.size = size
        self.fwhm = fwhm
        self.center = center
        self.initial_angles = initial_angles
        self.initial_depth = initial_depth
        self.amp = amp
        self.norm = norm
        self.arr2d = makeGaussian(self.size, self.fwhm, center=self.center, amp=self.amp, norm=self.norm)
        if initial_depth:
            self.extend(initial_depth)
            if initial_angles:
                self.rotate(self.initial_angles)

    def extend(self, depth):
        self.arr3d = [self.arr2d]*depth

    def rotate(self, angles):
        for rot_ind, rot in enumerate(angles):
            self.arr3d = r(self.arr3d, rot, axes=(rot_ind, (rot_ind+1)%3), reshape=False, mode='nearest')

    def shift(self, deltas):
        self.arr3d = s(self.arr3d, deltas)