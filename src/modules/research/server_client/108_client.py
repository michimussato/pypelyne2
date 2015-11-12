import socket
from logging import *
import os
import json
import sys
import src.conf.SETTINGS as SETTINGS


class client():
    def __init__( self, host='127.0.0.1', port=50001):
        # basicConfig( level = debugLevel )
        self.host = host
        self.port = port

        self.main()

    def recvList( self, sock ):
        try:
            # read the length of the data, letter by letter until we reach EOL
            length_str = ''
            #char = sock.recv( 32768 )
            char = sock.recv( 1 )

            #print char

            while char != '\n':
                length_str += char
                #warning( 'till here' )
                #char = sock.recv( 32768 )
                char = sock.recv( 1 )

            total = int( length_str )
            # use a memoryview to receive the data chunk by chunk efficiently
            view = memoryview( bytearray( total ) )
            next_offset = 0
        
            while total - next_offset > 0:
                recv_size = sock.recv_into( view[ next_offset: ], total - next_offset )
                next_offset += recv_size
        #try:

            data = json.loads( view.tobytes() )
            info( 'JSON serialized data successfully received' )
        #except ( TypeError, ValueError ), e:
        except:
            try:
                data = sock.recv( 4096 )
                info( 'non serialized data successfully received (type: %s, data: %s)' %( type( dataRecv ), data ) )
                logging.info( 'server response of type %s::%s' %( type( dataRecv ), data ) )
                
                if  type( data ) == str:
                    print 'doing str stuff'
                    pass
                elif  type( data ) == list:
                    print 'doing list stuff'
                    pass
            except:
                warning( 'data could not be received. don\'t know how to handle yet.' )
                return 0
                #raise Exception( 'Data received was not in JSON format' )
        return data



    def main( self ):

        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        #s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        try:
            sock.connect( ( self.host, self.port ) )
            info( 'connection to server successful' )
        except socket.error:
            warning( 'server not reachable on port %s' %( self.port ) )
            sys.exit()
        #s.setblocking( 0 )
        #info( 'connection to server successful' )
        #s.connect( ( host, port ) )

        while True:

            #path = None

            #for path in range( 300 ):

            data = raw_input( 'path: ' )

            #if not data.endswith( os.sep ):
            #    data = data + os.sep

            #print type( data )

            if not str( data ).lower() == 'q' and not str( data ).lower() == 'quit':
                if not data.endswith( os.sep ):
                    pass
                    #data = data + os.sep

                data = str( data )

                try:

                    #s = socket.socket()
                    #s.bind( ( '', port ) )
                    try:
                        
                        #info( 'connection to server successful' )

                        sock.sendall( data )
                        info( 'string sent to server: %s' %( data ) )

                        dataRecv = self.recvList( sock )

                        path = dataRecv[ 0 ]
                        isPath = dataRecv[ 1 ]
                        pathExists = dataRecv[ 2 ]
                        content = dataRecv[ 3 ]

                        #print dataRecv[ 0 ]
                        #print type( dataRecv )

                        #for i in dataRecv:
                        #    print i
                        #info( 'server response of type %s::%s' %( type( dataRecv ), dataRecv ) )
                        
                        # syntax: ( socket, isPath, pathExists, content, receiver )
                        if isPath == 'True' and pathExists == 'True':
                            #path exists on server
                            info( 'full response of server:%s' %( dataRecv ) )
                            info( 'content of %s on server:%s' %( path, content ) )
                            for item in content:
                                info( 'content on server: %s' %( os.path.join( path, item ) ) )

                        elif isPath == 'True' and pathExists == 'False':
                            #path does not exist, although it is in the correct format
                            warning( 'folder %s not found on server' %( path ) )

                        elif isPath == 'False' and pathExists == 'False':
                            #wrong path format (ie no leading / on unix)
                            warning( '%s is not a path format, you idiot' %( data ) )

                        else:
                            warning( '%s ??????????????????' %( data ) )

                        '''
                        if  type( dataRecv ) == str:
                            #print 'doing str stuff'
                            pass
                        elif  type( dataRecv ) == list:
                            #print 'doing list stuff'
                            pass
                        '''

                    except socket.error:
                        warning( 'server available but could not connect' )



                except socket.error:
                    warning( 'server %s not available.' %( host ) )
                    continue
            else:
                info( 'exitting' )
                #sock.close()
                break

        #info( 'connection closed by client' )
        #sock.close()


if __name__ == '__main__':
    # client = client( host = '192.168.0.17', port = 50505, debugLevel = INFO )
    client = client(host=SETTINGS.SERVER_IP)
