
#include "RR_DataTypes_jobs_comm_SDK.h"
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

#ifdef QT_CORE_LIB
  #include <QStringList>
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







#ifdef QT_CORE_LIB


QString	_JobMinInfo::IDstr() const
{ 
	return rrJ::ID2str(m_ID); 
};

QString     _SettingsOnly::custom_UserInfo() const
{
    return custom_Str(CUSTOMUserInfoName);
}

void        _SettingsOnly::customSet_UserInfo(const QString &info)
{
    customSet_Str(CUSTOMUserInfoName,info);

}

QString     _SettingsOnly::custom_StrByID(const int &id) const
{
    if (id<0 || id>=m_customData_MaxValues) return QString();
    int itemNr=0;
    for (int p=0; p<m_customData_FirstValuePos; p++) {
        if (itemNr==id) {
            CUSTOMData_Modes mode;
            if (m_customDataBlock[p]==CUSTOMData_ModeUni)
                mode=cdUnicode;
            else if (m_customDataBlock[p]==CUSTOMData_ModeChar)
                mode=cdChar;
            else break; //not a string format
            p++;
            int posStart=(m_customDataBlock[p] << 8) +m_customDataBlock[p+1];
            p+=2;
            int length=(m_customDataBlock[p] << 8) +m_customDataBlock[p+1];
            p+=2;
            //char *name= (char *) &customDataBlock[p];
            //nameLen=strlen(name);
            return custom_sub(posStart, length,mode);
        }
        if (m_customDataBlock[p]==0) itemNr++;
    }
    return QString();
}


int       _SettingsOnly::custom_maxIDs() const
{
    return m_customData_MaxValues;
}


QString     _SettingsOnly::custom_NameByID(const int &id) const
{
    if (id<0 || id>=m_customData_MaxValues) return  QString();
    int itemNr=0;
    for (int p=0; p<m_customData_FirstValuePos; p++) {
        if (itemNr==id) {
            CUSTOMData_Modes mode;
            if (m_customDataBlock[p]==CUSTOMData_ModeUni)
                mode=cdUnicode;
            else if (m_customDataBlock[p]==CUSTOMData_ModeChar)
                mode=cdChar;
            else break; //not a string format
            p++;
            //int posStart=(customDataBlock[p] << 8) +customDataBlock[p+1];
            p+=2;
            //int length=(customDataBlock[p] << 8) +customDataBlock[p+1];
            p+=2;
            char *name= (char *) &m_customDataBlock[p];
            return QString::fromLatin1(name);
        }
        if (m_customDataBlock[p]==0) itemNr++;
    }
    return QString();
}


QString     _SettingsOnly::custom_Str(const QString &inName) const
{
    for (int p=0; p<m_customData_FirstValuePos; ) {
            CUSTOMData_Modes mode;
            if (m_customDataBlock[p]==CUSTOMData_ModeUni)
                mode=cdUnicode;
            else if (m_customDataBlock[p]==CUSTOMData_ModeChar)
                mode=cdChar;
            else break; //not a string format
            p++;
            int posStart=(m_customDataBlock[p] << 8) +m_customDataBlock[p+1];
            p+=2;
            int length= (m_customDataBlock[p] << 8) +m_customDataBlock[p+1];
            p+=2;
            char *name= (char *) &m_customDataBlock[p];
            if (QString::fromLatin1(name).compare(inName,Qt::CaseInsensitive)==0)
                return custom_sub(posStart, length,mode);
            p+=int(strlen(name))+1;
    }
    return QString();
}


void        _SettingsOnly::customSet_Str(const QString &name,const QString &data)
{
    QStringList names, values;  
    custom_All(names, values);  
    bool foundit=false;
    for (int v=0; v<values.count(); v++) {
        if (names[v].compare(name,Qt::CaseInsensitive)==0) {
            foundit=true;
            if (data.isEmpty()) {
                values.removeAt(v);
                names.removeAt(v);
            } else values[v]=data;
        }
    }
    if (!foundit && !data.isEmpty()) {
        names.append(name);
        values.append(data);
    }
    customSet_All(names, values);  
}

void        _SettingsOnly::customSet_StrByID(const int &id, const QString &data)
{
    if (id<0 || id>=m_customData_MaxValues) return ;
    QStringList names, values;  
    custom_All(names, values);  
    if (data.isEmpty()) {
        values.removeAt(id);
        names.removeAt(id);
    } else values[id]=data;
    customSet_All(names, values);  
}

QString _SettingsOnly::custom_sub(const int &position,const int &length,const CUSTOMData_Modes &mode) const
{
    QString ret;
    int p=position;
    while (ret.length()<length) {
        if (mode==cdUnicode) {
            rrChar c=(m_customDataBlock[p] << 8) +m_customDataBlock[p+1];
            p+=2;
            ret+=c;
        } else {
            char c=m_customDataBlock[p];
            p++;
            ret+=c;
        }
    }
    return ret;
}


