
#include "RR_DataTypes_jobsClasses_SDK.h"
//#include "RR_DataTypes_RR_SDK.h"
#include "RR_defines_SDK.h"
//#include "../sharedLib/RR_files_SDK.h"
#include "math.h"


#ifndef rrPlugin
#ifdef QT_CORE_LIB
  #if (defined(defrrServerconsole))
  #endif
#endif
#endif

#ifdef DEF_RenderAppsStruct
    //#include "../shared/RR_DataTypes_RenderApp.h"
#endif



namespace  rrJ {




_JobSave::_JobSave()
:_JobSubmitter()
{
	rrClearSave();
}


void _JobSave::rrClearSave()
{
    memset(&(this->m_alignStruct_JobSave),0,sizeof(_JobSave)-sizeof(_JobSubmitter));

	if (m_previewNumberOfFrames<=1) m_previewNumberOfFrames=3;
	else if (m_previewNumberOfFrames>MaxPreviewImages) (m_previewNumberOfFrames=MaxPreviewImages);
	if (m_seqStep<=0) m_seqStep=1;
    m_previewStep=1;
    m_previewStart=-1;

	for (int p=0; p<MaxPreviewImages;p++) m_previewFrameInfo[p].value=0;
	StructureIDSave=StructureID_JobSave;
	VariablesIDSave=VariablesID_JobSave;
	infoChanged_JobSave();
}







bool _JobSave::isDisabled(_rrTime Current_time)
{
	return (m_disabled || (Current_time<m_timeToEnable) || (m_status<=sWaitForJobs) || (m_status==sWaitForApprovalMain) || (m_status==sWaitForApprovalDone)  );
}







void _JobSave::infoChanged_JobSave(_rrTime *jetzt)
{
	if (jetzt!=NULL) {
		m_lastInfoChanged=*jetzt;
	} else {
		m_lastInfoChanged.setCurrentTime();
	}
}


#ifndef rrPlugin
    #ifdef defrrServerconsole
    #endif
#endif



_rrString8_250 _JobSave::statusAsString()
{
	_rrString8_250 ret;
	if (m_disabled) ret="Disabled - ";
	//return (disabled || (Current_time<TimeToEnable) || (Status<=sWaitForJobs) || (Status==sWaitForApprovalMain) || (Status==sWaitForApprovalDone)  );
	if (m_status >=sFinished) ret+="Finished";
	else if (m_status >=sScriptFinished) ret+="Script (Finish)";
	else if (m_status >=sWaitForApprovalDone) ret+="Approval Wait";
	else if (m_status >=sScriptPostRender) ret+="Script (PostRender)";
	else if (m_status >=sMainRender) ret+="Render";
	else if (m_status >=sWaitForApprovalMain) ret+="Approval Wait";
    else if (m_status >=sScriptAfterPreview) ret+="Script (Preview)";
	else if (m_status >=sPreviewRender) ret+="Preview";
	else if (m_status >=sScriptPreRender) ret+="Script (PreRender)";
	else if (m_status >=sWaitForJobs) 
	{
		int noWaits=0;
		for (int iw=0; iw<MaxWaitFor;iw++) {
			if (m_waitForIDs[iw]!=0) noWaits++;
			else break;
		}
        _rrString8_250 strgTMP;
        if (noWaits==1) strgTMP="Wait for 1 job";
        else createArgString8(strgTMP,"Wait for %d jobs",noWaits);
        ret+=strgTMP;
	}
	else ret+="First Check";

	return ret;
}




bool _JobSave::isJobMarkedAsError()
{
	return ((m_errorCountServer>0) || (m_errorCount>5));
}





} // end namespace rrj
