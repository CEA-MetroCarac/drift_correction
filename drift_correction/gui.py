"""
Main functions dedicated to the drift correction processing
"""
from pathlib import Path
import diplib  # VERY IMPORTANT !!! diplib import BEFORE napari is mandatory
import napari
from magicgui import magic_factory

from qtpy.QtWidgets import QProgressBar, QApplication

from drift_correction import process_3d_array
from drift_correction.utils import save_and_plot


def on_init(widget):
    """ Drift_correction widget initialization """
    widget.native.setStyleSheet("QWidget{font-size: 12pt;}")
    # widget.native.layout().addStretch()

    global widget_
    widget_ = widget

    widget._progress_bar = QProgressBar()
    widget._progress_bar.setValue(0)
    widget.native.layout().addWidget(widget._progress_bar)


@magic_factory(widget_init=on_init, layout='vertical',
               save_tmat={"widget_type": "CheckBox", "label": "plot and save shifts"},
               call_button="ALIGN FRAMES")
def napari_widget(input_stack: 'napari.layers.Image',
                  index_min: int = 0, index_max: int = 9999,
                  save_tmat: bool = True) -> 'napari.layers.Image':
    """ Drift_correction widget in Napari """

    global widget_
    widget = widget_

    def pbar_update(k, ntot):
        widget._progress_bar.setValue(int(100 * (k + 1) / ntot))
        QApplication.processEvents()

    arr_aligned, shifts, shifts_cumul = process_3d_array(input_stack.data,
                                                         ind_min=index_min, ind_max=index_max,
                                                         pbar_update=pbar_update)

    if save_tmat:
        if hasattr(input_stack, 'source') and input_stack.source.path is not None:
            dirname = Path(input_stack.source.path).parent
        else:
            dirname = Path.cwd()
        save_and_plot(dirname, shifts, shifts_cumul)

    return napari.layers.Image(arr_aligned, name=input_stack.name + " ALIGNED")


def launch():
    """ Launch Napari with the 'drift_correction' pluggin """
    viewer = napari.Viewer()
    viewer.window.add_dock_widget(napari_widget(), area="right")
    napari.run()


if __name__ == "__main__":
    launch()
