# Running in Docker

We have created a docker image containing all the dependencies as well as the source code in the repository. To get the most recent version of the docker image, make sure to pull the latest image first
```bash
docker pull ghcr.io/scientificcomputing/example-paper-fenics:latest
```

Now you can start a docker container using the command
```bash
docker run --rm -it ghcr.io/scientificcomputing/example-paper-fenics
```
This will bring you into the default working directory at `/repo` where you will find the folder `example-paper-fenics` containing the source code from the repository.

From here you can follow the steps outlined in [](reproducing-main) to reproduce the results.

## Sharing the results in the container with your local machine
You might want to move the results the you create in the container to your local machine. To do this you need to mount a volume from local machine into the container. For example, you can mount the current directory (which is stored in the environment variable $PWD) into the folder `/repo/local` by running the container using the following command
```bash
docker run --rm -v $PWD:/repo/local -it ghcr.io/scientificcomputing/example-paper-fenics
```
When entering the container now you should now see both the folder `example-paper-fenics` and a folder called `local`. Once you have generated some results inside `example-paper-fenics` you can copy these results over to the folder called `local` and they should appear in the current directory on you local machine. For example, you could try to copy the readme file
```bash
cp /repo/example-paper-fenics/README.md /repo/local/.
```
and you should now see the readme file appearing on your machine.
