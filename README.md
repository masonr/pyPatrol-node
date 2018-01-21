# pyPatrol

Distributed ping and service monitor using Python3 + Sanic 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* This project requires Python 3.5+.

* The following pip packages are also required:
  * [sanic](https://pypi.python.org/pypi/Sanic)
  * [python-valve](https://pypi.python.org/pypi/python-valve) [v0.2.1 or later]
  * [aiohttp](https://pypi.python.org/pypi/aiohttp)
  * [requests](https://pypi.python.org/pypi/requests)
  
```bash
  $ pip3 install sanic "python-valve>=0.2.1" aiohttp requests
```

* The host machine must be IPv6-capable.

### Installing

1. Clone the git repo

```bash
  $ git clone https://github.com/masonr/pyPatrol
```

2. Run the unittests
```bash
  $ cd pyPatrol
  $ python3 test.py
```
After running all of the tests for each module, the final output should say - "OK".

## How To Run

1. Navigate to the pyPatrol directory

```bash
  $ cd /path/to/pyPatrol
```

2. Run the Sanic application

```bash
  $ python3 app.py
```

## Capabilities / Documentation

[REST API Specifications](docs/REST_API/README.md)
* [/status](docs/REST_API/status.md) - Returns status of the pyPatrol node
* [/ping](docs/REST_API/ping.md) - Pings (via IPv4) a specified IP/hostname
* [/ping6](docs/REST_API/ping6.md) - Pings (via IPv6) a specified IP/hostname
* [/http_response](docs/REST_API/http_response.md) - Checks the HTTP response code of a given URL
* [/cert](docs/REST_API/cert.md) - Checks if an SSL certificate is valid or will expire within a specified threshold
* [/tcp_socket](docs/REST_API/tcp_socket.md) - Checks if a specified IP/hostname and port are listening for connections (TCP)
* [/steam_server](docs/REST_API/steam_server.md) - Checks if a Steam Server running on a specified IP/hostname and port is online
