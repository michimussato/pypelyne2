
#progress bar B is used for all jobs
if (rr.perJobCurrent()==0):
    rrGlobal.progress_SetMaxB(rr.perJobMax())
rrGlobal.progress_SetProgressB(rr.perJobCurrent())
#progress bar A is used for this script 
rrGlobal.progress_SetMaxA(5)
rrGlobal.progress_SetProgressA(0)
rrGlobal.refreshUI()

job= rr.getJob()

myUI= rrGlobal.getGenericUI()
myUI.addItem(rrGlobal.genUIType.label,"infoLabel","")
myUI.setText("infoLabel","Example Python script:\n Please enter the new values for sequence start and end:")
myUI.addItem(rrGlobal.genUIType.label,"jobIDLabel","")
myUI.setText("jobIDLabel","Job:"+job.IDstr())
myUI.addItem(rrGlobal.genUIType.layoutH,"seqLayout","")
myUI.addItem(rrGlobal.genUIType.spin,"spinStart","seqLayout")
myUI.addItem(rrGlobal.genUIType.spin,"spinEnd","seqLayout")
myUI.setText("spinStart","Start:")
myUI.setText("spinEnd","End:")
myUI.setValue("spinStart",int(job.seqStart))
myUI.setValue("spinEnd",int(job.seqEnd))
myUI.addItem(rrGlobal.genUIType.layoutH,"btnLayout","")
myUI.addItem(rrGlobal.genUIType.closeButton,"Change Job","btnLayout")
myUI.addItem(rrGlobal.genUIType.closeButton,"Abort","btnLayout")
myUI.execute()
if (myUI.value("Change Job")==1):
    modjobValues=rrJob.getClass_SettingsOnly()
    modjobValues.seqStart=myUI.value("spinStart")
    modjobValues.seqEnd=myUI.value("spinEnd")
    modjobFlags=rrJob.getClass_SettingsOnly()
    modjobFlags.seqStart=1;
    modjobFlags.seqEnd=1;
    modjobList =[]
    modjobList.append(job.ID)
    print("    Changing job "+job.IDstr()+"  min="+str(modjobValues.seqStart)+"  max="+str(modjobValues.seqEnd))
    if not rr.jobModify(modjobList  ,modjobValues, modjobFlags):
        rrGlobal.messageBox(rrGlobal.logLvL.warning, "Unable to modify job","","", False,30)

del myUI

