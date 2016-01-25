#ifndef rrNotifyWinmessage_H
#define rrNotifyWinmessage_H


#include <QString>
#include "../../shared_SDK/RR_DataTypes_plugins_SDK.h"

#ifdef RR_OS_WIN
#include <windows.h>
#define DllExport __declspec( dllexport )
#else
#define DllExport
#endif



extern "C"
{
	DllExport rrpNFY_Info_Def;
	DllExport rrpNFY_Init_Def;
	DllExport rrpNFY_Exit_Def;
	DllExport rrpNFY_Notify_Def;
}




#endif // rrNotifyWinmessage_H
