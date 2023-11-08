#!/usr/bin/env bash

# Removing the dl=0 from the end of the shared link from dropbox
# curl -L https://www.dropbox.com/s/6bkbw6v269dyfie/data.tar -o data.tar
wget https://www.dropbox.com/s/6bkbw6v269dyfie/data.tar
tar -xvf data.tar
