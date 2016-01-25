
#include "RR_DataTypes_RR_SDK.h"
#include "RR_MessageBox_SDK.h"
#include "../sharedLib/RR_files_SDK.h"
#include "RR_version_SDK.inc"

#include "../shared_SDK/RR_defines_SDK.h"

#ifndef rrPlugin
#endif


#ifdef QT_CORE_LIB
	#ifndef rrPlugin
		#ifdef RR_OS_WIN
		#endif
	#endif
	//#include <QDir>
	//#include <QMutex>
	//#include <QFile>
	#include <QThread>
	#if (!defined rrConsoleApp)
		//#include <QApplication>
	#endif
#endif


#if (!defined RR_OS_WIN)
	#include <sys/utsname.h>
#endif





#ifndef rrPlugin
#ifdef QT_CORE_LIB
#ifdef RR_OS_WIN
#endif
#ifdef RR_OS_WIN
#else
#endif
#if (!defined RR_OS_WIN)
#else
#endif
#endif //(QT_CORE_LIB)
#endif // ! plugin


#ifdef QT_CORE_LIB
bool IsValidRR_Root(const QString &path)
{

    if (path.isEmpty()) return false;
	#ifdef RR_OS_LINUX
	if (path.at(0)!=PD) return false; //path is relative...
	#endif

    if (rrFileExists(path+"sub"+PD+"cfg_global"+PD+"globalconfig.ini")) return true;
	if (rrDirectoryExists(path+"sub"+PD+"cfg_global"+PD)) return true;

#ifdef RR_OS_WIN
    if (rrFileExists(path+"bin"+PD+"win"+PD+"rrClientconsole.exe")) return true;
    if (rrFileExists(path+"bin"+PD+"win"+PD+"rrServerconsole.exe")) return true;
    if (rrFileExists(path+"sub"+PD+"cfg_global"+PD+"relink_win.cfg")) return true;
	if (rrFileExists(QString(path).replace("_debug","_release")+"sub"+PD+"cfg_global"+PD+"relink_win.cfg")) return true;
#elif defined (RR_OS_MAC)
    if (rrFileExists(path+"bin"+PD+"mac"+PD+"rrClientconsole")) return true;
    if (rrFileExists(path+"bin"+PD+"mac"+PD+"rrServerconsole")) return true;
	if (rrFileExists(path+"sub"+PD+"cfg_global"+PD+"relink_mac.cfg")) return true;
	if (rrFileExists(QString(path).replace("_debug","_release")+"sub"+PD+"cfg_global"+PD+"relink_mac.cfg")) return true;
#else
    if (rrFileExists(path+"bin"+PD+"lx64"+PD+"rrClientconsole")) return true;
    if (rrFileExists(path+"bin"+PD+"lx64"+PD+"rrServerconsole")) return true;
	if (rrFileExists(path+"sub"+PD+"cfg_global"+PD+"relink_lx.cfg")) return true;
	if (rrFileExists(QString(path).replace("_debug","_release")+"sub"+PD+"cfg_global"+PD+"relink_lx.cfg")) return true;
#endif

#ifdef defrrDebugJobExport
	return true;
#endif	
	
	return false;
}

#endif




_rrgApplication::_rrgApplication()
{
	OSx64=false;
	isLocalCopyExe=false;
#ifndef rrPlugin
#ifdef RR_OS_WIN
#else
#ifdef RR_OS_LINUX
#else
#endif
#endif
#endif

#ifdef RRx64
    OSx64=true;
#endif


	QAppIsInit=false;
	isConsole=true;
	isService=false;
	startedAt.setCurrentTime();
	displayName="rrApp";
	machineName="UnknownMachine";
	rrVersionInstalled="--";
	ourProcessUser="UnknownUser";
	processID=0;
	for (int i=0;i<maxNA; i++) {
		MACAddress[i].clear();
		localIPs[i]=0;
	}
	autoRun=false;
    noLogFile=true;
    noLogUI=false;
	allowNoServiceMapping=false;

#ifdef rrDEBUG
	noLogFile=false;
#endif
}


bool _rrgApplication::hasCommandlineFlag(_rrString8_100 flagName) const
{
	if (flagName.isEmpty()) return false;
	flagName.makeUpper();
	_rrString8_100 CmdParam;
	for (int i=1; i<argc; i++){
		#ifdef QT_CORE_LIB
		CmdParam=fromXmlString(argv[i]);
		#else
		CmdParam=argv[i];
		#endif
		if (CmdParam.isEqualUpperInput(flagName)) {
			return true;
		}
	}
	return false;
}

