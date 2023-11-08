"""
Script for converting file

SPDX-License-Identifier:    MIT
"""
import json
import logging
import sys
import typing
from pathlib import Path

import config
import dolfin
import numpy as np
from cardiac_geometries.geometry import Geometry, load_microstructure

logger = logging.Logger(__name__, logging.INFO)
ch = logging.StreamHandler(sys.stdout)
FORMAT = "%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s"
ch.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(ch)


def generate_fiber_xdmf_file(
    outfile: Path,
    microstructure_path: Path,
    fiber_path: Path,
) -> typing.Dict[str, float]:
    geo = Geometry.from_file(outfile, schema_path=outfile.with_suffix(".json"))

    f0, _, _ = load_microstructure(
        mesh=geo.mesh,
        microstructure_path=microstructure_path,
    )

    # Save fibers to a file that can be visualized in Paraview

    with dolfin.XDMFFile(fiber_path.as_posix()) as f:
        f.write(f0)

    logger.info(f"Saved fibers to {fiber_path}")
    # Compute some features. This could be some results presented in the paper

    return {
        "size": f0.vector().size(),
        "min": f0.vector().get_local().min(),
        "max": f0.vector().get_local().max(),
        "mean": f0.vector().get_local().mean(),
        "std": f0.vector().get_local().std(),
    }


def check_results(features_path: Path, features: dict):
    """
    Check if data from input file `features_path` matches input features

    Args:
        features_path (Path): Path to reference results
        features (dict): Results generated from current simulation
    """
    expected_features = json.loads(features_path.read_text())
    logger.info("Checking reproducibility")
    reproducible = True
    # Check each (key, value) pair in the features and check they are
    # within machine precision
    for key in expected_features.keys():
        if not np.isclose(expected_features[key], features[key], rtol=1e-8):
            logger.error(f"{key}: {expected_features[key]}!={features[key]}")
            reproducible = False

    if reproducible:
        logger.info("Results are reproducible")
    else:
        raise RuntimeError("Results are not reproducible")


def main() -> int:
    for heart_nr in [1, 2]:
        outfile = config.get_h5_path(heart_nr=heart_nr)
        microstructure_path = config.get_results_path(heart_nr=heart_nr)
        fiber_path = config.get_fiber_path(heart_nr=heart_nr)
        features_path = config.get_features_path(heart_nr=heart_nr)
        features = generate_fiber_xdmf_file(
            outfile=outfile,
            microstructure_path=microstructure_path,
            fiber_path=fiber_path,
        )
        # Check that results corresponds to the results from the paper
        check_results(features_path, features)

        # This is the line for writing the results
        # features_path.write_text(json.dumps(features, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
