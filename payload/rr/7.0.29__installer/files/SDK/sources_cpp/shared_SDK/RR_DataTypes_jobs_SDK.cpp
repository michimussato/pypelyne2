
#include "RR_DataTypes_jobs_SDK.h"
//#include "RR_DataTypes_RR_SDK.h"
#include "RR_defines_SDK.h"
//#include "../sharedLib/RR_files_SDK.h"
//#include "math.h"

#ifndef rrPlugin
#ifdef QT_CORE_LIB
  #if (defined(defrrServerconsole))
  #endif
#endif
#endif

#ifdef DEF_RenderAppsStruct
    //#include "../shared/RR_DataTypes_RenderApp.h"
#endif


#ifdef DEF_Python
#undef slots
#undef signals
#undef METHOD
#undef SIGNAL
#undef SLOT
//#include "../shared/RR_Python_embedded.h"
#endif



namespace  rrJ {

void _IDShort::fromInt32(quint32 id)
{
    m_passID= id & 0xFF;
    id = id >> 8;
    m_sec10= id & 0xFFFF;
    id = id >> 16;
    m_sec10_more=id;
}

quint32 _IDShort::int32()
{
    quint32 ret=0;
    ret+=m_passID;
    ret+=m_sec10 << 8;
    ret+=m_sec10_more << 24;
    return ret;
}

#ifdef QT_CORE_LIB
QString _IDShort::str()
{
    _IDDecomp tmp;
    tmp.m_passID=m_passID;
    tmp.m_subIP3=0;
    tmp.m_subIP4=0;
    tmp.m_random=0;
    tmp.m_time_msec=m_sec10_more  << 16;
    tmp.m_time_msec+=m_sec10;
    tmp.m_time_msec*=(1000*10);
    return tmp.str();
}
#endif

void _IDShort::fromIDDecomp(_IDDecomp id)
{
    m_passID=id.m_passID;
    id.m_time_msec/=(1000*10); 
    m_sec10=(id.m_time_msec & 0xFFFF);
    id.m_time_msec=id.m_time_msec >> 16;
    m_sec10_more=(id.m_time_msec & 0xFF);
}

void _IDShort::fromID(const quint64 &ID)
{
    _IDDecomp help;
    help.fromID(ID);
    this->fromIDDecomp(help);
}


void _IDDecomp::fromID(const quint64 &ID)
{
    *this=*((_IDDecomp *) &ID);
}

#ifdef QT_CORE_LIB
QString	_IDDecomp::str()
{
    QString ret;
	ret="}";
    //ID is created in reverse.
	if (m_passID>0) {
		m_passID-=1;
		ret=ID_letters_small.at(m_passID % ID_letters_small.size()) + ret;
		m_passID/=ID_letters_small.size();
		if (m_passID>0) 
			ret=ID_letters_small.at(m_passID % ID_letters_small.size()) + ret;
	} 

	m_time_msec/=(1000*10);                                    //=> different every 10 seconds
	ret=ID_letters.at(m_time_msec % ID_letters.size()) + ret;  //repeats every 6 minutes
	m_time_msec/=ID_letters.size();
	ret=ID_letters.at((m_time_msec) % ID_letters.size()) + ret;//repeats every 4h
	m_time_msec/=ID_letters.size();
	ret=ID_letters.at((m_time_msec) % ID_letters.size()) + ret;//repeats every 5,3d

	ret="{"+ret;
	return ret;	
}

QString	_IDDecomp::strFull()
{
	QString ret;
	ret="";
	quint32 time_rem;
	time_rem=(m_time_msec % (1000*60/6));

	ret=ID_letters.at(m_subIP3 % ID_letters.size()) + ret;
	ret=ID_letters.at(m_subIP4 % ID_letters.size()) + ret; 
	time_rem/=ID_letters.size();
	ret=ID_letters.at((time_rem) % ID_letters.size()) + ret;
	ret=ID_letters.at(time_rem % ID_letters.size()) + ret;
	ret="_"+ret;


	//this is the same as the short ID:
	if (m_passID>0) {
		m_passID-=1;
		ret=ID_letters_small.at(m_passID % ID_letters_small.size()) + ret;
		m_passID/=ID_letters_small.size();
		if (m_passID>0) 
			ret=ID_letters_small.at(m_passID % ID_letters_small.size()) + ret;
	} //else ret=' ' + ret;
	m_time_msec/=(1000*60/6); //=> 10 seconds-minutes
	ret=ID_letters.at(m_time_msec % ID_letters.size()) + ret;  //repeats every 6 minutes
	m_time_msec/=ID_letters.size();
	ret=ID_letters.at((m_time_msec) % ID_letters.size()) + ret;//repeats every 4h
	m_time_msec/=ID_letters.size();
	ret=ID_letters.at((m_time_msec) % ID_letters.size()) + ret;//repeats every 5,3d
	//ret="{"+ret;
	return ret;	
}

QString	ID2str(const quint64 &ID)
{
	_IDDecomp help;
    help.fromID(ID);
    return  help.str();
}

QString	ID2strFull(const quint64 &ID)
{
	_IDDecomp help;
    help.fromID(ID);
    return  help.strFull();
}

void getSSV(QString name,_rrString25 &scene,_rrString25 &shot,_rrString25 &version, QString sceneCfg, QString shotCfg, QString versionCfg, QString sceneCfgEnd, QString shotCfgEnd, QString versionCfgEnd, int sceneCfgLength, int shotCfgLength  )
{
    if (sceneCfg!="none") {
        scene.clear();
        bool foundIt=true;
        if (sceneCfg.isEmpty()) {

        } else if (name.indexOf(sceneCfg,0,Qt::CaseInsensitive)>=0) {
            name.remove(0,name.indexOf(sceneCfg,0,Qt::CaseInsensitive));
            name.remove(0,sceneCfg.length());
        } else {
            foundIt=false;
        }
        if (foundIt) {
            if (sceneCfgLength>0) {
                scene=name.left(sceneCfgLength);
            } else if ((!sceneCfgEnd.isEmpty()) && name.indexOf(sceneCfgEnd,0,Qt::CaseInsensitive)>=0) {
                scene=name.left(name.indexOf(sceneCfgEnd,0,Qt::CaseInsensitive));
            } else if (name.indexOf('_')>0) {
                scene=name.left(name.indexOf('_'));
            } else if (name.indexOf('.')>0) {
                scene=name.left(name.indexOf('.'));
            } else scene=name;
            name.remove(0,scene.length);
        }
    }


    if (shotCfg!="none") {
        shot.clear();
        bool foundIt=true;
        if (shotCfg.isEmpty()) {

        } else if (name.indexOf(shotCfg,0,Qt::CaseInsensitive)>=0) {
            name.remove(0,name.indexOf(shotCfg,0,Qt::CaseInsensitive));
            name.remove(0,shotCfg.length());
        } else {
            foundIt=false;
        }
        if (foundIt) {
            if (shotCfgLength>0) {
                shot=name.left(shotCfgLength);
            } else if ((!shotCfgEnd.isEmpty()) && name.indexOf(shotCfgEnd,0,Qt::CaseInsensitive)>=0) {
                shot=name.left(name.indexOf(shotCfgEnd,0,Qt::CaseInsensitive));
            } else if (name.indexOf('_')>0) {
                shot=name.left(name.indexOf('_'));
            } else if (name.indexOf('.')>0) {
                shot=name.left(name.indexOf('.'));
            } else shot=name;
            name.remove(0,shot.length);
        }
    }


    
    if (versionCfg!="none") {
        version.clear();
        bool foundIt=true;
        if (versionCfg.isEmpty()) {

        } else if (name.indexOf(versionCfg,0,Qt::CaseInsensitive)>=0) {
            name.remove(0,name.indexOf(versionCfg,0,Qt::CaseInsensitive));
            name.remove(0,versionCfg.length());
        } else {
            foundIt=false;
        }
        if (foundIt) {
            if ((!shotCfgEnd.isEmpty()) && name.indexOf(versionCfgEnd,0,Qt::CaseInsensitive)>=0) {
                version=name.left(name.indexOf(versionCfgEnd,0,Qt::CaseInsensitive));
            } else if (name.indexOf('_')>0) {
                version=name.left(name.indexOf('_'));
            } else if (name.indexOf('.')>0) {
                version=name.left(name.indexOf('.'));
            } else version=name;
            name.remove(0,version.length);
        }
    }
}

/*
QString	numberToStr(quint64 number,const int &length)
{
	QString ret;
	ret=""; 
	for (int i=0; i<length; i++) {
		ret=ID_letters.at(number % ID_letters.size()) + ret;
		number/=ID_letters.size();
		if (number==0) break;
	}
	return ret;	
}*/


QString getDirectoryNo(QString dir, int start, int count)
{
	if (dir.size()<5) return dir;
	if (start<0) start=0;

	if (dir.at(1)==PD) dir.remove(0,2);
	if (dir.at(0)==PD) dir.remove(0,1);
	if ((dir.at(1)==':') && (dir.at(2)==PD)) dir.remove(0,3);
	for (int i=1; i<start; i++) {
		if (dir.indexOf(PD)<0) return dir;
		else dir.remove(0,dir.indexOf(PD)+1);
	}
	for (int i=1; i<count; i++) {
		if (dir.indexOf(PD)<0) return dir;
		else dir.replace(dir.indexOf(PD),1,'_');
	}
	if (dir.indexOf(PD)>0) dir.truncate(dir.indexOf(PD));
	return dir;
}

QString getDirectoryUntilNo(QString dir, int start, int count)
{
    QString orgdir=dir;

	if (dir.size()<5) return dir;
	if (start<0) start=0;

	if (dir.at(1)==PD) dir.remove(0,2);
	if (dir.at(0)==PD) dir.remove(0,1);
	if ((dir.at(1)==':') && (dir.at(2)==PD)) dir.remove(0,3);
	for (int i=1; i<start; i++) {
		if (dir.indexOf(PD)<0) return dir;
		else dir.remove(0,dir.indexOf(PD)+1);
	}
	for (int i=1; i<count; i++) {
		if (dir.indexOf(PD)<0) return dir;
        else dir.replace(dir.indexOf(PD),1,"%#%");
	}
    //same function as above, everything removed, but we need actually the opposite.

    //ok, first remove the last part, now it is really the opposite:
	if (dir.indexOf(PD)>0) dir.remove(0,dir.indexOf(PD)+1);
    else dir="";
    dir.replace("%#%",PDs);

    orgdir.truncate(orgdir.length()- dir.length());
    return orgdir;
}




#endif





#ifdef QT_CORE_LIB

QString	jobStatusAsString(quint8 Status)
{
	QString ret;
	if (Status >=sFinished) ret+="Finished";
	else if (Status >=sScriptFinished) ret+="Script Finished";
	else if (Status >=sWaitForApprovalDone) ret+="Approval Wait";
	else if (Status >=sScriptPostRender) ret+="Script Post Render";
	else if (Status >=sMainRender) ret+="Render";
	else if (Status >=sWaitForApprovalMain) ret+="Approval Wait";
    else if (Status >=sScriptAfterPreview) ret+="Script Preview";
	else if (Status >=sPreviewRender) ret+="Preview";
	else if (Status >=sScriptPreRender) ret+="Pre Render";
	else if (Status >=sWaitForJobs) 
	{
		ret+="Wait for jobs";
	}
	else ret+="First Check";

	return ret;
}
#endif




} // end namespace rrj
