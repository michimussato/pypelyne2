
#include "RR_DataTypes_jobsClasses_SDK.h"
#include "RR_DataTypes_jobs_comm_SDK.h"
#include "RR_DataTypes_RR_SDK.h"
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
    #include "../shared/RR_DataTypes_RenderApp.h"
#endif


#ifdef QT_CORE_LIB
  #include <QStringList>
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


_JobSend::_JobSend()
:_JobSave()
{
	rrClearSend(true);
}





void _JobSend::rrClearSend(bool
                           #ifdef defrrServerconsole
                           isRR70
                           #endif
                           )
{
    m_infoAverageMemoryUsage=0;
    m_framesTotalNonMulti=  int(((m_seqEnd - m_seqStart) / m_seqStep)+1);
	if (m_imageMulti>0)	
		 m_framesTotal= m_framesTotalNonMulti*m_imageMulti;
	else m_framesTotal= m_framesTotalNonMulti;
	m_framesLeft= m_framesTotal-m_framesDone;
	m_infoLastFrameDone=-1;
    m_infoAverageFrameTime=0;
	m_clients_rendering_count=0;
	m_fileserverTimeDifference=rrFileserverTimeDifference_InitValue;
	m_fileserverTimeDifferenceOffset=0;
	m_framesUnAssignedFoundNr=0;
	m_framesPlaceholderFound=0;
	m_renderTime_remaining_seconds=-9999;
	m_renderTime_remaining_PS=-9999;
	m_isRendering=false;
	m_lastChecked.value=0;
	m_clientNeed=0;
	m_deleteJob=false;
	StructureIDSend=StructureID_JobSend;
	VariablesIDSend=VariablesID_JobSend;
	m_check_next_seconds=10;
    m_foldersearchtime=0;
#ifdef defrrServerconsole
    calcPreviewSteps(isRR70);
#endif
}







qint64	_JobSend::fn2F(double FileFrameNumber,qint8 MultiFrameID) const
{
	/*if (ImageSingleOutputFile) {
		if (m_imageMulti) return MultiFrameID;
		else return 0; 
	}*/
	double helper=((FileFrameNumber-m_seqFileOffset)-m_seqStart);
	if (helper<0) return -1;
	helper= (helper / m_seqStep) ;
	if (m_imageMulti) helper+=m_framesTotalNonMulti*MultiFrameID;
	if (helper>=m_framesTotal) return m_framesTotal-1;
	return rrRound(helper);
}

double _JobSend::F2fn(qint64 JobFrameNumber,qint8 *MultiFrameID) const
{
/*	if (ImageSingleOutputFile) {
		if (MultiFrameID) *MultiFrameID=(JobFrameNumber & 0xFF);
		return ((JobFrameNumber % framesTotalNonMulti) * SeqStep)+SeqStart-SeqFileOffset;
	}*/
	if (MultiFrameID) *MultiFrameID= (JobFrameNumber / m_framesTotalNonMulti) & 0xFF;
	return ((JobFrameNumber % m_framesTotalNonMulti) * m_seqStep)+m_seqStart+m_seqFileOffset;
}



double _JobSend::F2fnNoOffset(qint64 JobFrameNumber,qint8 *MultiFrameID) const
{
	/*if (ImageSingleOutputFile) {
		if (MultiFrameID) *MultiFrameID=(JobFrameNumber & 0xFF);
		return 0;
	}*/
	if (MultiFrameID) *MultiFrameID= (JobFrameNumber / m_framesTotalNonMulti) & 0xFF;
	return ((JobFrameNumber % m_framesTotalNonMulti) * m_seqStep)+m_seqStart;
}

void _JobSend::addLogUser(qint16 whoMachine, qint16 whoUser, qint8 what, qint16 param1, quint8 param2)
{
    qint16 start= param1;
    quint8 step=param2;
    qint16 end=whoUser;
    addLogFrames(whoMachine,what,start,end,step);
}

#ifdef defrrServerconsole

