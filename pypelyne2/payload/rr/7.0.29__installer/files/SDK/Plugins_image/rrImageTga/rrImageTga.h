#ifndef rrImageTga_H
#define rrImageTga_H


#include "rrImageTga.h"
#include "../../shared_SDK/RR_DataTypes_plugins_SDK.h"


#ifdef RR_OS_WIN
#define DllExport __declspec( dllexport )
#else
#define DllExport
#endif

extern "C"
{
	DllExport rrpIMG_Info_Def;
	DllExport rrpIMG_LoadHeader_Def;
	DllExport rrpIMG_Decode8_Def;
	DllExport rrpIMG_Encode8_Def;
	DllExport rrpIMG_Decode16_Def;
	DllExport rrpIMG_Encode16_Def;
	DllExport rrpIMG_Decodef_Def;
	DllExport rrpIMG_Encodef_Def;
}




#endif // rrImageTga_H
