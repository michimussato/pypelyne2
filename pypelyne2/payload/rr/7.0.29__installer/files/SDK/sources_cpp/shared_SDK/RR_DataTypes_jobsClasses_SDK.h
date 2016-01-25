#ifndef RR_DataTypesJobsClassesSDK_H
#define RR_DataTypesJobsClassesSDK_H

#include "RR_defines_features_classid_SDK.h"
#include "RR_defines_SDK.h"
#include "RR_DataTypes_jobs_SDK.h"
#include "RR_DataTypes_RenderApp_SDK.h"
#include "RR_DataTypes_client_SDK.h"



#ifdef QT_CORE_LIB
	#include <QString>
#endif



class __RRSDK;
class __RR;

namespace rrRA { 
    struct _RenderApp;
    }



namespace rrJ { 







enum _eErrorMessage {
	eUnknown=0,
	eCrashed=1,
	eOutputdirNotFound=2,
	eNoFreeSpaceLeft=3,
	eFileserverTimeDifference=4,
	eNoFrameRendered=5,
	eSeqDivAdjusted=6,
	eToManyCrashes=7,
	eSceneNotFound=8,
	eRenderAppNotFound=9,
	eExecuteError=10,
	eNoDriveSpaceLeft=11,
	eUNCMapFailed=12,
	eNoRenderLicense=13,
	eClientRenderCrashed=14,
	eSendToOften=15,
	eClientLowSysMem=16,
	eClientRenderCrashedPermanently=17,
	eClientRenderFroze=18,
	eRenderAppWrongVersion=19,
	eClientNoRenderTimeIssue=20,
	eDoublePostExecution=22,
	eAbortFrameTime=23,
    eClientFoundLogError=24,
	eToManyLimitsReached=25,
};




#pragma pack(4)  //4-byte alignment


struct _Error
{
    qint16		who;
    qint8		what;
    _rrTime	when; 
};



struct _Log
{
  	_rrTime32	when; 
  	qint8		what;
  	quint8		jobStatus;
	quint8		clRendering;
    //if the log report was from/for a client, then the following 3 variables are the frames the client got.
    //if not, then it is the unique ID of the user or short job ID. The short job ID is split between two variables
	quint8		sStep;
    quint16		sEnd_user_job1;
    quint16		sStart_job2;
    quint16		fMissing;
    qint16		who; //machine
};



struct _jClient
{
    bool	assigned;			   // Assigned for the job
	quint8  times_sended;
	quint8  times_aborted;
	quint8  times_crashed;
    quint8	lastsend_jobStatus;
	quint8 	lastsend_ThreadID;   
    quint16	lastsend_step;
    quint32	lastsend_start;	 
	quint32	lastsend_end;
    quint16	totalFramesRendered;		// On job rendering/finished/crashed/aborted the clients sends a number of frames done (read from logfile)
    quint16	lastSegmentTimeRendered;
	quint32	totalTimeRendered;		   // render time till now
};



struct _Stat
{
	quint16		saveDelay;
	quint16		saveDelaySteps;

	quint8		maxValues;
	quint16		statsMaxClients;
	quint16		statsMaxPS;
	quint16		statsMaxAvMem;
	quint32		statsMaxFramesDone;

	struct {
        qint16 renderingClients;
        qint16 renderingPS;
        qint32 avMemoryUsage;
        qint32 framesDone;
        qint32 totalJobRenderTimeSeconds;
			}  	values[MaxStats];
} ;



//defined later:
class _JobSubmitter;
class _JobSave;
class _JobSend;
class _JobRuntime;
struct _SettingsOnly;
struct _JobMinInfo;


//##################################  class _JobBasics ############################################
//##################################  class _JobBasics ############################################
//Scene parser plugins and application plugins send _JobBasics to the submitter


class _JobBasics
{
public:
	//version information of this struct
	//Same StructureID= same memory structure. Probably just JobBasicsFree was reduced and replaced with a new variable
	//If VariablesID changed, then there are more variables than before
    quint16		StructureIDBasics;
    quint16		VariablesIDBasics;
    quint16		StructureIDSubmitter;
    quint16		VariablesIDSubmitter;
    quint16		StructureIDSave;
    quint16		VariablesIDSave;
    quint16		StructureIDSend;
    quint16		VariablesIDSend;
	quint16		StructureIDRunTime;
	quint16		VariablesIDRunTime;


