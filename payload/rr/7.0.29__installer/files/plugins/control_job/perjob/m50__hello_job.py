
#progress bar B is used for all jobs
if (rr.perJobCurrent(()==0):
    rrGlobal.progress_SetMaxB(rr.perJobMax())
rrGlobal.progress_SetProgressB(rr.perJobCurrent())
#progress bar A is used for this script 
rrGlobal.progress_SetMaxA(5)
rrGlobal.progress_SetProgressA(0)
rrGlobal.refreshUI()



job= rr.getJob()
print "I am job " +job.sceneName
rrGlobal.progress_SetProgressA(1)

rrGlobal.writeLog(rrGlobal.logLvL.info, "Example Python script:\n I am job " +job.sceneName,"Hello Job Script")
rrGlobal.progress_SetProgressA(2)

rrGlobal.messageBox(rrGlobal.logLvL.info, "Example Python script:\n I am job " +job.sceneName,"","", False,30)
rrGlobal.progress_SetProgressA(3)

msgRet= rrGlobal.messageBox(rrGlobal.logLvL.info, "Do you like me?","Yes","No", False,30)
rrGlobal.progress_SetProgressA(4)

print msgRet
rrGlobal.progress_SetProgressA(5)



