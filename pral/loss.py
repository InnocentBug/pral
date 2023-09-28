import h5py
import numpy as np
from scipy.optimize import curve_fit


def get_density(name):
    with h5py.File(f"{name}_ana.h5", "r") as h5_handle:
        density = h5_handle["density_field"][:]

    density = np.average(density, axis=(0, 3))
    rho0 = np.sum(density) / (64 * 5.0)

    density /= rho0

    middle = density.shape[2] // 2
    return_list = []
    for i in range(3):
        return_list += [[density[i, :, 2], density[i, :, middle], density[i, :, -1]]]

    for i in range(3):
        for j in range(3):
            min = np.min(return_list[i][j])
            max = np.max(return_list[i][j])

            return_list[i][j] -= min + (max - min) / 2

    return return_list


def target_function(x, amplitude, period, shift):
    return amplitude * np.cos(2 * np.pi / period * x + shift)


def get_fit_characteristics(rho):
    x = np.linspace(0, len(rho) * 1 / 7.0, len(rho))

    param, cov = curve_fit(target_function, x, rho, p0=[1.0, 2.0, 0.0])
    fit = target_function(x, *param)
    err = np.sum(np.sqrt(np.diag(cov)))
    msd = np.average((rho - fit) ** 2)

    return x, fit, err, msd, param[0], param[1]


def get_small_a_loss(data):
    bottom = data[0]
    bottom_target_amplitude = 0.15
    bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = (
        bottom_err
        + bottom_msd
        + (bottom_amplitude - bottom_target_amplitude) ** 2
        + (bottom_period - bottom_target_period) ** 2
    )

    middle = data[1]
    middle_target_amplitude = 0.0
    # middle_target_period = 2.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = middle_err + middle_msd + (middle_amplitude - middle_target_amplitude) ** 2

    top = data[2]
    top_target_amplitude = 0.15
    top_target_period = 2.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = (
        top_err
        + top_msd
        + (top_amplitude - top_target_amplitude) ** 2
        + (top_period - top_target_period) ** 2
    )

    # print(f"small a {bottom_loss} {middle_loss} {top_loss}")

    return bottom_loss + middle_loss + top_loss


def get_small_b_loss(data):
    bottom = data[1]
    bottom_target_amplitude = 0.2
    bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = (
        bottom_err
        + bottom_msd
        + (bottom_amplitude - bottom_target_amplitude) ** 2
        + (bottom_period - bottom_target_period) ** 2
    )

    middle = data[1]
    middle_target_amplitude = 0.0
    # middle_target_period = 2.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = middle_err + middle_msd + (middle_amplitude - middle_target_amplitude) ** 2

    top = data[2]
    top_target_amplitude = 0.2
    top_target_period = 2.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = (
        top_err
        + top_msd
        + (top_amplitude - top_target_amplitude) ** 2
        + (top_period - top_target_period) ** 2
    )

    # print(f"small b {bottom_loss} {middle_loss} {top_loss}")

    return bottom_loss + middle_loss + top_loss


def get_small_c_loss(data):
    bottom = data[1]
    bottom_target_amplitude = 0.05
    bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = (
        bottom_err
        + bottom_msd
        + (bottom_amplitude - bottom_target_amplitude) ** 2
        + (bottom_period - bottom_target_period) ** 2
    )

    middle = data[1]
    middle_target_amplitude = 0.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = middle_err + middle_msd + (middle_amplitude - middle_target_amplitude) ** 2

    top = data[2]
    top_target_amplitude = 0.05
    top_target_period = 2.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = (
        top_err
        + top_msd
        + (top_amplitude - top_target_amplitude) ** 2
        + (top_period - top_target_period) ** 2
    )

    # print(f"small c {bottom_loss} {middle_loss} {top_loss}")

    return bottom_loss + middle_loss + top_loss


def get_medium_a_loss(data):
    bottom = data[1]
    bottom_target_amplitude = 0.4
    bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = (
        bottom_err
        + bottom_msd
        + (bottom_amplitude - bottom_target_amplitude) ** 2
        + (bottom_period - bottom_target_period) ** 2
    )

    middle = data[1]
    middle_target_amplitude = 0.05
    middle_target_period = 2.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = (
        middle_err
        + middle_msd
        + (middle_amplitude - middle_target_amplitude) ** 2
        + (middle_period - middle_target_period) ** 2
    )

    top = data[2]
    top_target_amplitude = 0.4
    top_target_period = 2.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = (
        top_err
        + top_msd
        + (top_amplitude - top_target_amplitude) ** 2
        + (top_period - top_target_period) ** 2
    )

    return bottom_loss + middle_loss + top_loss


def get_medium_b_loss(data):
    bottom = data[1]
    bottom_target_amplitude = 0.4
    bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = (
        bottom_err
        + bottom_msd
        + (bottom_amplitude - bottom_target_amplitude) ** 2
        + (bottom_period - bottom_target_period) ** 2
    )

    middle = data[1]
    middle_target_amplitude = 0.05
    middle_target_period = 2.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = (
        middle_err
        + middle_msd
        + (middle_amplitude - middle_target_amplitude) ** 2
        + (middle_period - middle_target_period) ** 2
    )

    top = data[2]
    top_target_amplitude = 0.4
    top_target_period = 2.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = (
        top_err
        + top_msd
        + (top_amplitude - top_target_amplitude) ** 2
        + (top_period - top_target_period) ** 2
    )

    return bottom_loss + middle_loss + top_loss


