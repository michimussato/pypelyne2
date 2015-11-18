import SocketServer
import struct
import datetime
import sys
import time

StructureID_rrCommands  =0x0B03
StructureID_RRN_TCP_HeaderData_v3 = 0x0D03
Size_RRCommands = 1232
Size_RRN_TCP_HeaderData_v3 = 198
rrnData_commands = 7
log_command="print(' \\\'"
log_command_end="')"
log_command_intern_prestring="          "
log_debug= False
commandTimeout=180

def flushLog():
    sys.stdout.flush()        
    sys.stderr.flush()        

def logMessage_intern(lvl, msg):
    if (len(lvl)==0):
        msg=datetime.datetime.now().strftime("%H:%M.%S") + " rrKSO      : " + str(msg)
    else:
        msg=datetime.datetime.now().strftime("%H:%M.%S") + " rrKSO - " + str(lvl) + ": " + str(msg)
    msg= msg.replace("\'","\\\'").replace("\n","\\\n")
    print(log_command_intern_prestring+msg)


def logMessageGen(lvl, msg):
    if (len(lvl)==0):
        msg=datetime.datetime.now().strftime("%H:%M.%S") + " rrKSO      : " + str(msg)
    else:
        msg=datetime.datetime.now().strftime("%H:%M.%S") + " rrKSO - " + str(lvl) + ": " + str(msg)
    msg= msg.replace("\'","\\\'").replace("\n","\\\n")
    msg= log_command+msg+log_command_end
    exec(msg)
    
def logMessageDebug( msg):
    if (log_debug):
            logMessage_intern("DGB", msg)

def logMessage(msg):
    logMessageGen("",msg)


def logMessageError(msg):
    logMessageGen("ERR", str(msg)+"\n\n")
    logMessageGen("ERR", "Error reported, aborting render script")
    flushLog();



class _RRCommands():
    StructureID=StructureID_rrCommands
    ctype=4 
    command=0
    paramID=0
    paramX=0
    paramY=0
    paramS=""
    paramSlength=0
    paramSType=0
   

    def toBinary(self):
        keptfree=0
        return struct.pack("=HBBhbbQii1002sHH200?bb",self.StructureID,self.ctype, self.command, keptfree, keptfree,keptfree,self.paramID, self.paramX, self.paramY, keptfree, keptfree, self.paramS, self.paramSlength,self.paramSType)

    def fromBinary(self, buf):
        tmp= struct.unpack("=HBBhbbQii1002sHH200?bb",buf)
        self.StructureID= tmp[0] 
        self.ctype= tmp[1] 
        self.command= tmp[2] 
        self.paramID= tmp[6] 
        self.paramX= tmp[7] 
        self.paramY= tmp[8]
        paramsTemp=tmp[9];
        self.paramSlength= tmp[10]
        self.paramSType= tmp[11]
        self.paramS=""   
        for c in range(0, self.paramSlength):  #string is actually unicode 16bit, but for now a dirty ANSI conversion is fine 
            self.paramS= self.paramS+ paramsTemp[c*2]
        
    def rightStructure(self):
        return (self.StructureID== StructureID_rrCommands)



    
class _RRN_TCP_HeaderData_v3():
    StructureID= StructureID_RRN_TCP_HeaderData_v3
    dataLen=0   
    dataType=0  
    dataNrElements=0
    appType=14  

    def toBinary(self):
        keptfree=0
        keptfreeS=""
        return struct.pack("=HIIHbhB182s",self.StructureID,keptfree,self.dataLen,keptfree,self.dataType,self.dataNrElements,self.appType,keptfreeS)

    def fromBinary(self, buf):
        tmp= struct.unpack("=HIIHbhB182s",buf)
        self.StructureID= tmp[0] 
        self.dataLen= tmp[2] 
        self.dataType= tmp[4] 
        self.dataNrElements= tmp[5] 
        self.appType= tmp[6] 

    def rightStructure(self):
        return (self.StructureID== StructureID_RRN_TCP_HeaderData_v3)

rrKSONextCommand=""



class rrKSOTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        logMessageDebug("Handler")
        headerData=_RRN_TCP_HeaderData_v3()
        headerData.fromBinary(self.request.recv(Size_RRN_TCP_HeaderData_v3))
        if ((not headerData.rightStructure()) or (headerData.dataType!=rrnData_commands) or (headerData.dataLen!=Size_RRCommands) ):
            self.server.continueLoop=False
            logMessageGen("ERR","TCP header wrong! "
                   + " ID:"+ str(headerData.StructureID)+"!=" +str(StructureID_RRN_TCP_HeaderData_v3)
                   + " type:"+ str(headerData.dataType)+"!=" +str(rrnData_commands)
                   + " len:"+ str(headerData.dataLen)+"!=" +str(Size_RRCommands)
                   )
            return
        command = _RRCommands()
        command.fromBinary(self.request.recv(Size_RRCommands))
        if (( not command.rightStructure())):
            self.server.continueLoop=False
            logMessageGen("ERR","TCP data wrong! "
                   + "ID:"+ str(command.StructureID)+"!=" +str(StructureID_rrCommands)
                   )
            return
        if (( command.paramSlength==0)):
            logMessageGen("ERR","Empty command received.")
            return
        global rrKSONextCommand
        rrKSONextCommand=command.paramS

    



class rrKSOServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    timeout = commandTimeout
    daemon_threads = True
    allow_reuse_address = True
    continueLoop = True
    
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
    
    def handle_timeout(self):
        logMessage_intern("ERR",'Timeout!')
        self.continueLoop=False
    
    def handle_error(self, request, client_address):
        logMessage_intern("ERR"," Issue while handline connection to " + str(client_address))
        self.continueLoop=False
        import traceback
        logMessage_intern("ERR",traceback.format_exc())



def writeRenderPlaceholder(filename):
    logMessageGen("---",filename );
    import socket
    hostName=socket.gethostname()
    hostName=hostName[:100]
    file = open(filename,"wb")
    file.write("rrDB") #Magic ID
    file.write("\x01\x0B") #DataType ID
    for x in range(0, len(hostName)):
        file.write(hostName[x])
        file.write("\x00")     #unicode
    for x in range(len(hostName),51):
        file.write("\x00\x00")
    file.write(chr(len(hostName)))
    file.write("\x00")
    file.write("\x00\x00")
    file.close();


def writeRenderPlaceholder_nr(filename, frameNr, padding, ext):
    padding=int(padding)
    if (padding==0):
        padding=4
    filenameFinal=filename +str(frameNr).zfill(int(padding)) + ext
    writeRenderPlaceholder(filenameFinal)


#logMessageDebug("KSO_IMPORTED__KSO_IMPORTED__KSO_IMPORTED__KSO_IMPORTED__KSO_IMPORTED__KSO_IMPORTED__KSO_IMPORTED")

