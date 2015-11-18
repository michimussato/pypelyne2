#include "RR_DataTypes_other_SDK.h" //NOT _rrString.h, other_SDK.h includes _rrString.h
#include "RR_DataTypes_rrString.h"

//#include "RR_files_SDK.h"




_rrString25 int2Str(const int &number) 
{ 
	_rrString25 ret;
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
	_itow_s(number,ret.value,ret.ArraySize,10); 
//	swprintf_s(ret.value,ret.ArraySize,L"%d",number);
#else
    _rrString8_25 ret2;
    sprintf(ret2.value,"%d",number);
    ret2.calcLength();
    ret=ret2.value;
#endif

	ret.calcLength(); 
	return ret;
	};  


_rrString25 float2Str(float number,const int &precision ,const  rrChar &decMark)
{
    _rrString25 ret;
    _rrString25 ret2;
    int numInt=int(number);
    float mult=1.0f;
    for (int i=0; i<precision; i++) mult*=10.0f;
    int numInt2= (int) rrRound( (number-float(numInt))*mult );

#if (defined(RR_OS_WIN) && defined(_MSC_VER))
	_itow_s(numInt,ret.value,ret.ArraySize,10); 
    _itow_s(numInt2,ret2.value,ret.ArraySize,10); 
    ret.calcLength(); 
    ret2.calcLength(); 
#else
    _rrString8_25 retT;
    sprintf(retT.value,"%d",numInt);
    retT.calcLength();
    ret=retT.value;
    sprintf(retT.value,"%d",numInt2);
    retT.calcLength();
    ret2=retT.value;
#endif
    ret+=decMark;
    for (int i=ret2.length; i<precision; i++) ret+='0';
    ret+=ret2;
	return ret;
}


bool rrIsDigit(const rrChar &b) 
{
    return (
        (b=='0')
        || (b=='1')
        || (b=='2')
        || (b=='3')
        || (b=='4')
        || (b=='5')
        || (b=='6')
        || (b=='7')
        || (b=='8')
        || (b=='9')
        || (b=='-')
        ) ;
}



#ifdef  QT_CORE_LIB



QString toXmlString(QString txt)
{
    QString xml;
    xml=txt.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\"","&quot;").replace("'","&apos;")
        .replace(QChar(196),"&#196;").replace(QChar(214),"&#214;").replace(QChar(220),"&#220;").replace(QChar(228),"&#228;").replace(QChar(246),"&#246;").replace(QChar(252),"&#252;").replace(QChar(223),"&#223;").remove("\0").toLatin1();
    return xml;
}


QString fromXmlString(QString txt)
{
    QString xml;
    xml=txt.replace("&lt;","<").replace("&gt;",">").replace("&quot;","\"").replace("&apos;","'").replace("&amp;","&")
        .replace("&#196;",QChar(196)).replace("&#214;",QChar(214)).replace("&#220;",QChar(220)).replace("&#228;",QChar(228)).replace("&#246;",QChar(246)).replace("&#252;",QChar(252)).replace("&#223;",QChar(223))
        .remove("\0").toLatin1();
    return xml;
}


QString byte2Hex(const quint8 *buffer, const int &size)
{
	QString ret;
	for (int i=0; i<size; i++) {
		ret+=QString("%1").arg(buffer[i],2,16,QChar('0'));
	}
	return ret;
}

void cutAtFirstOccurence(QString &strg, const QString &cutA,const QString &cutB, const QString &cutC)
{
	if (strg.isEmpty()) return;
	int posA=-1;
	int posB=-1;
	int posC=-1;
	if (!cutA.isEmpty()) posA=strg.indexOf(cutA,0,Qt::CaseInsensitive);
	if (!cutB.isEmpty()) posB=strg.indexOf(cutB,0,Qt::CaseInsensitive);
	if (!cutC.isEmpty()) posC=strg.indexOf(cutC,0,Qt::CaseInsensitive);

	if ((posA<0)  || ((posB>=0) && posB<posA)) posA=posB;
	if ((posA<0)  || ((posC>=0) && posC<posA)) posA=posC;
	if (posA>=0) strg.truncate(posA);
}


