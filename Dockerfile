FROM finsberg/fenics-gmsh

WORKDIR /tmp

# Copy pyproject.toml first so that we done need to reinstall in case anoter file
# is changing ater rebuiding docker image
COPY requirements.txt  .
RUN python3 -m pip install pip --upgrade && python3 -m pip install --no-cache-dir -r requirements.txt && rm -rf /tmp

WORKDIR /app
COPY . /app
