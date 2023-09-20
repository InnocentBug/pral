import pral


def test__InputParamConstr():
    instance = pral._InputParam()
    assert instance.N_diblock == 64
    assert instance.f_diblock == 8 / 64
    assert instance.N_homo == 6
    assert instance.chi_AB == 40.0
    assert instance.chi_AC == 2.0
    assert instance.chi_BC == 30.0
    assert instance.kappa == 50.0
    assert instance.homo_concentration == 0.02
    assert instance.external_field_A == -1.0
    assert instance.external_field_B == 0
    assert instance.external_field_C == 1.0