void cutAtLastOccurence(QString &strg, const QString &cutA,const QString &cutB, const QString &cutC)
{
	if (strg.isEmpty()) return;
	int posA=-1;
	int posB=-1;
	int posC=-1;
	if (!cutA.isEmpty()) posA=strg.lastIndexOf(cutA,-1,Qt::CaseInsensitive);
	if (!cutB.isEmpty()) posB=strg.lastIndexOf(cutB,-1,Qt::CaseInsensitive);
	if (!cutC.isEmpty()) posC=strg.lastIndexOf(cutC,-1,Qt::CaseInsensitive);

	if ((posA<0)  || ((posB>=0) && posB>posA)) posA=posB;
	if ((posA<0)  || ((posC>=0) && posC>posA)) posA=posC;
	if (posA>=0) strg.truncate(posA);
}


void splitAtFirstOccurence(QString &strg, QString &strg2, const QString &cutA,const QString &cutB, const QString &cutC)
{
	if (strg.isEmpty()) return;
	int posA=-1;
	int posB=-1;
	int posC=-1;
	if (!cutA.isEmpty()) posA=strg.indexOf(cutA,0,Qt::CaseInsensitive);
	if (!cutB.isEmpty()) posB=strg.indexOf(cutB,0,Qt::CaseInsensitive);
	if (!cutC.isEmpty()) posC=strg.indexOf(cutC,0,Qt::CaseInsensitive);

	if ((posA<0)  || ((posB>=0) && posB<posA)) posA=posB;
	if ((posA<0)  || ((posC>=0) && posC<posA)) posA=posC;
	if (posA>=0) {
		strg2=strg;
		strg2.remove(0,posA);
		strg.truncate(posA);
	}
}


void splitAtLastOccurence(QString &strg, QString &strg2, const QString &cutA,const QString &cutB, const QString &cutC)
{
	if (strg.isEmpty()) return;
	int posA=-1;
	int posB=-1;
	int posC=-1;
	if (!cutA.isEmpty()) posA=strg.lastIndexOf(cutA,-1,Qt::CaseInsensitive);
	if (!cutB.isEmpty()) posB=strg.lastIndexOf(cutB,-1,Qt::CaseInsensitive);
	if (!cutC.isEmpty()) posC=strg.lastIndexOf(cutC,-1,Qt::CaseInsensitive);

	if ((posA<0)  || ((posB>=0) && posB>posA)) posA=posB;
	if ((posA<0)  || ((posC>=0) && posC>posA)) posA=posC;
	if (posA>=0) {
		strg2=strg;
		strg2.remove(0,posA);
		strg.truncate(posA);
	}
}


QString rrrShortNameLetters="ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789_-";


QString rrCalcShortName(const QString &longName)
{
	QString shortname;
	int i=0;
	shortname="";
	if (longName.startsWith("co",Qt::CaseInsensitive)  && (longName.compare("Color_ID",Qt::CaseInsensitive)!=0) && (longName.compare("CompanyProjectName",Qt::CaseInsensitive)!=0)) {
		shortname="co";
		i=2;
	} else if (longName.startsWith("pp",Qt::CaseInsensitive)) {
		shortname="pp";
		i=2;
	} else if (longName.startsWith("os",Qt::CaseInsensitive)) {
		shortname="os";
		i=2;
	}

	for (; i<longName.size();i++) {
		if (rrrShortNameLetters.indexOf(longName.at(i),0, Qt::CaseSensitive)>=0) {
			shortname+=longName.at(i);
		}
	}
	return shortname;
}

bool _rrStringCompareShort(const QString &strg1, QString strg2) 
{
	strg2=strg2.remove(' ');
	if (strg1.toUpper()==(strg2.toUpper())) return true;
	if (strg1.length()<10 || strg2.length()<10) return (rrCalcShortName(strg1)==rrCalcShortName(strg2));
	return false;
}

