import datetime
import socket
import ssl
#from sanic.response import json, text

def check_cert(hostname):
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )

    conn.settimeout(3.0)

    try:
        conn.connect((hostname, 443))
    except ssl.SSLError: # expired or misconfigured
        return
    except socket.timeout: # timeout connecting to host
        print("TIMEOUT")
        return "timeout"
    except: # other error
        return

    cert = conn.getpeercert()
    valid_until = cert['notAfter']
    print(valid_until)
    return valid_until

def invoke(hostname):
    print(hostname)
    return json({"valid_until": check_cert("google.com")})