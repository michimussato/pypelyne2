#ifndef RR_DataTypes_rrString_SDK_H
#define RR_DataTypes_rrString_SDK_H

#include "../shared_SDK/RR_defines_SDK.h"

// String class of constant size, no pointer used.
// This way a class keeps its size, no matter which job or which platform.
// The RRender classes can be send via TCPIP buffer, and written to a file without any special string lengthCheck and write functions.
// And they can be used in any programming language


#ifdef RR_OS_WIN
    #include <windows.h>
    #define rrStructAlign2
  #else
    #define rrStructAlign2  __attribute__((aligned(2)))
#endif
#include <string>
#include <cstring>


#ifdef RR_OS_WIN
	typedef wchar_t rrChar;  //UTF-16
	#define rrCharLen(C) (quint16)wcslen( C )
#else
	typedef unsigned short rrChar;  //UTF-16
	int rrCharLen(const rrChar *C);
#endif




#ifdef QT_CORE_LIB
    DllExport_sharedLib QString rrFromRRUTF8(QString txt);
    DllExport_sharedLib QString rrToRRUTF8(QString txt, bool keepOriginal=false);
	DllExport_sharedLib QString rrSec2dhms(qint64 value);
	DllExport_sharedLib QString rrSec2dhm(qint64 value);
	DllExport_sharedLib QString rrSec2hms(int value, const bool cutfront=false);
	DllExport_sharedLib QString rrSec2hm(int value);
	DllExport_sharedLib QString rrSec2ms(qint64  value);
	DllExport_sharedLib QString rrMill2s(int value,const bool &showfirst=false);
    DllExport_sharedLib QString rrSpaceTsd(qint64 value, bool keepSpaceForOptMinus=false);
    DllExport_sharedLib QString rrPointTsd(qint64 value, bool keepSpaceForOptMinus=false);
    DllExport_sharedLib QString bool2str(const bool &value, const bool &asText=false);
    DllExport_sharedLib inline  QString bool2String(const bool &value) {return bool2str(value); };
	DllExport_sharedLib QString OS2String(const _rrOS &os);
    DllExport_sharedLib QString OS2String_short(const _rrOS &os,const bool &addBit);
    DllExport_sharedLib QString thisOS2String_short(const bool &addBit);
    DllExport_sharedLib QString rrFromRRUni16(QString txt);  
    DllExport_sharedLib QString rrToRRUni16(QString txt, bool keepOriginal=false);  
    DllExport_sharedLib QString toXmlString(QString txt);    //converts special characters < > & into xml conform syntax
    DllExport_sharedLib QString fromXmlString(QString txt);  //converts xml conform syntax into special characters < > &
    DllExport_sharedLib bool    _rrStringCompareShort(const QString &strg1,const QString strg2);   //compares the string and then only the uppercase letters (for commandline flags)
    DllExport_sharedLib QString rrCalcShortName(const QString &longName);
    DllExport_sharedLib QString byte2Hex(const quint8 *buffer, const int &size);
    DllExport_sharedLib void    cutAtFirstOccurence(QString &strg, const QString &cutA,const QString &cutB, const QString &cutC=QString());
    DllExport_sharedLib void    cutAtLastOccurence(QString &strg, const QString &cutA,const QString &cutB, const QString &cutC=QString());
    DllExport_sharedLib void    splitAtFirstOccurence(QString &strg, QString &strg2, const QString &cutA,const QString &cutB, const QString &cutC=QString());
    DllExport_sharedLib void    splitAtLastOccurence(QString &strg, QString &strg2, const QString &cutA,const QString &cutB, const QString &cutC=QString());
#endif








#define INC_StringType	_rrString8_evenSize
#define INC_CharType	char
#define INC_CharSize	1
#define INC_strlen		strlen


#pragma pack(2) 