QString rrFromRRUTF8(QString txt)
{
	int pstart=txt.indexOf("<UTF8",0,Qt::CaseInsensitive);
	while (pstart>=0){
		txt.remove(pstart,5);
		if (txt.at(pstart)==' ') txt.remove(pstart,1);
		int pEnd=-1;
		for (int p=pstart; p<txt.size(); p++ ) {
			if (txt.at(p)=='>') {
					txt.remove(p,1);
					pEnd=p;
					break;
			}
		}
		if (pEnd<0) pEnd=txt.size()-1;
        QString Strg= txt.mid(pstart,pEnd-pstart).trimmed();
        Strg=Strg.fromUtf8(Strg.toLatin1());
		txt.remove(pstart, pEnd-pstart);
        txt.insert(pstart,Strg);
		pstart=txt.indexOf("<UTF8",0,Qt::CaseInsensitive);
	}

    return txt;
}

QString rrToRRUTF8(QString txt, bool keepOriginal)
{
    if (txt.contains("<UTF8")) return txt;
    for (int pos=0; pos<txt.length(); pos++) {
        if (txt[pos]>0xFF) {
			int idx;
            int sp=txt.lastIndexOf(' ',pos);
			idx=txt.lastIndexOf('\n',pos);		if (sp<idx)  sp=idx;
			idx=txt.lastIndexOf('\r',pos);		if (sp<idx)  sp=idx;
			idx=txt.lastIndexOf('\t',pos);		if (sp<idx)  sp=idx;
			if (sp<0) sp=0;
            else sp++;

            int ep=txt.indexOf(' ',pos);
			idx=txt.indexOf('\n',pos);			if (idx>0 && (ep<0 || ep>idx))  ep=idx;		
			idx=txt.indexOf('\r',pos);			if (idx>0 && (ep<0 || ep>idx))  ep=idx;		
			idx=txt.indexOf('\t',pos);			if (idx>0 && (ep<0 || ep>idx))  ep=idx;		
			if (ep<0) ep=txt.length()-1;
            else ep--;

            if (sp<=ep) {
                QString part=txt.mid(sp,ep-sp+1);
                if (keepOriginal) pos= ep+1;
                else {
                    txt.remove(sp,ep-sp+1);
                }
                QString newString;
                newString="<UTF8" + QString::fromLatin1(part.toUtf8()) + ">";
                txt.insert(sp,newString);
                pos+=newString.length();
			} 
        }
    }
    return txt;
}







QString rrSpaceTsd(qint64 value, bool keepSpaceForOptMinus)
{
    QString pre;
    if (value<0)  {
        pre="-";
        value=-value;
    } else if (keepSpaceForOptMinus)  pre=" ";

    QString ret;
    if (value>1000) {
        ret=QString("%1").arg((value % 1000),3,10,QChar('0'));
    } else {
        ret=QString("%1%2").arg(pre).arg(value);
        return ret;
    }
    value/=1000;
    if (value>1000) {
        ret=QString("%1 %2").arg((value % 1000),3,10,QChar('0')).arg(ret);
    } else {
        ret=QString("%1%2 %3").arg(pre).arg(value).arg(ret);
        return ret;
    }
    value/=1000;
    if (value>1000) {
        ret=QString("%1 %2").arg((value % 1000),3,10,QChar('0')).arg(ret);
    } else {
        ret=QString("%1%2 %3").arg(pre).arg(value).arg(ret);
        return ret;
    }
    value/=1000;
    ret=ret=QString("%1%2 %3").arg(pre).arg(value).arg(ret);
    return ret;
}


