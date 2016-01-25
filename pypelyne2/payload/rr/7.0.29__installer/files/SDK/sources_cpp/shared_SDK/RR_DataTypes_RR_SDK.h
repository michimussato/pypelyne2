
#ifndef RR_DataTypes_RR_SDK_H
#define RR_DataTypes_RR_SDK_H

#include "RR_defines_features_classid_SDK.h"
#include "RR_defines_SDK.h"
#include "RR_DataTypes_RR_sub_SDK.h"

class QWidget;
class _rrLogfile;


const quint16 rrMaxLogFileBuffer	=3000; //3kb




//To prevent Mis-Spelling in the source, names of config parameter
//used in function RR.cfgGetX( name )

#define  cfgjGetProjectNameBy			  "jGetProjectNameBy"  
#define  cfgjGetProjectNameByDirStart     "jGetProjectNameByDirStart"  
#define  cfgjGetProjectNameByDirCount     "jGetProjectNameByDirCount"  
#define  cfgjHistoryDBExport                 "jHistoryDBExport"  
#define  cfgjHistoryDBDeleteAfterDays     "jHistoryDBDeleteAfterDays"  
#define  cfgjHistoryDBExportName            "jHistoryDBExportName"  
#define  cfgjStartRenderInMiddle             "jStartRenderInMiddle"  
#define  cfgjDeleteFinishedAfterDays         "jDeleteFinishedAfterDays"  
#define  cfgjDeleteUnFinishedAfterDays     "jDeleteUnFinishedAfterDays"  
#define  cfgjDeleteIfNumber                 "jDeleteIfNumber"  
#define  cfgjm_maxCrashesClientDeassign     "jm_maxCrashesClientDeassign"  
#define  cfgjMaxLimitsClientDeassign     "jMaxLimitsClientDeassign"  
#define  cfgjWaitForApprovedMain             "jWaitForApprovedMain"  
#define  cfgjWaitForApprovedDone             "jWaitForApprovedDone"  
#define  cfgjDoNotCheckOverwrite            "jDoNotCheckOverwrite"  
#define  cfgjGetSSVbySetting                "jGetSSVbySetting"  
#define  cfgjGetSSVbyFile                "jGetSSVbyFile"  
#define  cfgjGetSSVScene                    "jGetSSVScene"  
#define  cfgjGetSSVShot                    "jGetSSVShot"  
#define  cfgjGetSSVVersion                "jGetSSVVersion"  
#define  cfgjGetSSVSceneEnd                    "jGetSSVSceneEnd"  
#define  cfgjGetSSVShotEnd                   "jGetSSVShotEnd"  
#define  cfgjGetSSVVersionEnd                "jGetSSVVersionEnd"  
#define  cfgjGetSSVSceneLength                    "jGetSSVSceneLength"  
#define  cfgjGetSSVShotLength                   "jGetSSVShotLength"  