template <int aSize>
class _rrString8_evenSize {
  public:
    static const unsigned short ArraySize= aSize;
	char  value[aSize+1];
    char memAlign; //required for linux as templates do not use pragma pack and I get different alignments even on linux between different applications. Even with the same code...
	unsigned short length;
    DllExport_sharedLib _rrString8_evenSize() {clear(); length=0;  }
    DllExport_sharedLib _rrString8_evenSize(const rrChar * C) {clear(); length=0;  if (C==NULL) return; length=(quint16) rrCharLen(C); if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]=(C[i] & 0xFF); value[length]=0;}
    DllExport_sharedLib _rrString8_evenSize(const char * C) {clear(); length=0;  if (C==NULL) return; length=(quint16) strlen(C); if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0;}
    DllExport_sharedLib _rrString8_evenSize(const char * C, int len) {clear(); length=len; if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0;}
	DllExport_sharedLib bool operator == (const char *C) const{ if (C==NULL || (C[0]!=value[0])) return false;   int l2=(quint16) strlen(C); return ((length==l2) && (memcmp(&value[0],C,length)==0));}
	DllExport_sharedLib void operator =  (const std::string &S) { length=(quint16) S.size() & 0xFFFF; if (length>ArraySize) length=ArraySize;  for (uint i=0; i<length;i++) value[i]=S.at(i); value[length]=0; }
	DllExport_sharedLib void fromChar(const char * C, const int &len)		{if (C==NULL) { length=0; return; }  length=len; if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0; }
    DllExport_sharedLib bool isEqualUpperInput (const _rrString8_evenSize &t)  const			{ if (length!=t.length) return false; for (uint i=0; i<length;i++) if (t.value[i]!=toupper( value[i])) return false; return true;}
	DllExport_sharedLib int toInt(bool *ok=NULL) const {if (ok!=NULL) {for (uint i=0; i<length;i++) if ( (!isdigit(value[i])) && !(i==0 && value[i]=='-')) {*ok=false; return 0;} *ok=true;}   return atoi(value); }; 
	#include "RR_DataTypes_rrString_SDK_inc.h"

#ifdef RR_OS_WIN
	DllExport_sharedLib void operator =  (const rrChar * C) { if (C==NULL) {length=0; return;} length=(quint16) wcslen(C); if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]=(C[i] & 0xFF);  value[length]=0; } 
    DllExport_sharedLib void toWchar_t(wchar_t * buffer,const int &buflength) {	int len=buflength-1;  if (len>length) len=length;	MultiByteToWideChar(CP_ACP, 0, value, -1, buffer, len+1); } 
    DllExport_sharedLib void addNr(const qint64 &nr) {_i64toa_s(nr,&value[length],ArraySize-length-1,10); calcLength();}; 
    DllExport_sharedLib void addNr(const qint64 &nr, const quint8 &framepadding) {char buf[32]; _i64toa_s(nr,buf,32,10); size_t len=strlen(buf); for (size_t il=len; il<framepadding; il++) (*this)+='0'; (*this)+=buf;    }; 
#else
    DllExport_sharedLib void addNr(const int &nr) {sprintf(&value[length],"%d",nr); calcLength();};
    DllExport_sharedLib void addNr(const int &nr, const quint8 &framepadding) {char buf[32]; sprintf(buf,"%d",nr); size_t len=strlen(buf); for (size_t il=len; il<framepadding; il++) (*this)+='0'; (*this)+=buf;    };
#endif

#if (defined QT_CORE_LIB)
    DllExport_sharedLib _rrString8_evenSize(const QString &Q) { length=Q.size(); if (length>ArraySize) length=ArraySize; memcpy(&value[0],Q.toLatin1(),length); value[length]=0;}
	DllExport_sharedLib void operator =  (const QString &Q) { length=Q.size(); if (length>ArraySize) length=ArraySize; memcpy(&value[0],Q.toLatin1(),length); value[length]=0; }
    DllExport_sharedLib bool operator == (const QString &Q) const { _rrString8_evenSize t; t=Q; return (t==*this);}
    DllExport_sharedLib bool operator != (const QString &Q) const { _rrString8_evenSize t; t=Q; return (t!=*this);}
	DllExport_sharedLib operator		QString () const {return QString::fromLatin1(value,length);}
	DllExport_sharedLib void operator += (const rrChar &C) { if (length==ArraySize) return; value[length]=C & 0xFF; length++; value[length]=0; }
	DllExport_sharedLib QString operator +  (const QString &Q) { QString comp=*this; comp+=Q; return comp; }
	DllExport_sharedLib QString operator +  (const char * c) { QString comp=*this; comp+=QString::fromLatin1(c); return comp; }
	DllExport_sharedLib int lastIndexOf(const rrChar &C, int from = -1)  const {char cc=C & 0xFF; int i=length-1; if ((from>=0) && (from<length)) i=from;  for (; i>=0; i--) {if (value[i]==cc) return i;} return -1; } 
	DllExport_sharedLib int  indexOf(const rrChar &C, int from = -1) const  {char cc=C & 0xFF; int i=0; if ((from>=0) && (from<length)) i=from;  for (; i<length; i++) {if (value[i]==cc) return i;} return -1; } 
