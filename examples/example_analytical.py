"""
Analytical examples
"""
import numpy as np
import matplotlib.pyplot as plt
import diplib as dip
import napari

from drift_correction.drift_correction import napari_widget, process

try:
    from utils import multi_dots
except ModuleNotFoundError:
    from examples.utils import multi_dots


def ex_staggered_dots(show_napari=False):
    """ Example of image stack alignment based on a staggered rows of dots """
    nx = ny = 512
    radius = 12
    space = 36
    nframes = 60
    np.random.seed(0)

    img0 = multi_dots(nx, ny, radius, space, staggered=True)

    arr = np.zeros((nframes, ny, nx))
    for k in range(nframes):
        shift = k * np.array([3., 1.])
        shift += np.random.uniform(low=-2.0, high=2.0, size=2)
        print(shift)
        img = dip.Shift(img0, shift, interpolationMethod='linear')
        img += 0.75 * (2. * np.random.random(img0.shape) - 1.)
        img = np.clip(img, a_min=0, a_max=1)
        arr[k] = img

    if show_napari:

        viewer = napari.Viewer()
        layer = viewer.add_image(arr, name='Image Stack')
        widget = napari_widget()
        widget.input_stack.value = layer
        viewer.window.add_dock_widget(widget, area="right")
        result = widget()
        result.colormap = 'green'
        napari.run()

        plt.show()  # plot shifts.png and shifts_cumul.png once napari is closed

    else:
        arr_aligned, shifts, shifts_cumul = process(arr)
        print()
        print(shifts)
        print(shifts_cumul)
        return arr_aligned, shifts, shifts_cumul


if __name__ == "__main__":
    ex_staggered_dots(show_napari=False)
