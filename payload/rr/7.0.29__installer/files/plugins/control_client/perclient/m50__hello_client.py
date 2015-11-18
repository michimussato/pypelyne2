#_ClientStatusThread.jobID
#_ClientStatusThread.jobSeqStart
#_ClientStatusThread.jobSeqEnd
#_ClientStatusThread.jobSeqStep
#_ClientStatusThread.jobSeqStartJobNr
#_ClientStatusThread.jobSeqEndJobNr
#_ClientStatusThread.jobSeqStepJobNr
#_ClientStatusThread.jobMultiFrameID
#_ClientStatusThread.jobIsPreview
#_ClientStatusThread.jobStatus
#_ClientStatusThread.jobFramesDone
#_ClientStatusThread.clientStatus
#_ClientStatusThread.jobCPU_Usage
#_ClientStatusThread.jobMemoryUsage
#bool _ClientStatusThread.hasKSOLoaded()
#bool _ClientStatusThread.isRendering()
#string _ClientStatusThread.clientStatusAsStringSingle()


#_ClientHardware.totalMemory
#_ClientHardware.ghzEffective
#_ClientHardware.nrCores
#_ClientHardware.version
#_ClientHardware.OS
#_ClientHardware.isX64
#_ClientHardware.PS
#string _ClientHardware.OSasString()


#_ClientStatus.StructureID
#_ClientStatus.VariablesID
#_ClientStatus.name
#_ClientStatus.localTextureSpaceUsed
#_ClientStatus.maxJobThreads
#_ClientStatus.CPU_Usage
#_ClientStatus.isRunningAsService
#_ClientStatus.availMemory
#_ClientStatus.loggedUser
#_ClientStatus.tempHDD
#_ClientStatus.maxCoresSetForJob
#_ClientStatus.version
#_ClientStatus.noUserInteraction
#_ClientStatusThread _ClientStatus.jobThread(_ClientStatus client, int threadID )


#_Client includes all _ClientStatus variables and functions
#_Client.hw
#bool _Client.isSelected()
#bool _Client.isJobSelected()


# rrGlobal.writeLog(int rrLog_level, const char * error_msg, const char * Location)
# rrGlobal.writeLog(int rrLog_level, const char * error_msg, const char * Location)
# rrGlobal.messageBox(int rrLog_level,  const char * msg, const char * btn1, const char * btn2, const bool &showCancel, const int &waitTime)


#rrClient rr.getClient()
#rrClient rr.clientAll_get(const int &index)
#int rr.clientAll_count()

client= rr.getClient()
rrGlobal.messageBox(rrGlobal.logLvL.info, "Example Python script:\n You have selected client " + client.name ,"","", False,30)