QString rrPointTsd(qint64 value, bool keepSpaceForOptMinus)
{
    QString pre;
    if (value<0)  {
        pre="-";
        value=-value;
    } else if (keepSpaceForOptMinus)  pre=" ";

    QString ret;
    if (value>1000) {
        ret=QString("%1").arg((value % 1000),3,10,QChar('0'));
    } else {
        ret=QString("%1%2").arg(pre).arg(value);
        return ret;
    }
    value/=1000;
    if (value>1000) {
        ret=QString("%1.%2").arg((value % 1000),3,10,QChar('0')).arg(ret);
    } else {
        ret=QString("%1%2.%3").arg(pre).arg(value).arg(ret);
        return ret;
    }
    value/=1000;
    if (value>1000) {
        ret=QString("%1.%2").arg((value % 1000),3,10,QChar('0')).arg(ret);
    } else {
        ret=QString("%1%2.%3").arg(pre).arg(value).arg(ret);
        return ret;
    }
    value/=1000;
    ret=ret=QString("%1%2.%3").arg(pre).arg(value).arg(ret);
    return ret;
}

QString rrMill2s(int value,const bool &showfirst)
{
	if (showfirst || value>1000) 
		return QString("%1.%2").arg(value /1000).arg(value %1000,3,10,QChar('0'));
	else
		return QString(".%2").arg(value %1000,3,10,QChar('0'));
}


QString rrSec2dhms(qint64 value)
{
	if (value > 36*3600 )
		return QString("%1d %2h").arg((value/3600/24)).arg((value/3600) % 24);
	else
		return QString("%1:%2.%3").arg((value/3600),2,10,QChar('0')).arg(((value/60)%60),2,10,QChar('0')).arg((value % 60),2,10,QChar('0'));
}

QString rrSec2dhm(qint64 value)
{
	return QString("%1d %2:%3").arg((value/3600/24)).arg((value/3600),2,10,QChar('0')).arg(((value/60)%60),2,10,QChar('0'));
}

QString rrSec2hms(int value, const bool cutfront)
{
	
	if ((!cutfront) || (value>60*60) || (value<-60*60)) {
		if (value<0) {
			return QString("%1:%2.%3").arg((value/3600),2,10,QChar('0')).arg((((-value)/60)%60),2,10,QChar('0')).arg(((-value) % 60),2,10,QChar('0'));
		} else
			return QString("%1:%2.%3").arg((value/3600),2,10,QChar('0')).arg(((value/60)%60),2,10,QChar('0')).arg((value % 60),2,10,QChar('0'));
	}
	if (value<-60 ||  value>60) {
		if (value<0) {
			return QString("%1.%2").arg(((value/60)%60),2,10).arg(((-value) % 60),2,10,QChar('0'));
		}
		else return QString("%1.%2").arg(((value/60)%60),2,10).arg((value % 60),2,10,QChar('0'));
	}
	if (value<0) {
		value=-value;
		return QString("-0.%3").arg((value % 60),2,10,QChar('0'));
	} else
		return QString(" 0.%3").arg((value % 60),2,10,QChar('0'));
}

QString rrSec2hm(int value)
{
	if (value<0)
		return QString("%1:%2").arg(value/3600,2,10,QChar('0')).arg((-value/60 )%60,2,10,QChar('0'));
	else
		return QString("%1:%2").arg(value/3600,2,10,QChar('0')).arg((value/60 )%60,2,10,QChar('0'));
}

QString rrSec2ms(qint64 value)
{
	return QString("%1.%2").arg(value/60,2,10,QChar('0')).arg(value % 60,2,10,QChar('0'));
}

QString bool2str(const bool &value, const bool &asText)
{
	if (asText) {
		if (value) return "true"; else return "false"; 
	} else if (value) return "1"; else return "0"; 
}

QString OS2String(const _rrOS &os)
{
	switch (os) {
		case rrosAll:
			return "All/Unknown";
		case rrosWindows:
			return "Windows";
		case rrosLinux:
			return "Linux";
		case rrosMac:
			return "Mac";
	}
	return "";
}

QString OS2String_short(const _rrOS &os,const bool &addBit)
{
    QString ret;
    switch (os) {
        case rrosAll:
            ret="all";
            break;
        case rrosWindows:
            ret="win";
            break;
        case rrosLinux:
            ret="lx";
            break;
        case rrosMac:
            ret="mac";
            break;
    }
    if (addBit) {
    #ifdef RRx64
        ret+="64";
    #else
        ret+="32";
    #endif
    }
    return ret;
}

