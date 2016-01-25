
#ifndef RR_defines_H
#define RR_defines_H

#if (defined(WIN64) || defined(_WIN64) || defined(__WIN64__) || defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__))
	#define RR_OS_WIN
	#define WIN32_LEAN_AND_MEAN 
	#define strcasecmp _stricmp
    //#define _WIN32_WINNT 0x0601
#elif defined(__APPLE__) && (defined(__GNUC__) || defined(__xlC__) || defined(__xlc__))
	#define RR_OS_MAC
        #define RR_OS_OSX
#else // defined(__linux__) || defined(__linux)
	#define RR_OS_LINUX
	#define RR_OS_LX
#endif

#if (defined(BIT64) || defined(WIN64) || defined(_WIN64) || defined(__WIN64__) || defined(__amd64__) || defined(X64)  )
	#define RRx64
#else 
	#define RRx32
#endif

#ifdef RR_OS_LX
#define GCC_VERSION (__GNUC__ * 100+ __GNUC_MINOR__)
#if GCC_VERSION >= 404
 #define RR_NEW_GCC
#endif
#endif


#ifdef defrrShared
    #ifdef _WIN32
        #define DllExport_sharedLib __declspec(dllexport)
        #define DllHidden
    #else
        #define DllExport_sharedLib __attribute__ ((visibility ("default")))
        #define DllHidden __attribute__ ((visibility ("hidden")))
    #endif
#else
    #ifdef _WIN32
        #define DllExport_sharedLib 
        #define DllHidden
    #else
        #define DllExport_sharedLib 
        #define DllHidden 
    #endif
#endif


#ifdef _WIN32
    #define DllExport_plugin __declspec(dllexport)
#else
    #define DllExport_plugin   
#endif




//Shortcuts to enable/disable a line or a { } block
//rrDD = Debug Disable
//rrDE = Debug Enable
#ifdef rrDEBUG
	#define rrDebug
	#define rrDD if (false)
	#define rrDE if (true)
    #define rrIsDebug true
	#define rrD75D if (false)
	#define rrD75E if (true)
#else
	#define rrDD if (true)
	#define rrDE if (false)
    #define rrIsDebug false
	#define rrD75D if (true)
	#define rrD75E if (false)
#endif


#ifdef RR_OS_LINUX
	#include <stdlib.h>
    #include <unistd.h>
#endif

#  if (__STDC_VERSION__ >= 199901L)
#   define PREDEF_STANDARD_C_1999
#  endif

#if (defined(RR_OS_WIN))
    #define _isinf(x) (!_finite(x))
#elif (defined (RRx64) && defined (RR_OS_MAC))
    #include <float.h>
    //#undef isnan
    //#define _isnan std::isnan
    //#define _isinf isinf
    #define _isnan isnan
    #define _isinf isinf
#else
    #include <math.h>
    #define _isnan isnan
    #define _isinf isinf
#endif





#ifdef  QT_CORE_LIB
	#include <QString> 
	#include <QFile> 
	#include <QDate> 
	#include <cctype>
#else
	#include <string>
	#include <cctype>
	#include <stdio.h>
    //#include <stdlib.h>
    typedef signed char qint8;         /* 8 bit signed */
	typedef unsigned char quint8;      /* 8 bit unsigned */
	typedef short qint16;              /* 16 bit signed */
	typedef unsigned short quint16;    /* 16 bit unsigned */
	typedef int qint32;                /* 32 bit signed */
	typedef unsigned int quint32;      /* 32 bit unsigned */
	#if defined(RR_OS_WIN) 
		typedef __int64 qint64;            /* 64 bit signed */
		typedef unsigned __int64 quint64;  /* 64 bit unsigned */
	#else
		typedef long long qint64;           /* 64 bit signed */
		typedef unsigned long long quint64; /* 64 bit unsigned */
	#endif
	typedef qint64 qlonglong;
	typedef quint64 qulonglong;
	typedef unsigned int uint;
	#define qVersion() "0"
#endif 

#ifdef RR_OS_WIN
	typedef wchar_t rrChar;  //UTF-16
#else
	typedef unsigned short rrChar;  //UTF-16
#endif






enum _rrOS {
	rrosAll=0,
	rrosWindows=1,
	rrosLinux=2,
	rrosMac=3,
};

enum _rrBit {
	rrXAll=0,
	rrX32=1,
	rrX64=2,
};


