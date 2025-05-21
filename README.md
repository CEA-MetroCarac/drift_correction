<p align="center" width="100%">
    <img align="center" width=250 src=./resources/logo.png>
</p>

This tool is dedicated to easily realign frames of a stack images using napari as a viewer and diplib for shift calculation.

Input format are ``.tif``, .``dm3``/``.dm4``, ``.npy`` or any other format supported by napari.

The saving of the realigned stack is obtained from the napari files widget at .tif format.

Extra files that display the performed correction frame by frame and the cumulative one can also be saved

<p align="center" width="100%">
    <img align="center" src="./resources/drift_correction.gif">
</p>
<p align="center" width="100%">
    <img align="center" width="45%" src="./resources/shifts.png">
    <img align="center" width="45%" src="./resources/shifts_cumulative.png">
</p>
<p align="center">
    <em>Illustration of the drift correction processing on a analytical test case (above) and the  corresponding calculated shifts frame by frame (bottom left) and cumulative one (bottom right).</em>
</p>

## Installation and launching

```bash
pip install git+https://github.com/CEA-MetroCarac/drift_correction.git
drift_correction
```

## Scripting mode

The drift correction can be performed using python scripting (without the napari GUI), considering a 3D array for 'arr', as::

    from drift_correction.drift_correction import process

    arr_aligned, shifts, shifts_cumul = process(arr,
                                                ind_min=0, ind_max=9999, pbar_update=None,
                                                dirname=None, fname_aligned=None, working_dir=None)

See the (example_analytical.py)(./examples/example_analytical.py) for a demo and the docstring for more details about the arguments of the function. 