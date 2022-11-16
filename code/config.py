from pathlib import Path

here = Path(__file__).absolute().parent


def get_msh_path(heart_nr: int) -> Path:
    return here / ".." / "data" / "mesh" / f"heart{heart_nr:02}.msh"


def get_h5_path(heart_nr: int) -> Path:
    return here / ".." / "data" / f"heart_{heart_nr:02}.h5"


def get_results_dir(create: bool) -> Path:
    folder = here / "results"
    if create:
        folder.mkdir(exist_ok=True)
    return folder


def get_results_path(heart_nr: int, create: bool = True) -> Path:
    return get_results_dir(create=create) / f"microstructure_{heart_nr:02}.h5"


def get_fiber_path(heart_nr: int, create: bool = True) -> Path:
    return get_results_dir(create=create) / f"fiber_{heart_nr:02}.xdmf"


def get_features_path(heart_nr: int, create: bool = True) -> Path:
    return get_results_dir(create=create) / f"features_{heart_nr:02}.json"
