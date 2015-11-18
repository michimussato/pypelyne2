
#include "RR_DataTypes_jobsClasses_SDK.h"
#include "RR_defines_SDK.h"
#include "RR_DataTypes_RR_sub_SDK.h"
#include "../sharedLib/RR_files_SDK.h"


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

#ifdef QT_CORE_LIB
  #include <QStringList>
#endif

#ifdef DEF_Python
#undef slots
#undef signals
#undef METHOD
#undef SIGNAL
#undef SLOT
//#include "../shared/RR_Python_embedded.h"
#endif


#ifndef min
#define min(a,b)            (((a) < (b)) ? (a) : (b))
#endif



namespace  rrJ {

_JobBasics::_JobBasics()
{
	initialize();
}

void _JobBasics::initialize()
{
	StructureIDBasics=StructureID_JobBasics;
	VariablesIDBasics=VariablesID_JobBasics;
	StructureIDSubmitter=0;
	VariablesIDSubmitter=0;
	StructureIDSave=0;
	VariablesIDSave=0;
	StructureIDSend=0;
	VariablesIDSend=0;
	StructureIDRunTime=0;
	VariablesIDRunTime=0;
	rrClearBasics();
}



void  _JobBasics::rrClearBasics()
{
	quint16 Sic_StructureIDBasics=StructureIDBasics;
	quint16 Sic_VariablesIDBasics=VariablesIDBasics;
	quint16 Sic_StructureIDSubmitter=StructureIDSubmitter;
	quint16 Sic_VariablesIDSubmitter=VariablesIDSubmitter;
	quint16 Sic_StructureIDSave=StructureIDSave;
	quint16 Sic_VariablesIDSave=VariablesIDSave;
	quint16 Sic_StructureIDSend=StructureIDSend;
	quint16 Sic_VariablesIDSend=VariablesIDSend;
	quint16 Sic_StructureIDRunTime=StructureIDRunTime;
	quint16 Sic_VariablesIDRunTime=VariablesIDRunTime;
	
	memset(this,0,sizeof(_JobBasics));

	StructureIDBasics=Sic_StructureIDBasics;
	VariablesIDBasics=Sic_VariablesIDBasics;
	StructureIDSubmitter=Sic_StructureIDSubmitter;
	VariablesIDSubmitter=Sic_VariablesIDSubmitter;
	StructureIDSave=Sic_StructureIDSave;
	VariablesIDSave=Sic_VariablesIDSave;
	StructureIDSend=Sic_StructureIDSend;
	VariablesIDSend=Sic_VariablesIDSend;
	StructureIDRunTime=Sic_StructureIDRunTime;
	VariablesIDRunTime=Sic_VariablesIDRunTime;

#ifdef RR_OS_WIN
	m_rrJobOS=rrosWindows;
#elif defined(RR_OS_MAC)
    m_rrJobOS=rrosMac;
#else
    m_rrJobOS=rrosLinux;
#endif
	m_imageFramePadding=4;
	m_seqStart=1;
	m_seqEnd=1;
	m_seqStep=1;
}





#ifdef QT_CORE_LIB
QString	_JobBasics::IDstr() const
{
    return rrJ::ID2str(m_ID);
}

QString	_JobBasics::IDstrFull() const
{
    return rrJ::ID2strFull(m_ID);
}


QString	_JobBasics::ID2str() const
{
	return rrJ::ID2str(m_ID);
}

QString	_JobBasics::ID2strFull() const
{
	return rrJ::ID2strFull(m_ID);
}




QString	_JobBasics::getSceneDisplayName()
{
	QString scene_cut = m_sceneName;
	int position;
	position = scene_cut.lastIndexOf('.');
	if (position>3) scene_cut.truncate(position);
	scene_cut.remove(PDs+"RENDER_PICTURES",Qt::CaseInsensitive);
	scene_cut.remove(PDs+"Scenes",Qt::CaseInsensitive);
    scene_cut.remove(PDs+"<FN4>",Qt::CaseInsensitive);
    scene_cut.remove("<FN4>",Qt::CaseInsensitive);
    scene_cut.remove("<FN");
    scene_cut.remove("<");
    scene_cut.remove(">");
	scene_cut.remove(PDs+PDs);

	//\greyhame\orb\_orbweaver\_production\3d\orbweaver_xsi\sh_0100\render\sh_0100_render_037_fb
	int p=scene_cut.lastIndexOf(PD);
	if (p>0) p=scene_cut.lastIndexOf(PD,p-1);
	//if (p>0) p=scene_cut.lastIndexOf(PD,p-1);
	//if (p>0) p=scene_cut.lastIndexOf(PD,p-1);
	if (p>0) {
		scene_cut.remove(0,p);
		scene_cut="..."+scene_cut;
	}
	
	//...\orbweaver_xsi\sh_0100\render\sh_0100_render_037_fb

	scene_cut.replace(":"+PDs,"))))");// next functions should not change drive
	scene_cut.replace(PDs,"((((");			  // woraround to replace "\" with " \ ", otherwise we could have an infinite loop
	scene_cut.replace("((((",PDs+QString("    ")); 
	scene_cut.replace("))))",":"+PDs);
	return scene_cut;
}


QString     _JobBasics::custom_UserInfo() const
{
    return custom_Str(CUSTOMUserInfoName);
}

void        _JobBasics::customSet_UserInfo(const QString &info)
{
    customSet_Str(CUSTOMUserInfoName,info);

}


int       _JobBasics::custom_maxIDs() const
{
    return m_customData_MaxValues;
}

QString     _JobBasics::custom_StrByID(const int &id) const
{
    if (id<0 || id>=m_customData_MaxValues) return QString();
    int itemNr=0;
    for (int p=0; p<m_customData_FirstValuePos;) {
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
        char *name= (char *) &m_customDataBlock[p];
        p+=int(strlen(name))+1;
        if (itemNr==id) {
            return custom_sub(posStart, length,mode);
        }
        itemNr++;
    }
    return QString();
}


void _JobBasics::custom_ClearAll()
{
	m_customData_MaxValues=0;
	m_customData_FirstValuePos=0;
	m_customData_MaxBufferUsage=0;
}




QString     _JobBasics::custom_NameByID(const int &id) const
{
    if (id<0 || id>=m_customData_MaxValues) return  QString();
    int itemNr=0;
    for (int p=0; p<m_customData_FirstValuePos;) {
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
        p+=int(strlen(name))+1;
        if (itemNr==id) {
            return QString::fromLatin1(name);
        }
        itemNr++;
    }
    return QString();
}


QString     _JobBasics::custom_Str(const QString &inName) const
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


void        _JobBasics::customSet_Str(const QString &name,const QString &data)
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

void        _JobBasics::customSet_StrByID(const int &id,const QString &data)
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

QString _JobBasics::custom_sub(const int &position,const int &length,const CUSTOMData_Modes &mode) const
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
            ret+=QChar(c);
        }
    }
    return ret;
}