def get_medium_c_loss(data):
    bottom = data[1]
    bottom_target_amplitude = 0.0
    # bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = bottom_err + bottom_msd + (bottom_amplitude - bottom_target_amplitude) ** 2

    middle = data[1]
    middle_target_amplitude = 0.05
    middle_target_period = 2.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = (
        middle_err
        + middle_msd
        + (middle_amplitude - middle_target_amplitude) ** 2
        + (middle_period - middle_target_period) ** 2
    )

    top = data[2]
    top_target_amplitude = 0.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = top_err + top_msd + (top_amplitude - top_target_amplitude) ** 2

    return bottom_loss + middle_loss + top_loss


def get_large_a_loss(data):
    bottom = data[1]
    bottom_target_amplitude = 0.4
    bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = (
        bottom_err
        + bottom_msd
        + (bottom_amplitude - bottom_target_amplitude) ** 2
        + (bottom_period - bottom_target_period) ** 2
    )

    middle = data[1]
    middle_target_amplitude = 0.1
    middle_target_period = 4.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = (
        middle_err
        + middle_msd
        + (middle_amplitude - middle_target_amplitude) ** 2
        + (middle_period - middle_target_period) ** 2
    )

    top = data[2]
    top_target_amplitude = 0.4
    top_target_period = 2.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = (
        top_err
        + top_msd
        + (top_amplitude - top_target_amplitude) ** 2
        + (top_period - top_target_period) ** 2
    )

    return bottom_loss + middle_loss + top_loss


def get_large_b_loss(data):
    bottom = data[1]
    bottom_target_amplitude = 0.4
    bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = (
        bottom_err
        + bottom_msd
        + (bottom_amplitude - bottom_target_amplitude) ** 2
        + (bottom_period - bottom_target_period) ** 2
    )

    middle = data[1]
    middle_target_amplitude = 0.05
    middle_target_period = 2.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = (
        middle_err
        + middle_msd
        + (middle_amplitude - middle_target_amplitude) ** 2
        + (middle_period - middle_target_period) ** 2
    )

    top = data[2]
    top_target_amplitude = 0.4
    top_target_period = 2.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = (
        top_err
        + top_msd
        + (top_amplitude - top_target_amplitude) ** 2
        + (top_period - top_target_period) ** 2
    )

    return bottom_loss + middle_loss + top_loss


def get_large_c_loss(data):
    bottom = data[1]
    bottom_target_amplitude = 0.0
    # bottom_target_period = 2.0
    (
        bottom_x,
        bottom_fit,
        bottom_err,
        bottom_msd,
        bottom_amplitude,
        bottom_period,
    ) = get_fit_characteristics(bottom)

    bottom_loss = bottom_err + bottom_msd + (bottom_amplitude - bottom_target_amplitude) ** 2

    middle = data[1]
    middle_target_amplitude = 0.05
    middle_target_period = 4.0
    (
        middle_x,
        middle_fit,
        middle_err,
        middle_msd,
        middle_amplitude,
        middle_period,
    ) = get_fit_characteristics(middle)

    middle_loss = (
        middle_err
        + middle_msd
        + (middle_amplitude - middle_target_amplitude) ** 2
        + (middle_period - middle_target_period) ** 2
    )

    top = data[2]
    top_target_amplitude = 0.0
    # top_target_period = 2.0
    top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(top)

    top_loss = top_err + top_msd + (top_amplitude - top_target_amplitude) ** 2

    return bottom_loss + middle_loss + top_loss


def get_small_loss(ret_list=None):
    if ret_list is None:
        ret_list = get_density("small")
    return (
        get_small_a_loss(ret_list[0])
        + get_small_b_loss(ret_list[1])
        + get_small_c_loss(ret_list[2])
    )


def get_medium_loss(ret_list=None):
    if ret_list is None:
        ret_list = get_density("medium")
    return (
        get_medium_a_loss(ret_list[0])
        + get_medium_b_loss(ret_list[1])
        + get_medium_c_loss(ret_list[2])
    )


def get_large_loss(ret_list=None):
    if ret_list is None:
        ret_list = get_density("large")
    return (
        get_large_a_loss(ret_list[0])
        + get_large_b_loss(ret_list[1])
        + get_large_c_loss(ret_list[2])
    )


def get_loss(name=None, particle_type=None):
    if name not in [None, "small", "medium", "large"]:
        raise RuntimeError("wrong name ofr loss")
    if particle_type not in [None, "a", "A", "b", "B", "c", "C"]:
        raise RuntimeError("wrong particle type in loss")

    if name == "small":
        ret_list = get_density(name)
        if particle_type in ("a", "A"):
            return get_small_a_loss(ret_list[0])
        if particle_type in ("b", "B"):
            return get_small_b_loss(ret_list[1])
        if particle_type in ("c", "C"):
            return get_small_c_loss(ret_list[2])
        return get_small_loss(ret_list)
    if name == "medium":
        ret_list = get_density(name)
        if particle_type in ("a", "A"):
            return get_medium_a_loss(ret_list[0])
        if particle_type in ("b", "B"):
            return get_medium_b_loss(ret_list[1])
        if particle_type in ("c", "C"):
            return get_medium_c_loss(ret_list[2])
        return get_medium_loss(ret_list)
    if name == "large":
        ret_list = get_density(name)
        if particle_type in ("a", "A"):
            return get_large_a_loss(ret_list[0])
        if particle_type in ("b", "B"):
            return get_large_b_loss(ret_list[1])
        if particle_type in ("c", "C"):
            return get_large_c_loss(ret_list[2])
        return get_large_loss(ret_list)

    return get_small_loss() + get_medium_loss() + get_large_loss()
