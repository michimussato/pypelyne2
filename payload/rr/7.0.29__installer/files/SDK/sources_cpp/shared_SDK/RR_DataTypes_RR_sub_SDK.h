
#ifndef RR_DataTypes_RR__PRE_SDK_H
#define RR_DataTypes_RR__PRE_SDK_H

#include "RR_defines_features_classid_SDK.h"
#include "../shared_SDK/RR_defines_SDK.h"
#include "../sharedLib/RR_other_SDK.h"
//#include "RR_Logfile_SDK.h"


const char  rrGlobalCommandlineFlags[]=
		"Global RR Commandline arguments:\n"
		"   -Debug:       output debug messages into logfile [rrRoot]\\sub\\log\\ \n"
		"   -LogFlushAll: Directly write all log messages to file (otherwise buffered)\n"
		"                 (Required if application crashes)\n"
		"   -LocalDataFolder [dir]: Set the local data folder to [dir]\n"
		"   -defaultFontSize [number] :Set the default font size\n"
		"   -smallerFontSize [number] :Set the smaller font size\n"
		"   \n"
		"   -lightUI:  default light UI \n"
		"   -darkUI:   dark UI \n"
		"   -violaUI:  girly UI...\n"
		"   -easterUI:  very colorful UI...\n";



#pragma pack(4)

enum _rrgCfg_param_type {
	rrgCfgBool=0,
	rrgCfgQString=1,
	rrgCfgInt=2,
	rrgCfgFloat=3
};

struct _rrgUNC_map
{
	_rrString8_250 UNC;
	char drive;
	bool use;
    bool requiresLogin;
};

class _rrgCfg_param {
private:
	qint16		min;
	quint16		max;
public:
	_rrgCfg_param();
	qint8		type;
	bool		b;
	_rrString100	s;
	qint16		i;
	float		f;
	_rrString8_100		category;
	_rrString8_100		name;
	void   setI(qint64 newI); //function checks if new value in min/max 
	void   setF(float  newF); //function checks if new value in min/max 
	void   init(bool    value,_rrString8_100 icat, _rrString8_100 iname);
	void   init(_rrString100 value,_rrString8_100 icat, _rrString8_100 iname);
	void   init(qint16  value,qint16  imin,qint16  imax,_rrString8_100 icat, _rrString8_100 iname);
	void   initf(float   value,float  imin,float  imax,_rrString8_100 icat, _rrString8_100 iname);
	void   init(const char * value, _rrString8_100 icat, _rrString8_100 iname);
};


class _rrgPaths 
{
public:
	_rrString250 root;  //exeRoot is in dev environment before relink config file. Without dev environment root=exeRoot
	_rrString250 bin;   //always 32bit
	_rrString250 sub;
	_rrString250 cfg_global;
	_rrString250 cfg_user;
	_rrString250 website;
	_rrString250 autoload;
	_rrString250 clientScripts;
	_rrString250 websiteTemplates;
    _rrString250 renderAppConfigs;
    _rrString250 postScriptConfigs;
    _rrString250 renderAppSetEnv;
    _rrString250 renderAppInstalls;
    _rrString250 renderAppSubmitPlugins;
    _rrString250 log;
    _rrString250 historyDB;
	_rrString250 plugin_ServerJob;
	_rrString250 plugin_ServerNotify;
	_rrString250 bin64;		//64bit on x64 machines
	_rrString250 plugin_Image;
	_rrString250 plugin_SubmitterSceneParser;

	_rrString250 clientLocal_Root;
	_rrString250 clientLocal_Textures;
	_rrString250 clientLocal_exe;
	_rrString250 clientLocal_temp;
	_rrString250 clientLocal_RenderOut;
	_rrString250 clientLocal_CachedScenes;
	_rrString250 clientLocal_RendererPrefs;

	_rrString250 threadCheckPath;
	_rrString250 exeRoot; //exeRoot is in dev environment before relink config file, root is the RR share with all settings
	
	_rrString250 loadStatus;
	_rrString250 stats;
	_rrString250 pluginBase;
	_rrString250 binLocalCache; //in case we have a local copy, this is the bin folder with the executables.
	_rrString250 free5;
};


//typedef bool LogLevelEnabled[rrMaxLogTypes];
class __RR;
const quint8  rrMaxCfg				=200; 
const quint16 rrMaxOSConversions    =60; 


class _rrgConfig
{
public:
	_rrgConfig();
    _rrTime         settingsFileDate;
    bool            loaded;
    quint8          m_count;

    bool            notFoundB;
    qint16          notFoundI;
    float           notFoundF;
    _rrString100    notFoundS;
    _rrgCfg_param   params[rrMaxCfg];
	
    LogLevelEnabled iLog_Level_enabled;
    LogLevelEnabled iLog_Level_enabledUI;
    bool            eLog_Level_send[20];
    _rrgUNC_map     UNCMap[19];

    _rrString8_200  OSConversion[rrMaxOSConversions][4];
	
	void initialize();
    //void resetToRR60config(__RR &RR);
	#ifndef rrPlugin
	#endif
	
private:

};

#define maxNA 8



class _rrgApplication
{
public:
	_rrgApplication();
    bool    hasCommandlineFlag(_rrString8_100 flagName) const;
    bool    hasCommandlineFlagValue(_rrString8_100 flagName,_rrString8_100 &retValue) const;

    bool            isConsole;
    bool            isService;
    bool            QAppIsInit;
    _rrTime         startedAt;

    _rrOS           OS;
    bool            OSx64;
    quint32         localIPs[maxNA]; //linked with MACAddress
    _rrString8_75   machineName;
    _rrString100    ourProcessUser;
    _rrString8_12   MACAddress[maxNA];

    bool            autoRun;      //Application should run without user interaction, no questions, nothing to click (for submitter, installer...)
    _rrString250    freeB;//logfileName;
    bool            noLogFile;
    bool            noLogUI;
    bool            freeF;//LogFlushAll;
    rr_AppType      appType;
    _rrString50      displayName;
    quint64         threadID;
    int             argc;
    char	**      argv;

    _rrString50      rrVersionInstalled;


    bool            allowNoServiceMapping;
    bool            machineNameOverridden;
    bool            isLocalCopyExe;
    qint64          processID;
    _rrTime         rrExeFileDate;//used for dump files
    qint64          free6;
    _rrString8_75   free7;//ExrSceneName; //used to communicate with exr plugin
    _rrString8_75   free8;

	private:
} ;


class __RRSDK;


#pragma pack()




#ifndef rrPlugin
#ifdef QT_CORE_LIB
#endif
#endif




#endif 
