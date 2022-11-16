"""Script for converting file """
import json
from pathlib import Path

import config
import dolfin
from cardiac_geometries.geometry import Geometry
from cardiac_geometries.geometry import load_microstructure


def generate_fiber_xdmf_file(heart_nr: int) -> None:
    outfile = config.get_h5_path(heart_nr=heart_nr)
    geo = Geometry.from_file(outfile, schema_path=outfile.with_suffix(".json"))

    microstructure_path = config.get_results_path(heart_nr=heart_nr)
    f0, s0, n0 = load_microstructure(
        mesh=geo.mesh,
        microstructure_path=microstructure_path,
    )

    # Save fibers to a file that can be visualized in paraview
    fiber_path = config.get_fiber_path(heart_nr=heart_nr)
    with dolfin.XDMFFile(fiber_path.as_posix()) as f:
        f.write(f0)

    # Compute some features. This could be some results presented in the paper
    features_path = config.get_features_path(heart_nr=heart_nr)
    features = {
        "size": f0.vector().size(),
        "min": f0.vector().get_local().min(),
        "max": f0.vector().get_local().max(),
        "mean": f0.vector().get_local().mean(),
        "std": f0.vector().get_local().std(),
    }

    # Check that results corresponds to the results from the paper
    check_results(features_path, features)

    # This is the line for writing the results
    # features_path.write_text(json.dumps(features, indent=2))


def check_results(features_path: Path, features):
    expected_feautres = json.loads(features_path.read_text())
    assert expected_feautres == features


def main() -> int:
    for heart_nr in [1, 2]:
        generate_fiber_xdmf_file(heart_nr=heart_nr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
