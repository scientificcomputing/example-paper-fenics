(reproducing-main)=
# Reproducing

## Data

Data is available in a Dropbox folder. Use the script `download_data.sh` in the data folder to download the data, i.e
```bash
cd data
bash download_data.sh
```

The data folder should have the following structure after the data is downloaded.
```
├── README.md
├── data.tar
├── download_data.sh
└── mesh
    ├── heart01.msh
    └── heart02.msh
```
These meshes are originally taken from {cite}`martinez2019repository`, but since the original data is about 26GB we decided to make a smaller dataset for this example.

Eventually when you publish a paper you could put this data on e.g [Zenodo](https://zenodo.org). That will make sure the data gets it's own [Digital Object Identifier](https://www.doi.org/) (DOI).


## Scripts
All the scripts are located in the folder called `code` in the repository. Is is assumed that you run the script from within this folder.

### Pre-processing
In order to reproduce the results you need to first run the pre-processing script
```
python3 pre_processing.py
```
This will convert the meshes from Gmsh to a dolfin format.

### Fiber generation
The next step is to run the fiber generation. You can do this by running the script
```
python3 run_fiber_generation.py
```
This will create a new folder `code/results` containing files called `microstructure_<heart_nr>.h5`.

### Postprocessing
The final step is to postprocess the results by running the script
```
python3 postprocess.py
```
This will generate a file for visualizing the fibers in the Paraview (inside `code/results` called  `fiber_<heart_nr>.xdmf`). This script will also compare some features computed from the fibers with the results published in the (artificial) paper. If the results differ, then the program will raise an error.

```{bibliography}
:filter: docname in docnames
```
