#ifndef RR_DataTypesStructureIDS_H
#define RR_DataTypesStructureIDS_H
#include "RR_DataTypes_other_SDK.h"

//StructureIDs and VariablesIDs
//
//
//Usage:
//   our_StructureID != received_StructureID:
//   The data structure changed that much that you cannot read values any more from the struct.
//   You have to abort.
//
//   our_VariablesID < received_VariablesID:
//   Data was added to the struct 
//   We are 'to old' to know about this.
//   But we still can read our data.
//   We just don't care about the new values.
//
//   our_VariablesID > received_VariablesID:
//   The external program is too old. 
//   We have more variables in our struct than the external program part.
//   If we need the new variables we should abort.
//  
//
//   Note:
//   It is possible to hard-code the comparison our_VariablesID and do not use the latest from the header files.
//   This way you set that you will never(!) use any new variables.
//   And your app still works with older plugins.


// Note for jobs: If the size of a parent struct chages, all child mayor_IDs will change as you cannot access the members any more.
//
//
//


#if ( defined(defrrServerconsole)  ||defined(defrrtestPlugins) || defined(defrrControl)  || defined(defrrConfig) || defined(defrrSubmitter)  || defined(defpyRR2)  || defined(defpyRR3) || defined(defrrPythonconsole)  )
    #define DEF_Python
#endif

#ifdef DEF_Python
#if ((defined defrrControl) || (defined defrrSubmitter)|| (defined defrrtestPlugins) || defined(defrrConfig))
#define rrPythonUIFunctions
#endif
#endif


#ifndef defrrVerifyExrModes
	#define DEF_PluginsIMG
#endif


#if (  defined(defrrClient) \
        || defined(defrrClientconsole) \
        || defined(defrrClientwatch)  \
        || defined(defrrServerconsole)\
        || defined(defrrConfig)\
        || defined(defrrViewer)\
        || defined(defrrHistorydb)\
        || defined(defrrControl)\
        || defined(defrrSubmitter)\
        || defined(defrrSubmitterconsole)\
        || defined(defrrPythonconsole)\
		|| defined(defrrExrCropRegion)\
		|| defined(defrrAssembleTiles)\
		|| defined(defrrSequenceCheck)\
		|| defined(defrrVerifyExrModes)\
        )
    #define DEF_LCMP
#endif




#if (      defined(defrrClient) \
        || defined(defrrClientconsole) \
        || defined(defrrServerconsole)\
        || defined(defrrControl)\
        || defined(defrrSubmitter)\
		|| defined(defrrAssembleTiles)\
		|| defined(defrrTestErrorHandling)\
        )
	#if (!defined (RR_OS_MAC))
    #define DEF_USE_BREAKPAD
	#endif
#endif



#if (defined(defrrLicense))
    //#define DEF_ClientCommands
    //#define DEF_RenderAppsStruct
    //#define DEF_ClientRenderApps
    #define DEF_RR_RenderApps
    //#define DEF_RR_User
    //#define DEF_RR_Clients
#endif


#if (defined(defrrTestSomeThing))
    //#define DEF_ClientCommands
    //#define DEF_RenderAppsStruct
    //#define DEF_ClientRenderApps
    //#define DEF_RR_RenderApps
    //#define DEF_RR_User
    //#define DEF_RR_Clients
#endif

#if (defined(defrrViewer))
    //#define DEF_ClientCommands
    //#define DEF_RenderAppsStruct
    //#define DEF_ClientRenderApps
    //#define DEF_RR_RenderApps
    //#define DEF_RR_User
    #define DEF_RR_Clients
#endif


#if (defined(defpyRR2) || defined(defpyRR3) || defined(defnodeJsRR))
    //#define DEF_ClientCommands
    //#define DEF_RenderAppsStruct
    //#define DEF_ClientRenderApps
    //#define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
    #define DEF_Python
#endif


#if (defined(defrrHistorydb))
    //#define DEF_ClientCommands
    //#define DEF_RenderAppsStruct
    //#define DEF_ClientRenderApps
    //#define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
#endif


#if (defined(defrrConfig))
    //#define DEF_ClientCommands
    #define DEF_RenderAppsStruct
    #define DEF_ClientRenderApps
    #define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
#endif

#if (defined(defrrControl))
    //#define DEF_ClientCommands
    #define DEF_RenderAppsStruct
    #define DEF_ClientRenderApps
    #define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
#endif


#if (defined(defrrSubmitter) || defined(defrrSubmitterconsole))
    //#define DEF_ClientCommands
    #define DEF_ClientRenderApps
    #define DEF_RenderAppsStruct
    #define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
#endif

#if (defined(defrrServerconsole))
    #define DEF_ClientCommands
    #define DEF_RenderAppsStruct
    #define DEF_ClientRenderApps
    #define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
#endif

#if (defined(rrPlugin)) //server plugins, class _rrClient
    #define DEF_ClientCommands
    #define DEF_ClientRenderApps
    #define DEF_RR_Clients
#endif


