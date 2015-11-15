import sys
import socket
import threading
import logging
import json
import src.conf.SETTINGS as SETTINGS


class Server:
    def __init__(self):

        self.sock = None

        self.sockets = []
        self.threads = []

        # self.start()

    def send_list(self, sock, dst_address, data):
        try:
            serialized = json.dumps(data)
            # send the length of the serialized data first
            sock.send('%d\n' % (len(serialized)))
            # send the serialized data
            sock.sendall(serialized)
            logging.info(' server %s:%s | JSON serialized data successfully sent to %s:%s' % (SETTINGS.SERVER_IP,
                                                                                              SETTINGS.SERVER_PORT,
                                                                                              dst_address[u'ip'],
                                                                                              dst_address[u'port']))
        except Exception, e:
            logging.info(' server %s:%s | JSON serialized data cannot be sent to %s:%s (%s)' % (SETTINGS.SERVER_IP,
                                                                                                SETTINGS.SERVER_PORT,
                                                                                                dst_address[u'ip'],
                                                                                                dst_address[u'port'],
                                                                                                e))
            try:
                sock.sendall(data)
                logging.info(' server:%s | non serialized data successfully sent %s:%s' % (SETTINGS.SERVER_PORT,
                                                                                           dst_address[u'ip'],
                                                                                           dst_address[u'port']))
            except Exception, e:
                logging.warning(' server:%s | data could not be sent to %s:%s (%s)' % (SETTINGS.SERVER_PORT,
                                                                                       dst_address[u'ip'],
                                                                                       dst_address[u'port'],
                                                                                       e))

    def new_thread(self, new_thread_sock, dict_client_address):
        self.sockets.append(new_thread_sock)
        # peer_address = new_thread_sock.getpeername()
        # peer_ip = peer_address[0]
        # peer_port = peer_address[1]
        logging.info(' server %s:%s | connection to %s:%s established' % (SETTINGS.SERVER_IP,
                                                                          SETTINGS.SERVER_PORT,
                                                                          dict_client_address[u'ip'],
                                                                          dict_client_address[u'port']))
        while True:
            server_response = {}
            try:
                client_request = new_thread_sock.recv(1024)
                print type(client_request)
                print repr(client_request)

                if len(client_request) == 0:
                    # http://stackoverflow.com/questions/26995145/python-client-disconnect-if-server-closes-connection
                    # But when a socket is closed on the peer, the read on the other side is aborted
                    # and returns 0 bytes. It's the same logic as an eof when reading from a true file
                    raise socket.error

                logging.info(' server %s:%s | client %s:%s sent the following: %s' % (SETTINGS.SERVER_IP,
                                                                                      SETTINGS.SERVER_PORT,
                                                                                      dict_client_address[u'ip'],
                                                                                      dict_client_address[u'port'],
                                                                                      client_request))

                # if not client_request == '':
                #     do something with client_request

                server_response[u'client_request'] = client_request
                self.send_list(new_thread_sock, dict_client_address, server_response)

                print server_response

                # else:
                #     new_thread_sock.close()
            except socket.error:
                self.sockets.remove(new_thread_sock)
                new_thread_sock.close()
                logging.info(' server %s:%s | connection to %s:%s closed' % (SETTINGS.SERVER_IP,
                                                                             SETTINGS.SERVER_PORT,
                                                                             dict_client_address[u'ip'],
                                                                             dict_client_address[u'port']))

                break

    def start(self):
        logging.info('server starting')
        logging.info('server ip is %s' % SETTINGS.SERVER_IP)
        try:
            logging.info('trying port %s' % SETTINGS.SERVER_PORT)

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.sock.bind((SETTINGS.SERVER_IP, SETTINGS.SERVER_PORT))

            self.sock.listen(5)
            logging.info('port succeeded')
            # break

        except socket.error, e:
            logging.info('port failed: %s' % e)

        logging.info('server listening at %s:%s' % (SETTINGS.SERVER_IP, SETTINGS.SERVER_PORT))

        while True:
            dict_client_address = {}
            try:
                client_connection, client_address = self.sock.accept()
                dict_client_address[u'ip'] = client_address[0]
                dict_client_address[u'port'] = client_address[1]
                thread = threading.Thread(target=self.new_thread, args=(client_connection, dict_client_address))
                thread.start()

            except KeyboardInterrupt:
                self.stop()
                # for sock in self.sockets:
                #     print 'closing'
                #     sock.close()
                print 'done'
                sys.exit()
                # if not bool(self.sockets):
                #     # print len(self.sockets)
                #     self.stop()
                # else:
                #     print '%s open connections - stop first. keyboard event ignored.' % len(self.sockets)

    def stop(self):
        # http://stackoverflow.com/questions/27139240/i-need-the-server-to-send-messages-to-all-clients-python-sockets
        # self.sock.close()
        # self.sock.shutdown(socket.SHUT_RDWR)
        for sock in self.sockets:
            logging.warning('closing connection to: %s' % str(sock.getpeername()))
            sock.sendall('bye')
            sock.close()
        # self.sock.shutdown()
        # sys.exit()
