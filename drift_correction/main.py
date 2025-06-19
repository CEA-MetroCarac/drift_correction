"""
Main functions dedicated to the drift correction processing
"""
import sys
from pathlib import Path
import time
import numpy as np
import diplib as dip
from tifffile import imread, imwrite

from drift_correction.utils import WorkingDirectory, hsorted, plot


def process_3d_array(arr3d, working_dir=None,
                     ind_min=0, ind_max=9999, pbar_update=None):
    """
    Drift correction processing from a given stack (3D-array)

    Parameters
    ----------
    arr3d: numpy.ndarray((nframes, ny, nx))
        Image stack to handle
    working_dir: str, optional
        Dirname related to the working directory where the images stack is split into individual
        frames before processing. If None, create a temporarily directory
    ind_min: int, optional
        Index related to the first frame to handle
    ind_max: int, optional
        Index related to the last frame to handle
    pbar_update: fun, optional
        Progress bar function with arguments that consist in the current index and
        the total number of images to process ('nframes')

    Returns
    -------
    arr_aligned: numpy.ndarray((nframes, my, mx))
        The aligned and cropped image stack. (The cropping area is related to the 'valid' one)
    shifts: numpy.ndarray((ntot, 2))
        Shifts (translations) calculated between 2 successive frames (tx, ty)
    shifts_cumul: numpy.ndarray((nframes, 2))
        Cumulative shifts (tx, ty)
    """
    assert arr3d.ndim == 3

    with WorkingDirectory(dirname=working_dir) as working_dir:
        dirname = working_dir / "images"
        dirname.mkdir(parents=True, exist_ok=True)

        [fname.unlink() for fname in dirname.glob("img*.tif")]

        for i, img in enumerate(arr3d):
            imwrite(dirname / f"img_{i:04d}.tif", img)

        return process_dirname(dirname, ind_min=ind_min, ind_max=ind_max, pbar_update=pbar_update)


def process_dirname(dirname, ind_min=0, ind_max=9999, pbar_update=None):
    """
    Drift correction processing '.tif' images located in a directory named 'dirname_img'

    Parameters
    ----------
    dirname: str or Path
        Pathname of the directory where the .tif images are located
    ind_min: int, optional
        Index related to the first frame to handle
    ind_max: int, optional
        Index related to the last frame to handle
    pbar_update: fun, optional
        Progress bar function with arguments that consist in the current index and
        the total number of images to process ('ntot')

    Returns
    -------
    arr_aligned: numpy.ndarray((ntot, my, mx))
        The aligned and cropped image stack. (The cropping area is related to the 'valid' one)
    shifts: numpy.ndarray((ntot, 2))
        Shifts (translations) calculated between 2 successive frames (tx, ty)
    shifts_cumul: numpy.ndarray((ntot, 2))
        Cumulative shifts (tx, ty)
    """
    fnames = hsorted(dirname.glob('*.tif'))[ind_min:ind_max + 1]
    if len(fnames) == 0:
        return

    shape = imread(fnames[0]).shape
    arr_aligned = np.zeros((len(fnames), shape[0], shape[1]))

    shifts = []
    for k, fname in enumerate(fnames):
        img_ = imread(fname)
        img = dip.ImageRead(str(fname))

        if k > 0:

            # shift calculation
            shift = np.asarray(dip.FindShift(ref, img))
            shift_cumul += shift

            # cumulative shift application
            img_reg = dip.Shift(img, -shift_cumul, interpolationMethod='linear')
            arr_aligned[k] = np.asarray(img_reg)

        else:

            shift = np.array([0., 0.])
            shift_cumul = np.array([0., 0.])
            arr_aligned[0] = np.asarray(img)

        ref = img
        shifts.append(shift)
        pbar_stdout_update(k, len(fnames))
        if pbar_update:
            pbar_update(k, len(fnames))

    shifts = np.asarray(shifts)
    shifts_cumul = np.cumsum(shifts, axis=0)

    # 'valid' area determination
    dx, dy = shifts_cumul[:, 0], shifts_cumul[:, 1]
    imin = max(0, -int(np.ceil(dy.min())))
    imax = min(shape[0], shape[0] - int(np.floor(dy.max())))
    jmin = max(0, -int(np.ceil(dx.min())))
    jmax = min(shape[1], shape[1] - int(np.floor(dx.max())))

    arr_aligned = arr_aligned[:, imin:imax, jmin:jmax]

    return arr_aligned, shifts, shifts_cumul


def pbar_stdout_update(k, ntot):
    """ Progress Bar evolution written in the console """

    global t0
    if k == 0:
        t0 = time.time()

    pbar = "\r[{:50}] {:.0f}% {:.0f}/{} {:.2f}s"
    percent = 100 * (k + 1) / ntot
    cursor = "*" * int(percent / 2)
    exec_time = time.time() - t0
    sys.stdout.write(pbar.format(cursor, percent, k + 1, ntot, exec_time))
    if k == ntot:
        print()