#else
	DllExport_sharedLib void operator += (const rrChar &C) { if (length==ArraySize) return; value[length]=(C & 0xFF); length++; value[length]=0; }
	DllExport_sharedLib int lastIndexOf(const rrChar &C, int from = -1) const  {char cc=(C & 0xFF); int i=length-1; if ((from>=0) && (from<length)) i=from;  for (; i>=0; i--) {if (value[i]==cc) return i;} return -1; } 
	DllExport_sharedLib int  indexOf(const rrChar &C, int from = -1) const  {char cc=(C & 0xFF); int i=0; if ((from>=0) && (from<length)) i=from;  for (; i<length; i++) {if (value[i]==cc) return i;} return -1; } 
#endif
};


#undef INC_StringType
#undef INC_CharType	
#undef INC_strlen		
#undef INC_CharSize	
#define INC_StringType	_rrString8_UnevenSize
#define INC_CharType	char
#define INC_CharSize	1
#define INC_strlen		strlen



template <int aSize>
class _rrString8_UnevenSize {
  public:
    static const unsigned short ArraySize= aSize;
	char  value[aSize+1];
	unsigned short length;
    DllExport_sharedLib _rrString8_UnevenSize() {clear(); length=0;  }
    DllExport_sharedLib _rrString8_UnevenSize(const rrChar * C) {clear(); length=0;  if (C==NULL) return; length=(quint16) rrCharLen(C); if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]=(C[i] & 0xFF); value[length]=0;}
    DllExport_sharedLib _rrString8_UnevenSize(const char * C) {clear(); length=0;  if (C==NULL) return; length=(quint16) strlen(C); if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0;}
    DllExport_sharedLib _rrString8_UnevenSize(const char * C, int len) {clear(); length=len; if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0;}
	DllExport_sharedLib bool operator == (const char * C) const{ if (C==NULL || (C[0]!=value[0])) return false;   int l2=(quint16) strlen(C); return ((length==l2) && (memcmp(&value[0],C,length)==0));}
	DllExport_sharedLib void operator =  (const std::string &S) { length=(quint16) S.size() & 0xFFFF; if (length>ArraySize) length=ArraySize;  for (uint i=0; i<length;i++) value[i]=S.at(i); value[length]=0; }
	DllExport_sharedLib void fromChar(const char * C, const int &len)		{if (C==NULL) { length=0; return; }  length=len; if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0; }
    DllExport_sharedLib bool isEqualUpperInput (const _rrString8_UnevenSize &t)  const			{ if (length!=t.length) return false; for (uint i=0; i<length;i++) if (t.value[i]!=toupper( value[i])) return false; return true;}
	DllExport_sharedLib int toInt(bool *ok=NULL) const {if (ok!=NULL) {for (uint i=0; i<length;i++) if ( (!isdigit(value[i])) && !(i==0 && value[i]=='-')) {*ok=false; return 0;} *ok=true;}   return atoi(value); }; 
	#include "RR_DataTypes_rrString_SDK_inc.h"

#ifdef RR_OS_WIN
	DllExport_sharedLib void operator =  (const rrChar * C) { if (C==NULL) {length=0; return;} length=(quint16) wcslen(C); if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]=(C[i] & 0xFF);  value[length]=0; } 
    DllExport_sharedLib void toWchar_t(wchar_t * buffer,const int &buflength) {	int len=buflength-1;  if (len>length) len=length;	MultiByteToWideChar(CP_ACP, 0, value, -1, buffer, len+1); } 
    DllExport_sharedLib void addNr(const qint64 &nr) {_i64toa_s(nr,&value[length],ArraySize-length-1,10); calcLength();}; 
    DllExport_sharedLib void addNr(const qint64 &nr, const quint8 &framepadding) {char buf[32]; _i64toa_s(nr,buf,32,10); size_t len=strlen(buf); for (size_t il=len; il<framepadding; il++) (*this)+='0'; (*this)+=buf;    }; 
