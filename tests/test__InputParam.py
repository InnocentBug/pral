import numpy as np
import pytest

import pral


def test_default_constructor():
    instance = pral.InputParam()
    assert instance.N_diblock == 64
    assert instance.f_diblock == 8 / 64
    assert instance.N_homo == 6
    assert instance.chi_AB == 40.0
    assert instance.chi_AC == 2.0
    assert instance.chi_BC == 30.0
    assert instance.kappa == 50.0
    assert instance.homo_concentration == 0.02
    assert instance.external_field_A == -1.0
    assert instance.external_field_B == 0.0
    assert instance.external_field_C == 1.0


def test_manual_constructor():
    instance = pral.InputParam(32, 0.4, 4, 30.0, 10.5, 25, 40, 0.01, -2.0, 0.4, 2.1)
    assert instance.N_diblock == 32
    assert instance.f_diblock == 0.4
    assert instance.N_homo == 4
    assert instance.chi_AB == 30.0
    assert instance.chi_AC == 10.5
    assert instance.chi_BC == 25.0
    assert instance.kappa == 40.0
    assert instance.homo_concentration == 0.01
    assert instance.external_field_A == -2.0
    assert instance.external_field_B == 0.4
    assert instance.external_field_C == 2.1


def test_from_numpy():
    instance = pral.InputParam.from_numpy(
        np.asarray([32, 0.4, 4, 30.0, 10.5, 25, 40, 0.01, -2.0, 0.4, 2.1])
    )
    assert instance.N_diblock == 32
    assert instance.f_diblock == 0.4
    assert instance.N_homo == 4
    assert instance.chi_AB == 30.0
    assert instance.chi_AC == 10.5
    assert instance.chi_BC == 25.0
    assert instance.kappa == 40.0
    assert instance.homo_concentration == 0.01
    assert instance.external_field_A == -2.0
    assert instance.external_field_B == 0.4
    assert instance.external_field_C == 2.1


def test_to_numpy():
    array = np.asarray([32, 0.4, 4, 30.0, 10.5, 25, 40, 0.01, -2.0, 0.4, 2.1])
    instance = pral.InputParam.from_numpy(array)
    array2 = instance.to_numpy()
    assert np.all(array == array2)


def test_range_check():
    with pytest.raises(pral.ParameterRangeException):
        instance = pral.InputParam(N_diblock=10)

    with pytest.raises(pral.ParameterRangeException):
        instance = pral.InputParam(N_diblock=5000)
