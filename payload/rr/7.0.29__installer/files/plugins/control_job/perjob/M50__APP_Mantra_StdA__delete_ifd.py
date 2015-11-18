import os
job= rr.getJob()

msgRet= rrGlobal.messageBox(rrGlobal.logLvL.info, "Delete .ifd files?\n"+job.sceneName,"Yes","No", False,30)
if (msgRet):
    for frameNr in range(int(job.seqStart),int(job.seqEnd)):
        frameName= job.sceneName
        frameName=frameName.replace("<FN4>",str(frameNr).zfill(4)) 
        os.remove(frameName)
