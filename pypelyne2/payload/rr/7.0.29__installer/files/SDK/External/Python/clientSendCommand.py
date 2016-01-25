def findRR_Root():
    # findRR_Root adds the RR path as search path for the module
    # This function will only work if RR was installed on the machine
    # If you are using it from an external machine, you have to add the path to the rrPy module yourself
    # sys.path.append(MyModulePath)
    import os
    import platform
    import sys
    import struct
    if (not os.environ.has_key('RR_ROOT')):
        return
    modPath=os.environ['RR_ROOT']
    is64bit=(struct.calcsize("P") == 8)
    if (sys.platform.lower() == "win32") :
        if (is64bit):
            modPath=modPath + '/bin/win64'
        else:
            modPath=modPath + '/bin/win'
        modPath=modPath.replace("\\","/")
    elif (sys.platform.lower() == "darwin"):
        if (is64bit):
            modPath=modPath + '/bin/mac64/lib/python/27'
        else:
            modPath=modPath + '/bin/mac/lib/python/27'
    else:
        modPath=modPath + '/bin/lx64/lib'
    #modPath=modPath.replace("_debug","_release")
    sys.path.append(modPath)
    print("added module path "+modPath)
    

findRR_Root()
import libpyRR2 as rrLib


### --------------------------------------------------------------------- INIT
print("Set up server and login info.")
#A login is required if you have enabled 'Auth required for all connections' in rrConfig tab rrLogin
#Or if you connect via an router (router has to be setup in rrConfig as well)
#Note:  tcp does not keep an open connection to the rrServer.
#Every command re-connects to the server
tcp = rrLib._rrTCP("")
rrServer=tcp.getRRServer()   #This function does only work in your company. It uses the RR_ROOT environment installed by rrWorkstationInstaller
if (len(rrServer)==0):
    print (tcp.errorMessage())
if not tcp.setServer(rrServer, 7773):
    print ("Error setServer: "+ tcp.errorMessage())
    sys.exit()
tcp.setLogin("TestUser", "Password")


jobUserName="renderfarm"               #retrieve only job details of user "renderfarm" to resuce network traffic, rrServer workload and this Pythons memory.
tcp.jobSetFilter(jobUserName);

import socket
this_machine=socket.gethostname()
clientApplyList=[] 

### --------------------------------------------------------------------- CLIENTS
print("\nCheck clients")
if not tcp.clientGetList():
  print("Error getting clients: " + tcp.errorMessage())
else:
  clients = tcp.clients
  nbClients = clients.count()
  print("Number of client found: " + str(nbClients))
  for i in xrange(0, nbClients):
    cl = clients.at(i)
    print("\tCpuUsage %6.2f name: %s" %(cl.CPU_Usage,cl.name) )
    if (cl.name==this_machine):
        clientApplyList.append(i)


tcp.clientSendCommand(clientApplyList,rrGlobal._ClientCommand.cDisable,"")
    

        
print "done"