#else
    DllExport_sharedLib void addNr(const int &nr) {sprintf(&value[length],"%d",nr); calcLength();};
    DllExport_sharedLib void addNr(const int &nr, const quint8 &framepadding) {char buf[32]; sprintf(buf,"%d",nr); size_t len=strlen(buf); for (size_t il=len; il<framepadding; il++) (*this)+='0'; (*this)+=buf;    };
#endif

#if (defined QT_CORE_LIB)
    DllExport_sharedLib _rrString8_UnevenSize(const QString &Q) { length=Q.size(); if (length>ArraySize) length=ArraySize; memcpy(&value[0],Q.toLatin1(),length); value[length]=0;}
	DllExport_sharedLib void operator =  (const QString &Q) { length=Q.size(); if (length>ArraySize) length=ArraySize; memcpy(&value[0],Q.toLatin1(),length); value[length]=0; }
    DllExport_sharedLib bool operator == (const QString &Q) const { _rrString8_UnevenSize t; t=Q; return (t==*this);}
    DllExport_sharedLib bool operator != (const QString &Q) const { _rrString8_UnevenSize t; t=Q; return (t!=*this);}
	DllExport_sharedLib operator		QString () const {return QString::fromLatin1(value,length);}
	DllExport_sharedLib void operator += (const rrChar &C) { if (length==ArraySize) return; value[length]=C & 0xFF; length++; value[length]=0; }
	DllExport_sharedLib QString operator +  (const QString &Q) { QString comp=*this; comp+=Q; return comp; }
	DllExport_sharedLib QString operator +  (const char * c) { QString comp=*this; comp+=QString::fromLatin1(c); return comp; }
	DllExport_sharedLib int lastIndexOf(const rrChar &C, int from = -1)  const {char cc=C & 0xFF; int i=length-1; if ((from>=0) && (from<length)) i=from;  for (; i>=0; i--) {if (value[i]==cc) return i;} return -1; } 
	DllExport_sharedLib int  indexOf(const rrChar &C, int from = -1) const  {char cc=C & 0xFF; int i=0; if ((from>=0) && (from<length)) i=from;  for (; i<length; i++) {if (value[i]==cc) return i;} return -1; } 
#else
	DllExport_sharedLib void operator += (const rrChar &C) { if (length==ArraySize) return; value[length]=(C & 0xFF); length++; value[length]=0; }
	DllExport_sharedLib int lastIndexOf(const rrChar &C, int from = -1) const  {char cc=(C & 0xFF); int i=length-1; if ((from>=0) && (from<length)) i=from;  for (; i>=0; i--) {if (value[i]==cc) return i;} return -1; } 
	DllExport_sharedLib int  indexOf(const rrChar &C, int from = -1) const  {char cc=(C & 0xFF); int i=0; if ((from>=0) && (from<length)) i=from;  for (; i<length; i++) {if (value[i]==cc) return i;} return -1; } 
#endif
};





#undef INC_StringType
#undef INC_CharType	
#undef INC_strlen		
#undef INC_CharSize	
#define INC_StringType	_rrString8_AllSize
#define INC_CharType	char
#define INC_CharSize	1
#define INC_strlen		strlen



template <int aSize>
class _rrString8_AllSize {
  public:
    static const unsigned short ArraySize= aSize;
	unsigned short length;
	char  value[aSize+1];
    DllExport_sharedLib _rrString8_AllSize() {clear(); length=0;  }
    DllExport_sharedLib _rrString8_AllSize(const rrChar * C) {clear(); length=0;  if (C==NULL) return; length=(quint16) rrCharLen(C); if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]=(C[i] & 0xFF); value[length]=0;}
    DllExport_sharedLib _rrString8_AllSize(const char * C) {clear(); length=0;  if (C==NULL) return; length=(quint16) strlen(C); if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0;}
    DllExport_sharedLib _rrString8_AllSize(const char * C, int len) {clear(); length=len; if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0;}
	DllExport_sharedLib bool operator == (const char * C) const{ if (C==NULL || (C[0]!=value[0])) return false;   int l2=(quint16) strlen(C); return ((length==l2) && (memcmp(&value[0],C,length)==0));}
	DllExport_sharedLib void operator =  (const std::string &S) { length=(quint16) S.size() & 0xFFFF; if (length>ArraySize) length=ArraySize;  for (uint i=0; i<length;i++) value[i]=S.at(i); value[length]=0; }
	DllExport_sharedLib void fromChar(const char * C, const int &len)		{if (C==NULL) { length=0; return; }  length=len; if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length); value[length]=0; }
    DllExport_sharedLib bool isEqualUpperInput (const _rrString8_AllSize &t)  const			{ if (length!=t.length) return false; for (uint i=0; i<length;i++) if (t.value[i]!=toupper( value[i])) return false; return true;}
	DllExport_sharedLib int toInt(bool *ok=NULL) const {if (ok!=NULL) {for (uint i=0; i<length;i++) if ( (!isdigit(value[i])) && !(i==0 && value[i]=='-')) {*ok=false; return 0;} *ok=true;}   return atoi(value); }; 
	#include "RR_DataTypes_rrString_SDK_inc.h"

