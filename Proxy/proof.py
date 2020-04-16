import socket
import ssl
import select
from pprint import pprint
from Https.proxy import Proxy


def main():
    with Proxy() as p:
            p.init()
            while True:
                request = p.listen()
                p.send(request)


def do_something(connstream, data):
    print(data.decode(errors='ignore'))
    connstream.send(b'HTTP/1.1 200 OK')


def deal_with_client(connstream):
    data = connstream.read()
    # empty data means the client is finished with us
    info = b''
    while data:
        if not do_something(connstream, data):
            break
        data = connstream.read()

    pprint(info.decode(errors='ignore'))
    connstream.send(b'HTTP/1.1 200 OK')



if __name__ == "__main__":
    # main()
    # """
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context = ssl.create_default_context()

    context.load_cert_chain(certfile="E:\Desktop\proxy\certs\self-signed.pem",
                            keyfile="E:\Desktop\proxy\certs\key.pem"
                            )

    bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bindsocket.bind(('', 9000))
    bindsocket.listen(1)

    while True:
        newsocket, fromaddr = bindsocket.accept()
        connstream = context.wrap_socket(newsocket, server_side=True, do_handshake_on_connect=False)
        try:
            select.select([connstream], [], [])
            deal_with_client(connstream)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
    # """

