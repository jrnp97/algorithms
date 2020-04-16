import re
from socket import socket


def p_headers(h_raw: str) -> dict:
    """
    This function extract and detect all headers on request.
    :param h_raw:
    :return: None
    """
    exp = re.compile("(H|h)(o|O)(s|S)(t|T)")
    data = h_raw.split('\r\n')  # Separate data into list.
    d = dict({})
    # Extract port manually
    for k in data:
        try:
            key = k.split(':')[0] if len(d) > 0 else k.split(' ')[0]
            value = k.split(' ')[1]
            # Extract port
            ex_info = value.split(':')
            if bool(re.match(exp, key)) and len(ex_info) == 2:
                d.update(dict({'Port': ex_info[1]}))
                value = ex_info[0]
            elif bool(re.match(exp, key)) and len(ex_info) == 1:
                d.update(dict({'Port': '80'}))
            d.update(dict({key: value}))
            # Extract Type
            d.update(dict({'Type': list(d.keys())[0]}))
        except IndexError:  # as e:
            return {}  # Error processing header information (not found)
    else:
        return d


def connect_bypass(raw_data: bytes) -> bytes:
    str_data = raw_data.decode(errors='ignore')  # Convert to string
    exp = re.compile(r'(CONNECT (www|http:|https:)+[^\s]+[\w])\w+')
    new_raw = re.sub(exp, "GET /", str_data).encode()
    return new_raw


class Request:

    def __init__(self, res_raw: bytes, con: socket, ad: tuple) -> None:
        """
        This function make the Request instance and process the request byte string.
        :param res_raw:  request byte string.
        """
        self.conn = con
        self.address = ad
        self.raw_data = res_raw  # Set raw data
        t = res_raw.decode(errors='ignore').split('\r\n\r\n')
        self.raw_h = t[0].encode()  # Set headers raw data.
        self.headers = p_headers(t[0])  # Identify headers and saved.
        try:
            self.raw_b = t[1].encode()  # Set body raw data.
            self.body = t[1].split('\r\n') if len(t[1]) > 0 else ""  # Save body data.
        except IndexError:
            self.raw_b = b''

    def connect_2_step(self):
        self.raw_data = connect_bypass(self.raw_data)
        t = self.raw_data.decode(errors='ignore').split('\r\n\r\n')
        self.headers = p_headers(t[0])  # Identify headers and saved.

    def show(self):
        print("=" * 30)
        print("Request Information")
        print("-"*20)
        print("{}".format(self.raw_data.decode(errors='ignore')))
        print("=" * 30)
        print("[*] Receive data")
