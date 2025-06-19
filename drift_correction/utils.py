"""
Utilities functions
"""
import re
from pathlib import Path
import numpy as np
import tifffile
import dm3_lib as dm3
import matplotlib.pyplot as plt


def get_reader(path):
    """ Return reader for 'tif' or 'dm' file """
    if isinstance(path, str):
        if path.endswith(('.tif', '.tiff')):
            return read_tif
        elif path.endswith(('.dm3', '.dm4')):
            return read_dm
    return None


def read_tif(fname):
    """ Return arr and name from a .tif file """
    with tifffile.TiffFile(fname) as tif:
        arr = np.array([page.asarray() for i, page in enumerate(tif.pages)])
        return [(arr.astype(np.float32), {"name": Path(fname).name})]


def read_dm(fname):
    """ Return arr and name from a .dm file """
    arr = dm3.DM3(fname).imagedata
    return [(arr.astype(np.float32), {"name": Path(fname).name})]


def plot(values, fname):
    """ Plot and save shifts 'values' in a 'fname' figure file """
    _, ax = plt.subplots()
    ax.plot(values[:, 0], label="transl_x")
    ax.plot(values[:, 1], label="transl_y")
    ax.set_xlabel('# Frames')
    ax.legend()
    plt.savefig(fname)


def save_and_plot(dirname, shifts, shifts_cumul):
    """ Plot and save 'shifts' and 'shifts_cumul' """
    plot(shifts, dirname / "shifts.png")
    plot(shifts_cumul, dirname / "shifts_cumul.png")
    np.savetxt(dirname / "shifts.txt", shifts)
    np.savetxt(dirname / "shifts_cumul.txt", shifts_cumul)


def hsorted(list_):
    """ Sort the given list in the way that humans expect """
    list_ = [str(x) for x in list_]
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list_, key=alphanum_key)