void        _JobBasics::custom_All( QStringList &names, QStringList &values) const
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


QString _JobBasics::custom_AllAsString()
{
    QString ret;
    QStringList names, values;  
    custom_All(names, values);  
    for (int v=0; v<values.count(); v++) {
        if (names[v]==CUSTOMUserInfoName) continue;
        ret+=QString("|%1: '%2' ").arg(names[v]).arg(values[v]);
    }
    return ret;
}


bool _JobBasics::custom_isEqual(_JobBasics * otherJob)
{
    return (memcmp(otherJob->m_customDataBlock,m_customDataBlock,CUSTOMDataBlockSize)==0); 
}


void  _JobBasics::customSet_All(const QStringList &names,const QStringList &values)
{
    memset(m_customDataBlock,0,CUSTOMDataBlockSize);
    m_customData_MaxValues=names.count();
    if (m_customData_MaxValues>values.count()) m_customData_MaxValues=values.count();
    QList<bool> isUnicode;
    int maxlen=0;
    //first check which data is unicode
    for (int i=0; i<m_customData_MaxValues; i++) {
        QString curValue=values[i];
        bool curUni=false;
        maxlen+=names.at(i).length();
        maxlen+=5;
        maxlen+=values.at(i).length();
        for (int c=0; c<curValue.length(); c++) {
            if (curValue.at(c)>0xFF) {
                curUni=true;
                break;
            }
        }
        isUnicode.append(curUni);
        if (maxlen+10>CUSTOMDataBlockSize) {
            m_customData_MaxValues=i;
            break;
        }
    }
    QList<int> posSetArray;
    int p=0;
    for (int i=0; i<m_customData_MaxValues; i++) {
        if (isUnicode.at(i))
            m_customDataBlock[p]=CUSTOMData_ModeUni;
        else
            m_customDataBlock[p]=CUSTOMData_ModeChar;
        p++;
        posSetArray.append(p);//value start
        p+=2; 
        quint16 len= values[i].length();

        m_customDataBlock[p]=(len >> 8) & 0xFF;
        m_customDataBlock[p+1]=(len & 0xFF );

		quint16 result= m_customDataBlock[p] << 8;
		result+= m_customDataBlock[p+1];


        p+=2;
        QString name=names[i];
        for (int c=0; c<name.length(); c++) {
            m_customDataBlock[p]=name.at(c).unicode() & 0xFF;
            p++;
        }
        m_customDataBlock[p]=0; // string end \0
        p++;
    }
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

    for (int i=0; i<m_customData_MaxValues; i++) {
        p=posSetArray.at(i);
        m_customDataBlock[p]=(posArray.at(i) >> 8 ) & 0xFF;
        m_customDataBlock[p+1]=posArray.at(i) & 0xFF;
    }

}
#endif  //QT_CORE_LIB