void _JobSend::addLogServerJob(qint8 what, quint64 otherjob)
{
    _IDShort tmp;
    tmp.fromID(otherjob);
    QString t2=tmp.str();

    quint32 shortID=tmp.int32();
    quint16 end= (shortID >> 16 ) & 0xFFFF;
    quint16 start= shortID & 0xFFFF;

    _IDShort ids;
    ids.fromInt32((end <<  16) + start);
    QString t7=ids.str();

    addLogFrames(rrWhoMachineServer,what,start,end,0);
}

void _JobSend::addLogServer(qint8 what ,qint16 param1,qint16 param2,quint8 param3)
{
    addLogFrames(rrWhoMachineServer,what,param1,param2,param3);
}
#endif


void _JobSend::addLogFrames(qint16 who,qint8 what,qint64  sStart,qint64  sEnd,qint64  sStep)
{
	if (m_logCount>=MaxLog) {
		int half_max;
        half_max=int(floor((float) MaxLog/2.0f));
		for (int i=half_max; i<MaxLog;i++) 
			m_log[i-half_max]=m_log[i];
        m_logCount=int(ceil((float) MaxLog/2.0f));
	}
	/*if (Status==sPostRender && log[maxLog-1].jobStatus==sPostRender && what==lReceiveJob && log[maxLog-1].what==lReceiveJob) {
		addError(0,eDoublePostExecution);
	}*/

    if (what==lAbortLowPriority) {
        if ((m_log[m_logCount-1].who==who) && (m_log[m_logCount-1].what==what)) return;
    }

	m_logCount++;
	m_log[m_logCount-1].who=who;
	m_log[m_logCount-1].what=what;
	m_log[m_logCount-1].when.setCurrentTime();

    sStep = rrRound(float(sStep)*m_seqStep);
	while (sStart<0) sStart+=0xFFFF; while (sStart> 0xFFFF) sStart-=0xFFFF;
	while (sEnd<0) sEnd+=0xFFFF; while (sEnd> 0xFFFF) sEnd-=0xFFFF;
	if (sStep<0) sStep=0; else if (sStep>0xFF) sStep=0xFF;

	m_log[m_logCount-1].sStart_job2= ((sStart) &0xFFFF);
	m_log[m_logCount-1].sEnd_user_job1= ((sEnd) &0xFFFF);
	m_log[m_logCount-1].sStep= ((sStep) &0xFF);
	if (m_clients_rendering_count>250) m_log[m_logCount-1].clRendering=250; else m_log[m_logCount-1].clRendering=(m_clients_rendering_count &0xFF);
	if (m_framesLeft<30000) m_log[m_logCount-1].fMissing=m_framesLeft;
	else m_log[m_logCount-1].fMissing=30000;
	m_log[m_logCount-1].jobStatus=m_status;

	infoChanged_JobSave();
}


#ifdef DEF_Python



QString _JobSend::jobFilesFolderName_Resolved_Python() const
{
    if (m_jobFilesFolderName.startsWith('/') || m_jobFilesFolderName.startsWith('\\') || (m_jobFilesFolderName.length>2 && m_jobFilesFolderName.value[1]==':')) {
        if (m_jobFilesFolderName.endsWith(PDs))
             return m_jobFilesFolderName;
        else return m_jobFilesFolderName+PDs;
    }

    #if (!defined(defpyRR2) && !defined(defpyRR3))
    if (rrPython_Embedded_active!=NULL) return rrPython_Embedded_active->RR.path.website + m_jobFilesFolderName+PDs;
    #endif

    return m_jobFilesFolderName;
};


