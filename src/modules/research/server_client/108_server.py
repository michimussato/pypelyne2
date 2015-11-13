import os
import sys
import socket
import threading
import logging
import json
import src.conf.SETTINGS as SETTINGS


class Server:
    def __init__(self, host=SETTINGS.SERVER_IP, port=SETTINGS.SERVER_PORT):

        self.host = host
        self.port = port
        self.sockets = []
        self.threads = []
        # how many ports should be checked if given port fails?
        self.portRange = 2

        self.main()
        
    def send_list(self, sock, dict_addr, data):
        try:
            serialized = json.dumps(data)
            # send the length of the serialized data first
            sock.send('%d\n' % (len(serialized)))
            # send the serialized data
            sock.sendall(serialized)
            logging.info(' server %s:%s | JSON serialized data successfully sent to %s:%s' % (self.host,
                                                                                              self.port,
                                                                                              dict_addr[u'ip'],
                                                                                              dict_addr[u'port']))
        except Exception, e:
            logging.info(e)
            try:
                # raise Exception( 'You can only send JSON-serializable data' )
                # send the length of the serialized data first
                sock.sendall(data)
                logging.info(' server:%s | non serialized data successfully sent %s:%s' % (self.port,
                                                                                           dict_addr[u'ip'],
                                                                                           dict_addr[u'port']))
            except (TypeError, ValueError), e:
                logging.warning(' server:%s | data could not be sent to %s:%s. don\'t know how to handle yet.' % (self.port,
                                                                                                                  dict_addr[u'ip'],
                                                                                                                  dict_addr[u'port']))

    def list_content(self, sock, dict_addr):
        self.sockets.append(sock)
        logging.info(' server %s:%s | connection to %s:%s established' % (self.host,
                                                                          self.port,
                                                                          dict_addr[u'ip'],
                                                                          dict_addr[u'port']))
        while True:
            response = {}
            try:
                path = sock.recv(1024)
                
                if not path == '':
                    if os.path.isabs(path):
                        path = os.path.normpath(path)
                        if os.path.isdir(path) and os.path.exists(path):
                            logging.info(' server %s:%s | valid path received from %s:%s: %s' % (self.host,
                                                                                                 self.port,
                                                                                                 dict_addr[u'ip'],
                                                                                                 dict_addr[u'port'],
                                                                                                 path))

                            content = os.listdir(path)
                            response[u'content'] = content
                            response[u'path_has_valid_format'] = True
                            response[u'path_exists'] = True
                            response[u'path_queried'] = path
                            self.send_list(sock, dict_addr, response)

                        else:
                            content = None
                            logging.warning(' server %s:%s | path received from %s:%s valid but does not exist: %s' % (self.host,
                                                                                                                       self.port,
                                                                                                                       dict_addr[u'ip'],
                                                                                                                       dict_addr[u'port'],
                                                                                                                       path))
                            response[u'content'] = content
                            response[u'path_has_valid_format'] = True
                            response[u'path_exists'] = False
                            response[u'path_queried'] = path
                            self.send_list(sock, dict_addr, response)
                    else:
                        content = None
                        logging.warning(' server %s:%s | invalid path received from %s:%s: %s' % (self.host,
                                                                                                  self.port,
                                                                                                  dict_addr[u'ip'],
                                                                                                  dict_addr[u'port'],
                                                                                                  path))
                        response[u'content'] = content
                        response[u'path_has_valid_format'] = False
                        response[u'path_exists'] = False
                        response[u'path_queried'] = path
                        self.send_list(sock, dict_addr, response)
                else:
                    sock.close()
            except socket.error:
                self.sockets.remove(sock)
                sock.close()
                logging.info(' server %s:%s | connection to %s:%s closed' % (self.host,
                                                                             self.port,
                                                                             dict_addr[u'ip'],
                                                                             dict_addr[u'port']))
                
                break

    def main(self):

        logging.info('server starting')
        logging.info('server ip is %s' % self.host)
        counter = 1
        sock = None

        while True:
            try:
                logging.info('trying port %s' % self.port)

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((self.host, self.port))

                sock.listen(5)
                logging.info('port succeeded')
                break

            except socket.error:
                logging.info('port failed')

                if counter < self.portRange:
                    counter += 1
                    self.port += 1
                else:
                    logging.warning('tried %s port(s) without success. server failed to start.' % counter)
                    sys.exit()

        logging.info('server listening at %s:%s' % (self.host, self.port))

        while True:
            dict_addr = {}
            try:
                conn, addr = sock.accept()
                dict_addr[u'ip'] = addr[0]
                dict_addr[u'port'] = addr[1]
                thread = threading.Thread(target=self.list_content, args=(conn, dict_addr))
                thread.start()

            except KeyboardInterrupt:
                print len(self.sockets)
                sys.exit()


if __name__ == '__main__':
    server = Server()
