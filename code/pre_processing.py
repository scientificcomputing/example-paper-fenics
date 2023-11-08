"""
Script for converting GMSH files to Dolfin format
using cardiac geometries

https://computationalphysiology.github.io/cardiac_geometries/

SPDX-License-Identifier:    MIT
"""
import typing
from pathlib import Path
import logging
import cardiac_geometries
import config
from cardiac_geometries.geometry import Geometry
from cardiac_geometries.geometry import H5Path
import sys

# We set default log level to be info
logger = logging.Logger(__name__, logging.INFO)
ch = logging.StreamHandler(sys.stdout)
FORMAT = "%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s"
ch.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(ch)

schema = {
    "mesh": H5Path(
        h5group="/mesh",
        is_mesh=True,
    ),
    "ffun": H5Path(
        h5group="/ffun",
        is_meshfunction=True,
        dim=2,
        mesh_key="mesh",
    ),
    "markers": H5Path(
        h5group="/markers",
        is_dolfin=False,
    ),
}


def convert_mesh(
    msh_file: typing.Union[Path, str],
    outfile: typing.Union[Path, str],
) -> None:
    """
    Convert an .msh file to DOLFIN h5 format

    Args:
        msh_file (typing.Union[Path, str]): Path to input mesh (.msh extension)
        outfile (typing.Union[Path, str]): Path to outfile (.h5 extension)
    """
    geometry = cardiac_geometries.gmsh2dolfin(msh_file, unlink=True)
    logger.info(f"Converting {msh_file}")
    geo = Geometry(
        mesh=geometry.mesh,
        markers=geometry.markers,
        ffun=geometry.marker_functions.ffun,
        schema=schema,
    )

    geo.save(outfile)
    logger.info(f"Saved to {outfile}")


def main() -> int:
    """
    Convert meshes from `../data/mesh/heart0*.msh` to `../data/heart_0*.h5`

    Returns:
        int: 0 if code runs as expected
    """
    for heart_nr in [1, 2]:
        msh_file = config.get_msh_path(heart_nr=heart_nr)
        outfile = config.get_h5_path(heart_nr=heart_nr)
        convert_mesh(msh_file=msh_file, outfile=outfile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