#define  cfgjPreferedProjects1             "jPreferedProjects1"  
#define  cfgjPreferedProjects2             "jPreferedProjects2"  
#define  cfgjPreferedProjects3             "jPreferedProjects3"  
#define  cfgjPreferedProjects4             "jPreferedProjects4"  
#define  cfgjPreferedProjects5             "jPreferedProjects5"  
#define  cfgjPreferedProjects6             "jPreferedProjects6"  
#define  cfgjPreferedProjects7             "jPreferedProjects7"  
#define  cfgjPreferedProjects8             "jPreferedProjects8"  
#define  cfgjPreferedProjects9             "jPreferedProjects9"  
#define  cfgjPreferedProjects10             "jPreferedProjects10"  
#define  cfgjPreferedProjects1cl             "jPreferedProjects1cl"  
#define  cfgjPreferedProjects2cl             "jPreferedProjects2cl"  
#define  cfgjPreferedProjects3cl             "jPreferedProjects3cl"  
#define  cfgjPreferedProjects4cl             "jPreferedProjects4cl"  
#define  cfgjPreferedProjects5cl             "jPreferedProjects5cl"  
#define  cfgjPreferedProjects6cl             "jPreferedProjects6cl"  
#define  cfgjPreferedProjects7cl             "jPreferedProjects7cl"  
#define  cfgjPreferedProjects8cl             "jPreferedProjects8cl"  
#define  cfgjPreferedProjects9cl             "jPreferedProjects9cl"  
#define  cfgjPreferedProjects10cl         "jPreferedProjects10cl"  
#define  cfgjPreviewPriorityIncrease         "jPreviewPriorityIncrease"  
#define  cfgjScriptPriorityIncrease         "jScriptPriorityIncrease"  
#define  cfgjPrioLvlAmode                "jPrioLvlAmode"  
#define  cfgjPrioLvlBmode                "jPrioLvlBmode"  
#define  cfgjPrioLvlCmode                "jPrioLvlCmode"  
#define  cfgjPrioLvlApmin                "jPrioLvlApmin"  
#define  cfgjPrioLvlApmax                "jPrioLvlApmax"  
#define  cfgjPrioLvlBpmin                "jPrioLvlBpmin"  
#define  cfgjPrioLvlBpmax                "jPrioLvlBpmax"  
#define  cfgjPrioReduceCrash             "jPrioReduceCrash"  
#define  cfgjPrioReduceCrashClient       "jPrioReduceCrashClient"  
#define  cfgjAverageAbortOnReceive         "jAverageAbortOnReceive"  
#define  cfgjAverageAbortAfterFrame         "jAverageAbortAfterFrame"  
#define  cfgjAverageAbort                 "jAverageAbort"  
#define  cfgjAverageAbortHourDelay         "jAverageAbortHourDelay"  
#define  cfgjAbortReservedClientsOnJobReceive "jAbortReservedClientsOnJobReceive"  
#define  cfgjEqualExclusivePrio "jEqualExclusivePrio"  
#define  cfgOLDcAverageClients           "cAverageClients"  
#define  cfgOLDcAverageForUser           "cAverageForUser"  
#define  cfgOLDcAverageAbort             "cAverageAbort"  
#define  cfgOLDcAverageAbortHourDelay    "cAverageAbortHourDelay"  
#define  cfgjChunkSize                   "jChunkSize"  
#define  cfgjPrivilegLoggedIn            "jPrivilegLoggedIn"  

//#define  cfgcAverageClients                 "cAverageClients"
//#define  cfgcAverageForUser                 "cAverageForUser"
#define  cfgcLocTex_LeaveFreeSpaceMB         "cLocTex_LeaveFreeSpaceMB"  
#define  cfgcLocTex_maxDaysToKeep         "cLocTex_maxDaysToKeep"  
//#define  cfgcSatelliteAbortIfMasterStarts  "cfgcSatelliteAbortIfMasterStarts"
//#define  cfgcSatelliteUseDisabledClients  "cSatelliteUseDisabledClients"
//#define  cfgcSatelliteUseOfflineClients     "cfgcSatelliteUseOfflineClients"
#define  cfgcMaxClientsInFileCached         "cfgcMaxClientsInFileCached"  


#define  cfgwCreateWebsite             "wCreateWebsite"  
#define  cfgwCreateStats                 "wCreateStats"  
#define  cfgwCreateGlobalIndex             "wCreateGlobalIndex"  
#define  cfgwCreateUserIndex             "wCreateUserIndex"  
#define  cfgwCreateProjectIndex         "wCreateProjectIndex"  
#define  cfgwCreateHtAccess             "wCreateHtAccess"  
#define  cfgwCreateHtAccessPath         "wCreateHtAccessPath"  
#define  cfgwJpegsMultiplyAlpha         "wJpegsMultiplyAlpha"  
#define  cfgwCacheFrameLimit             "wCacheFrameLimit"  
#define  cfgwCacheApp3D                 "wCacheApp3D"  
#define  cfgwCacheAppArchive             "wCacheAppArchive"  
#define  cfgwCacheAppComp             "wCacheAppComp"  
#define  cfgwJobDataLocation          "wJobDataLocation"  

