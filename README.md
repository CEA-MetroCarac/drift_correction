<p align="center" width="100%">
    <img align="center" width=300 src=./resources/logo.png>
</p>

**Drift-correction** is an application designed to easily realign frames in image stacks, using [Napari](https://napari.org/) as the viewer and the [DIPlib](https://diplib.org/) library for shift calculation.

Supported input formats include ``.tif``, .``dm3``/``.dm4``, ``.npy`` and any other format compatible with Napari.

Additional files showing the frame-by-frame and cumulative shifts can be saved in the same directory as the input file.

The realigned stack can be saved via the Napari **Files** tab.


<p align="center" width="100%">
    <img align="center" src="./resources/drift_correction.gif">
</p>
<p align="center">
    <em>Illustration of drift correction on a synthetic test case — the uncorrected stack is shown in gray, and the corrected (cropped) version in green.</em>
</p>

<p align="center" width="100%">
    <img align="center" width="45%" src="./resources/shifts.png">
    <img align="center" width="45%" src="./resources/shifts_cumul.png">
</p>
<p align="center">
    <em>The corresponding frame-by-frame (left) and cumulative (right) shifts.</em>
</p>

## Installation and launching

For a simple install (drift-correction via python scripting only):

```bash
pip install git+https://github.com/CEA-MetroCarac/drift_correction.git
```

For an install with the napari-GUI:

```bash
pip install git+https://github.com/CEA-MetroCarac/drift_correction.git#egg=drift_correction[napari]
pip install PyQt5     # or PyQt6, PySide2, PySide6, if no Qt backend have been already installed in your env.
drift-correction
```

## Scripting mode

Drift correction can also be performed via Python scripting (without the Napari GUI), by passing a 3D array ``arr3d`` or a ``dirname`` to the dedicated functions as shown in:

```bash
from drift_correction import process_array, process_dirname

arr_aligned, shifts, shifts_cumul = process_3d_array(arr3d, ind_min=0, ind_max=9999)
arr_aligned, shifts, shifts_cumul = process_dirname(dirname, ind_min=0, ind_max=9999)
```

See [example_analytical.py](./examples/example_analytical.py) for a demonstration and refer to the docstrings [process_3d_array()](./drift_correction/main.py#L14-L42) and [process_dirname()](./drift_correction/main.py#L57-L81) for more details on the arguments to be passed to the functions.

## Acknowledgements

This work, carried out at **CEA-PFNC** (Platform for Nanocharacterisation), was supported by the “Recherche Technologique de Base” program of the French National Research Agency (ANR).