#ifndef RR_DataTypesJobsCommSDK_H
#define RR_DataTypesJobsCommSDK_H

#include "RR_defines_features_classid_SDK.h"
#include "RR_defines_SDK.h"
#include "RR_DataTypes_jobs_SDK.h"
#include "RR_DataTypes_RenderApp_SDK.h"
//#include "RR_DataTypes_client_SDK.h"
#include "RR_DataTypes_jobsClasses_SDK.h"



#ifdef QT_CORE_LIB
	#include <QString>
#endif



namespace rrRA { 
    //struct _RenderApp;
    }



namespace rrJ { 

#pragma pack(4)  //4-byte alignment



#define _JobMinInfo_isIdle	      1
#define _JobMinInfo_isRendering  (1 << 1)
#define _JobMinInfo_isDisabled	 (1 << 2)
#define _JobMinInfo_isWaitFor	 (1 << 3)
#define _JobMinInfo_isFinished	 (1 << 4)
#define _JobMinInfo_filterAll    (0xFF)  //All jobs

enum _JobFilterIDs { 
	jfIsIdle = _JobMinInfo_isIdle,
	jfIsRendering = _JobMinInfo_isRendering,
	jfIsDisabled = _JobMinInfo_isDisabled,
	jfIsWaitFor = _JobMinInfo_isWaitFor,
	jfIsFinished = _JobMinInfo_isFinished,
	jfIsAll = _JobMinInfo_filterAll
};


struct _JobMinInfo
{
    quint64		m_ID;
    _rrString25	m_userName;
    _rrString50	m_companyProjectName;
    _rrString25	m_softName;
    qint32		m_queueIDAtServer;
    quint8      m_filterMask;
	#ifdef QT_CORE_LIB
	QString		IDstr() const;
	#endif
};


struct _jobListRequest
{
    enum _requestType {rMinInfoOnly, rJobBasic, rJobSend };
	_jobListRequest(){memset(this,0,sizeof(_jobListRequest));  StructureID=StructureID_jobListRequest; };
    quint16			StructureID;
    _rrTime         m_lastSend_ServerTime;
    _rrString50     m_contains;
    _rrString50     m_project;
    _rrString25     m_user;
    _rrString25     m_renderApp;
    quint8          m_filterMask;
    quint64         m_jobID;
    quint8          m_requestType;
    bool            rightStructureVersion() {return (StructureID == StructureID_jobListRequest); };
};


class _jobListSend {
private:
public:
	quint16			StructureID;
    _rrTime         m_sendServerTime;
    qint16			m_minInfoCount;
    _JobMinInfo		m_minInfo[MaxJobs]; 	//List of all jobs
    qint16			m_jobInfoCount;
    quint8          m_jobInfoType;          //_JobBasics=2, _JobSend=3
    //job data is appended later as zip chunks


    void clear() { memset(this, 0, sizeof(_jobListSend)); StructureID=StructureID_jobList; };
    _jobListSend()  {clear();};
    bool            rightStructureVersion() {return (StructureID == StructureID_jobList); };
};


#define JobSettingsOnlyFree_MAX 30-2-1

struct _SettingsOnly
{
	//Missing: recheck if all params in
    double		m_seqStart,
                m_seqEnd,
                m_seqStep,
                m_seqFileOffset;
    _rrString25	m_userName;
    _rrString25	m_customSeQName;
    _rrString25	m_customSHotName;
    _rrString25	m_customVersionName;
    _rrString50	m_companyProjectName;
    _rrString250	m_additionalCommandlineParam;

    quint32		m_color;

    quint16		m_seqDivMin,
                m_seqDivMax;
	
    qint16		m_maxClientsAtATime;
    qint32		m_maxFrameTime;
	
    rrRS::_PrePostCommand   m_prePostCommands	[rrRS::MaxPrePostCommand];
    bool                    m_rrOptions		[rrRS::MaxRROptions];
    rrRS::_CustomOptions	m_customOptions	[rrRS::MaxCustomOptions];
    quint8		m_customOptionsMax;
    quint8		m_prePostCommandMax;
    quint8		m_rrOptionsMax;