#ifndef rrPlugin
#ifdef QT_CORE_LIB
#ifdef RR_OS_WIN
#else
#endif
#endif //QT_CORE_LIB
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#endif //plugin






void _JobBasics::check_SplitImageFileInto_DirFileExt_Channel(int channel,bool percentFaddingFormat)
{
	if (channel<0) return;
	if (channel>MaxImageChannels) return;
	QString str=m_imageChannels[channel].fileName;

	QString ImageFileName_org=m_imageChannels[channel].fileName;
	QString ImageExt_org=m_imageChannels[channel].extension;

	if (m_imageSingleOutputFile) {
		if (!m_imageChannels[channel].extension.isEmpty()) {
			m_imageChannels[channel].fileName=m_imageChannels[channel].fileName+m_imageChannels[channel].extension;
			m_imageChannels[channel].extension.clear();
		}
	} else {
		if (percentFaddingFormat && (m_imageChannels[channel].extension.isEmpty()) && (str.contains('%')) && (str.contains('d')) && (str.lastIndexOf('%')<str.lastIndexOf('d')) ) {
			m_imageChannels[channel].fileName=str.left(str.lastIndexOf('%'));
			str.remove(0,str.lastIndexOf('%')+1);
			QString pad=str.left(str.indexOf('d'));
			str.remove(0,str.indexOf('d')+1);
			m_imageChannels[channel].extension=str;
		} else if ((m_imageChannels[channel].extension.isEmpty()) && (str.contains('#'))) {
			str.replace("[#","#").replace("#]","#");
			m_imageChannels[channel].fileName=str.left(str.indexOf('#'));
			str.remove(0,str.indexOf('#'));
			while ((!str.isEmpty()) && (str.at(0)=='#')) {
				str.remove(0,1);
			}
			m_imageChannels[channel].extension=str;
		} else if ((m_imageChannels[channel].extension.isEmpty()) && (str.contains('.'))) {
//			int pos=str.lastIndexOf('.');
				//frame name does not contain a number, so split before extension
				QString base;
				base=str.left(str.lastIndexOf('.'));
				while ((base.size()>1) && base.at(base.size()-1).isDigit())
					base.truncate(base.size()-1);
				str.remove(0,str.lastIndexOf('.'));
				m_imageChannels[channel].fileName=base;
				m_imageChannels[channel].extension=str;
		}
		QString extUp=m_imageChannels[channel].extension;
		extUp=extUp.toUpper();
		if (
			(extUp==".AVI") || (extUp==".MOV") || (extUp==".WMV") || (extUp==".DV") || (extUp==".FLV") || 
			(extUp==".MPEG") || (extUp==".MPG") || (extUp==".MP4") || (extUp==".MPE") || 
			(extUp==".OMF") || (extUp==".OMFI") || (extUp==".MXF") || 
			(extUp==".WMA") || (extUp==".WAV") || (extUp==".MP3") || 
			(extUp==".VOB") || (extUp==".ASF") ||
			(extUp==".SWF") || (extUp==".SWFT") || (extUp==".SVG")
			) {
				m_imageChannels[channel].fileName=ImageFileName_org+ImageExt_org;
				m_imageChannels[channel].extension.clear();
				m_imageSingleOutputFile=true;
		}
	}


	QChar PDlocal;
	str=m_imageDir;
	if (str.contains('\\')) PDlocal='\\';
	else PDlocal='/';

	while (str.indexOf("\\\\",2,Qt::CaseInsensitive)>0) {
		int pos=str.indexOf("\\\\",2,Qt::CaseInsensitive);
		str.remove(pos,1);
	}
	while (str.indexOf("//",2,Qt::CaseInsensitive)>0) {
		int pos=str.indexOf("//",2,Qt::CaseInsensitive);
		str.remove(pos,1);
	}
	if ((!str.isEmpty()) && (!str.endsWith('\\')) && (!str.endsWith('/')) )
		str+=PDlocal;
	m_imageDir=str;

}