#define  cfgfFtpUpload             "fFtpUpload"  
#define  cfgfServer                 "fServer"  
#define  cfgfServerPort             "fServerPort"  
#define  cfgfUser                 "fUser"  
#define  cfgfPass                 "fPass"  
#define  cfgfProxyType             "fProxyType"  
#define  cfgfProxyHttp             "fProxyHttp"  
#define  cfgfProxyServer             "fProxyServer"  
#define  cfgfProxyUser             "fProxyUser"  
#define  cfgfProxyPass             "fProxyPass"  
#define  cfgfProxyPort             "fProxyPort"  
#define  cfgfPath                 "fPath"  
#define  cfgfUploadGlobalTables     "fUploadGlobalTables"  
#define  cfgfUploadProjectTables     "fUploadProjectTables"  
#define  cfgfUploadUserTables     "fUploadUserTables"  
#define  cfgfUploadJobSites         "fUploadJobSites"  
#define  cfgfUploadImgStats         "fUploadImgStats"  
#define  cfgfUploadImgRGBsmall     "fUploadImgRGBsmall"  
#define  cfgfUploadImgRGB         "fUploadImgRGB"  
#define  cfgfUploadImgAlpha         "fUploadImgAlpha"  
#define  cfgfUploadQuicktimes     "fUploadQuicktimes"  
#define  cfgfNoHtDelete             "fNoHtDelete"  


#define  cfgeSendEmails             "eSendEmails"  
#define  cfgeStatusMinuteDelay     "eStatusMinuteDelay"  
#define  cfgeErrorMinuteDelay     "eErrorMinuteDelay"  
#define  cfgeSendStatus             "eSendStatus"  
#define  cfgeSendError             "eSendError"  
#define  cfgeSmtpServer             "eSmtpServer"  
#define  cfgeSmtpServerPort         "eSmtpServerPort"  
#define  cfgeAuthType             "eAuthType"  
#define  cfgeSecurityType             "eSecurityType"  
#define  cfgeAuthAccount             "eAuthAccount"  
#define  cfgeAuthPass             "eAuthPass"  
#define  cfgeEmailFromDomain         "eEmailFromDomain"  
#define  cfgeDomainEmailStatus     "eDomainEmailStatus"  
#define  cfgeDomainEmailError     "eDomainEmailError"  
#define  cfgeDomainEmail             "eDomainEmail"  


#define  cfgsMultiUserFileServerLogin  "sMultiUserFileServerLogin"  
#define  cfgsMultiUserFileServerLoginProject  "sMultiUserFileServerLoginProject"  
#define  cfgsDailyExecuteTime         "sDailyExecuteTime"  
#define  cfgsJobSendDelay             "sJobSendDelayNew"  
#define  cfgsWOL_ClientNeedLimit         "sWOL_ClientNeedLimit"  
#define  cfgsWOL_WaitBetweenWOLTime     "sWOL_WaitBetweenWOLTime"  
#define  cfgsWOL_Port                 "sWOL_Port"  
#define  cfgsWOL_Subnet                 "sWOL_Subnet"  
#define  cfgsWOL_TypeBroadCast          "sWOL_TypeBroadCast"  
#define  cfgsWOL_TypeDirectedSubnet     "sWOL_TypeDirectedSubnet"  

#define  cfgsServerOS                 "nServerOS"  
#define  cfgsServerOSInfo             "nServerOSInfo"  
#define  cfgsFrameCheckmode				"sFrameCheckmode"  



