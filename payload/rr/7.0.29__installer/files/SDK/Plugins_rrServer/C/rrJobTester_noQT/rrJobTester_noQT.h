#ifndef rrJobTester_noQT_H
#define rrJobTester_noQT_H

#include "../../shared_SDK/RR_DataTypes_plugins_SDK.h"

#ifdef RR_OS_WIN
#include <windows.h>
#define DllExport __declspec( dllexport )
#else
#define DllExport
#endif



extern "C"
{
	DllExport rrpJOB_Info_Def;
	DllExport rrpJOB_Init_Def;
	DllExport rrpJOB_Exit_Def;
	DllExport rrpJOB_Execute_Def;
}




#endif // rrJobTester_noQT_H