enum rr_AppType {
	rraNone=0,
	rraServer=1,
	rraClient=2,
	rraSubmitter=3,
	rraControl=4,
	rraPostScript=5,
	rraTest=6,
	rraLogFile=7,
	rraClientWatch=8,
	rraConfig=9,
	rraViewer=10,
	rraInstaller=11,
	rraHistorydb=12,
    rraScript=13,
    rraRenderer=14,
};

//#include "RR_DataTypes_rrString_SDK.h"
//#include "RR_DataTypes_time_SDK.h"


const char  rrCopyrightnotice[108]="Copyright(c)  Holger Schoenberger. All rights reserved.\n    Binary Alchemy - digital materialization";
const char  rrCopyrightnoticeShort[65]="Copyright(c)  Holger Schoenberger. All rights reserved.";


const rrChar PD_WIN='\\';
const rrChar PD_LX='/';
#ifdef RR_OS_WIN
	const rrChar PD=PD_WIN;
	#else
	const rrChar PD=PD_LX;
#endif

#ifdef  QT_CORE_LIB
#ifdef RR_OS_WIN
	const QString LineEnd = "\r\n";
	const QString PDs = QString::fromWCharArray(&PD,1);
#else
	const QString LineEnd = "\n";
	const QString PDs = QString::fromUtf16(&PD,1);
#endif
#endif







//used for writeLog(int rrLog_level, int flags, const QString &error_msg, const QString &Location);
enum _rrLogLvL {
	rrlCritical=0,   //This error should not happen. 
					 //Data lost e.g. TCP buffer not received/send; Important config file not saved
                     //THIS RESTARTS RR APPLICATIONS!!!!!
	rrlError=1,      //Errors are also logged into an C_All_error.log or C_server_error.log
	rrlWarning=2,    //e.g. could not connect to server; website file could not be saved; client does not connect any more
	rrlInfo=3,       //"Important" information e.g. clients are aborted because; job is resetted;
	rrlProgress=4,   //Less important e.g. commands send to client

	rrlDebugMain=10,
	rrlDebugDetailed=11, //only used in server check thread after each function call
	rrlDebugNetwork=12,
	rrlDebugJobs=13,
	rrlDebugUI=14,
	rrlDebugThreads=15,
	rrlDebugShowLocations=16,
	rrlDebugPlugins=17,
	rrlDebugClients=18,
	rrlDebugQT=19,
	rrlDebugShowStackTrace=20,
	rrlDebugWebsite=21,
	rrlDebugJobCheck=22,
	rrlDebugFtp=23,
	rrlDebugFtpVerbose=24,
    rrlDebugPython=25,

    rrMaxLogTypes
};


//const qint16 rrlLogFileError=0x0002; //Prevent loop from error message written in logFile->flush();_prv
const qint16 rrlLogNoDebugInfo=0x0004;	//Do not show address
const qint16 rrlNoMessageWindow=0x0008;   //Do not open a message dialog
const qint16 rrlNoTimeDisplay=0x00010;   //Do not show time
const qint16 rrlLogIntoFileOnly=0x00020;   
const qint16 rrlLogAlwaysDebugInfo=0x0040;	
const qint16 rrlMessageBoxAlignLeft=0x0080;	
//const quint16 rrMaxLogTypes			=25; 

typedef bool LogLevelEnabled[rrMaxLogTypes];



#define flushPrint fflush(stdout); fflush(stderr);
#define rrHasFlag(variable,flag) (( variable & flag )>0)
#define rrRound(d) qint64(d<0 ? d-.5 : d+.5)
#define limitInt( max ) if (index>=max) index=max-1; else if (index<0) index=0


//Helper function to remove an possible error
//Calling the function multiple times is not a problem as delete(NULL) does nothing.
#define rrDeletePointer(Pointer) if (Pointer!=NULL) delete Pointer;  Pointer=NULL;
#define rrDeleteArray(Pointer) if (Pointer!=NULL) delete [] Pointer;  Pointer=NULL;
#define rrDeleteAlloc(Pointer) if (Pointer!=NULL) free(Pointer);  Pointer=NULL;


//if a class cannot be copied with a=b (simple memory address copy)
//e.g. classes with pointers or QStrings
#define RR_DISABLE_COPY(Class) \
	private: \
     Class(const Class &); \
     Class &operator=(const Class &);\
    public: 











#endif