    quint8		m_rrJobOS;		//path variables are currently in format ... [win/lx/max]
    quint8		m_sceneOS;		//Which OS was used to create the scene file = in which format are the texture links inside the file
    quint8		m_sceneAppBit;    //32 or 64bit

    rrRA::_RenderAppBasic m_soft;

    _rrString250	m_sceneName;
    _rrString250	m_sceneDatabaseDir;
    _rrString250	m_localTexturesFile;

    _rrString50	    m_camera;
    _rrString50	    m_layer;
    _rrString50	    m_channel;
    _rrString250	m_requiredLicenses; //for licensing, each license name tiled with ;

    _rrString250	m_imageDir;
    _rrString250	m_imageFileName;
    _rrString250	m_imageFileNameVariables;
    _rrString25	    m_imageExtension;
    char		    m_imagePreNumberLetter;
    quint8		    m_imageFramePadding;
	struct {	
            _rrString250     fileName;
            _rrString25      extension;
           }        m_imageChannels[MaxImageChannels];
    qint16		    m_imageWidth; //also used as command name
    qint16		    m_imageHeight;
    bool		    m_imageSingleOutputFile;
    _rrString25	    m_imageFormatOverride;
    qint8		    m_imageMulti;			//Multiple file output per frame, e.g. fields or single frame tiling
    _rrString10	    m_imageMultiAdd   [MaxImageMulti];
    _rrString10      m_imageStereoL;
    _rrString10      m_imageStereoR;


    double		    m_seqStart,	//max frame precision //double: 562.949.953.421.312,0  = 500 x 10^12
                    m_seqEnd,
                    m_seqStep,
                    m_seqFileOffset;
    _rrString8_100	m_seqFrameSet;		//not supported yet
    bool		    m_seqIsFloatFrames;	//not supported yet


    quint64		    m_ID;
    quint8		    m_preID;                      //used for submission and converted in new job in server
    quint8		    m_maxWaitForPreID;            //used for submission and converted in new job in server
    quint8		    m_waitForPreID[MaxWaitFor];   //used for submission and converted in new job in server

    _rrString250	    m_additionalCommandlineParam;

    int             m_customData_MaxValues;
    int             m_customData_MaxBufferUsage;
    int             m_customData_FirstValuePos;
    quint8          m_customDataBlock[CUSTOMDataBlockSize]; //FORMAT SPECS: first the names with char/unicode info, an position and length, then the data.
                                                          //u####name0c####name0c####name0u####name0datadatadatadatadatadata
    bool		    m_uiIsChecked;
    _rrString8_25   m_shotgunID;

    qint8		    m_jobBasicsFree[32];