#ifdef RR_OS_WIN
	DllExport_sharedLib void operator =  (const rrChar * C) { if (C==NULL) {length=0; return;} length=(quint16) wcslen(C); if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]=(C[i] & 0xFF);  value[length]=0; } 
    DllExport_sharedLib void toWchar_t(wchar_t * buffer,const int &buflength) {	int len=buflength-1;  if (len>length) len=length;	MultiByteToWideChar(CP_ACP, 0, value, -1, buffer, len+1); } 
    DllExport_sharedLib void addNr(const qint64 &nr) {_i64toa_s(nr,&value[length],ArraySize-length-1,10); calcLength();}; 
    DllExport_sharedLib void addNr(const qint64 &nr, const quint8 &framepadding) {char buf[32]; _i64toa_s(nr,buf,32,10); size_t len=strlen(buf); for (size_t il=len; il<framepadding; il++) (*this)+='0'; (*this)+=buf;    }; 
#else
    DllExport_sharedLib void addNr(const int &nr) {sprintf(&value[length],"%d",nr); calcLength();};
    DllExport_sharedLib void addNr(const int &nr, const quint8 &framepadding) {char buf[32]; sprintf(buf,"%d",nr); size_t len=strlen(buf); for (size_t il=len; il<framepadding; il++) (*this)+='0'; (*this)+=buf;    };
#endif

#if (defined QT_CORE_LIB)
    DllExport_sharedLib _rrString8_AllSize(const QString &Q) { length=Q.size(); if (length>ArraySize) length=ArraySize; memcpy(&value[0],Q.toLatin1(),length); value[length]=0;}
	DllExport_sharedLib void operator =  (const QString &Q) { length=Q.size(); if (length>ArraySize) length=ArraySize; memcpy(&value[0],Q.toLatin1(),length); value[length]=0; }
    DllExport_sharedLib bool operator == (const QString &Q) const { _rrString8_AllSize t; t=Q; return (t==*this);}
    DllExport_sharedLib bool operator != (const QString &Q) const { _rrString8_AllSize t; t=Q; return (t!=*this);}
	DllExport_sharedLib operator		QString () const {return QString::fromLatin1(value,length);}
	DllExport_sharedLib void operator += (const rrChar &C) { if (length==ArraySize) return; value[length]=C & 0xFF; length++; value[length]=0; }
	DllExport_sharedLib QString operator +  (const QString &Q) { QString comp=*this; comp+=Q; return comp; }
	DllExport_sharedLib QString operator +  (const char * c) { QString comp=*this; comp+=QString::fromLatin1(c); return comp; }
	DllExport_sharedLib int lastIndexOf(const rrChar &C, int from = -1)  const {char cc=C & 0xFF; int i=length-1; if ((from>=0) && (from<length)) i=from;  for (; i>=0; i--) {if (value[i]==cc) return i;} return -1; } 
	DllExport_sharedLib int  indexOf(const rrChar &C, int from = -1) const  {char cc=C & 0xFF; int i=0; if ((from>=0) && (from<length)) i=from;  for (; i<length; i++) {if (value[i]==cc) return i;} return -1; } 