void _JobBasics::check_SplitImageFileInto_DirFileExt(bool percentPaddingFormat)
{
    //QChar pathDelim=PD;
    if (m_imageFileName.contains('\\') && m_imageFileName.contains('/')) {
        if (m_imageFileName.indexOf('\\') < m_imageFileName.indexOf('/')) {
            m_imageDir.replace('/','\\');
            //pathDelim='\\';
        } else {	
            m_imageDir.replace('\\','/');
            //pathDelim='/';
        }
    }


	if (m_imageDir.isEmpty() && (m_imageFileName.contains('\\') || m_imageFileName.contains('/'))) { //we could have read a linux or a windows scene file, path conversion is done later
		rrChar PDl='/';
		if (m_imageFileName.contains('\\')) PDl='\\';
		int posChannel=-1;
		posChannel= m_imageFileName.indexOf("<Channel>");
		int posLayer=-1;
		posLayer= m_imageFileName.indexOf("<Layer>");
        posLayer= min(posLayer,posChannel);
		int posDir= m_imageFileName.lastIndexOf(PDl,posLayer);
		if (posDir>=0) {
			m_imageDir= m_imageFileName;
			m_imageDir.setLength(posDir+1);
			m_imageFileName.remove(0,posDir+1);
		}
	}
	QString ImageFileName_org=m_imageFileName;
	QString ImageExt_org=m_imageExtension;

    if (m_imageDir.length>3 && m_imageDir.value[1]==':' &&  m_imageDir.value[2]!='/' && m_imageDir.value[2]!='\\') {
        if (m_imageDir.contains('\\')) {
            m_imageDir.insert(2,'\\');
        } else {
            m_imageDir.insert(2,'/');
        }
    }

	if (m_imageSingleOutputFile) {
		if (!m_imageExtension.isEmpty()) {
			m_imageFileName=m_imageFileName+m_imageExtension;
			m_imageExtension.clear();
		}
	} else {
		if (m_imageExtension.isEmpty() && (m_imageFileName.endsWith(".file"))) {
			//Execute jobs

		} else if (m_imageExtension.isEmpty()) {
			QString str=m_imageFileName;
			if (percentPaddingFormat && (str.contains('%')) && (str.contains('d')) && (str.lastIndexOf('%')<str.lastIndexOf('d'))) {
				m_imageFileName=str.left(str.lastIndexOf('%'));
				str.remove(0,str.lastIndexOf('%')+1);
				QString pad=str.left(str.indexOf('d'));
				str.remove(0,str.indexOf('d')+1);
				m_imageExtension=str;
				m_imageFramePadding=pad.toInt();
				if (m_imageFramePadding<1) m_imageFramePadding=1;
			} else if (str.contains('#')) {
				str.replace("[#","#").replace("#]","#");
				m_imageFileName=str.left(str.indexOf('#'));
				str.remove(0,str.indexOf('#'));
				m_imageFramePadding=0;
				while ((!str.isEmpty()) && (str.at(0)=='#')) {
					m_imageFramePadding++;
					str.remove(0,1);
				}
				m_imageExtension=str;
			} else if (str.contains('.')) {
	//			int pos=str.lastIndexOf('.');
					//frame name does not contain a number, so split before extension
					QString base;
					base=str.left(str.lastIndexOf('.'));
					while ((base.size()>1) && base.at(base.size()-1).isDigit())
						base.truncate(base.size()-1);
					str.remove(0,str.lastIndexOf('.'));
					m_imageFileName=base;
					m_imageExtension=str;
			}
		}
		QString extUp=m_imageExtension;
		extUp=extUp.toUpper();
		if (
			(extUp==".AVI") || (extUp==".MOV") || (extUp==".WMV") || (extUp==".DV") || (extUp==".FLV") || 
			(extUp==".MPEG") || (extUp==".MPG") || (extUp==".MP4") || (extUp==".MPE") || 
			(extUp==".OMF") || (extUp==".OMFI") || (extUp==".MXF") || 
			(extUp==".WMA") || (extUp==".WAV") || (extUp==".MP3") || 
			(extUp==".VOB") || (extUp==".ASF") ||
			(extUp==".SWF") || (extUp==".SWFT") || (extUp==".SVG")
			) {
				m_imageFileName=ImageFileName_org+ImageExt_org;
				m_imageExtension.clear();
				m_imageSingleOutputFile=true;
		}


		if (!m_imageSingleOutputFile) {
			if (m_imageFileName.endsWith(m_imageExtension)) {
				m_imageFileName.setLength(m_imageFileName.length-m_imageExtension.length);
			}
			for (int c=0; c<MaxImageChannels; c++) {
				QString str=m_imageChannels[c].fileName;
				if ((!m_imageChannels[c].fileName.isEmpty()) && m_imageChannels[c].extension.isEmpty()) {
					if (percentPaddingFormat && (str.contains('%')) && (str.contains('d'))  && (str.lastIndexOf('%')<str.lastIndexOf('d'))  ) {
						m_imageChannels[c].fileName=str.left(str.lastIndexOf('%'));
						str.remove(0,str.lastIndexOf('%')+1);
						QString pad=str.left(str.indexOf('d'));
						str.remove(0,str.indexOf('d')+1);
						m_imageChannels[c].extension=str;
						m_imageFramePadding=pad.toInt();
						if (m_imageFramePadding<2) m_imageFramePadding=2;
					} else if (str.contains('#')) {
						str.replace("[#","#").replace("#]","#");
						m_imageChannels[c].fileName=str.left(str.indexOf('#'));
						str.remove(0,str.indexOf('#'));
						m_imageFramePadding=0;
						while ((!str.isEmpty()) && (str.at(0)=='#')) {
							m_imageFramePadding++;
							str.remove(0,1);
						}
						m_imageChannels[c].extension=str;
					} else if (str.contains('.')) {
			//			int pos=str.lastIndexOf('.');
							//frame name does not contain a number, so split before extension
							QString base;
							base=str.left(str.lastIndexOf('.'));
							while ((base.size()>1) && base.at(base.size()-1).isDigit())
								base.truncate(base.size()-1);
							str.remove(0,str.lastIndexOf('.'));
							m_imageChannels[c].fileName=base;
							m_imageChannels[c].extension=str;
					}
				}
			}
		}
	}


	QChar PDlocal;
	QString str=m_imageDir;
	if (str.contains('\\')) PDlocal='\\';
	else PDlocal='/';

	while (str.indexOf("\\\\\\\\",0,Qt::CaseInsensitive)>=0) {
		int pos=str.indexOf("\\\\\\\\",0,Qt::CaseInsensitive);
		str.remove(pos,2);
	}
	while (str.indexOf("\\\\",2,Qt::CaseInsensitive)>0) {
		int pos=str.indexOf("\\\\",2,Qt::CaseInsensitive);
		str.remove(pos,1);
	}
	while (str.indexOf("//",2,Qt::CaseInsensitive)>0) {
		int pos=str.indexOf("//",2,Qt::CaseInsensitive);
		str.remove(pos,1);
	}
	if ((!str.isEmpty()) && (!str.endsWith('\\')) && (!str.endsWith('/')) )
		str+=PDlocal;
	m_imageDir=str;

}