	_JobBasics();
    void            rrClearBasics();
#ifndef rrPlugin
	#ifdef QT_CORE_LIB
	#endif
#endif

#ifdef QT_CORE_LIB
    QString	    IDstr() const;
    QString	    IDstrFull() const;
	QString		ID2str() const;
    QString		ID2strFull() const;
    QString	    getSceneDisplayName();
    QString     custom_UserInfo() const;
    void        customSet_UserInfo(const QString &info);
    int         custom_maxIDs() const;
    QString     custom_NameByID(const int &id) const;
    QString     custom_StrByID(const int &id) const;
    void        customSet_StrByID(const int &id,const QString &value);
    QString     custom_Str(const QString &name) const;
    void        customSet_Str(const QString &name,const QString &value);
    void        custom_All(QStringList &names, QStringList &values) const; //    QStringList names, values;  pJob->custom_All(names, values);  for (int v=0; v<values.count(); v++) {
    void        customSet_All(const QStringList &names,const QStringList &values);
    bool        custom_isEqual(_JobBasics * otherJob);
    QString     custom_AllAsString();
	void	    custom_ClearAll();
#endif
    void		initialize();
    void		check_SplitImageFileInto_DirFileExt(bool percentFaddingFormat=false);
    void		check_SplitImageFileInto_DirFileExt_Channel(int channel,bool percentFaddingFormat=false);
    void		replaceSquareBracketVariables();
    int         getWaitForPreID(int index) const { limitInt(rrJ::MaxWaitFor); return m_waitForPreID[index]; };
    void        setWaitForPreID(int index, const quint8 &value ) {limitInt(rrJ::MaxWaitFor); m_waitForPreID[index]=value; };
    _rrString250 channelFileName(int index) const { limitInt(rrJ::MaxImageChannels); return m_imageChannels[index].fileName; };
    void        setChannelFileName(int index, const _rrString250 &value ) {limitInt(rrJ::MaxImageChannels); m_imageChannels[index].fileName=value; };
    _rrString25  channelExtension(int index) const { limitInt(rrJ::MaxImageChannels); return m_imageChannels[index].extension; };
    void        setChannelExtension(int index, const _rrString25 &value ) {limitInt(rrJ::MaxImageChannels); m_imageChannels[index].extension=value; };

private:
#ifdef QT_CORE_LIB
    QString     custom_sub(const int &position,const int &length,const CUSTOMData_Modes &mode) const;
#endif
};




//##################################  class _JobSubmitter ############################################
//##################################  class _JobSubmitter ############################################
//The submitter sends _JobSubmitter to the Server


#define JobSubmitterFree_MAX 30-2-1

class _JobSubmitter: public _JobBasics
{
    quint32		    m_alignStruct_JobSubmitter;
public:
    _rrString25	    m_userName;
    _rrString25	    m_submitMachine; //used for command wait for last X jobs I send...
    _rrString25	    m_customSeQName;
    _rrString25	    m_customSHotName;
    _rrString25	    m_customVersionName;
    _rrString50	    m_companyProjectName;

    _rrTime         m_dateSend;
    quint8		    m_color;
    bool		    m_seqDivideEnabled;
    quint16		    m_seqDivMin,
                    m_seqDivMax;
    qint16		    m_maxClientsAtATime;
    bool	        m_disabled;
    qint32          m_requiredMemoryGB;

    
    _jClient	    m_clients[rrC::MaxClients];


    rrRS::_PrePostCommand	m_prePostCommands[rrRS::MaxPrePostCommand];
    quint8		            m_prePostCommandMax;
    bool					m_rrOptions [rrRS::MaxRROptions];
    quint8		            m_rrOptionsMax;
    rrRS::_CustomOptions	m_customOptions  [rrRS::MaxCustomOptions];
    quint8		            m_customOptionsMax;


    qint8           m_verboseLevel;
    qint8           m_renderQuality;
    qint8           m_priority;
    quint64         m_waitForIDs[MaxWaitFor];
    _rrString25      m_notifyFinish;
    _rrString150     m_notifyFinishClientName;
    qint8           m_notifyFinishParam;
    quint8          m_notifyFinishWhen;
    _rrTime         m_timeToEnable;
    _rrString250     m_jobFilesFolderName;

    qint8           m_previewNumberOfFrames;
    qint32          m_localTexturesCount;
    qint32          m_localTexturesSizeMB;
    qint16          m_maxFrameTime;
    qint8           m_maxCrashes;
    quint16         m_minFileSizeKb;
    qint8           m_maxLimitsReached;

    qint8           m_jobSubmitterFree[JobSubmitterFree_MAX];


	_JobSubmitter();
	void		rrClearSubmitter();

#ifdef QT_CORE_LIB
    QString		getJobLogString(bool IsPreviewRendering=false, int freezetime=0);
    QString		getJobLogStringShort(bool IsPreviewRendering=false, int freezetime=0);
    quint32     ID2ShortID();
    #ifndef rrPlugin
    #endif
    QString     jobFilesFolderName_Resolved(const __RRSDK &RR) const;
#endif
#if (!defined rrPlugin)
#endif    
//#ifdef DEF_Python
    inline bool	rrOptions_Get(const int &id) {return m_rrOptions[id]; };
    bool		clientAssigned_Get(const int &cNr) {return m_clients[cNr].assigned; };
    void		clientAssigned_Set(const int &cNr, const bool &value) {m_clients[cNr].assigned=value; };
	int			clientValue_Get(const int &cNr, const int &valueID);
//#endif

protected:

};


//##################################  class _JobSave ############################################
//##################################  class _JobSave ############################################
//The Server saves _JobSave into the database file

#define rrSaveFree_MAX (30-4-4-8-1)

class _JobSave: public _JobSubmitter
{
    quint32		m_alignStruct_JobSave;
public:

    qint8		m_errorCountServer;
    qint8		m_errorCount;
    _Error		m_errors[MaxError];
    qint16		m_logCount;
    _Log		m_log[MaxLog];
    _Stat		m_infoStat;
    qint16		m_infoTotalSend;
    qint16		m_infoTotalCrashed;
    qint16		m_infoTotalAborted;
    float		m_infoAverageClients;
    float		m_infoAverageClientPS;
    qint32		m_infoAverageFrameTime;

    bool		m_infoAnalyse_Done;
    quint8		m_infoAnalyse_error, m_infoAnalyse_warning, m_infoAnalyse_info;


    _rrTime     m_lastSettingsChanged;
    _rrTime     m_lastInfoChanged;
    _rrTime     m_lastErrorEmail;
    qint64		m_infoRenderTime_seconds;
    qint64		m_infoRenderTime_PS;
    float       m_infoRenderTime_Ghz_h;
    qint32		m_framesDone;
    quint8		m_status;
    _rrTime     m_timeFinished;
    bool		m_userApproved;
    bool		m_scriptPreviewExecuted;
    quint16		m_seqDivMinOrg,
                m_seqDivMaxOrg;
    _rrTime     m_overwriteExisting_LastOldFile;
    qint32		m_previewStart;
    qint32		m_previewStep; //RR6.0 and non-sequencedivide-jobs
    _rrTime     m_previewFrameInfo[MaxPreviewImages];
    _rrString25	m_previewFrameInfoName[MaxPreviewImages];
    qint8		m_FOI_Created;
    _rrString50	m_FOI_FileName;
    qint16		m_infoTotalLimitsReached;

    qint8		m_rrSaveFree[rrSaveFree_MAX];


	_JobSave();
 	bool		addError(qint16 who,qint8 what);
	void		infoChanged_JobSave(_rrTime *jetzt=NULL);     //Changes like frames done increased, add log message, new client rendering... displayed
    bool		isJobMarkedAsError();
    bool		isDisabled(_rrTime Current_time);
    bool        isScriptStatus() {return ((m_status==rrJ::sScriptPreRender) || (m_status==rrJ::sScriptAfterPreview) || (m_status==rrJ::sScriptPostRender) || (m_status==rrJ::sScriptFinished)); };
    _rrString8_250	statusAsString();
	void		rrClearSave();

protected:

};


//##################################  class _JobSend ############################################
//##################################  class _JobSend ############################################
//The Server sends _JobSend to Control
//Server plugins get this class as parameter

class _JobSend: public _JobSave 
{
    quint32		m_alignStruct_JobSend;
public:
    qint64		m_renderTime_remaining_seconds;
    qint64		m_renderTime_remaining_PS;
    qint32		m_framesLeft;
    qint32		m_framesTotal;
    qint32		m_framesTotalNonMulti;
    qint32		m_framesPlaceholderFound;

    qint32		m_infoLastFrameDone;
    qint16		m_clients_rendering_count;
    qint32		m_infoAverageMemoryUsage;
    quint16		m_fileserverTimeDifference;
    qint16		m_fileserverTimeDifferenceOffset;
    qint32		m_framesUnAssignedFoundNr;
    qint32		m_check_interval;
    _rrTime     m_lastChecked;
    qint32		m_check_next_seconds;
    float		m_clientNeed;

    bool		m_deleteJob;
    bool		m_isRendering;
    qint32		m_queueIDAtServer;
    quint16     m_foldersearchtime;
    quint8      m_renderLicenseNeeded;

