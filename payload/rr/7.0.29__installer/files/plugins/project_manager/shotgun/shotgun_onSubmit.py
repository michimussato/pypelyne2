import  rrGlobal
import  rrSG
import  rr

def submitRender():
    rrGlobal.progress_SetMaxA(3)
    rrGlobal.progress_SetProgressA(0)
    rrGlobal.refreshUI()
    import royalRifle
    global rRifle
    rRifle=royalRifle.RoyalRifle()
    rrGlobal.progress_SetProgressA(1)
    rrGlobal.refreshUI()


    jobFirst= rr.jobSelected_get(0)
    submitUser=jobFirst.userName
    projectName=jobFirst.companyProjectName
    sequenceId=jobFirst.customSeqName
    shotId=jobFirst.customShotName
    if (len(sequenceId)>0):
        shotId=sequenceId+"-"+shotId
#    rrGlobal.messageBox(rrGlobal.logLvL.info, "shotId is " +str(shotId),"","", False,30)
    renderDataList = []
    for jNr in range(0, rr.jobSelected_count()):
        job= rr.jobSelected_get(jNr)
        renderDataAdd = {'job_id':job.IDstr(), 'render_pass':job.layer, 'render_camera':job.camera, 'render_application':job.renderer.name, 'render_scene_name':job.sceneName, 'frames':int(job.framesTotal)}
        renderDataList.append(renderDataAdd)

    #create new submit and render entity
    submitEntity=rRifle.submitRender(renderDataList, submitUser, projectName, sequenceId, shotId, taskId=None)
    #debug: warning, very very long string...#  rrGlobal.messageBox(rrGlobal.logLvL.info, "SubmitEntity is " +str(submitEntity),"","", False,30)
    rrGlobal.progress_SetProgressA(2)
    for jNr in range(0, rr.jobSelected_count()):
        job= rr.jobSelected_get(jNr)
        shreID= rRifle.getRenderEntityFromRRJobId(job.IDstr())
        shreID=str(shreID['id'])
        #rrGlobal.messageBox(rrGlobal.logLvL.info, "RenderEntity of job is " +str(shreID),"","", False,30)
        rr.jobAll_setShotgunID(jNr,shreID)
        #job= rr.jobSelected_get(jNr)
        #rrGlobal.messageBox(rrGlobal.logLvL.info, "RenderEntity of job is " +str(job.shotgunID),"","", False,30)
        #job.shotgunID=shreID
        #rr.jobSelected_set(jNr,job)
        #job= rr.jobSelected_get(jNr)
        #rrGlobal.messageBox(rrGlobal.logLvL.info, "RenderEntity of job is " +str(job.shotgunID),"","", False,30)
    rrGlobal.progress_SetProgressA(3)

submitRender()
