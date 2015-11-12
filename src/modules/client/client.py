import socket
import sys
import json
import logging
import src.conf.SETTINGS as SETTINGS


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # self.connect()

    def disconnect(self):
        self.socket.sendall('shake_hands_goodbye')
        response = self.receive_serialized(self.socket)
        logging.info('server %s says %s' % (SETTINGS.SERVER_IP, response))
        self.socket.close()
        sys.exit()

    def connect(self):
            logging.info('connecting to server')
            logging.info('server ip is %s' % SETTINGS.SERVER_IP)

            while True:
                try:
                    logging.info('trying to connect to %s:%s' % (SETTINGS.SERVER_IP, SETTINGS.SERVER_PORT))
                    self.socket.connect((SETTINGS.SERVER_IP, SETTINGS.SERVER_PORT))
                    logging.info('connection to server successful')
                    self.socket.sendall('shake_hands_hello')

                    response = self.receive_serialized(self.socket)
                    print response
                    logging.info('server %s says %s' % (SETTINGS.SERVER_IP, response))
                    # self.server_alive = True
                    break
                except Exception, e:
                    logging.info('connection failed: %s' % e)

    def receive_serialized(self, sock):

        print sock

        # read the length of the data, letter by letter until we reach EOL
        length_str = ''
        char = sock.recv(1)

        while char != '\n':
            length_str += char
            # logging.warning('till here')
            char = sock.recv(1)

        total = int(length_str)
        # use a memoryview to receive the data chunk by chunk efficiently
        view = memoryview(bytearray(total))
        next_offset = 0

        while total - next_offset > 0:
            recv_size = sock.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
        try:
            deserialized = json.loads(view.tobytes())
            # return deserialized
        # except (TypeError, ValueError), e:
        except Exception, e:
            # raise Exception('Data received was not in JSON format')
            logging.error('Data received was not in JSON format: %s' % e)
            # return 1

        return deserialized