#else
	DllExport_sharedLib void operator += (const rrChar &C) { if (length==ArraySize) return; value[length]=(C & 0xFF); length++; value[length]=0; }
	DllExport_sharedLib int lastIndexOf(const rrChar &C, int from = -1) const  {char cc=(C & 0xFF); int i=length-1; if ((from>=0) && (from<length)) i=from;  for (; i>=0; i--) {if (value[i]==cc) return i;} return -1; } 
	DllExport_sharedLib int  indexOf(const rrChar &C, int from = -1) const  {char cc=(C & 0xFF); int i=0; if ((from>=0) && (from<length)) i=from;  for (; i<length; i++) {if (value[i]==cc) return i;} return -1; } 
#endif
};




typedef _rrString8_evenSize<3000> _rrString8_3000;
typedef _rrString8_evenSize<1000> _rrString8_1000;
typedef _rrString8_evenSize<500> _rrString8_500;
typedef _rrString8_evenSize<250> _rrString8_250;
typedef _rrString8_evenSize<200> _rrString8_200;
typedef _rrString8_evenSize<150> _rrString8_150;
typedef _rrString8_UnevenSize<125> _rrString8_125;
typedef _rrString8_evenSize<100> _rrString8_100;
typedef _rrString8_UnevenSize<75> _rrString8_75;
typedef _rrString8_evenSize<50> _rrString8_50;
typedef _rrString8_evenSize<30> _rrString8_30;
typedef _rrString8_UnevenSize<25> _rrString8_25;
typedef _rrString8_UnevenSize<15> _rrString8_15;
typedef _rrString8_evenSize<12> _rrString8_12;
typedef _rrString8_evenSize<10> _rrString8_10;
typedef _rrString8_evenSize<8> _rrString8_8;
typedef _rrString8_UnevenSize<7> _rrString8_7;
typedef _rrString8_evenSize<6> _rrString8_6;




#undef INC_StringType
#undef INC_CharType	
#undef INC_strlen		
#undef INC_CharSize	
#define INC_StringType	_rrString
#define INC_CharType	rrChar
#define INC_CharSize	2
#define INC_strlen		rrCharLen


template <int aSize>
class _rrString {
  public:
    static const unsigned short ArraySize= aSize;
	rrChar  value[aSize+1];
	unsigned short length;
    unsigned short type; //unused for now
    DllExport_sharedLib _rrString()                          {clear(); length=0; type=0; };
    DllExport_sharedLib _rrString(const char &c)             {clear();  type=0; length=1; value[0]=c; value[length]=0;};
    DllExport_sharedLib _rrString(const char * C)            {clear(); length=0; type=0; if (C==NULL) return; length=(quint16) strlen(C); if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]=C[i]; value[length]=0;};
    DllExport_sharedLib _rrString(const char * C, int len)   {clear(); length=0; type=0; if (C==NULL) return; length=len; if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]=C[i]; value[length]=0;};
    DllExport_sharedLib _rrString(const rrChar * C, int len) {clear(); length=len; if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length*2); value[length]=0;}
    DllExport_sharedLib _rrString(const rrChar * C)          {clear(); length=0;  if (C==NULL) return; length=(quint16) rrCharLen(C); if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length*2); value[length]=0;}
    DllExport_sharedLib operator _rrString8_250() const      {_rrString8_250 comp;  toChar(comp.value,comp.ArraySize); comp.length=length; return comp;}
    DllExport_sharedLib operator _rrString8_500() const      {_rrString8_500 comp;  toChar(comp.value,comp.ArraySize); comp.length=length; return comp;}
	DllExport_sharedLib void operator += (const char &c)    { if ((length+1)>ArraySize) return; value[length]=c; length+=1; value[length]=0; };
	DllExport_sharedLib void operator += (const char * C)   { if (C==NULL) return; quint16 Clen=(quint16) strlen(C); if ((length+Clen)>ArraySize) Clen=ArraySize-length;  for (uint i=0; i<Clen;i++) value[length+i]=C[i]; length+=Clen; value[length]=0; };
	DllExport_sharedLib void operator =  (const char * C)   { if (C==NULL) return; length=(quint16) strlen(C); if (length>ArraySize) length=ArraySize; for (uint i=0; i<length;i++) value[i]= quint8(C[i]); value[length]=0; };
	DllExport_sharedLib bool operator == (const char * C) const { if (C==NULL) return false; if ((quint16) strlen(C)!=length) return false; for (uint i=0; i<length;i++) { if (value[i]!=quint8(C[i])) return false;} return true;};
	DllExport_sharedLib bool operator == (const rrChar * C) const { if (C==NULL) return false; int l2=(quint16) rrCharLen(C); return ((length==l2) && (memcmp(&value[0],C,length)==0));}
    DllExport_sharedLib void addNr(const qint64 &nr) {_rrString8_15 temp;  temp.addNr(nr); this->add(temp.value); };

    //converter:
	DllExport_sharedLib void toChar(char * c, quint16 bufLen) const	{ bufLen--; if (length<bufLen) bufLen=length; for (uint i=0; i<bufLen;i++) c[i]=value[i] &0xFF; c[bufLen]=0; };  
    DllExport_sharedLib _rrString8_250 to_rrString8_250() const { _rrString8_250 comp; toChar(comp.value,comp.ArraySize); comp.length=length; return comp; };
    DllExport_sharedLib _rrString8_500 to_rrString8_500() const { _rrString8_500 comp; toChar(comp.value,comp.ArraySize); comp.length=length; return comp; };
    DllExport_sharedLib bool isEqual (const char *C, int Clen)	const	{ if (length!=Clen) return false; for (uint i=0; i<length;i++) if (toupper( C[i])!=toupper( value[i])) return false; return true;};  
	DllExport_sharedLib bool endsWith(const char &C) const		{return ((length>0) && (value[length-1]==C) ); };  
    DllExport_sharedLib int  indexOf(const char *c) {return indexOf(_rrString(c)); };
	#include "RR_DataTypes_rrString_SDK_inc.h"