QString thisOS2String_short(const bool &addBit)
{
    #ifdef RR_OS_WIN
    return OS2String_short(rrosWindows,addBit);
    #elif defined (RR_OS_LX)
    return OS2String_short(rrosLinux,addBit);
    #else
    return OS2String_short(rrosMac,addBit);
    #endif
}



QString rrFromRRUni16(QString txt)
{
	int  pstart=txt.indexOf("<UNI16",0,Qt::CaseInsensitive);
	while (pstart>=0){
		txt.remove(pstart,6);
		if (txt.at(pstart)==' ') txt.remove(pstart,1);
		int pEnd=-1;
		for (int p=pstart; p<txt.size(); p++ ) {
			if (txt.at(p)=='>') {
					txt.remove(p,1);
					pEnd=p;
					break;
			}
		}
		if (pEnd<0) pEnd=txt.size()-1;
        QString Strg= txt.mid(pstart,pEnd-pstart).trimmed();
        QString newString;
        ushort comb;
        for (int i=0; i<Strg.length()/2; i+=1) {
            comb= (Strg.at(i*2).unicode() & 0xFF) << 8;
            comb+= (Strg.at(i*2+1).unicode() & 0xFF);
            newString+=QChar(comb);
        }
        txt.remove(pstart, pEnd-pstart);
        txt.insert(pstart,newString);
		pstart=txt.indexOf("<UNI16",0,Qt::CaseInsensitive);
	}
    return txt;
}

QString rrToRRUni16(QString txt, bool keepOriginal)
{
    if (txt.contains("<UNI16")) return txt;
    for (int pos=0; pos<txt.length(); pos++) {
        if (txt[pos]>0xFF) {
            int sp=txt.lastIndexOf(' ',pos);
            if (sp<0) sp=0;
            else sp++;
            int ep=txt.indexOf(' ',pos);
            if (ep<0) ep=txt.length()-1;
            else ep--;
            if (sp<=ep) {
                QString part=txt.mid(sp,ep-sp+1);
                if (keepOriginal) pos= ep+1;
                else {
                    txt.remove(sp,ep-sp+1);
                }
                QString newString;
                newString="<UNI16";
                for (int i=0; i<part.length(); i++) {
                    QChar c=part.at(i);
                    newString+= QChar (char((c.unicode() >> 8) & 0xFF));
                    newString+= QChar (char( c.unicode()       & 0xFF));
                }
                newString+='>';
                txt.insert(pos,newString);
                pos+=newString.length();
            }

        }
    }
    return txt;
}


#endif // QT_Core








//################################################ _rrStringList  ########################################
//################################################ _rrStringList  ########################################
//################################################ _rrStringList  ########################################



_rrStringList::_rrStringList()
{
	m_count=0;
	m_args=NULL;
    memset(m_conv,0, sizeof(m_conv));
}

_rrStringList::~_rrStringList()
{
	if (m_args!=NULL) free(m_args);
	m_args=NULL;
}


void _rrStringList::append(const _rrString500 &newArg,const  bool &checkIfExist, const bool &checkCaseSensitive)
{
    if (checkIfExist && find(newArg,checkCaseSensitive)>=0) return;
	m_count++;
	if (m_args==NULL) {
		m_args =(_rrString500 *) calloc(m_count,sizeof(_rrString500));
	} else {
		m_args=(_rrString500 *) realloc(m_args,m_count*sizeof(_rrString500));
	}
	if (m_args==NULL) {
		m_count=0;
		return;
	}
	m_args[m_count-1]=newArg;
}

int _rrStringList::find(const _rrString500 &arg, const bool &caseSensitive)
{
    if (caseSensitive) {
        for (int i=0; i<m_count; i++) {
            if (arg==m_args[i]) return i;
        } 
    }  else {
        for (int i=0; i<m_count; i++) {
            if (arg.isEqual(m_args[i])) return i;
        } 
    }
    return -1;
}


