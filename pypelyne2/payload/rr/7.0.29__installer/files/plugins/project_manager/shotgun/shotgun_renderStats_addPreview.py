import  rrGlobal
import  rrSG
import  rr

def addPreview():
    rrGlobal.progress_SetMaxA(rr.jobSelected_count())
    rrGlobal.progress_SetProgressA(0)
    rrGlobal.refreshUI()
    import royalRifle
    global rRifle
    rRifle=royalRifle.RoyalRifle()



    jobFirst= rr.jobSelected_get(0)
    submitUser=jobFirst.userName
    projectName=jobFirst.companyProjectName
    sequenceId=jobFirst.customSeqName
    shotId=jobFirst.customShotName
    renderDataList = []
    for jNr in range(0, rr.jobSelected_count()):
        rrGlobal.progress_SetProgressA(jNr)
        rrGlobal.refreshUI()
        job= rr.jobSelected_get(jNr)
        shreID=job.shotgunID
        if (len(shreID)<=1):
            print("Job has no Shotgun ID.")
            continue
        pathList = []
        pathList.append(job.previewFilenameThumbnail(0))
        pathList.append(job.previewFilenameThumbnail(-1))
        pathList.append(job.previewFilenameThumbnail(99))
        rRifle.addPreviewImages(shreID, pathList)
  

addPreview()