#define  cfgnServerMACAddress         "nServerMACAddress"  
#define  cfgnServerName                 "nServerName"  
#define  cfgnServerIP1                 "nServerIP1"  
#define  cfgnServerIP2                 "nServerIP2"  
#define  cfgnServerIP3                 "nServerIP3"  
#define  cfgnBackupServerName         "nBackupServerName"  
#define  cfgnBackupServerIP1             "nBackupServerIP1"  
#define  cfgnBackupServerIP2             "nBackupServerIP2"  
#define  cfgnBackupServerIP3             "nBackupServerIP3"  
#define  cfgnUseServerIP                 "nUseServerIP"  
#define  cfgnWebServerStart             "nWebServerStart"  
#define  cfgnWebServerPort             "nWebServerPort"  
#define  cfgnClientConnectPSec         "nClientConnectPSec"  
#define  cfgnRRServerPort             "nRRServerPort"  
#define  cfgnRRServerAdapter             "nRRServerAdapter"  
#define  cfgnTCPRequiresAuth             "nTCPRequiresAuth"  
#define  cfgnRouterIPold                 "nRouterIP"  
#define  cfgnAuthWhiteList                 "nAuthWhiteList"  


#define  cfguUsername                   "uUsername"  
#define  cfguPass                       "uPass"  
#define  cfglockClientConfig            "lockClientConfig"  
#define  cfglockClientClose             "lockClientClose"  
#define  cfglockRRConfig                "lockRRConfig"  
#define  cfgEncodePreview               "encodePreview"  
#define  cfgHideJobsIfNoFolderAccess    "hideJobsIfNoFolderAccess"  


#define  cfgCost                         "cfgCost"  
#define  cfgCostDisplay               "cfgCostDisplay"  
#define  cfgLocalDecimalMark          "cfgLocalDecimalMark"  

#define  cfgVideoPreview              "VideoPreview"  
#define  cfgVideoFull                 "VideoFull"  
#define  cfgUIcolor                   "UIcolor"  
#define  cfgFontWin                   "FontWin"  
#define  cfgFontWinSmall              "FontWinSmall"  
#define  cfgFontLx                    "FontLx"  
#define  cfgFontLxSmall               "FontLxSmall"  
#define  cfgFontOsx                   "FontOsx"  
#define  cfgFontOsxSmall              "FontOsxSmall"  
#define  cfgConfigVersionMajor        "ConfigVersionMajor"  
#define  cfgConfigVersionMinor        "ConfigVersionMinor"  

#define  cfgExr20				      "Exr20"  



#define  cfgsgPythonPathWin         "sgPythonPathWin"  
#define  cfgsgPythonPathLx          "sgPythonPathLx"  
#define  cfgsgPythonPathMac         "sgPythonPathMac"  
#define  cfgsgRRName                "sgRRName"  
#define  cfgsgAuthKey               "sgAuthKey"  
#define  cfgsgEntityJob             "sgEntityJob"  
#define  cfgsgEntitySubmit          "sgEntitySubmit"  
#define  cfgsgUrl                   "sgUrl"  
#define  cfgsgProxy                 "sgProxy"  
#define  cfgsgProxyPort             "sgProxyPort"  
#define  cfgsgProxyUser             "sgProxyUser"  
#define  cfgsgProxyPass             "sgProxyPass"  
#define  cfgsgProxyNoRRServer       "sgProxyNoRRServer"  
#define  cfgsgEnable                "sgEnable"  



#pragma pack(4)


#ifdef RRx32
//old #define __RRSDK_struct_size 22276
#define __RRSDK_struct_size 22356
#define __RRSDK_struct_appPos 20752
#else
#define __RRSDK_struct_size 22400
#define __RRSDK_struct_appPos 20768
#endif


class __RRSDK 
{
	RR_DISABLE_COPY(__RRSDK)
//****************************Data***************************************
//****************************Data***************************************
//****************************Data***************************************
protected:
	quint16				size__RRSDK;
	quint16				StructureID;
	quint16				StructureIDnonSDK;
    char				p_freeB[rrMaxLogFileBuffer-1];//was: LogFileBuffer[rrMaxLogFileBuffer];
public:
    char				m_logfileDateSeperator;

protected:
    qint32				p_freeC;//LogFileMax;
    _rrTime             p_freeD;//LogFileLastWritten;
    bool				p_setupCfgExecuted;
    bool				p_criticalErrorOccured;
    bool				p_errorCloseApp;
    QWidget			  * p_mainWindow;


public:
    void			  * m_freeA;
    _rrgConfig		  * cfg;
    _rrgPaths			path;
    _rrgApplication		app;
    bool				m_configFilesReloaded; //used by the main application

