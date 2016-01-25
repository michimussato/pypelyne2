#include "rrJobTester.h"

#include "../../shared_SDK/RR_DataTypes_jobs_SDK.h"
#include "../../shared_SDK/RR_DataTypes_RR_SDK.h"
#include "../../shared_SDK/RR_files_SDK.h"
#include "../../shared_SDK/RR_version.inc"

//Note: QT is not required, but without QT you do not have the writelog functions.

#define MyPluginName QString("TestPlugin")


DllExport int pInfo(rrP::_dataJOB_Info * const data)
{
    data->RRVersion= rrVersion;
    data->QTVersion= qVersion();
    data->MinorID=rrP::MinorID_JOB;

    //Human readable informations about the plugin:
    data->pluginName=       MyPluginName;
    data->pluginAuthor=     "RR, Holger Schoenberger";
    data->pluginVersion=    "1.0";

    //Check if the data structure is compatible:
    if (data->StructureID!=rrP::StructureID_JOB) {
        data->StructureID=rrP::StructureID_JOB;
        return rrP::rRRDataVersionConflict;
    } else {
        data->StructureID=rrP::StructureID_JOB;
    }
	data->setDebugCompile();


	data->executedWhenFlags=rrP::JobExecALL;

	return rrP::rSuccessful;
}



DllExport int pInit(rrP::_dataJOB_InitExit * const data)
{
#if (!defined rrDEBUG)
	try 
	{
#endif
		//pInit is called once before this plugin is used. (not before pInfo!)
		data->RR->WriteLog(rrlDebugPlugins,0,MyPluginName+": Inititialised",MyPluginName);



	return rrP::rSuccessful;
#if (!defined rrDEBUG)
	}
	catch (...)
	{
		return rrP::rCError;
	}
#endif
}



DllExport int pExit(rrP::_dataJOB_InitExit * const data)
{
#if (!defined rrDEBUG)
	try 
	{
#endif
		//pExit is called once before the plugin is not used any more.
		data->RR->WriteLog(rrlDebugPlugins,0,MyPluginName+": Exit function",MyPluginName);


		
	return rrP::rSuccessful;
#if (!defined rrDEBUG)
	}
	catch (...)
	{
		return rrP::rCError;
	}
#endif
}



DllExport int pExecute(rrP::_dataJOB_Execute * const data)
{
#if (!defined rrDEBUG)
	try 
	{
#endif
        if (!data->job->isRightStructVersion()) return rrP::rRRDataVersionConflict;
		data->RR->WriteLog(rrlProgress,0,QString("%1: executed for job %2, status %3").arg(MyPluginName).arg(data->job->ID2str()).arg(data->job->StatusAsString()),MyPluginName);
		switch (data->job->Status) {
			case rrJ::sFirstCheck: 
				{

				}
				break;
			case rrJ::sPreRender: 
				{

				}
				break;
			case rrJ::sPreviewRender: 
				{

				}
				break;
			case rrJ::sWaitForApprovalMain: 
				{

				}
				break;
			case rrJ::sMainRender: 
				{

				}
				break;
			case rrJ::sPostRender: 
				{

				}
				break;
			case rrJ::sWaitForApprovalDone: 
				{

				}
				break;
			case rrJ::sPostDone: 
				{

				}
				break;
			case rrJ::sFinished: 
				{

				}
				break;
			default: break; //default removes any "you have not used all cases bla bla...." compiler warnings
		}

	return rrP::rSuccessful;
#if (!defined rrDEBUG)
	}
	catch (...)
	{
		return rrP::rCError;
	}
#endif
}


