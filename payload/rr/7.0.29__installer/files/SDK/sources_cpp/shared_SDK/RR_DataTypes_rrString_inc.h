//INC_StringType	rrString8_UnevenSize
//INC_CharType		char
//INC_strlen		strlen
//INC_CharSize		1



void operator =  (const INC_StringType &t) { length=t.length; memcpy(value,t.value,(ArraySize+1)*INC_CharSize);}; /* full copy required, do not optimize!!!*/ 
void operator =  (const INC_CharType * const C) { if (C==NULL) {length=0; return;} length=(quint16) INC_strlen(C); if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length*INC_CharSize); value[length]=0; };
void operator =  (const INC_CharType &C) { length=1; value[0]=quint8(C); value[length]=0; };

INC_StringType operator +  (const char &c) {INC_StringType comp(*this); comp+=c; return comp; };
INC_StringType operator +  (const INC_StringType &t) {INC_StringType comp(*this); comp+=t; return comp; };
void operator += (const INC_StringType &t) { for (uint i=0; i<t.length;i++) {if (length==ArraySize) break; value[length]=t.value[i]; length++;} value[length]=0; };
void operator += (const INC_CharType *C) { if (C==NULL) return; uint Clen=(quint16) INC_strlen(C); if ((length+Clen)>ArraySize) Clen=ArraySize-length;  for (uint i=0; i<Clen;i++) value[length+i]=C[i]; length+=Clen; value[length]=0; };
void operator += (const INC_CharType &C) { if ((length+1)>ArraySize) return;  value[length]=C; length++; value[length]=0; };

bool operator == (const INC_StringType &t) const { return ((length==t.length) && (memcmp(value,t.value,length*INC_CharSize)==0));};
bool operator != (const INC_StringType &t) const { return ((length!=t.length) || (memcmp(value,t.value,length*INC_CharSize)!=0));};
bool operator <  (const INC_StringType &t) const { uint len=length; if (t.length<len) len=t.length; int comp=memcmp(value,t.value,len*INC_CharSize); if (comp==0) return (length<t.length); else return (comp<0); };
bool operator >  (const INC_StringType &t) const { uint len=length; if (t.length<len) len=t.length; int comp=memcmp(value,t.value,len*INC_CharSize); if (comp==0) return (length>t.length); else return (comp>0); };




int  lastIndexOf(const INC_CharType &C, int from = -1) const;  
int  indexOf(const INC_CharType &C, int from = 0) const;  
int  indexOf(const INC_StringType &t, int from = 0) const;  
int  indexOfCaseSen(const INC_StringType &t, int from = 0) const;

bool contains(const char *c) const {return   (indexOf(c)>=0); } ;
bool contains(const char &C) const {return   (indexOf(C)>=0); } ;
bool contains(const INC_StringType &str) const {return   (indexOf(str)>=0); } ;

bool startsWith(const INC_CharType &C) const;  
bool startsWith(const char *c) const;  
bool startsWith(const char *c,int len) const; 
bool startsWithCaseSen(const char *c) const;  
bool startsWith(INC_StringType upa) const;  

bool endsWith(const INC_CharType &C) const;  
bool endsWith(const char *c) const;  
bool endsWith(const char *c,int len) const; 
bool endsWith(const INC_StringType &upa) const;  


bool isEqual(const INC_StringType &t)	const;  
bool isEqualSameCase(const INC_StringType &t)	const;  
bool isEqual(const INC_CharType *C, int Clen)	const;  
bool isEqualSameCase(const INC_CharType *C, int Clen) const; 
int  compare(const INC_StringType &t) const; 

bool isEmpty() const;  
bool hasData() const;  

void trim(); 


INC_StringType & replace(const INC_CharType &o,const INC_CharType &n);  
INC_StringType & replace(const INC_StringType &o,const INC_StringType &n);
INC_StringType & replaceCaseSen(const INC_StringType &o,const INC_StringType &n);  

INC_StringType		remove(const INC_CharType &o);  
void				remove(const int &start, const int &length);  
INC_StringType &	remove(const INC_StringType &o);  
INC_StringType &	removeCaseSens(const INC_StringType &o);  


void insert(const int &pos, const INC_StringType &strg) ;  
INC_StringType mid(const int &start, const int &len) ;  
INC_StringType left(int len);  

void clear();
void clearUnused();

void setLength(const qint16 &len);
void calcLength();

void makeUpper(); 
void makeLower();


void add(const INC_CharType * c, uint Clen);
void add(const char * c);
void add(const INC_StringType &C);
INC_StringType combined(const char * c) const;
INC_StringType combined(const INC_StringType &C) const;
