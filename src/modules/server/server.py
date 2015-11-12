import sys
import json
import socket
import threading
import logging
import src.conf.SETTINGS as SETTINGS


class Server:
    def __init__(self):
        self._ip = None
        # self.host = SETTINGS.SERVER_IP
        # self.port = SETTINGS.SERVER_PORT
        self.sockets = []
        self.threads = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.start()
        
    def start(self):
        logging.info('server starting @ %s:%s' % (SETTINGS.SERVER_IP, SETTINGS.SERVER_PORT))

        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((SETTINGS.SERVER_IP, SETTINGS.SERVER_PORT))

            self.sock.listen(5)

            self.listen()

        except socket.error, e:
            logging.error('server failed: %s' % e)
            
    def listen(self):
        logging.info('server is now listening at %s:%s' % (SETTINGS.SERVER_IP, SETTINGS.SERVER_PORT))
        while True:
            try:
                connection, address = self.sock.accept()
                logging.info('new client connection from %s' % str(address))
                thread = threading.Thread(target=self.do_something, args=(connection, address))
                thread.start()
                # self.threads.append(t)
            
            except KeyboardInterrupt, e:
                logging.warning(e)
                sys.exit()

    def send_string(self, sock, addr, data):
        sock.sendall(data)

    def send_list(self, sock, addr, data):
        try:
            serialized = json.dumps([path, addr, data])
            # send the length of the serialized data first
            sock.send('%d\n' % len(serialized))
            # send the serialized data
            sock.sendall(serialized)
            logging.info(' server %s:%s | JSON serialized data successfully sent to %s:%s' % (SETTINGS.SERVER_IP,
                                                                                              SETTINGS.SERVER_PORT,
                                                                                              addr[0],
                                                                                              addr[1]))
        except Exception, e:
            logging.warning(' server %s:%s | sending JSON serialzed data not possible: %s' % e)
            try:
                sock.sendall(data)
                logging.info(' server:%s | non serialized data successfully sent %s:%s' % (SETTINGS.SERVER_IP,
                                                                                           addr[0],
                                                                                           addr[1]))
            except (TypeError, ValueError), e:
                logging.warning(' server:%s | data could not be sent to %s:%s. (%s).' % (SETTINGS.SERVER_IP,
                                                                                         addr[0],
                                                                                         addr[1],
                                                                                         e))

    def do_something(self, sock, addr):
        self.sockets.append(sock)

        logging.info(' server %s:%s | connection to %s:%s established asdf' % (SETTINGS.SERVER_IP,
                                                                               SETTINGS.SERVER_PORT,
                                                                               addr[0],
                                                                               addr[1]))
        # print sock
        # print addr
        # print arg
        while sock:

            response = sock.recv(1024)

            print response

            if response == 'shake_hands_hello':
                logging.info('client %s:%s sent hello' % (addr[0], addr[1]))
                self.send_string(sock, addr, 'hello')
                # self.sockets.remove(sock)
                # sock.close()
                # logging.info('%s connections left open' % (len(self.sockets)))
                # break

            elif response == 'shake_hands_goodbye':
                logging.info('client %s:%s sent bye bye' % (addr[0], addr[1]))
                self.sockets.remove(sock)
                sock.close()
                logging.info('%s connections left open' % (len(self.sockets)))
                break

            # if response == 'bye':
            #     # self.sendSerialized(socket, response)
            #     # logging.info('client %s:%s sent bye bye' % (addr[0], addr[1]))
            #     # self.sendList(sock, 'bye', None)
            #     self.sockets.remove(sock)
            #     sock.close()
            #     logging.info('%s connections left open' % (len(self.sockets)))
            #     break
