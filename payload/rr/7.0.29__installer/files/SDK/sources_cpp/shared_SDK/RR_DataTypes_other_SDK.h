
#ifndef RR_DataTypesOtherSDK_H
#define RR_DataTypesOtherSDK_H

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
	#define rrCharLen(C) (quint16)wcslen( C )
#else
	typedef unsigned short rrChar;  //UTF-16
	int rrCharLen(const rrChar *C);
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

#include "RR_DataTypes_rrString.h"
#include "RR_DataTypes_time_SDK.h"


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







struct _rrBytePerc  //used to store precentage data 0-100% in a byte 0-0xFF
{
    quint8 value;
    _rrBytePerc() {value=0;};
    inline float toF() const  {return (float(value)/255.0f);};  //result range: 0-1
    inline float toFperc() const  {return (float(value)/2.55f);};  //result range: 0-100
    //inline qint64 toIperc() const  {return rrRound(float(value)/2.55f);};  //result range: 0-100
    inline quint8 toIperc() const  {return int(float(value)/2.55f + 2.55f/2.0f);};  //result range: 0-100
    inline void fromF(const float &inF) {if (inF>1.0) value=0xFF; else if (inF<0.0) value=0; value=rrRound(inF*255.0f) & 0xFF; if (value==0 && inF>0.0f) value=1;};
    inline void fromFPerc(float inF) {inF/=100.0f; fromF(inF);};
    bool noMaxima() {return (value>0 && value<254); };
    inline bool	operator >  (_rrBytePerc const &in) {return (value>in.value);};
    inline bool	operator <  (_rrBytePerc const &in) {return (value<in.value);};
    inline bool	operator >= (_rrBytePerc const &in) {return (value>=in.value);};
    inline bool	operator <= (_rrBytePerc const &in) {return (value<=in.value);};
    inline void	operator -= (_rrBytePerc const &in) {if (in.value>value) value=0; else value-=in.value; };
    inline void	operator += (_rrBytePerc const &in) {if (value+in.value>0xFF) value=0xFF; else value+=in.value;};
	#ifdef QT_CORE_LIB
    QString str() const { return QString("%1%").arg(rrRound(value*100.0f/255.0f)); };
	#endif
};

class _cJobThreadInstance;

class _rrCPUValue
{
    friend class _cJobThreadInstance;
    friend struct _RenderStats;
public:
    float valueSystem; //value range 0-1
    float nrCores;
    _rrCPUValue(const float &invalueSystem,const int &innrCores) {valueSystem=invalueSystem; nrCores=float(innrCores); };
    _rrCPUValue(const _rrCPUValue &in) {valueSystem=in.valueSystem; nrCores=in.nrCores; };
    operator _rrBytePerc() const {_rrBytePerc ret; ret.fromF(valueSystem); return ret;};
    inline float asSystemFloat() {return valueSystem; };
    inline float asCoreFloat() {return (valueSystem*nrCores); };
    inline float asSystemPerc() {return valueSystem*100.0f; };
    inline float asCorePerc() {return (valueSystem*nrCores*100.0f); };
    inline void clearValue() {valueSystem=0.0f;};
    inline void clear() {valueSystem=0.0f;};
    inline void setbyCore(const float &f) {valueSystem=f/nrCores;};
    inline void setbySystem(const float &f) {valueSystem=f;};
    inline void setbySystemPerc(const int &f) {valueSystem=float(f)/100.0f;};
    inline void addbyCore(const float &f) {valueSystem+=f/nrCores;};
    inline void addbySystem(const float &f) {valueSystem+=f;};
    inline void addbyCoreProc(const float &f) {valueSystem+=f/100.0f/nrCores;};
    inline void addbySystemProc(const float &f) {valueSystem+=f/100.0f;};
    inline void clamp() {if (valueSystem<0.0) valueSystem=0.0f; else if (valueSystem>1.0) valueSystem=1.0f;};
    inline void	operator =  (_rrCPUValue const &in) {valueSystem=in.valueSystem; nrCores=in.nrCores; };
    inline void	operator -= (_rrCPUValue const &in) {valueSystem-=in.valueSystem;};
    inline void	operator += (_rrCPUValue const &in) {valueSystem+=in.valueSystem;};
    inline void	operator *= (float const &mult) {valueSystem*=mult;};
    inline void	operator /= (float const &div) {valueSystem/=div;};
    inline bool	operator >  (_rrCPUValue const &in) {return (valueSystem>in.valueSystem);};
    inline bool	operator <  (_rrCPUValue const &in) {return (valueSystem<in.valueSystem);};
    inline bool	operator >= (_rrCPUValue const &in) {return (valueSystem>=in.valueSystem);};
    inline bool	operator <= (_rrCPUValue const &in) {return (valueSystem<=in.valueSystem);};
    _rrCPUValue operator -  (_rrCPUValue const &in) const {_rrCPUValue ret(*this); ret-=in; return ret;};
    _rrCPUValue operator +  (_rrCPUValue const &in) const {_rrCPUValue ret(*this); ret+=in; return ret;};
    bool  isValid() const {return (valueSystem>=0.0f); };
	#ifdef QT_CORE_LIB
    QString strSystemPerc() const {return QString("%1%").arg(rrRound(valueSystem*100.0f)); };
    QString strCorePerc() const {return QString("%1%").arg(rrRound(valueSystem*nrCores*100.0f)); };
    QString strCoreF() const {return QString("%1").arg(valueSystem*nrCores, 0, 'f',1); };
	#endif

private: 
    _rrCPUValue() { }; 
};






_rrString25		rr_AppType_asString(const rr_AppType &appType);
void			rrSleep(int ms);
unsigned long	z_compressBound_copy (unsigned long sourceLen);


#ifndef rrPlugin
	#ifdef QT_CORE_LIB
	#endif
#endif

_rrString8_250 rrLastOSError8(int errorCode=-1);
_rrString500   rrLastOSError(int errorCode=-1);









#endif
