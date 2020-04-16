"""This script define http proxy class"""
import socket
import logging
from base import Request

logging.basicConfig(filename='E:\\Desktop\\proxy\\logfile.log', level=logging.DEBUG)


class Proxy:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def __init__(self):
        self._PORT = 9000
        self._MAX_CONN = 1
        self._BUFFER = 4096
        self._SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._STATUS = False

    def init(self) -> None:
        """
        This method bind localhost address to socket.
        :return: str
        """
        try:
            self._SOCK.bind(('', self._PORT))  # Set port to socket
            self._SOCK.listen(self._MAX_CONN)  # Set max connection to listen socket.
            self._STATUS = True
            logging.info("[*] Server started successfully...")
        except Exception as e:
            logging.error("[-] Error creating server -> {0}".format(e))
            raise OSError("[-] Error creating server -> {0}".format(e))

    def send(self, request: Request) -> None:
        """
        -----------------------
        :param request:
        :return: str
        """
        try:
            logging.info("Send request to server -> {0}:{1}".format(request.headers['Host'], request.headers['Port']))
            response = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to client
            response.connect((request.headers['Host'], int(request.headers['Port'])))
            # Send data
            response.send(request.raw_data)
            response.settimeout(10)
            # Received response
            try:
                data = b''
                info = response.recv(self._BUFFER)  # Received data
                while info:
                    data += info
                    try:
                        info = response.recv(self._BUFFER)  # Received data
                    except socket.timeout:
                        break
            except socket.timeout:
                logging.warning('[!] Request response empy')
                data = b''

            # Send response
            request.conn.send(data)
            request.conn.close()
            # Close response socket
            response.close()
            logging.info("[*] Request send successfully...")
        except KeyError:
            request.conn.close()
            logging.warning("[!!] Request warning...")
        except OSError as error:
            logging.error("[-] Error send request to host -> {0}".format(error))
            raise OSError("[-] Error send request to host -> {0}".format(error))

    def listen(self):
        """
        This method accept petitions.
        :return: Request
        """
        if self._STATUS:
            cnn, ad = self._SOCK.accept()  # Accept connection from browser
            cnn.settimeout(0.5)  # Set non-blocking to socket
            try:
                data = b''
                info = cnn.recv(self._BUFFER)  # Received data
                while info:
                    data += info
                    try:
                        info = cnn.recv(self._BUFFER)  # Received data
                    except socket.timeout:
                        break
            except socket.timeout:
                logging.warning('[!] Request response empy')
                data = b''

            return Request(data, cnn, ad)
        else:
            logging.warning("[!] Server is down, method don't execute...")

    def close(self) -> None:
        """
        This method close socket.
        :return: str
        """
        if self._STATUS:
            try:
                self._SOCK.close()
                self._STATUS = False
                logging.info("[+] Server down successfully...")
            except Exception as e:
                logging.error("[-] Error shutdown socket -> {0}".format(e))
                raise OSError("[-] Error shutdown socket -> {0}".format(e))
        else:
            logging.warning("[!] Server is down, method don't execute...")
