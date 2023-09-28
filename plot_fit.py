import sys

import matplotlib.pyplot as plt
import numpy as np
from gyana.plot_util import savefig

from pral import get_density, get_fit_characteristics, get_loss


def main(argv):
    for name in ("small", "medium", "large"):
        data = get_density(name)
        fig, ax = plt.subplots()
        for i, ptype in enumerate(["A", "B", "C"]):
            ax.set_title(f"loss = {get_loss(name)}")
            bottom = data[i][0]
            (
                bottom_x,
                bottom_fit,
                bottom_err,
                bottom_msd,
                bottom_amplitude,
                bottom_period,
            ) = get_fit_characteristics(bottom)

            (line,) = ax.plot(
                bottom_x, bottom, label=f"bottom {ptype}: {np.round(get_loss(name, ptype),2)}"
            )
            ax.plot(bottom_x, bottom_fit, "--", color=line.get_color())

            middle = data[i][1]
            (
                middle_x,
                middle_fit,
                middle_err,
                middle_msd,
                middle_amplitude,
                middle_period,
            ) = get_fit_characteristics(middle)
            (line,) = ax.plot(
                middle_x, middle, label=f"middle {ptype}: {np.round(get_loss(name, ptype),2)}"
            )
            ax.plot(middle_x, middle_fit, "--", color=line.get_color())

            top = data[i][2]
            top_x, top_fit, top_err, top_msd, top_amplitude, top_period = get_fit_characteristics(
                top
            )
            (line,) = ax.plot(top_x, top, label=f"top {ptype}: {np.round(get_loss(name, ptype),2)}")
            ax.plot(top_x, top_fit, "--", color=line.get_color())

            ax.legend(loc="best")

        print(name)
        savefig(fig, "", f"{name}_profile.pdf")
        plt.close(fig)


if __name__ == "__main__":
    main(sys.argv[1:])
