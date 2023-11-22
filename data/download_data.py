import tarfile
from pathlib import Path
import requests  # pip install requests
from tqdm import tqdm  # pip install tqdm


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


if __name__ == "__main__":
    datafile = Path("data.tar")
    download(datafile, "https://www.dropbox.com/s/6bkbw6v269dyfie/data.tar?dl=1")
    data = tarfile.TarFile(datafile)
    data.extractall()
