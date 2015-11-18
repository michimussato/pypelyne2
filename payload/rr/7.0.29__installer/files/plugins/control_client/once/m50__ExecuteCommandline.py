#This python script sends a command to all client.
#In this case it does not send an abort or enable
#it will send a commandline for the client to execute.
#
#The client will create a batch file RR_LocalData/_command.bat.
#It executes the command and writes the output into RR_LocalData/_command.txt.
#If you want to keep your log output, you should redirect it into a file via your commandline.
#For Example:  myCommand 1>/fileserver/share/MyCommand_<LocalHost>.txt   2>/fileserver/share/MyCommand_<LocalHost>_error.txt
#
#You can use all variables (like <LocalHost>) from render configs, as long as they are not job specific.
#
#The command buffer can only take up to 500 letters.


selectedClients=[]
nrClients= rr.clientAll_count()
for c in range(0, nrClients):
    if (rr.clientAll_get(c).isSelected()):
        selectedClients.append(c)
rrGlobal.messageBox(rrGlobal.logLvL.info, "Example Python script:\n You have selected "+ str(len(selectedClients))+ " Clients\n Sending command to selected Clients." ,"","", False,30)

CmdLine=          'echo "Hello"<NL>'
CmdLine=CmdLine+  'echo "I am alive""<NL>'

if not rr.clientSendCommand(selectedClients ,rrGlobal._ClientCommand.cCommandLine, CmdLine):
    rrGlobal.messageBox(rrGlobal.logLvL.warning, "Unable to send command to client","","", False,30)
else:
    rrGlobal.messageBox(rrGlobal.logLvL.info, "Command send","","", False,30)





