import numpy as np
import pytest

from examples.example_analytical import ex_staggered_dots


def test_staggered_dots():
    _, _, shifts_cumul = ex_staggered_dots()

    assert shifts_cumul[-1] == pytest.approx(np.array([175.60457583, 56.7499515]))