void replaceSquareBracketVariablesSub(_rrString250 &txt)
{
    if (!txt.contains('[') || !txt.contains(']')) return;
    txt.replace("[User]","<User>");
    txt.replace("[LocalHost]","<LocalHost>");
    txt.replace("[CompanyProject]","<CompanyProject>");
    txt.replace("[Layer]","<Layer>");
    txt.replace("[Channel]","<Channel>");
    txt.replace("[Camera]","<Camera>");
    txt.replace("[Camera_no.]","<Camera_no.>");
    txt.replace("[Scene]","<Scene>");
    txt.replace("[SceneFolder]","<SceneFolder>");
    txt.replace("[Database]","<Database>");
    txt.replace("[DatabaseName]","<DatabaseName>");
}

void _JobBasics::replaceSquareBracketVariables()
{
    replaceSquareBracketVariablesSub(m_imageFileName);
    replaceSquareBracketVariablesSub(m_imageDir);
    for (int c=0; c<rrJ::MaxImageChannels; c++) {
        replaceSquareBracketVariablesSub(m_imageChannels[c].fileName);
    }

}














_JobBasicsArray::_JobBasicsArray()
: StructureIDBasics(StructureID_JobBasics), VariablesIDBasics(VariablesID_JobBasics),  m_structSize (sizeof(_JobBasics))
{
	clear();
	m_maxArraySize=0;
	m_jobs=NULL;
}