#ifdef QT_CORE_LIB
    DllExport_sharedLib _rrString (const QString &Q) { clear(); length=Q.size(); if (length>ArraySize) length=ArraySize; memcpy(&value[0],Q.unicode(),length*2); value[length]=0; };
	DllExport_sharedLib void operator =  (const QString &Q) { length=Q.size(); if (length>ArraySize) length=ArraySize; memcpy(&value[0],Q.unicode(),length*2); value[length]=0; };
	DllExport_sharedLib bool operator <  (const QString &Q) const { quint16 len=length; if (Q.size()<len) len=Q.size(); const ushort *pQ=Q.utf16(); int comp=memcmp(&value[0],pQ,len*2); if (comp==0) return length<Q.size(); else return (comp<0); };
	DllExport_sharedLib bool operator >  (const QString &Q) const { quint16 len=length; if (Q.size()<len) len=Q.size(); const ushort *pQ=Q.utf16(); int comp=memcmp(&value[0],pQ,len*2); if (comp==0) return length>Q.size(); else return (comp>0); };
	DllExport_sharedLib bool operator == (const QString &Q) const { if (Q.size()!=length) return false; const ushort *pQ=Q.utf16(); return (memcmp(&value[0],pQ,length*2)==0);};
	DllExport_sharedLib bool operator != (const QString &Q) const { if (Q.size()!=length) return true;  const ushort *pQ=Q.utf16(); return (memcmp(&value[0],pQ,length*2)!=0);};
	DllExport_sharedLib void operator += (const QString &Q) { const ushort *pQ=Q.utf16(); for (int i=0; i<Q.size();i++) {if (length==ArraySize) break; value[length]=pQ[i]; length++;} value[length]=0; };
	DllExport_sharedLib QString operator +  (const char *c) { QString comp=*this; comp+=QString::fromLatin1(c); return comp; }
    DllExport_sharedLib QString operator +  (const rrChar * C) { QString comp=*this; comp+=_rrString(C); return comp; }
	DllExport_sharedLib QString operator +  (const QString &Q) { QString comp=*this; comp+=Q; return comp; }
	DllExport_sharedLib operator		QString () const {return QString::fromUtf16((ushort *) &value[0],length);};
	DllExport_sharedLib bool	startsWith(const QString &Q) const {QString S(*this); return S.startsWith(Q,Qt::CaseInsensitive); }; 
	DllExport_sharedLib bool	endsWith(const QString &Q) const {QString S(*this); return S.endsWith(Q,Qt::CaseInsensitive); }; 
	DllExport_sharedLib bool	contains(const QString &Q) const {QString S(*this); return S.contains(Q,Qt::CaseInsensitive); }; 
    DllExport_sharedLib void fromRRUTF8(const char * c) { QString tempStr(c); *this=rrFromRRUTF8(tempStr); };
    DllExport_sharedLib void fromUTF8(const char * c) { *this=QString::fromUtf8(c); };
    DllExport_sharedLib _rrString8_500 toRRUTF8() const  {
                                QString tempStr=rrToRRUTF8(QString(*this),false);
                                _rrString8_500 ret;
                                ret.length=tempStr.size(); 
                                if (ret.length>ret.ArraySize) ret.length=ret.ArraySize; 
                                memcpy(&ret.value[0],tempStr.toLatin1(),ret.length); 
                                ret.value[ret.length]=0;
                                return ret;
                                };