void        _SettingsOnly::custom_All( QStringList &names, QStringList &values) const
{
    names.clear();
    values.clear();
    for (int p=0; p<m_customData_FirstValuePos; ) {
            CUSTOMData_Modes mode;
            if (m_customDataBlock[p]==CUSTOMData_ModeUni)
                mode=cdUnicode;
            else if (m_customDataBlock[p]==CUSTOMData_ModeChar)
                mode=cdChar;
            else break; //not a string format
            p++;
            quint16 posStart=(m_customDataBlock[p] << 8) +m_customDataBlock[p+1];
            p+=2;
            quint16 length=(m_customDataBlock[p] << 8) +m_customDataBlock[p+1];
            p+=2;
            char *name= (char *) &m_customDataBlock[p];
            names.append(QString::fromLatin1(name));
            values.append(custom_sub(posStart, length,mode));
            p+=int(strlen(name))+1;
    }
}


void        _SettingsOnly::customSet_All(const QStringList &names,const QStringList &values)
{
    memset(m_customDataBlock,0,CUSTOMDataBlockSize);
    m_customData_MaxValues=names.count();
    if (m_customData_MaxValues>values.count()) m_customData_MaxValues=values.count();

    //check which value is unicode
    QList<bool> isUnicode;
    for (int i=0; i<m_customData_MaxValues; i++) {
        QString curValue=values[i];
        bool curUni=false;
        for (int c=0; c<curValue.length(); c++) {
            if (curValue.at(c)>0xFF) {
                curUni=true;
                break;
            }
        }
        isUnicode.append(curUni);
    }

    //put all names into data array and remember the position for the data offset number
    QList<int> posSetArray;
    int p=0;
    for (int i=0; i<m_customData_MaxValues; i++) {
        if (isUnicode.at(i))
            m_customDataBlock[p]=CUSTOMData_ModeUni;
        else
            m_customDataBlock[p]=CUSTOMData_ModeChar;
        p++;
        posSetArray.append(p); //data offset position
        p+=2; 
        quint16 len= values[i].length();
        m_customDataBlock[p]=(len >> 8) & 0xFF;
        m_customDataBlock[p+1]=(len & 0xFF );
        p+=2;
        QString name=names[i];
        for (int c=0; c<name.length(); c++) {
            m_customDataBlock[p]=name.at(c).unicode() & 0xFF;
            p++;
        }
        m_customDataBlock[p]=0; // string end \0
        p++;
        if (p+10>CUSTOMDataBlockSize) {
            m_customData_MaxValues=i;
            break;
        }
    }

    //put all values into data array
    m_customData_FirstValuePos=p;
    QList<int> posArray;
    for (int i=0; i<m_customData_MaxValues; i++) {
        posArray.append(p);
        QString val=values[i];
        if (isUnicode.at(i)) {
            for (int c=0; c<val.length(); c++) {
                m_customDataBlock[p]=(val.at(c).unicode() >> 8 ) & 0xFF;
                m_customDataBlock[p+1]=val.at(c).unicode() & 0xFF;
                p+=2;
            }
        } else {
            for (int c=0; c<val.length(); c++) {
                m_customDataBlock[p]=val.at(c).unicode() & 0xFF;
                p++;
            }
        }
    }
    m_customData_MaxBufferUsage=p;

    //update data offset positions
    for (int i=0; i<m_customData_MaxValues; i++) {
        p=posSetArray.at(i);
        m_customDataBlock[p]=(posArray.at(i) >> 8 )& 0xFF;
        m_customDataBlock[p+1]=posArray.at(i) & 0xFF;
    }
}

#endif   //QT_CORE_LIB












_JobCommandSend::_JobCommandSend()
{
	memset(this,0, sizeof(_JobCommandSend));
	m_userID=-1;	
	m_count=0;
}


_JobCommandSend::_JobCommandSend(qint16 inUserID)
{
	memset(this,0, sizeof(_JobCommandSend));
	m_userID=inUserID;	
	m_count=0;
}


#ifdef QT_CORE_LIB
QString		_JobCommandSend::idsAsString()
{
	QString ret;
	for (int j=0; j<m_count; j++) {
		ret+=ID2str(m_jobIDs[j])+", ";
		if (j % 10==9) {ret+="\n";}
	}
	return ret;
}
#endif


_JobSettingsSend::_JobSettingsSend() {
	clear();
}

void _JobSettingsSend::clear()
{
	memset(this,0, sizeof(_JobSettingsSend));
	StructureID=StructureID_JobSettingsOnly;
	VariablesID=VariablesID_JobSettingsOnly;
	m_userID=-1;	
	m_count=0;
}

#ifdef QT_CORE_LIB
QString		_JobSettingsSend::idsAsString()
{
	QString ret;
	for (int j=0; j<m_count; j++) {
		ret+=ID2str(m_jobIDs[j])+", ";
		if (j % 10==9) {ret+="\n";}
	}
	return ret;
}
#endif



} // end namespace rrj
