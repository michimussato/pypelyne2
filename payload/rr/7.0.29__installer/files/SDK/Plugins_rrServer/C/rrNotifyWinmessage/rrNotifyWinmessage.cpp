#include "rrNotifyWinmessage.h"

#include "../../shared_SDK/RR_DataTypes_jobs_SDK.h"
#include "../../shared_SDK/RR_files_SDK.h"
#include "../../shared_SDK/RR_version.inc"
#include "Wtsapi32.h"


DllExport int pInfo(rrP::_dataNFY_Info * const data)
{
    data->RRVersion= rrVersion;
    data->QTVersion= qVersion();
    data->MinorID=rrP::MinorID_NFY;

    //Human readable informations about the plugin:
    data->pluginName=       "WinMessage";
    data->pluginAuthor=     "RR, Holger Schoenberger";
    data->pluginVersion=    "1.0";

    //Check if the data structure is compatible:
    if (data->StructureID!=rrP::StructureID_NFY) {
        data->StructureID=rrP::StructureID_NFY;
        return rrP::rRRDataVersionConflict;
    } else {
        data->StructureID=rrP::StructureID_NFY;
    }
	data->setDebugCompile();

	data->paramMax=0;

	return rrP::rSuccessful;
}



DllExport int pInit(rrP::_dataNFY_InitExit * const data)
{
#if (!defined rrDEBUG)
	try 
	{
#endif


	return rrP::rSuccessful;
#if (!defined rrDEBUG)
	}
	catch (...)
	{
		return rrP::rCError;
	}
#endif
}



DllExport int pExit(rrP::_dataNFY_InitExit * const data)
{
#if (!defined rrDEBUG)
	try 
	{
#endif

		
	return rrP::rSuccessful;
#if (!defined rrDEBUG)
	}
	catch (...)
	{
		return rrP::rCError;
	}
#endif
}



DllExport int pNotify(rrP::_dataNFY_Notify * const data)
{
#if (!defined rrDEBUG)
	try 
	{
#endif
        if (!data->job->isRightStructVersion()) return rrP::rRRDataVersionConflict;
		if (data->job->NotifyFinishClientName.isEmpty()) {
			return rrP::rDataError;
		}
        


		QString text=QString("Job %1 finished. \nScene:%2 \nImage:%3%4").arg(data->job->ID2str()).arg(data->job->SceneName).arg(data->job->ImageDir).arg(data->job->ImageFileName).toLatin1();
		wchar_t * textW = new wchar_t[text.size()+3];
		text.toWCharArray(textW);
		textW[text.size()]='\0';

		QString title="rrNotify";
		wchar_t * titleW = new wchar_t[title.size()+3];
		title.toWCharArray(titleW);
		titleW[title.size()]='\0';


		 HANDLE HOtherMachine= WTSOpenServerW(data->job->NotifyFinishClientName.value);
		 if (HOtherMachine!=NULL) {
			 DWORD pResponse;
			 if (!WTSSendMessageA(HOtherMachine,WTS_CURRENT_SESSION,title.toLatin1().data(),title.size(),text.toLatin1().data(),text.size(),MB_OK,0,&pResponse,FALSE)) {
			 }
			 WTSCloseServer(HOtherMachine);
		 }
		 rrDeleteArray(textW);
		 rrDeleteArray(titleW);

		/* ALTERNATIVE, THE MANUAL WAY
		QByteArray msg;
		msg="Royal Render";
		msg.append('\0');
		msg+=QString(data->job->UserName).toLatin1();
		msg.append('\0');
		msg+=QString("Job %1 finished. \nScene:%2 \nImage:%3%4").arg(data->job->ID2str()).arg(data->job->SceneName).arg(data->job->ImageDir).arg(data->job->ImageFileName).toLatin1();
		msg.append('\0');

		BOOL fResult;
		HANDLE hFile;
		DWORD cbWritten;

		hFile = CreateFile((WCHAR*) QString("\\\\%1\\mailslot\\messngr\0").arg(data->job->NotifyFinishClientName).utf16(),
		GENERIC_WRITE,
		FILE_SHARE_READ,
		(LPSECURITY_ATTRIBUTES)NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		(HANDLE) NULL);

		if (hFile == INVALID_HANDLE_VALUE) {
			return rrP::rOtherError;
		}

		fResult = WriteFile(hFile,
			msg.data(),
			(DWORD) ( msg.length() ) ,
			&cbWritten,
			(LPOVERLAPPED)NULL);
	
		CloseHandle(hFile);
*/
//		if (!fResult) return rrP::rOtherError;

	return rrP::rSuccessful;
#if (!defined rrDEBUG)
	}
	catch (...)
	{
		return rrP::rCError;
	}
#endif
}