    qint8		m_verboseLevel;
    qint8		m_renderQuality;

    quint64		m_waitForIDs[rrJ::MaxWaitFor];
    qint8		m_priority;
    qint8		m_dataAlignFix_Linux;
    _rrString25	m_notifyFinish;
    qint8		m_notifyFinishParam;
    qint8		dataAlignFix_Linux2;
    _rrString25	m_notifyFinishClientName;
    quint8		m_notifyFinishWhen;
    qint8		m_dataAlignFix_Linux3;
    qint8		m_dataAlignFix_Linux4;
    _rrTime     m_timeToEnable;
    qint8		m_previewNumberOfFrames;
    qint8		m_maxCrashes;
    qint32      m_requiredMemoryGB;
    int         m_customData_MaxValues;
    int         m_customData_MaxBufferUsage;
    int         m_customData_FirstValuePos;
    quint8      m_customDataBlock[CUSTOMDataBlockSize];
    quint16		m_minFileSizeKb;
    qint8		m_maxLimitsReached;
    qint8		m_jobSubmitterFree[JobSettingsOnlyFree_MAX];

#ifdef QT_CORE_LIB
    QString     custom_UserInfo() const;
    void        customSet_UserInfo(const QString &info);
    int         custom_maxIDs() const;
    QString     custom_StrByID(const int &id) const;
    QString     custom_NameByID(const int &id) const;
    void        customSet_StrByID(const int &id,const QString &value);
    QString     custom_Str(const QString &name) const;
    void        customSet_Str(const QString &name,const QString &value);
    void        custom_All(QStringList &names, QStringList &values) const; //    QStringList names, values;  pJob->custom_All(names, values);  for (int v=0; v<values.count(); v++) {
    void        customSet_All(const QStringList &names,const QStringList &values);
    QString     custom_sub(const int &position,const int &length,const CUSTOMData_Modes &mode) const;
#endif
    bool		rrOptions_Get(const int &id) {return m_rrOptions[id]; };

};




class _JobCommandSend {

private:
public:
	_JobCommandSend(qint16 UserID);
	_JobCommandSend();
    qint16		m_count;
    qint16		m_userID;
    quint64		m_jobIDs[MaxJobsCommandArray];
    quint8		m_jobCommand;
	
    quint64		m_param1;
    quint64		m_param2;
    qint64		m_param3;//unused and not transfered to job
    qint64		m_param4;//unused and not transfered to job
    
    #ifdef QT_CORE_LIB
	QString		idsAsString();
    #endif
};




class _JobSettingsSend{
private:
public:
	_JobSettingsSend();
    quint16         StructureID;
    quint16         VariablesID;
    qint16          m_count;
    qint16          m_userID;
    quint64         m_jobIDs[MaxJobsCommandArray];
    _SettingsOnly   m_jobValues, m_jobEnable; //enable is just used as boolean
    #ifdef QT_CORE_LIB
    QString         idsAsString();
    #endif
	void clear();
};


class _JobBasicNew {
public:
    _JobBasicNew() {StructureID=StructureID_JobBasicNew; m_job.rrClearBasics(); overrideParameter.clear(); };
    quint16          StructureID;
    _rrString1000    overrideParameter;
    rrJ::_JobBasics  m_job;

    bool rightStructureVersion() {return ((StructureID == StructureID_JobBasicNew) && (m_job.StructureIDBasics == StructureID_JobBasics) ); };
};


#pragma pack()  //restore default alignment


#ifdef QT_CORE_LIB
    QString	ID2str(const quint64 &ID);
    QString	ID2strFull(const quint64 &ID);
    QString	jobStatusAsString(quint8 Status);
    void    getSSV(QString name,_rrString25 &scene,_rrString25 &shot,_rrString25 &version, QString sceneCfg, QString shotCfg, QString versionCfg, QString sceneCfgEnd, QString shotCfgEnd, QString versionCfgEnd, int sceneCfgLength, int shotCfgLength );
#endif



} //endNamespace

#endif

