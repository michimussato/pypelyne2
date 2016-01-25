#ifndef RR_DataTypesRenderAppSDK_H
#define RR_DataTypesRenderAppSDK_H

#include "RR_defines_SDK.h"
#include "RR_defines_features_classid_SDK.h"
#include "../sharedLib/RR_DataTypes_rrString_SDK.h"


#ifdef RR_OS_WIN

#else
   #include <stdio.h>
#endif



namespace rrRS {

const quint16  MaxCustomOptions  =30; 
const quint16  MaxPrePostCommand =30; 
const quint16  MaxRROptions		 =35; 
//const quint16  MaxPathPresets	 =10; 

enum _RROptionsUsageLocation {
	oulNone=0,
	oulRenderSettings=1,
	oulRROptions=2,
	oulRROverrides=3,
	oulRRCommandline=4,
	oulHidden=5
};


#undef ENUM_TYPE_RRO
#define ENUM_TYPE_RRO(ID, name, submitterlocation, description, allowchangeDefault, checkedDefault) name=ID,
#undef ENUM_TOTAL
#define ENUM_TOTAL(item) item
enum _RROptions {
    #include "RR_DataTypes_RenderApp_SDK.enum"
};

#undef ENUM_TYPE_RRO
#define ENUM_TYPE_RRO(ID, name, submitterlocation, description, allowchangeDefault, checkedDefault) submitterlocation,
#undef ENUM_TOTAL
#define ENUM_TOTAL(item) 
const quint8 _RROptionsUsage[MaxRROptions] = 
{
    #include "RR_DataTypes_RenderApp_SDK.enum"
};

#undef ENUM_TYPE_RRO
#define ENUM_TYPE_RRO(ID, name, submitterlocation, description, allowchangeDefault, checkedDefault) description,
#undef ENUM_TOTAL
#define ENUM_TOTAL(item) 
const char  _RROptionsname[MaxRROptions][40] = 
{
    #include "RR_DataTypes_RenderApp_SDK.enum"
};


#ifdef DEF_RR_RenderApps
extern _rrString8_evenSize<40> _RROptionsnameFile[MaxRROptions];
void set_RROptionsnameFile();
#endif 

enum _PrePostCommandType
{
	_ppPre=0,
	_ppPost=1,
	_ppFinished=2,
    _ppPreview=3
};

const qint16 rrInvalidSettingValue = -9999;

#pragma pack(4)  //4-byte alignment

struct _PrePostCommand
{
	_rrString25	name;
	bool		enabled;
	quint8		type;
	qint32		paramA,paramB;
};

struct _CustomOptions
{
	_rrString25	name;
	bool		enabled;
	qint32		value;
};

#pragma pack()  


} //namespace rrRS 







namespace rrRA { 



//class _RenderAppList;



#pragma pack(4)  //4-byte alignment


struct _RenderAppBasic //used in jobs and _RenderApp
{
private:
    int         m_version_minor;

public:
    _rrString25  name;
    _rrString25  rendererName;
    qint16      version;
    _rrString25  type;


    _rrString25  rendererVersion;
    bool        tiled;
    quint8      isWhichBit;

    qint8       renderAppListID;

    void	   clearBasic(){type.clear(); name.clear();	rendererName.clear();	version=0;	m_version_minor=0;	rendererVersion.clear();	tiled=false;	isWhichBit=0;	renderAppListID=-1; };
    int		&  getVersionMinor() { return m_version_minor;};
#ifdef QT_CORE_LIB
    void       setVersionBoth(QString ver) {
                                        if (ver.contains('.',Qt::CaseInsensitive)) {
				                            version=ver.left(ver.indexOf('.')).toInt();
				                            ver.remove(0,ver.indexOf('.')+1);
                                            if (ver.contains('.',Qt::CaseInsensitive)) {
                                                ver=ver.left(ver.indexOf('.'));
                                            }
                                            setVersionMinor(ver);
                                            } else {
                                                version=ver.toInt();
                                            }
                                           };
    void	   setVersionMinor(QString ver) {if (ver.size()>3) {ver.truncate(3); } m_version_minor=ver.toInt(); if (ver.size()==1) m_version_minor*=100; else if (ver.size()==2) m_version_minor*=10; };
	QString	   getVersionMinorDisplay() const {
                            QString t=QString("%1").arg(m_version_minor,3,10,QChar('0'));
							while ((t.size()>1) && (t.at(t.size()-1)==QChar('0'))) t.truncate(t.size()-1); 
							return t;};
#else
	void	   setVersionMinor(_rrString8_25 ver) {if (ver.length>3) {ver.length=3; } version_minor=atoi(ver.value); if (ver.length==1) version_minor*=100; else if (ver.length==2) version_minor*=10; };
	_rrString8_25	 getVersionMinorDisplay() {
							_rrString8_25 t("000");
						#ifdef RR_OS_WIN
							if (version_minor<10) _itoa_s(version_minor,&t.value[2],25,10);
							else if (version_minor<100) _itoa_s(version_minor,&t.value[1],25,10);
							else _itoa_s(version_minor,t.value,25,10);
						#else
                            if (version_minor<10)       sprintf(&t.value[2],"%d",version_minor);
                            else if (version_minor<100) sprintf(&t.value[1],"%d",version_minor);
                            else                        sprintf(&t.value[0],"%d",version_minor);
						#endif
							t.calcLength();
							while (t.endsWith('0')) t.length--;
							t.value[t.length]=0;
							return t;};
#endif
};

#pragma pack()  


} //namespace


#endif 