_rrString500 & _rrStringList::at(const int &pos) const
{
	if ((pos>=0) && (pos<m_count)) 
		return (m_args[pos]);
	else
		return (m_args[0]);
}


char * _rrStringList::atAsChar(const int &pos) const
{
	if ((pos>=0) && (pos<m_count)) 
		m_args[pos].toChar(m_conv,500); 
	else
		m_args[0].toChar(m_conv,500); 
	return m_conv;
}


void _rrStringList::sort(const bool &nameSortedReverse)
{
    _rrString500 cpy;
	if (nameSortedReverse) {
		for (int i=m_count-1; i>0; i--) { //Bubblesort, yeah!
			for (int j=0; j<i; j++) {
				if (m_args[j].compare(m_args[j+1])<0) {
					cpy = m_args[j];
					m_args[j]=m_args[j+1];
					m_args[j+1]=cpy;
				}
			}
		}
	} else {
		for (int i=m_count-1; i>0; i--) { //Bubblesort, yeah!
			for (int j=0; j<i; j++) {
				if (m_args[j].compare(m_args[j+1])>0) {
					cpy = m_args[j];
					m_args[j]=m_args[j+1];
					m_args[j+1]=cpy;
				}
			}
		}
	}
}

void _rrStringList::copyFrom(const _rrStringList &oth)
{
    if (m_args!=NULL) free(m_args);
    m_count=oth.m_count;
    m_args =(_rrString500 *) calloc(m_count,sizeof(_rrString500));
    memcpy(m_args,oth.m_args,sizeof(_rrString500)*m_count);
}










//################################################ _rrString  ########################################
//################################################ _rrString  ########################################
//################################################ _rrString  ########################################





#undef INC_StringType
#undef INC_CharType	
#undef INC_strlen		
#undef INC_CharSize	
#define INC_StringType	_rrString8_evenSize
#define INC_CharType	char
#define INC_CharSize	1
#define INC_strlen		strlen
#include "RR_DataTypes_rrString_inc.cpp"



#undef INC_StringType
#undef INC_CharType	
#undef INC_strlen		
#undef INC_CharSize	
#define INC_StringType	_rrString8_UnevenSize
#define INC_CharType	char
#define INC_CharSize	1
#define INC_strlen		strlen
#include "RR_DataTypes_rrString_inc.cpp"



#undef INC_StringType
#undef INC_CharType	
#undef INC_strlen		
#undef INC_CharSize	
#define INC_StringType	_rrString
#define INC_CharType	rrChar
#define INC_CharSize	2
#define INC_strlen		rrCharLen
#include "RR_DataTypes_rrString_inc.cpp"



//all template types that want to be used have to be defined ones

template class _rrString8_evenSize<1000> ;
template class _rrString8_evenSize<500> ;
template class _rrString8_evenSize<250> ;
template class _rrString8_evenSize<200> ;
template class _rrString8_evenSize<150> ;
template class _rrString8_UnevenSize<125> ;
template class _rrString8_evenSize<100> ;
template class _rrString8_UnevenSize<75> ;
template class _rrString8_evenSize<50> ;
template class _rrString8_evenSize<30> ;
template class _rrString8_UnevenSize<25> ;
template class _rrString8_UnevenSize<15> ;
template class _rrString8_evenSize<12> ;
template class _rrString8_evenSize<10> ;
template class _rrString8_evenSize<8> ;
template class _rrString8_UnevenSize<7> ;
template class _rrString8_evenSize<6> ;


template class _rrString8_evenSize<40> ;
template class _rrString8_evenSize<14> ;

template class _rrString<2500> ;
template class _rrString<1000> ;
template class _rrString<500> ;
template class _rrString<250> ;
template class _rrString<225> ;
template class _rrString<200> ;
template class _rrString<150> ;
template class _rrString<125> ;
template class _rrString<100> ;
template class _rrString<75> ;
template class _rrString<50> ;
template class _rrString<30> ;
template class _rrString<25> ;
template class _rrString<10> ;

template class _rrString<48> ;
