# Catweb v2: The kittens go multi-tier ;-)
This demo for Docker Enterprise Edition Std/Adv is based on the original catweb demo by Steven Thwaites [https://github.com/sthwaites/catweb](https://github.com/sthwaites/catweb).
This evolution of that demo is pretty useless, although it's fun to demo some of the features in Docker EE. In this specific case it uses a backend overlay network and the HTTP Routing Mesh.

## Getting started

Clone the repo:

`git clone https://github.com/pvdbleek/catweb_v2`

### Components

#### Service: catweb-frontend

This is the frontend container which uses python (flask) app to render an `index.html` to display a random anitmated gif of a kitten.
It fetches the image from ``catweb-imageserver`` through proxy.
It's exposed through HRM on it's own URL.

To build:

``` 
cd catweb-frontend 
docker build -t <your_namespace>/<your_repo> .
docker push <your_namespace>/<your_repo>
```
#### Service: catweb-backend

This container is running in the backend network and is only accessible from the ``catweb-frontend`` service.
It runs ngingx to serve a bunch of animated gifs to the ``catweb-frontend`` containers.

To build:

``` 
cd catweb-imageserver 
docker build -t <your_namespace>/<your_repo> .
docker push <your_namespace>/<your_repo>
```

### Deploy
Adjust ``docker-compose.yml`` with your URL and images and deploy using:

```docker stack deploy -c docker-compose.yml catweb```

### End result:
! /catweb_stack_diagram.png
