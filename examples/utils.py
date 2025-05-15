"""
utilities functions dedicated to examples
"""
import numpy as np


def multi_dots(nx, ny, radius, space, staggered=False):
    """
    Create an image with a matrix of dots

    Parameters
    ----------
    nx, ny: ints
        Size of the image in x and y direction respectively
    radius: int or float
        Radius of the dots (in px)
    space: int
        Space between rows/cols (in px)
    staggered: bool, optional
        Activation key to consider staggered matrix of dots

    Returns
    -------
    img: numpy.ndarray((nx, ny))
        Resulting image
    """
    x0 = np.arange(nx)
    y0 = np.arange(ny)
    x, y = np.meshgrid(x0, y0)
    img = np.zeros_like(x, dtype=float)
    per = 2 * radius + space
    half_per = 0.5 * per
    mask = ((x % per - half_per) ** 2 + (y % per - half_per) ** 2) < radius ** 2
    if staggered:
        x = x + half_per
        y = y + half_per
        mask += ((x % per - half_per) ** 2
                 + (y % per - half_per) ** 2) < radius ** 2
    img[mask] = 1.
    return img