bool _rrgApplication::hasCommandlineFlagValue(_rrString8_100 flagName,_rrString8_100 &retValue) const
{
	flagName.makeUpper();
	_rrString8_100 CmdParam;
	for (int i=1; i<argc; i++){
		#ifdef QT_CORE_LIB
		CmdParam=fromXmlString(argv[i]);
		#else
		CmdParam=argv[i];
		#endif
		if (CmdParam.isEqualUpperInput(flagName)) {
			if (i+1 <argc) {
				#ifdef QT_CORE_LIB
				retValue=fromXmlString(argv[i+1]);
				#else
				retValue=argv[i+1];
				#endif
				return true;
			}
			break;
		}
	}
	return false;
}



_rrgCfg_param::_rrgCfg_param()
{
	category="";
	name="";
	type=rrgCfgBool;
	b=false;
}


_rrgConfig::_rrgConfig()
{
	//QWriteLocker locker(&cfg.Mutex);
	loaded=false;
	settingsFileDate.value=0;
	m_count=0;
	notFoundB=false;
	notFoundI=0;
	notFoundF=0.0f;
	notFoundS="";

	for (int i=0;i<rrMaxLogTypes;i++) iLog_Level_enabled[i]=false;
	for (int i=0;i<rrMaxLogTypes;i++) iLog_Level_enabledUI[i]=false;
	iLog_Level_enabled[rrlCritical]=true;
	iLog_Level_enabled[rrlError]=true;
	iLog_Level_enabled[rrlWarning]=true;
	iLog_Level_enabled[rrlInfo]=true;
	iLog_Level_enabled[rrlProgress]=true;	


	iLog_Level_enabledUI[rrlCritical]=true;
	iLog_Level_enabledUI[rrlError]=true;
	iLog_Level_enabledUI[rrlWarning]=true;
	iLog_Level_enabledUI[rrlInfo]=true;
	iLog_Level_enabledUI[rrlProgress]=true;	


/*#ifdef rrDEBUG
#ifndef defrrServerconsole
	for (int i=0;i<rrMaxLogTypes;i++) iLog_Level_enabled[i]=true; 
	for (int i=0;i<rrMaxLogTypes;i++) iLog_Level_enabledUI[i]=true; 
	iLog_Level_enabled[rrlDebugThreads]=false;	
	iLog_Level_enabled[rrlDebugDetailed]=false;	
	iLog_Level_enabled[rrlDebugQT]=false;	
	iLog_Level_enabled[rrlDebugNetwork]=false;
	iLog_Level_enabled[rrlDebugWebsite]=false;	
	iLog_Level_enabled[rrlDebugShowStackTrace]=false;	
	iLog_Level_enabled[rrlDebugFtpVerbose]=false;
	iLog_Level_enabled[rrlDebugPlugins]=false;	
	iLog_Level_enabled[rrlDebugJobs]=false;	

	iLog_Level_enabledUI[rrlDebugThreads]=false;	
	iLog_Level_enabledUI[rrlDebugDetailed]=false;	
	iLog_Level_enabledUI[rrlDebugQT]=false;	
	iLog_Level_enabledUI[rrlDebugNetwork]=false;
	iLog_Level_enabledUI[rrlDebugWebsite]=false;	
	iLog_Level_enabledUI[rrlDebugShowStackTrace]=false;	
	iLog_Level_enabledUI[rrlDebugFtpVerbose]=false;
	iLog_Level_enabledUI[rrlDebugPlugins]=false;	
	iLog_Level_enabledUI[rrlDebugJobs]=false;	
#endif
#endif*/

	for (int i=0;i<20;i++) eLog_Level_send[i]=false;
	eLog_Level_send[rrlCritical]=true;
	eLog_Level_send[rrlError]=true;

	for (int i=0;i<19;i++) {
		UNCMap[i].use=false;
		UNCMap[i].drive='A';
		UNCMap[i].UNC="";
        UNCMap[i].requiresLogin=false;
	}

	for (int i=0;i<rrMaxOSConversions;i++) {
		OSConversion[i][0].clear();
		OSConversion[i][1].clear();
		OSConversion[i][2].clear();
		OSConversion[i][3].clear();
	}
}