	//reserved for future use:
    bool				m_free1;
    bool				m_free2;
    bool				m_free3;
    qint64				m_free4;
    qint64				m_free5;
    qint64				m_free6;
    _rrString8_75		m_companyName;
    _rrString8_75		m_free8;
    _rrLogfile		*   m_logFile;
    _rrLogfile		*	m_logFileError;
    void			*	m_free11;
    void			*	m_free12;
    void			*	m_free13;
    void			*	m_free14;




//***************************Functions for plugins**************************************
//***************************Functions for plugins**************************************
//***************************Functions for plugins**************************************
public:
    bool			isValid() {return (rrsdkHasValidMemSize() && rrHasValidID_SDK() );} //plugins should always check this before using __RRSDK
	bool		&	cfgGetB(const char * name) const;
	qint16		&	cfgGetI(const char * name) const;
	_rrString100 &	cfgGetS(const char * name) const;
	float		&	cfgGetF(const char * name) const;
	bool		&	cfgGetB(const char * name);
	qint16		&	cfgGetI(const char * name);
	_rrString100 &	cfgGetS(const char * name);
	float		&	cfgGetF(const char * name);
    QWidget		*	getMainWindow() {return p_mainWindow;}; //Get main window for rrMessageBox( QWidget * parent,....

#ifdef QT_CORE_LIB
    virtual void    writeLog(int rrLog_level, int flags, const QString &error_msg, const QString &Location);
#endif
    void			writeLog_noQT(int rrLog_level, int flags, const _rrString250 &error_msg, const _rrString250 &Location);




//*************************** Other Functions usally not required **************************************
//*************************** Other Functions usally not required **************************************
//*************************** Other Functions usally not required **************************************
public:
    virtual			~__RRSDK();
	void			exitRRSDK(bool closeLog=true); //called before destruction
    bool			setupCfgWasExecuted() {return p_setupCfgExecuted;};
	#ifdef QT_CORE_LIB
    void			formatLogMessage(int rrLog_level, int flags, QString error_msg, const QString &Location, QString &Result);
    void			logFileWrite(int rrLog_level, int flags, const QString &error_msg, const QString &Location);
    void			logFileWriteError(int rrLog_level, int flags, const QString &error_msg, const QString &Location);
	#else
	#endif
    void			formatLogMessage_noQT(int rrLog_level, int flags, const _rrString250 &error_msg, const _rrString250 &Location, _rrString250 &Result);
    inline bool		wasCriticalError() {return p_criticalErrorOccured;};
    inline bool     weAreServerMachine() {return (cfgGetS(cfgnServerName).isEqual(app.machineName.value,app.machineName.length));};
	_rrString100		getServerConnectName(const bool &BackupServer=false);


protected:
    bool			rrsdkHasValidMemSize() {return ((sizeof(__RRSDK)==__RRSDK_struct_size) && (size__RRSDK==__RRSDK_struct_size)  && (size_t(&app)-size_t(this)==__RRSDK_struct_appPos)); };
	bool			rrHasValidID_SDK() {return ((StructureID==StructureID_rrGlobalSDK));}
	#ifdef QT_CORE_LIB
    void			logNoUIExecute(int rrLog_level, int error_ID, const QString &error_msg, const QString &Location);
	#endif
    void			logNoUIExecute_noQT(int rrLog_level, int error_ID, const _rrString250 &error_msg, const _rrString250 &Location);


#ifndef rrPlugin
	#ifdef QT_CORE_LIB
	#endif
#endif
};

#pragma pack()





#endif 