_JobBasicsArray::~_JobBasicsArray()
{
	free(m_jobs);
}

void _JobBasicsArray::clear()
{
	m_maxJobs=0;
	m_submitterParameter.clear();
}

bool _JobBasicsArray::setArraySize(const int &newSize)
{
	if (newSize<=m_maxArraySize) return true;
	if ((m_maxArraySize==0) || (m_jobs==NULL) ){
		m_jobs =(_JobBasics *) calloc(newSize,sizeof(_JobBasics));
		if (m_jobs) {
			for (int j=0;j<newSize;j++) {
				m_jobs[j].initialize();
			}
			m_maxArraySize=newSize;
		}
		else  return false;
	} else {
		m_jobs=(_JobBasics *) realloc(m_jobs,newSize*sizeof(_JobBasics));
		if (m_jobs) {
			for (int j=m_maxArraySize;j<newSize;j++) {
				m_jobs[j].initialize();
			}
			m_maxArraySize=newSize;
		}
		else  return false;
	}
	 return true;
}


_JobBasics * _JobBasicsArray::at(const int &j)
{
	if (j>=m_maxArraySize) return NULL;
	return &m_jobs[j];
}



bool  _JobBasicsArray::isVersionSupported(quint8	inVariablesIDBasics)
{
	return (
		(StructureIDBasics == StructureID_JobBasics) &&
		(VariablesIDBasics >= inVariablesIDBasics) &&
		(m_structSize == sizeof(_JobBasics))
		);
}


bool _JobBasicsArray::getNewJob(_JobBasics * &job)
{
	m_maxJobs++;
	setArraySize(m_maxJobs);
	job= at(m_maxJobs -1);
	if (!job) return false;
	job->rrClearBasics();
	return true;
}







} // end namespace rrJ
