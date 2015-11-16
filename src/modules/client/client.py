import socket
import logging
import os
import json
import sys
import src.conf.SETTINGS as SETTINGS


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_list(self):
        # data = None
        try:
            # read the length of the data, letter by letter until we reach EOL
            length_str = ''
            char = self.sock.recv(1)

            while char != '\n':
                length_str += char
                char = self.sock.recv(1)

            total = int(length_str)
            # use a memory view to receive the data chunk by chunk efficiently
            view = memoryview(bytearray(total))
            next_offset = 0

            while total - next_offset > 0:
                receive_size = self.sock.recv_into(view[next_offset:], total - next_offset)
                next_offset += receive_size

            data = json.loads(view.tobytes())
            logging.info('JSON serialized data successfully received')

        except Exception, e:
            print e
            try:
                data = self.sock.recv(4096)
                logging.info('non serialized data successfully received (type: %s, data: %s)' % (type(data), data))
                logging.info('server response of type %s::%s' % (type(data), data))

                if type(data) == str:
                    print 'doing str stuff'
                    pass
                elif type(data) == list:
                    print 'doing list stuff'
                    pass
            except Exception, e:
                logging.warning('data could not be received. %s' % e)
                return 0
                # raise Exception( 'Data received was not in JSON format' )

        return data

    def connect(self):
        try:
            self.sock.connect((SETTINGS.SERVER_IP, SETTINGS.SERVER_PORT))
            logging.info('connection to server successful')
            self.communicate()
        except socket.error:
            logging.warning('server not reachable on port %s' % SETTINGS.SERVER_PORT)
            sys.exit()

    def communicate(self):
        while True:

            # if data:
            try:
                data = str(raw_input('waiting for input here: '))

                if data.lower() == 'disconnect':
                    logging.info('exitting')

                    # could also be commented out. no difference.
                    self.sock.close()
                    break

                else:
                    try:
                        self.sock.sendall(data)
                        logging.info('string sent to server: %s' % data)

                        data_recv = self.receive_list()

                        print data_recv

                        # here comes the the stuff that the server responded
                        #
                        #

                    except socket.error:
                        logging.warning('server %s not available.' % SETTINGS.SERVER_IP)
                        raise Exception

            except KeyboardInterrupt, e:
                logging.warning('keyboard interrupt: %s' % e)
                # self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                break

            except Exception, e:
                logging.info('connection closed by client')
                self.sock.close()
                break
