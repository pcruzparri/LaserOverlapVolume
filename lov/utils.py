__all__=['makeGaussian', 'clipped_arr', 'get_plane_overlap']

import numpy as np

@np.vectorize
def makeGaussian(size, fwhm=3, center=None, amp=1, norm=False):
    def gaussian():
        """Note: Copied without modification from StackOverflow user giessel.

        Make a square gaussian kernel.

        size is the length of a side of the square
        fwhm is full-width-half-maximum, which
        can be thought of as an effective radius.
        """
        x = np.arange(0, size, 1, float)
        y = x[:, np.newaxis]

        if center is None:
            x0 = y0 = size // 2
        else:
            x0 = center[0]
            y0 = center[1]

        return np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)

    g = gaussian()
    if norm:
        return amp * g / np.sum(g)
    else:
        return g


def clipped_arr(arr, thresh=0.5):
    return np.array(np.where(arr > thresh)).T


def get_plane_overlap(arr1, arr2, thresh=0.5, clip=(0, 20), return_points=False):
    '''Get overlap points of two 3D arrays along a plane.
    '''
    # Combine both arrays and get the counted unique elements.
    total = np.unique(np.concatenate((clipped_arr(arr1, thresh=thresh), (clipped_arr(arr2, thresh=thresh))), axis=0),
                    return_counts=True, axis=0)

    # Get items with counts greater than 1 as the overlap points.
    p1_arr = np.array([i for i in total[0][np.where(total[1] > 1)] if i[0] == clip[0]])
    p2_arr = np.array([i for i in total[0][np.where(total[1] > 1)] if i[0] == clip[1]])

    if return_points:
        return p1_arr, p2_arr  # point locations in 3D matrix on two planes of the box along an axis
    else:
        return p1_arr.size  # Due to symmetry, only get the size overlapping point list on one of the planes.