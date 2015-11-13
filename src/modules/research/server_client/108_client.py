import socket
import logging
import os
import json
import sys
import src.conf.SETTINGS as SETTINGS


class Client:
    def __init__(self, host=SETTINGS.SERVER_IP, port=SETTINGS.SERVER_PORT):
        self.host = host
        self.port = port

        self.main()

    @staticmethod
    def receive_list(sock):
        try:
            # read the length of the data, letter by letter until we reach EOL
            length_str = ''
            char = sock.recv(1)

            while char != '\n':
                length_str += char
                char = sock.recv(1)

            total = int(length_str)
            # use a memory view to receive the data chunk by chunk efficiently
            view = memoryview(bytearray(total))
            next_offset = 0
        
            while total - next_offset > 0:
                receive_size = sock.recv_into(view[next_offset:], total - next_offset)
                next_offset += receive_size

            data = json.loads(view.tobytes())
            logging.info('JSON serialized data successfully received')

        except Exception, e:
            print e
            try:
                data = sock.recv(4096)
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

    def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
            logging.info('connection to server successful')
        except socket.error:
            logging.warning('server not reachable on port %s' % self.port)
            sys.exit()

        while True:
            data = raw_input('path: ')

            if not str(data).lower() == 'q' and not str(data).lower() == 'quit':
                if not data.endswith(os.sep):
                    pass

                data = str(data)

                try:
                    try:
                        sock.sendall(data)
                        logging.info('string sent to server: %s' % data)

                        data_recv = self.receive_list(sock)

                        path = data_recv['path_queried']
                        is_path = data_recv['path_has_valid_format']
                        path_exists = data_recv['path_exists']
                        content = data_recv['content']

                        if is_path and path_exists:
                            # path exists on server
                            logging.info('full response of server:%s' % data_recv)
                            logging.info('content of %s on server:%s' % (path, content))
                            for item in content:
                                logging.info('content on server: %s' % os.path.join(path, item))

                        elif is_path and not path_exists:
                            # path does not exist, although it is in the correct format
                            logging.warning('folder %s not found on server' % path)

                        elif not is_path and not path_exists:
                            # wrong path format (ie no leading / on unix)
                            logging.warning('%s is not a path format, you idiot' % data)

                        else:
                            logging.warning('%s ??????????????????' % data)

                    except socket.error:
                        logging.warning('server available but could not connect')

                except socket.error:
                    logging.warning('server %s not available.' % self.host)
                    continue
            else:
                logging.info('exitting')
                # could also be commented out. no difference.
                sock.close()
                break

        # info( 'connection closed by client' )
        # sock.close()


if __name__ == '__main__':
    client = Client()
