"""
Script for generating fiber orientations using the LDRB
algorithm

https://finsberg.github.io/ldrb/
"""
import config
import dolfin
import ldrb
from cardiac_geometries.geometry import Geometry


def generate_fibers(heart_nr: int) -> None:
    outfile = config.get_h5_path(heart_nr=heart_nr)
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

    microstructure_path = config.get_results_path(heart_nr=heart_nr)
    with dolfin.HDF5File(
        geo.mesh.mpi_comm(),
        microstructure_path.as_posix(),
        "w",
    ) as h5file:
        h5file.write(f0, "f0")
        h5file.write(s0, "s0")
        h5file.write(n0, "n0")


def main() -> int:
    for heart_nr in [1, 2]:
        generate_fibers(heart_nr=heart_nr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