#if (defined(defrrClient) || defined(defrrClientconsole) || defined(defrrClientwatch))
    #define DEF_ClientCommands
    #define DEF_RenderAppsStruct
    #define DEF_ClientRenderApps
    #define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
#endif


#if (defined(defrrTest_PrintDatasizesConsole))
    #define DEF_ClientCommands
    #define DEF_RenderAppsStruct
    #define DEF_ClientRenderApps
    #define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
#endif


#if (defined(defrrNotifyRRMessage))
    #define DEF_RR_Clients
#endif


#if (defined(defrrNotifyEmail))
    #define DEF_RR_User
#endif




#if (defined(defrrDebugJobExport))
    //#define DEF_ClientCommands
    #define DEF_RenderAppsStruct
    //#define DEF_ClientRenderApps
    #define DEF_RR_RenderApps
    #define DEF_RR_User
    #define DEF_RR_Clients
#endif





const quint16 StructureID_rrGlobalSDK =0x0102; //plugin communication 
const quint16 StructureID_rrGlobal    =0x0F01; //plugin communication 
const quint16 StructureID_rrCommands  =0x0B03; //send as tcp-data


namespace rrJ { 

    //note: if a parent class is changed (e.g. JobSubmitter), then all child classes are changed, too (JobSave,JobSend,JobRuntime)
    const quint16 StructureID_JobBasics			=0x0403; //jobs.db file and send as TCP-data
    const quint16 VariablesID_JobBasics			=0x0003; //jobs.db file and send as TCP-data
    const quint16 StructureID_JobSubmitter		=0x0506; //jobs.db file and send as TCP-data
    const quint16 VariablesID_JobSubmitter		=0x0008; //jobs.db file and send as TCP-data
    const quint16 StructureID_JobSave			=0x0606; //jobs.db file and send as TCP-data
    const quint16 VariablesID_JobSave			=0x0006; //jobs.db file and send as TCP-data	   
    const quint16 StructureID_JobSend			=0x0705; //jobs.db file and send as TCP-data
    const quint16 VariablesID_JobSend			=0x0005; //jobs.db file and send as TCP-data
    const quint16 StructureID_JobRuntime		=0x0805; //jobs.db file and send as TCP-data
    const quint16 VariablesID_JobRuntime		=0x0005; //jobs.db file and send as TCP-data
    const quint16 StructureID_HistoryJob		=0x0A04; //history db files
    const quint16 VariablesID_HistoryJob		=0x0003; //history db files

    const quint16 StructureID_JobSettingsOnly	=0x0903; //send as TCP-data
    const quint16 VariablesID_JobSettingsOnly	=0x0003; //send as TCP-data
    const quint16 StructureID_ControlList		=0x0A07; //send as TCP-data
    const quint16 VariablesID_ControlList		=0x0003; //send as TCP-data

    const quint16 StructureID_jobListRequest    =0xC601;  //send as TCP-data
    const quint16 StructureID_jobList           =0xC702;  //send as TCP-data
}

const quint16 StructureID_RRN_TCP_HeaderData_v2 = 0x0D02; //TCP connection
const quint16 StructureID_RRN_TCP_HeaderData_v3 = 0x0D03; //TCP connection

namespace rrC { 
    const quint16 StructureID_ClientStatus  =0x0201; //send as TCP-data
    const quint16 VariablesID_ClientStatus  =0x0002; //send as TCP-data
    const quint16 StructureID_ClientStatusMulti   =0xC101; //send as TCP-data
}
namespace rrCHK { 
	const quint16 StructureID_ImageOutputPlaceHolderFile =0x0B01; //saved in placeholder file 
}

const quint16 StructureID_UserListRequest  =0xC201;  //send as TCP-data
const quint16 StructureID_UserListMulti    =0xC301;  //send as TCP-data
const quint16 StructureID_UserModify       =0xC401;  //send as TCP-data
const quint16 StructureID_infoGlobal       =0xC501;  //send as TCP-data
const quint16 StructureID_JobBasicNew      =0xC01;   //send as TCP-data




namespace  rrP {
    const quint16 StructureID_IMG	=0xA002; //plugin library file
    const quint16     MinorID_IMG	=0x0002; //plugin library file
    const quint16 StructureID_PARS	=0xB002; //plugin library file
    const quint16     MinorID_PARS	=0x0001; //plugin library file
    const quint16 StructureID_NFY	=0xC002; //plugin library file
    const quint16     MinorID_NFY	=0x0001; //plugin library file
    const quint16 StructureID_JOB	=0xD002; //plugin library file
    const quint16     MinorID_JOB	=0x0001; //plugin library file
}


const quint16 StructureID_rrViewFile        =0x0E01; //saved in .rrimg file

const quint16 StructureID_rrClientStats     =0xA101;
const quint16 StructureID_rrServerStats     =0xA201;



namespace rrCM { 
    const quint16 StructureID_ClientSharedMemBuffer =0x0C02; //used for client-clientwatch communication
    const quint16 VariablesID_ClientSharedMemBuffer =0x0001; //used for client-clientwatch communication
}


#endif