#endif
};


typedef _rrString<2500> _rrString2500;
typedef _rrString<1000> _rrString1000;
typedef _rrString<500> _rrString500;
typedef _rrString<250> _rrString250;
typedef _rrString<225> _rrString225;
typedef _rrString<200> _rrString200;
typedef _rrString<150> _rrString150;
typedef _rrString<125> _rrString125;
typedef _rrString<100> _rrString100;
typedef _rrString<75> _rrString75;
typedef _rrString<50> _rrString50;
typedef _rrString<30> _rrString30;
typedef _rrString<25> _rrString25;
typedef _rrString<10> _rrString10;



#pragma pack()









class _rrStringList
{
private:
    //_rrStringList &operator=(const _rrStringList &oth) {_rrStringList(); copyFrom(oth);}; 
    
public:
    DllExport_sharedLib _rrStringList(const _rrStringList &oth) {_rrStringList(); copyFrom(oth);};
    DllExport_sharedLib void operator=(const _rrStringList &oth) {_rrStringList(); copyFrom(oth);};
    DllExport_sharedLib _rrStringList();
    DllExport_sharedLib ~_rrStringList();
    DllExport_sharedLib inline int count() const { return m_count; };
    DllExport_sharedLib void append(const _rrString500 &newArg,const bool &checkIfExist=false, const bool &checkCaseSensitive=true);
    DllExport_sharedLib _rrString500 &at(const int &pos) const;
	DllExport_sharedLib char * atAsChar(const int &pos) const;
    DllExport_sharedLib int find(const _rrString500 &arg, const bool &caseSensitive=true);
    DllExport_sharedLib inline _rrString500 &operator[](int j) const { return m_args[j]; }
    DllExport_sharedLib void clear() { 	if (m_args!=0) free(m_args); m_args=NULL; m_count=0; }
    DllExport_sharedLib void sort(const bool &nameSortedReverse=false);
    DllExport_sharedLib void copyFrom(const _rrStringList &oth);


private:
    int m_count;
    _rrString500 *m_args;
    mutable char m_conv[501];
};




#ifdef QT_CORE_LIB 
DllExport_sharedLib QString listStringMemorySize();

//has to be a macro as functions used should not be included here
#define writeStringMemorySize(appName,header) _rrTime jetzte(true); QString filename;  filename=rrApplicationPath()+".."+PDs+".."+PDs+".."+PDs+"sources"+PDs+"test"+PDs+"rrTest_PrintDatasizesConsole"+PDs+"results"+PDs;  filename=rrPathResolve(filename);  filename+="Stringonly_"+jetzte.asStringFileNameYearMinute()+"____"+QString(rrVersion).remove(' ')+"___"+osBitStr()+"___"+QString(appName)+".txt"; writeToLogFile(filename,QString("######### %1 ########").arg(header),true,false); writeToLogFile(filename,listStringMemorySize(),true,false); 
#endif





//createArgString( stringVariable , ArgString, ...) 
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
    #define createArgString8( stringVariable , ArgString, ...) sprintf_s( stringVariable .value, stringVariable .ArraySize, ArgString, ##__VA_ARGS__ )
  #else
	#include <string.h>
    #define createArgString8( stringVariable , ArgString, ...) sprintf( stringVariable .value,  ArgString, ##__VA_ARGS__)
#endif






DllExport_sharedLib bool          rrIsDigit(const rrChar &b);
DllExport_sharedLib _rrString25    int2Str(const int &number);
DllExport_sharedLib _rrString25    float2Str( float number,const int &precision ,const  rrChar &decMark);



#endif
