#ifndef RR_DataTypesJobsSDK_H
#define RR_DataTypesJobsSDK_H

#include "RR_defines_features_classid_SDK.h"
#include "RR_defines_SDK.h"
#include "../sharedLib/RR_DataTypes_rrString_SDK.h"
#include "../sharedLib/RR_DataTypes_time_SDK.h"



#ifdef QT_CORE_LIB
	#include <QString>
#endif




namespace rrJ { 



#undef ENUM_TYPE
#define ENUM_TYPE(name, val, extra) name=val,
enum _LogMessage {
	#include "RR_DataTypes_jobs_SDK_LogMessage.enum"
};
#undef ENUM_TYPE




const quint16  MaxJobs		      =15000; 
const quint16  MaxJobsCommandArray=7500; 

#ifdef RRx64
const quint16  MaxJobs_ServerMemLimit=15000; 
#elif defined defrrControl
const quint16  MaxJobs_ServerMemLimit=15000; 
#else
const quint16  MaxJobs_ServerMemLimit=7000; 
#endif

const quint16  MaxStats			 =200; 
const quint16  MaxLog			 =750; 
const quint16  MaxError			 =50; 
const quint16  MaxImageChannels  =25; 
const quint16  MaxWaitFor		 =20; 
const quint16  MaxPluginData	 =10; 
const quint16  MaxColors		 =11; 
const quint16  MaxColorsRandom	 =15; 
const quint16  MaxImageMulti	 =20; 
const quint16  MaxPreviewImages  =20; 
const quint16  CUSTOMDataBlockSize=5000; 

enum CUSTOMData_Modes {cdUnicode, cdChar, cdInt64};
const char CUSTOMData_ModeUni ='u';
const char CUSTOMData_ModeChar ='c';


enum _Status {
	sNone=0,
	sFirstCheck=20,				//job was received, next is first check to find outpout dir and existing files is not done yet
	sWaitForJobs=40,			//disabled while waiting for other jobs
	sScriptPreRender=60,		//pre-render-scripts are executed next
	sPreviewRender=80,			//job is rendering the preview frames
    sScriptAfterPreview=90,				    
	sWaitForApprovalMain=100,
	sMainRender=120,
	sScriptPostRender=140,
	sWaitForApprovalDone=160,
	sScriptFinished=180,
	sFinished=200,
};




#define rrLayerDefault	" -default- "
#define rrLayerAll		"** All **"
#define rrFileserverTimeDifference_InitValue 2*60*60


const quint32 _Colorss[MaxColors]	=
{
	(0xFFEEEEEE),
	(0xFFFFCCCC),
	(0xFFBBFFAA),
	(0xFFAACCFF),
	(0xFFFFFFCC),
	(0xFFEECCFF),
	(0xFFCCFFFF),
	(0xFF999999),
	(0xFFFF0000),
	(0xFF00FF00),
	(0xFF6666FF)
}; 


#define cfgJobSoftNameCommand	"rrCommand"

#ifdef QT_CORE_LIB
const QString NoOutputCheckname="no_check.file";
const QString NoOutputExecOnce="execOnce.file";
const QString NoOutputExecEachClient="execEachClient.file";
const QString ExecuteSoftName="Execute";
const QString PythonSoftName="Python";
const QString CommandJobName="CommandJob";
const QString CUSTOMUserInfoName="UserInfo";
const QString CUSTOMEnvName="rrEnvFile";
const QString CUSTOMEnvLineName="rrEnvLine";
const QString CUSTOMSubmitterParameter="rrSubmitterParameter";

const QString ID_letters="ABCDEFGHJKLMNOPQRSTUVWXYZ1234567890-";
const QString ID_letters_small="abcdefghjklnopqrstuvwxyz";
#endif



#ifdef QT_CORE_LIB
    QString     ID2str(const quint64 &ID);
    QString     ID2strFull(const quint64 &ID);
    QString     jobStatusAsString(quint8 Status);
    void        getSSV(QString name,_rrString25 &scene,_rrString25 &shot,_rrString25 &version, QString sceneCfg, QString shotCfg, QString versionCfg, QString sceneCfgEnd, QString shotCfgEnd, QString versionCfgEnd, int sceneCfgLength, int shotCfgLength );
    QString     getDirectoryNo(QString dir, int start, int count);
    QString     getDirectoryUntilNo(QString dir, int start, int count);
#endif


#pragma pack(1)  //No 4-byte alignment
struct _IDDecomp
{
    quint8      m_passID;
    quint8      m_subIP3;
    quint8      m_subIP4;
    quint32     m_time_msec; //unique every 49 days
    quint8      m_random;
    void        fromID(const quint64 &ID);
    qint64      toID() const { return *((quint64*) this);};
    #ifdef QT_CORE_LIB
    QString     str();
    QString     strFull();
    #endif
};
#pragma pack() // restore default Alignment 


struct _IDShort {
    quint8      m_passID;
    quint16     m_sec10;
    quint8      m_sec10_more; //actually I want a 24bit int.... sec10_more does not have any influence on the output str()

    #ifdef QT_CORE_LIB
    QString     str();
    #endif
    quint32     int32();
    void        fromInt32(quint32 id);
    void        fromIDDecomp(_IDDecomp id);
    void        fromID(const quint64 &ID);
};


} //endNamespace

#endif