QString  _JobSend::previewFilename_Base_Python(int IDnr) const
{
    if (IDnr<0) IDnr=m_previewNumberOfFrames/2;
    if (IDnr>m_previewNumberOfFrames) IDnr=m_previewNumberOfFrames-1;
    QString IFilename;
    QString FilenameAdd;
    int FrameNo= rrRound(F2fn( previewID2FrameNr(IDnr))) ;
    FilenameAdd=QString("%1").arg(FrameNo,5,10,QChar('0'));
    /*if (m_imageMulti>1) {
        int m=  m_imageMulti /2;  //m=4 preview frames per segment
        FrameNumberDisplay=QString("t%1  %2").arg(m).arg(FrameNo);
    } else {
        FrameNumberDisplay=QString("%1").arg(FrameNo);
    }*/
    IFilename=jobFilesFolderName_Resolved_Python()+QString("p%1").arg(FilenameAdd);
    return IFilename;
}

QString  _JobSend::previewFilenameThumbnail_Python(const int &IDnr) const
{
    return previewFilename_Base_Python(IDnr)+"_t.jpg";
}
QString  _JobSend::previewFilenameRGB_Python(const int &IDnr) const
{
    return previewFilename_Base_Python(IDnr)+".jpg";
}
QString  _JobSend::previewFilenameA_Python(const int &IDnr) const
{
    return previewFilename_Base_Python(IDnr)+"_a.jpg";
}
#endif //DEF_Python



QString  _JobSend::previewFilename_Base(const __RRSDK &RR,int IDnr) const
{
    if (IDnr==-1) IDnr=m_previewNumberOfFrames/4;
    else if (IDnr==-3) IDnr=m_previewNumberOfFrames*3/4;
    else if (IDnr<0) IDnr=m_previewNumberOfFrames/2;

    if (IDnr>m_previewNumberOfFrames) IDnr=m_previewNumberOfFrames-1;
    QString IFilename;
    QString FilenameAdd;
    int FrameNo= rrRound(F2fn( previewID2FrameNr(IDnr))) ;
    FilenameAdd=QString("%1").arg(FrameNo,5,10,QChar('0'));
    /*if (m_imageMulti>1) {
        int m=  m_imageMulti /2;  //m=4 preview frames per segment
        FrameNumberDisplay=QString("t%1  %2").arg(m).arg(FrameNo);
    } else {
        FrameNumberDisplay=QString("%1").arg(FrameNo);
    }*/
    IFilename=jobFilesFolderName_Resolved(RR)+QString("p%1").arg(FilenameAdd);
    return IFilename;
}

QString  _JobSend::previewFilenameThumbnail(const __RRSDK &RR,const int &IDnr) const
{
    return previewFilename_Base(RR,IDnr)+"_t.jpg";
}
QString  _JobSend::previewFilenameRGB(const __RRSDK &RR,const int &IDnr) const
{
    return previewFilename_Base(RR,IDnr)+".jpg";
}
QString  _JobSend::previewFilenameA(const __RRSDK &RR,const int &IDnr) const
{
    return previewFilename_Base(RR,IDnr)+"_a.jpg";
}


int _JobSend::previewID2FrameNr(const int &IDnr) const
{

	if (m_previewStart<0 || (!m_seqDivideEnabled)) {  //RR 6.0
        int sf=0;
	    if (m_imageMulti==0)
		    sf=IDnr*m_previewStep;
	    else {
		    // e.g. sequence from 1-10, image multi 4, previewStep 3, (m_previewNumberOfFrames should then be 16)
		    //we take p=11 for this example
		    int m= m_imageMulti;  //m=4 preview frames per segment
		    sf= IDnr / m; //sf=2
		    m= IDnr % m; //m=3
		    sf= sf*m_previewStep+m*m_framesTotalNonMulti;   //2*3=6  + m*framesTotalNonMulti=30  = 36
	    }
        return sf;
    }

    //RR 7.0:
    int base=0;
    if (m_imageMulti>1) {
        base= (m_imageMulti/2)*m_framesTotalNonMulti;
    }
    if (IDnr==0) return base+0;
    if (IDnr==m_previewNumberOfFrames-1) return base+m_framesTotalNonMulti-1;

	if (m_rrOptions[rrRS::rroPreviewContiguous]) {
		bool quarterFrames=false;
		int midNr=m_previewNumberOfFrames-2;
		if (midNr<0) midNr=2;
		if (m_previewNumberOfFrames>7) {
			quarterFrames= true;
			midNr-= 2;
		}
		if (quarterFrames) {
			if (IDnr==1) return base+m_framesTotalNonMulti/4;
			if (IDnr==m_previewNumberOfFrames-2) return base+m_framesTotalNonMulti/4+m_framesTotalNonMulti/2;
		}
		return ((m_framesTotalNonMulti-midNr)/2)+(IDnr-1);
	} else {
		return base + m_previewStart+ m_previewStep*(IDnr-1);
	}
}











