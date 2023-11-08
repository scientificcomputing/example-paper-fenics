# Data

Data is available in a dropbox folder. Use the script `download_data.sh` to download the data. The data folder should have the following structure after the data is downloaded.
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

In the [demo](../code/demo.py) there is also a recipe for how to download the data using python
