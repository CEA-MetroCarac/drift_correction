"""
Utilities functions
"""
from pathlib import Path
import numpy as np
import tifffile
import dm3_lib as dm3
import matplotlib.pyplot as plt
from qtpy.QtWidgets import QMessageBox


def error(message):
    """
    Shows a pop up with the given error message.
    """
    e = QMessageBox()
    print("ERROR: ", message)
    e.setText(message)
    e.setIcon(QMessageBox.Critical)
    e.setWindowTitle("Error")
    e.show()
    return e


def get_reader(fname):
    """ Return reader for 'tif' or 'dm' file """
    if isinstance(fname, str):
        if fname.endswith(('.tif', '.tiff')):
            return read_tif
        elif fname.endswith(('.dm3', '.dm4')):
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