bool _JobSend::isRightStructVersion()
{
    return 
        (
        (StructureIDBasics==StructureID_JobBasics) 
        && (VariablesIDBasics>=VariablesID_JobBasics)
        && (StructureIDSubmitter==StructureID_JobSubmitter)
        && (VariablesIDSubmitter>=VariablesID_JobSubmitter)
        && (StructureIDSave==StructureID_JobSave)
        && (VariablesIDSave>=VariablesID_JobSave)
        && (StructureIDSend==StructureID_JobSend)
        && (VariablesIDSend>=VariablesID_JobSend)
        );
}



_JobMinInfo _JobSend::toMinInfo()
{
    _JobMinInfo info; 
    exportMinInfo(info); 
    return info;
};

void  _JobSend::exportMinInfo(_JobMinInfo &info)
{
	info.m_ID= m_ID;
	info.m_userName= m_userName;
	info.m_softName= m_soft.name;
	info.m_companyProjectName= m_companyProjectName;
	info.m_queueIDAtServer=m_queueIDAtServer;
    info.m_filterMask=0;
    if (m_isRendering) info.m_filterMask+=_JobMinInfo_isRendering;
    if (m_disabled)	 info.m_filterMask+=_JobMinInfo_isDisabled;
    bool isWait=(m_status<=sWaitForJobs) || (m_status==sWaitForApprovalMain) || (m_status==sWaitForApprovalDone);
    if (isWait)		 info.m_filterMask+=_JobMinInfo_isWaitFor;
    if (m_status>=sFinished) info.m_filterMask+=_JobMinInfo_isFinished;
    if (!m_isRendering && !m_disabled && !isWait && (m_status<sFinished))  info.m_filterMask+=_JobMinInfo_isIdle;
}

void _JobSend::fromMinInfo(const rrJ::_JobMinInfo * jobMinInfo,const bool &fillQuestionMark, const bool &clearOther,const QString &projectRoot_NoAccess)
{
    if (clearOther) {
        rrClearBasics();
        rrClearSubmitter();
        rrClearSave();
        rrClearSend(true);
        if (rrHasFlag(jobMinInfo->m_filterMask,_JobMinInfo_isFinished)) m_status=sFinished;
        else if (rrHasFlag(jobMinInfo->m_filterMask,_JobMinInfo_isWaitFor)) m_status=sWaitForJobs;
        else  m_status=sPreviewRender;
        m_disabled=rrHasFlag(jobMinInfo->m_filterMask,_JobMinInfo_isDisabled);
    }
	m_ID= jobMinInfo->m_ID;
	m_userName= jobMinInfo->m_userName;
	m_soft.name= jobMinInfo->m_softName;
	m_companyProjectName= jobMinInfo->m_companyProjectName;
	m_queueIDAtServer=jobMinInfo->m_queueIDAtServer;
	m_isRendering=rrHasFlag(jobMinInfo->m_filterMask,_JobMinInfo_isRendering);
    m_disabled=rrHasFlag(jobMinInfo->m_filterMask,_JobMinInfo_isDisabled);
    if (rrHasFlag(jobMinInfo->m_filterMask,_JobMinInfo_isFinished)) m_status=sFinished;
    if (fillQuestionMark) {
       if (!projectRoot_NoAccess.isEmpty()) {
            m_sceneName="!Project root '"+projectRoot_NoAccess+"'cannot be accessed.";
            m_sceneDatabaseDir="?NoProjectRootAccess?";
            m_camera="?NoProjectRootAccess?";
            m_layer="?NoProjectRootAccess?";
            m_channel="?NoProjectRootAccess?";
            m_imageDir="?NoProjectRootAccess?";
            m_imageFileName="?NoProjectRootAccess?";  //DO NOT CHANGE (jobImageOut[0]==?) is used for loading preview images
            m_seqStart=-1;
            m_seqEnd=-1;
        } else {
            m_sceneName="?waiting for update. Or user right to view is missing.";
            m_sceneDatabaseDir="?update?";
            m_camera="?update?";
            m_layer="?update?";
            m_channel="?update?";
            m_imageDir="?update?";
            m_imageFileName="?update?";//DO NOT CHANGE (jobImageOut[0]==?) is used for loading preview images
            m_seqStart=-1;
            m_seqEnd=-1;
}
    }
}


