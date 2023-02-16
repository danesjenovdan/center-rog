#!/bin/bash

sudo docker login rg.fr-par.scw.cloud/djnd -u nologin -p $SCW_SECRET_TOKEN

# BUILD AND PUBLISH OBLJUBA DELA DOLG
sudo docker build -f rog/Dockerfile -t rog:latest .
sudo docker tag rog:latest rg.fr-par.scw.cloud/djnd/rog:latest
sudo docker push rg.fr-par.scw.cloud/djnd/rog:latest