# Doc Flow


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Service is a blockchain-based digital docflow.

## Features

- Auth on platform by login and password
- Role-base system
- Sign file and getting public key and signature
- Check sign file by public key and signature
- Upload file to IPFS and Ethereum blockchain
- View file on IPFS and Ethereum blockchain
- Access user manager 

## Tech

Dillinger uses a number of open source projects to work properly:

- Python 3.8
    -  sqlalchemey
    -  FastAPI
    -  SQLite
    -  Brownie
    -  Crypto
- Docker
- Solidity 0.8.15
- IPFS
- Ethereum
- JavaScript
- HTML
- CSS
- Bootstrap
- SQLite

## Installation

Requires Python 3.8+ to run.

Install the dependencies and devDependencies and start core server (default: `0.0.0.0:5000`):

```sh
cd docflow/core
pip install requirements.txt
python app.py
```

For run IPFS server (default: `0.0.0.0:5001/webui`):

```sh
cd docflow/ipfs
docker-compose build
docker-compose up -d ipfs
docker-compose logs -f ipfs
```


For run web interface (default: `0.0.0.0:8080`):

```sh
cd docflow/web
pip install requirements.txt
python app.py
```


## Docker

DocFlow is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

For run core server:
```sh
cd doc_flow/core
docker-compose build
docker-compose up -d
```

For run web interface:
```sh
cd doc_flow/web
docker-compose build
docker-compose up -d
```

For run IPFS server:
```sh
cd doc_flow/ipfs
docker-compose build
docker-compose up -d ipfs
```

## License

GPLv3
