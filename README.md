# Supplementary code for the paper: Title of paper
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scientificcomputing/example-paper-fenics/main?labpath=code%2Fdemo.ipynb)

This repository contains supplementary code for the paper
> Finsberg, H., Dokken, J. 2022.
> Title of paper, Journal of ..., volume, page, url


## Abstract
Provide the abstract of the paper

## Getting started

We provide a pre-build Docker image which can be used to run the the code in this repository. First thing you need to do is in ensure that you have [docker installed](https://docs.docker.com/get-docker/).

To start an interactive docker container you can execute the following command

```bash
docker run --rm -it ghcr.io/scientificcomputing/example-paper-fenics:latest
```

## Data

Data is available in a dropbox folder. Use the script `download_data.sh` in the data folder to download the data.

The data folder should have the following structure after the data is downloaded.
```
├── README.md
├── data.tar
├── download_data.sh
└── mesh
    ├── heart01.msh
    └── heart02.msh
```
These meshes are originally taken from <https://ora.ox.ac.uk/objects/uuid:951b086c-c4ba-41ef-b967-c2106d87ee06>, but since the original data is about 26GB we decided to make a smaller dataset for this example.

Eventually when you publish a paper you could put this data on e.g [Zenodo](https://zenodo.org). That will make sure the data gets it's own DOI.


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




## Citation

```
@software{Lisa_My_Research_Software_2017,
  author = {Lisa, Mona and Bot, Hew},
  doi = {10.5281/zenodo.1234},
  month = {12},
  title = {{My Research Software}},
  url = {https://github.com/scientificcomputing/example-paper},
  version = {2.0.4},
  year = {2017}
}
```


## Having issues
If you have any troubles please file and issue in the GitHub repository.

## License
MIT
