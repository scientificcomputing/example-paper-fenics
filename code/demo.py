# # Demo
#
# This is a simple demo on how to work with the code.
# Before running this code you should also make sure to download the data.
# We will do this using python. First let us check if we already have the data
#

from pathlib import Path


msh_dir = Path("mesh")
if not msh_dir.exists():
    # We need to download the data

    import tarfile
    from pathlib import Path
    import requests
    from tqdm import tqdm

    def download(path, link, desc=None):
        if desc is None:
            desc = f"Download data to {path}"

        response = requests.get(link, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(
            total=total_size_in_bytes,
            unit="iB",
            unit_scale=True,
            desc=desc,
        )

        with open(path, "wb") as handle:
            for data in response.iter_content(chunk_size=1000 * 1024):
                progress_bar.update(len(data))
                handle.write(data)
        progress_bar.close()

    # We download the file
    download("data.tar", link="https://www.dropbox.com/s/6bkbw6v269dyfie/data.tar?dl=1")

    # and extract it
    tar = tarfile.open("data.tar")
    tar.extractall()

# The data should contain a folder called `mesh`, let us see what is inside it

# !ls mesh

# In the dataset, there are two meshes. Let us pick the smallest heart which
# is heart number 1

heart_nr = 1

# Let us specify the path to gmsh file and make sure ths file exist


msh_file = msh_dir / f"heart{heart_nr:02}.msh"

assert msh_file.is_file()

# ## Pre-processing
#
# First step is to convert the gmsh file to dolfin format. We can do this with
# the `convert_mesh` function from the `pre-processing` module

# +
import pre_processing

outfile = Path(f"heart{heart_nr:02}.h5")
pre_processing.convert_mesh(msh_file=msh_file, outfile=outfile)
# -

# ## Fiber generation
#
# We can now take the mesh in dolfin format and generate the fiber
# orientations using the ldrb algorithm.

# +
import run_fiber_generation


microstructure_path = Path(f"microstructure{heart_nr:02}.h5")
run_fiber_generation.generate_fibers(
    outfile=outfile,
    microstructure_path=microstructure_path,
)
# -

# ## Post processing
#
# Finally we will run the postprocessing script where we convert the
# fiber fields to a file we can visualize in paraview, and compare some
# features against the features presented in an artificial paper
#

# +
from postprocess import generate_fiber_xdmf_file

fiber_path = Path(f"fiber_{heart_nr:02}.xdmf")
features = generate_fiber_xdmf_file(
    outfile=outfile,
    microstructure_path=microstructure_path,
    fiber_path=fiber_path,
)
print(features)
# -
