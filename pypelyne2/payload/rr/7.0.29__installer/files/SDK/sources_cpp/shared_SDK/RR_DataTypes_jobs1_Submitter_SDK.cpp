
#include "RR_DataTypes_jobsClasses_SDK.h"
#include "RR_DataTypes_RR_SDK.h"
#include "RR_defines_SDK.h"
#include "../sharedLib/RR_files_SDK.h"
//#include "math.h"


#ifndef rrPlugin
#ifdef QT_CORE_LIB
  #if (defined(defrrServerconsole))
  #endif
#endif
#endif

#ifdef DEF_RenderAppsStruct
    //#include "../shared/RR_DataTypes_RenderApp.h"
#endif


#ifdef DEF_Python
#undef slots
#undef signals
#undef METHOD
#undef SIGNAL
#undef SLOT
#include "../shared/RR_Python_embedded.h"
#endif



namespace  rrJ {


_JobSubmitter::_JobSubmitter()
:_JobBasics()
{
	rrClearSubmitter();
}





void	_JobSubmitter::rrClearSubmitter()
{
	m_alignStruct_JobSubmitter=0;
	m_userName.clear();
	m_userName="none";
	m_submitMachine.clear();
	m_customSeQName.clear();
	m_customSHotName.clear();
	m_customVersionName.clear();
	m_companyProjectName.clear();
	m_imageFormatOverride.clear();
	m_additionalCommandlineParam.clear();
	m_dateSend.setCurrentTime();
	m_color= 0;
	m_seqDivideEnabled=true;
	m_seqDivMin=10;
	m_seqDivMax=25;
	m_maxClientsAtATime=rrC::MaxClients;
	m_maxFrameTime=0;
    m_maxCrashes=30;
	m_maxLimitsReached=30;
	m_disabled=false;
	memset(m_clients,0,sizeof(_jClient)*rrC::MaxClients);
	//for (int c=0; c<rrC::MaxClients; c++ ) { clients[c].satellite_with_master=-1;	}
	memset(m_prePostCommands,0,sizeof(rrRS::_PrePostCommand)*rrRS::MaxPrePostCommand);
	memset(m_rrOptions,0,rrRS::MaxRROptions);
	memset(m_customOptions,0,sizeof(rrRS::_CustomOptions)*rrRS::MaxCustomOptions);
	m_customOptionsMax=0;
	m_prePostCommandMax=0;
	m_rrOptionsMax=0;
	m_verboseLevel=0;
	m_renderQuality=0;
	m_priority=50;
	memset(m_waitForIDs,0,MaxWaitFor*sizeof(quint64));
	m_notifyFinish.clear();
	m_notifyFinishClientName.clear();
	m_notifyFinishParam=0;
	m_timeToEnable.value=m_dateSend.value - 50*24*60*60;
	m_jobFilesFolderName.clear();
	m_jobFilesFolderName="none";
	m_previewNumberOfFrames=5;
	m_localTexturesCount=0;
	m_localTexturesSizeMB=0;
	memset(m_jobSubmitterFree,0,JobSubmitterFree_MAX);
	StructureIDSubmitter=StructureID_JobSubmitter;
	VariablesIDSubmitter=VariablesID_JobSubmitter;
    m_customSeQName="<auto>";
    m_customVersionName="<auto>";
    m_customSHotName="<auto>";
    m_requiredMemoryGB=0;
	m_minFileSizeKb=0;
}



#ifndef rrPlugin
#ifdef DEF_Python
#endif //DEF_Python
#ifdef RR_OS_WIN
#else
#endif
#endif //rrPlugin




#ifdef QT_CORE_LIB

#ifndef rrPlugin
#endif //!plugin



QString	_JobSubmitter::getJobLogString(bool IsPreviewRendering, int freezetime)
{
	QString Res;
    Res+=ID2str();
    if (freezetime>3)
        Res+=" Low CPU " +QString::number(freezetime)+ "min  ";
	Res+=" "+m_companyProjectName+"|"+m_soft.name+"|";
	Res+=m_customSeQName+"-"+m_customSHotName+"-"+m_customVersionName+"|";
	if (IsPreviewRendering) Res+="PREVIEW|";
	

    QString scene_cut;
    int position;
    if (!m_sceneName.startsWith('?')) {
	    scene_cut = m_sceneName;
	    
	    position = scene_cut.lastIndexOf('.');
	    if (position>3) scene_cut.truncate(position);
	    scene_cut.remove(PDs+"RENDER_PICTURES",Qt::CaseInsensitive);
	    scene_cut.remove(PDs+"Scenes",Qt::CaseInsensitive);
	    scene_cut.remove(PDs+PDs);


	    scene_cut.replace(":"+PDs,"))))");	// next functions should not chnage drive:
	    scene_cut.replace(PD,"((((");			// woraround to replace "\" with " \ ", otherwise we could have an infinite loop
	    scene_cut.replace("((((",QString(" ")+PD+QString(" ")); 
	    scene_cut.replace("))))",":"+PDs);			
    }

	position=Res.size()+scene_cut.size();
	if (position>55) 
		  Res+=scene_cut.right(55- Res.size());
	else  Res+=scene_cut + QString(55-position,' ');

	return Res;
}


QString	_JobSubmitter::getJobLogStringShort(bool , int freezetime)
{
	QString Res;
    Res+=ID2str();
    if (freezetime>3) Res+=" LowCPU " +QString::number(freezetime)+ "min|";
    Res+=m_soft.name.left(4)+"|"+m_companyProjectName.left(10);
	//Res+=CustomSeQName+"-"+CustomSHotName+"-"+CustomVersionName+"|";
	return Res;
}


QString _JobSubmitter::jobFilesFolderName_Resolved(const __RRSDK &RR) const
{
    if (m_jobFilesFolderName.startsWith('/') || m_jobFilesFolderName.startsWith('\\') || (m_jobFilesFolderName.length>2 && m_jobFilesFolderName.value[1]==':')) {
        if (m_jobFilesFolderName.endsWith(PDs))
             return m_jobFilesFolderName;
        else return m_jobFilesFolderName+PDs;
    }
    return RR.path.website + m_jobFilesFolderName+PDs;
};









quint32   _JobSubmitter::ID2ShortID()
{
    _IDShort tmp;
    tmp.fromID(m_ID);
    return tmp.int32();
}

#endif // QT_CORE







} // end namespace rrj
