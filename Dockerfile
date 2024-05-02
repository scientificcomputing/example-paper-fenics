# Use github pages for docker image
FROM ghcr.io/scientificcomputing/example-paper-fenics:v0.4.0

# Create user with a home directory
ARG NB_USER
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

# Copy current directory
WORKDIR ${HOME}
COPY . ${HOME}

# Convert demo.py into demo.ipynb
RUN python3 -m pip install jupytext jupyter
RUN python3 -m ipykernel install --name=python3 --user
RUN python3 -m jupytext --to notebook --execute --output ./code/demo.ipynb ./code/demo.py

# Change ownership of home directory
USER root
RUN chown -R ${NB_UID} ${HOME}

USER ${NB_USER}

ENTRYPOINT []
