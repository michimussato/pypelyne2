#ifndef rrSceneParserMantra_H
#define rrSceneParserMantra_H



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
	DllExport rrpPARS_Info_Def;
	DllExport rrpPARS_LoadSceneFile_Def;
}




#endif // rrSceneParserMantra_H
