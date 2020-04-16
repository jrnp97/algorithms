"""This script manage proxy sockets"""
import ssl
import socket
import logging
from base import Request
from Http.proxy import Proxy as Http


class Proxy(Http):

    def send(self, request: Request):
        if request.headers['Type'] == 'CONNECT':
            logging.info("Process CONNECT HTTP Verb on {}".format(request.headers['Host']))
            request.conn.send(b'HTTP/1.1 200 OK\r\nProxy-agent: Python Proxy/0.1.0 Draft 1\r\n\r\n')
            request.connect_2_step()
            logging.info("CONNECT HTTP Successfully on {}".format(request.headers['Host']))

        logging.info("Send request {} to {}:{}".format(request.headers['Type'],
                                                       request.headers['Host'],
                                                       request.headers['Port']
                                                       )
                     )
        # Initialize ssl client socket
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)  # Set SSL protocol to use
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_verify_locations("E:\\Desktop\\proxy\\certs\\ca-cert.pem")
        response = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                                       server_hostname=request.headers['Host'])
        response.connect((request.headers['Host'], 443))
        # Send request to client
        response.send(request.raw_data)
        data = b''
        response.settimeout(10)
        while True:
            try:
                t = response.recv(self._BUFFER)
                if t != b'':
                    data += t
                else:
                    break
            except socket.timeout:
                break
        logging.info("Get correctly response of {}".format(request.headers['Host']))
        request.conn.send(data)
        request.conn.close()
        response.close()
