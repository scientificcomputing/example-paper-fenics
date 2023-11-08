"""
Script for generating fiber orientations using the LDRB
algorithm

https://finsberg.github.io/ldrb/

SPDX-License-Identifier:    MIT
"""
import logging
import sys
from pathlib import Path

import config
import dolfin
import ldrb
from cardiac_geometries.geometry import Geometry

logger = logging.Logger(__name__, logging.INFO)
ch = logging.StreamHandler(sys.stdout)
FORMAT = "%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s"
ch.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(ch)


def generate_fibers(outfile: Path, microstructure_path: Path) -> None:
    geo = Geometry.from_file(outfile, schema_path=outfile.with_suffix(".json"))

    # Markers are a dictionary with values [marker, dim]
    # and we only need the dim
    markers = {
        "base": geo.markers["base"][0],
        "epi": geo.markers["epicardium"][0],
        "lv": geo.markers["left ventricle endocardium"][0],
        "rv": geo.markers["right ventricle endocardium"][0],
    }

    fiber_space = "CG_1"
    f0, s0, n0 = ldrb.dolfin_ldrb(
        mesh=geo.mesh,
        fiber_space=fiber_space,
        ffun=geo.ffun,
        markers=markers,
        alpha_endo_lv=60,  # Fiber angle on the endocardium
        alpha_epi_lv=-60,  # Fiber angle on the epicardium
        beta_endo_lv=0,  # Sheet angle on the endocardium
        beta_epi_lv=0,  # Sheet angle on the epicardium
    )

    with dolfin.HDF5File(
        geo.mesh.mpi_comm(),
        microstructure_path.as_posix(),
        "w",
    ) as h5file:
        h5file.write(f0, "f0")
        h5file.write(s0, "s0")
        h5file.write(n0, "n0")

    logger.info(f"Microstructure saved to {microstructure_path}")


def main() -> int:
    for heart_nr in [1, 2]:
        outfile = config.get_h5_path(heart_nr=heart_nr)
        microstructure_path = config.get_results_path(heart_nr=heart_nr)
        generate_fibers(outfile=outfile, microstructure_path=microstructure_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
