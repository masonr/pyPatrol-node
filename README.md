# pyPatrol

Distributed ping and service monitor using Python3 + Sanic 

## Getting Started

These instructions will get you a copy of the project up and running on your machine.

### Prerequisites

* This project requires Python 3.5+.

* The following pip packages are also required:
  * [sanic](https://pypi.python.org/pypi/Sanic)
  * [python-valve](https://pypi.python.org/pypi/python-valve) [v0.2.1 or later]
  * [aiohttp](https://pypi.python.org/pypi/aiohttp)
  * [requests](https://pypi.python.org/pypi/requests)
  * [sanic-openapi](https://pypi.python.org/pypi/sanic-openapi)
  
```bash
  $ pip3 install sanic "python-valve>=0.2.1" aiohttp requests sanic-openapi
```

### Configuration

Within the pyPatrol config file are several parameters that need to be set:
  * **node_name** - unique name of the pyPatrol node
  * **node_ip** - ip or hostname of the pyPatrol node
  * **node_port** - port that the pyPatrol service will bind to
  * **ipv4_capable** - pyPatrol node ipv4 capable?
  * **ipv6_capable** - pyPatrol node ipv6 capable?
  * **num_of_workers** - number of async workers
  * **server_host** - ip or hostname of the pyPatrol server
  * **server_port** - port of the pyPatrol server
  * **server_secret** - a secret string that authorizes the pyPatrol node with the server
  * **standalone** - standalone mode or connect to pyPatrol server
  * **use_ssl** - set if SSL (HTTPS) connections should be utilized
  * **ssl_cert** - SSL certificate file path if use_ssl is True
  * **ssl_key** - SSL key file path if use_ssl is True

### Installing

1. Clone the git repo

```bash
  $ git clone https://github.com/masonr/pyPatrol
```

2. Move the pyPatrol directory to /opt/

```bash
  $ mv pyPatrol /opt/
```

3. Copy the example configuration file

```bash
  $ cp pypatrol.example pypatrol.conf
```

4. Configure the pyPatrol node using the parameters described above in the _pypatrol.conf_ file

5. Run the unittests

```bash
  $ cd /opt/pyPatrol
  $ python3 test.py
```
After running all of the tests for each module, the final output should say - "OK".

## How To Run

1. Navigate to the pyPatrol directory

```bash
  $ cd /opt/pyPatrol
```

2. Run the Sanic application

```bash
  $ python3 app.py
```

### Running As A Service

#### systemd

1. Navigate to the misc subdirectory

```bash
  $ cd /opt/pyPatrol/misc
```

2. Edit the _pypatrol.service_ file and add the User to run the service as (suggested to be a non-root user). Then, copy the file into the systemd services directory

```bash
  $ sudo cp pypatrol.service /etc/systemd/system/
```

3. Start the pyPatrol service and verify that it is running correctly

```bash
  $ sudo service pypatrol start
  $ sudo service pypatrol status
```

4. _(Optional)_ Setup pyPatrol to start on boot

```bash
  $ sudo systemctl enable pypatrol
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