#if (defined(defrrServerconsole) || defined(defrrServer)  || defined(defrrControl))
    #define isAllowed(SettingsName) ((rApp==NULL) || (rApp->settings.s[rrRS::rs##SettingsName ]->allowChange))
#else
    #define isAllowed(SettingsName) (true)
#endif

#if (defined(defrrServerconsole) || defined(defrrServer)  || defined(defrrControl))
    #define isAllowed_rro(SettingsName) ((rApp==NULL) || (rApp->settings.s_RRoption_byID( SettingsName)->allowChange))
#else
    #define isAllowed_rro(SettingsName) (true)
#endif


#if (defined(defrrServerconsole) || defined(defrrServer)  || defined(defrrControl) || defined(defpyRR2)|| defined(defpyRR3)|| defined(defnodeJsRR))

#if (defined(defrrServerconsole) || defined(defrrServer)  || defined(defrrControl))
void _JobSend::setSettingsOnly_Send(_SettingsOnly &NewSettings,_SettingsOnly &BooleanSettings,rrRA::_RenderApp *rApp)
#else
void _JobSend::setSettingsOnly_Send(_SettingsOnly &NewSettings,_SettingsOnly &BooleanSettings,rrRA::_RenderApp *)
#endif
{
	//Missing: Check if each setting is allowed by render app
    double		OldSeqStart,
				OldSeqEnd,
                OldSeqStep,
                OldSeqFileOffset;
	qint32		OldframesTotalNonMulti;
	OldSeqStart=m_seqStart;
	OldSeqEnd=m_seqEnd;
	OldSeqStep=m_seqStep;
	OldSeqFileOffset=m_seqFileOffset;
	OldframesTotalNonMulti=m_framesTotalNonMulti;

    //Missing: Check if each setting is allowed by render app
	if (BooleanSettings.m_seqStart)       m_seqStart=NewSettings.m_seqStart;
	if (BooleanSettings.m_seqEnd)         m_seqEnd=NewSettings.m_seqEnd;
	if (BooleanSettings.m_seqStep)        m_seqStep=NewSettings.m_seqStep;
	if (BooleanSettings.m_seqFileOffset) m_seqFileOffset=NewSettings.m_seqFileOffset;
	if (BooleanSettings.m_verboseLevel) m_verboseLevel=NewSettings.m_verboseLevel;
	if (BooleanSettings.m_renderQuality) m_renderQuality=NewSettings.m_renderQuality;
	if (BooleanSettings.m_priority) m_priority=NewSettings.m_priority;
	if (!BooleanSettings.m_notifyFinish.isEmpty()) m_notifyFinish=NewSettings.m_notifyFinish;
	if (BooleanSettings.m_notifyFinishWhen) m_notifyFinishWhen=NewSettings.m_notifyFinishWhen;
	if (BooleanSettings.m_notifyFinishParam) m_notifyFinishParam=NewSettings.m_notifyFinishParam;
	if (BooleanSettings.m_notifyFinishClientName.length) m_notifyFinishClientName=NewSettings.m_notifyFinishClientName;
	if (BooleanSettings.m_timeToEnable.value) m_timeToEnable=NewSettings.m_timeToEnable;
	if (BooleanSettings.m_previewNumberOfFrames) m_previewNumberOfFrames=NewSettings.m_previewNumberOfFrames;
    QStringList boolnames, boolvalues;  
    QStringList names, values;  
    NewSettings.custom_All(names, values);  
    BooleanSettings.custom_All(boolnames, boolvalues);  
    for (int v=0; v<values.count(); v++) {
        if (boolvalues.at(v).length()>0) {
            customSet_Str(names.at(v),values.at(v));
        }
    }
	if isAllowed(UserName) 	                if (BooleanSettings.m_userName.length) m_userName=NewSettings.m_userName;
	if isAllowed(CustomSeQName) 		    if (BooleanSettings.m_customSeQName.length) m_customSeQName=NewSettings.m_customSeQName;	if isAllowed(CustomSHotName) 			if (BooleanSettings.m_customSHotName.length) m_customSHotName=NewSettings.m_customSHotName;
	if isAllowed(CustomVersionName) 		if (BooleanSettings.m_customVersionName.length) m_customVersionName=NewSettings.m_customVersionName;
	if isAllowed(AdditionalCommandlineParam)if (BooleanSettings.m_additionalCommandlineParam.length) m_additionalCommandlineParam=NewSettings.m_additionalCommandlineParam;
	if isAllowed(CompanyProjectName) 		if (BooleanSettings.m_companyProjectName.length) m_companyProjectName=NewSettings.m_companyProjectName;
    if isAllowed(Color_ID) 			        if (BooleanSettings.m_color) { m_color=NewSettings.m_color; setRandomColor(); }
	if isAllowed(SeqDivMin)                 if (BooleanSettings.m_seqDivMin) 
	{
		m_seqDivMin=NewSettings.m_seqDivMin;
		m_seqDivMinOrg=m_seqDivMin;
	}
    if isAllowed(SeqDivMax)                 if (BooleanSettings.m_seqDivMax) {
		m_seqDivMax=NewSettings.m_seqDivMax;
		m_seqDivMaxOrg=m_seqDivMax;
	}
    if isAllowed(MaxClientsAtATime)         if (BooleanSettings.m_maxClientsAtATime) m_maxClientsAtATime=NewSettings.m_maxClientsAtATime;
    if isAllowed(RequiredMemory)            if (BooleanSettings.m_requiredMemoryGB) m_requiredMemoryGB=NewSettings.m_requiredMemoryGB;
	if isAllowed(MaxFrameTime) 	            if (BooleanSettings.m_maxFrameTime) m_maxFrameTime=NewSettings.m_maxFrameTime;
	if isAllowed(MaxCrashes) 	            if (BooleanSettings.m_maxCrashes) m_maxCrashes=NewSettings.m_maxCrashes;
	if isAllowed(MaxLimitsReached) 	        if (BooleanSettings.m_maxLimitsReached) m_maxCrashes=NewSettings.m_maxLimitsReached;
	if isAllowed(MinFileSizeKb)             if (BooleanSettings.m_minFileSizeKb) m_minFileSizeKb=NewSettings.m_minFileSizeKb;

	for (int i=0; i<rrRS::rroTotalrrOptions; i++) {
        if isAllowed_rro(i)          if (BooleanSettings.m_rrOptions[i]) m_rrOptions[i]=NewSettings.m_rrOptions[i];
	}


	for (int i=0; i<rrRS::MaxPrePostCommand; i++) {
		if (BooleanSettings.m_prePostCommands[i].enabled) {
			QString UpCommandName;
			UpCommandName=NewSettings.m_prePostCommands[i].name;
			UpCommandName=UpCommandName.toUpper();
            #if (defined(defrrServerconsole) || defined(defrrServer)  || defined(defrrControl))
			bool AllowChange = true;
            if (rApp!=NULL) {
                rrRS::_renderSetting_PrePost * const opt= rApp->settings.s_PrePost(UpCommandName);
                if (opt!=NULL) AllowChange=opt->allowChange;
            }
			if (!AllowChange) continue;
            #endif
			int FoundID=-1;
			for (int a=0; a<m_prePostCommandMax; a++) {
				if (_rrStringCompareShort(UpCommandName, m_prePostCommands[a].name )) {
					FoundID=a;
					break;
				}
			}
			if (FoundID>=0) {
				m_prePostCommands[FoundID]=NewSettings.m_prePostCommands[i];
			} else if (m_prePostCommandMax<rrRS::MaxPrePostCommand){
				m_prePostCommandMax++;
				m_prePostCommands[m_prePostCommandMax-1]=NewSettings.m_prePostCommands[i];
			}
		}
	}

	for (int i=0; i<rrRS::MaxCustomOptions; i++) {
		if (BooleanSettings.m_customOptions[i].enabled) {
			QString UpCommandName;
			UpCommandName=NewSettings.m_customOptions[i].name;
			UpCommandName=UpCommandName.toUpper();
            #if (defined(defrrServerconsole) || defined(defrrServer)  || defined(defrrControl))
			bool AllowChange = true;
            if (rApp!=NULL) {
                rrRS::_renderSetting_Customoption * const opt= rApp->settings.s_Customoption(UpCommandName);
                if (opt!=NULL) AllowChange=opt->allowChange;
            }
			if (!AllowChange) continue;
            #endif
			int FoundID=-1;
			for (int a=0; a<m_customOptionsMax; a++) {
				if (_rrStringCompareShort(UpCommandName, m_customOptions[a].name )) {
					FoundID=a;
					break;
				}
			}
			if (FoundID>=0) {
				m_customOptions[FoundID]=NewSettings.m_customOptions[i];
			} else if (m_customOptionsMax<rrRS::MaxCustomOptions){
				m_prePostCommandMax++;
				m_customOptions[m_prePostCommandMax-1]=NewSettings.m_customOptions[i];
			}
		}
	}

    m_framesTotalNonMulti=  int(((m_seqEnd - m_seqStart) / m_seqStep)+1);
	if (m_imageMulti)	
		 m_framesTotal=m_framesTotalNonMulti*m_imageMulti;
	else m_framesTotal=m_framesTotalNonMulti;
	m_framesLeft=m_framesTotal-m_framesDone;

	if (BooleanSettings.m_waitForIDs[0]) {
		memcpy(m_waitForIDs ,NewSettings.m_waitForIDs,MaxWaitFor*sizeof(quint64));
		if (m_waitForIDs[0]>0) m_status=sWaitForJobs;
	}
}
#endif //#if (defined(defrrServerconsole) || defined(defrrServer)  || defined(defrrControl) || defined(pyRR2)|| defined(pyRR3))




QString _JobSend::companyProjectRootFolder(const __RRSDK &RR) const
{
	QString NewName;
	switch (RR.cfgGetI(cfgjGetProjectNameBy)) {
		case 1:
			NewName=m_userName;
			if (NewName==("<User>")) NewName=RR.app.ourProcessUser;
			break;
		case 2: 
			NewName=m_sceneDatabaseDir;
			break;
		case 3: 
			{
			QString scnCopy=m_sceneName;
			scnCopy=scnCopy.replace("<Database>",m_sceneDatabaseDir,Qt::CaseInsensitive);
			NewName=getDirectoryUntilNo(scnCopy,RR.cfgGetI(cfgjGetProjectNameByDirStart),RR.cfgGetI(cfgjGetProjectNameByDirCount));
			break;
			}
		case 4:
		default: 
			{
			QString imgCopy=m_imageDir;
			imgCopy=imgCopy.replace("<Database>",m_sceneDatabaseDir,Qt::CaseInsensitive);
			NewName=getDirectoryUntilNo(imgCopy,RR.cfgGetI(cfgjGetProjectNameByDirStart),RR.cfgGetI(cfgjGetProjectNameByDirCount));
			break;
			}
	}
    return NewName;
}


} // end namespace rrj