	_JobSend();
    #ifdef defrrServerconsole
    void		addLogServer(qint8 what,qint16 param1=0, qint16 param2=0, quint8 param3=1);
    void		addLogServerJob(qint8 what, quint64 otherjob);
    void        calcPreviewSteps(bool isV70);
    #endif
    void		addLogFrames(qint16 whoMachine, qint8 what,qint64 sStart=0,qint64  sEnd=0,qint64 sStep=0);
    void		addLogUser(qint16 whoMachine, qint16 whoUser, qint8 what, qint16 param1=0, quint8 param2=0);
	void		rrClearSend(bool isRR70);
	double		F2fnNoOffset(qint64 JobFrameNumber,qint8 *MultiFrameID=NULL) const;
	qint64		fn2F(double FileFrameNumber,qint8 MultiFrameID=0) const;
	double		F2fn(qint64 JobFrameNumber,qint8 *MultiFrameID=NULL) const;
    double		F2fn_noMulti(qint64 JobFrameNumber)  const {return F2fn(JobFrameNumber);};
    qint8		F2fn_getMulti(qint64 JobFrameNumber) const {qint8 mID; F2fn(JobFrameNumber,&mID); return mID;};
    bool        isRightStructVersion();
    void        fromMinInfo(const rrJ::_JobMinInfo * jobMinInfo,const bool &fillQuestionMark, const bool &clearOther,const QString &projectRoot_NoAccess);
    #if (defined(defrrServerconsole) || defined(defrrServer)  || defined(defrrControl) || defined(defpyRR2) || defined(defpyRR3) || defined(defnodeJsRR))
    void        setSettingsOnly_Send(_SettingsOnly &NewSettings,_SettingsOnly &BooleanSettings,rrRA::_RenderApp *rApp=NULL);
	#endif
    int         previewID2FrameNr(const int &IDnr) const;
#ifdef DEF_Python
    QString     previewFilenameThumbnail_Python(const int &IDnr)const;
    QString     previewFilenameRGB_Python(const int &IDnr) const;
    QString     previewFilenameA_Python(const int &IDnr) const;
    QString     previewFilename_Base_Python(int IDnr) const;
    QString     jobFilesFolderName_Resolved_Python() const;
#endif
#ifdef  QT_CORE_LIB
    QString     previewFilenameThumbnail(const __RRSDK &RR, const int &IDnr)const;
    QString     previewFilenameRGB(const __RRSDK &RR, const int &IDnr) const;
    QString     previewFilenameA(const __RRSDK &RR, const int &IDnr) const;
    QString     previewFilename_Base(const __RRSDK &RR, int IDnr) const;
#endif
    QString     companyProjectRootFolder(const __RRSDK &RR) const;
    void		exportMinInfo(_JobMinInfo &info);
    _JobMinInfo toMinInfo();
};




//##################################  class _JobBasicsArray ############################################
//##################################  class _JobBasicsArray ############################################
// Scene parser plugins fill this struct with their jobs.
// If isVersionSupported returns false, your plugin cannot use this struct.
// SetArraySize MUST BE called by the plugin before it writes to jobs[]!


class _JobBasicsArray {
public:
	_JobBasicsArray();
	~_JobBasicsArray();
	const quint16	StructureIDBasics;
	const quint16	VariablesIDBasics;
    _rrString500	m_submitterParameter;
    const quint16   m_structSize;
    int             m_maxJobs;									// Tells the submitter how many valid jobs are in the list
	
	_JobBasics * at(const int &j);				// Access the job pointers. Check for NULL. !!!!!!!!!!!!!Pointers to jobs.at(x) become invalid if you add a new job!!!!!!!!!!!
    bool         setArraySize(const int &newSize);			// Pointers to jobs.at(x) become invalid if SetArraySize() is called!
    bool         isVersionSupported(quint8	inVariablesIDBasics =VariablesID_JobBasics ); //check if we can use the input struct
    bool         getNewJob(_JobBasics * &Job);			// increases maxJobs, the array if required, sets Job, clears it and returnes true is successfull. !!!!!!!!!!!!!Pointer to job become invalid if you add a new job!!!!!!!!!!!
    void         clear();

private:
    int          m_maxArraySize;
    _JobBasics * m_jobs;

};



#pragma pack()  //restore default alignment

} //endNamespace rrJ

#endif

