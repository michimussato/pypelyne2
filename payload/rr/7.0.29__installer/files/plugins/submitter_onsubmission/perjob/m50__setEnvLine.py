
#progress bar B is used for all jobs
if (rr.perJobCurrent()==0):
    rrGlobal.progress_SetMaxB(rr.perJobMax())
rrGlobal.progress_SetProgressB(rr.perJobCurrent())
#progress bar A is used for this script 
rrGlobal.progress_SetMaxA(5)
rrGlobal.progress_SetProgressA(0)
rrGlobal.refreshUI()



job= rr.getJob()

envline="MySpecial=Render; What=Scenes"
job.customSet_Str("rrEnvLine",envline)

rr.setJob(job)



