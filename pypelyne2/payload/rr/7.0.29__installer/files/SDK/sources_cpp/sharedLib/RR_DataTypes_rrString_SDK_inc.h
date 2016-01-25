//INC_StringType	rrString8_UnevenSize
//INC_CharType		char
//INC_strlen		strlen
//INC_CharSize		1



DllExport_sharedLib void operator =  (const INC_StringType &t) { length=t.length; memcpy(value,t.value,(ArraySize+1)*INC_CharSize);}; /* full copy required, do not optimize!!!*/ 
DllExport_sharedLib void operator =  (const INC_CharType * const C) { if (C==NULL) {length=0; return;} length=(quint16) INC_strlen(C); if (length>ArraySize) length=ArraySize; memcpy(&value[0],C,length*INC_CharSize); value[length]=0; };
DllExport_sharedLib void operator =  (const INC_CharType &C) { length=1; value[0]=quint8(C); value[length]=0; };

DllExport_sharedLib INC_StringType operator +  (const char &c) {INC_StringType comp(*this); comp+=c; return comp; };
DllExport_sharedLib INC_StringType operator +  (const INC_StringType &t) {INC_StringType comp(*this); comp+=t; return comp; };
DllExport_sharedLib void operator += (const INC_StringType &t) { for (uint i=0; i<t.length;i++) {if (length==ArraySize) break; value[length]=t.value[i]; length++;} value[length]=0; };
DllExport_sharedLib void operator += (const INC_CharType *C) { if (C==NULL) return; uint Clen=(quint16) INC_strlen(C); if ((length+Clen)>ArraySize) Clen=ArraySize-length;  for (uint i=0; i<Clen;i++) value[length+i]=C[i]; length+=Clen; value[length]=0; };
DllExport_sharedLib void operator += (const INC_CharType &C) { if ((length+1)>ArraySize) return;  value[length]=C; length++; value[length]=0; };

DllExport_sharedLib bool operator == (const INC_StringType &t) const { return ((length==t.length) && (memcmp(value,t.value,length*INC_CharSize)==0));};
DllExport_sharedLib bool operator != (const INC_StringType &t) const { return ((length!=t.length) || (memcmp(value,t.value,length*INC_CharSize)!=0));};
DllExport_sharedLib bool operator <  (const INC_StringType &t) const { uint len=length; if (t.length<len) len=t.length; int comp=memcmp(value,t.value,len*INC_CharSize); if (comp==0) return (length<t.length); else return (comp<0); };
DllExport_sharedLib bool operator >  (const INC_StringType &t) const { uint len=length; if (t.length<len) len=t.length; int comp=memcmp(value,t.value,len*INC_CharSize); if (comp==0) return (length>t.length); else return (comp>0); };




DllExport_sharedLib int  lastIndexOf(const INC_CharType &C, int from = -1) const;  
DllExport_sharedLib int  indexOf(const INC_CharType &C, int from = 0) const;  
DllExport_sharedLib int  indexOf(const INC_StringType &t, int from = 0) const;  
DllExport_sharedLib int  indexOfCaseSen(const INC_StringType &t, int from = 0) const;

DllExport_sharedLib bool contains(const char *c) const {return   (indexOf(c)>=0); } ;
DllExport_sharedLib bool contains(const char &C) const {return   (indexOf(C)>=0); } ;
DllExport_sharedLib bool contains(const INC_StringType &str) const {return   (indexOf(str)>=0); } ;

DllExport_sharedLib bool startsWith(const INC_CharType &C) const;  
DllExport_sharedLib bool startsWith(const char *c) const;  
DllExport_sharedLib bool startsWith(const char *c,int len) const; 
DllExport_sharedLib bool startsWithCaseSen(const char *c) const;  
DllExport_sharedLib bool startsWith(INC_StringType upa) const;  

DllExport_sharedLib bool endsWith(const INC_CharType &C) const;  
DllExport_sharedLib bool endsWith(const char *c) const;  
DllExport_sharedLib bool endsWith(const char *c,int len) const; 
DllExport_sharedLib bool endsWith(const INC_StringType &upa) const;  


DllExport_sharedLib bool isEqual(const INC_StringType &t)	const;  
DllExport_sharedLib bool isEqualSameCase(const INC_StringType &t)	const;  
DllExport_sharedLib bool isEqual(const INC_CharType *C, int Clen)	const;  
DllExport_sharedLib bool isEqualSameCase(const INC_CharType *C, int Clen) const; 
DllExport_sharedLib int  compare(const INC_StringType &t) const; 

DllExport_sharedLib bool isEmpty() const;  
DllExport_sharedLib bool hasData() const;  

DllExport_sharedLib void trim(); 


DllExport_sharedLib INC_StringType & replace(const INC_CharType &o,const INC_CharType &n);  
DllExport_sharedLib INC_StringType & replace(const INC_StringType &o,const INC_StringType &n);
DllExport_sharedLib INC_StringType & replaceCaseSen(const INC_StringType &o,const INC_StringType &n);  

DllExport_sharedLib INC_StringType		remove(const INC_CharType &o);  
DllExport_sharedLib void				remove(const int &start, const int &length);  
DllExport_sharedLib INC_StringType &	remove(const INC_StringType &o);  
DllExport_sharedLib INC_StringType &	removeCaseSens(const INC_StringType &o);  


DllExport_sharedLib void insert(const int &pos, const INC_StringType &strg) ;  
DllExport_sharedLib INC_StringType mid(const int &start, const int &len) ;  
DllExport_sharedLib INC_StringType left(int len);  

DllExport_sharedLib void clear();
DllExport_sharedLib void clearUnused();

DllExport_sharedLib void setLength(const qint16 &len);
DllExport_sharedLib void calcLength();

DllExport_sharedLib void makeUpper(); 
DllExport_sharedLib void makeLower();


DllExport_sharedLib void add(const INC_CharType * c, uint Clen);
DllExport_sharedLib void add(const char * c);
DllExport_sharedLib void add(const INC_StringType &C);
DllExport_sharedLib INC_StringType combined(const char * c) const;
DllExport_sharedLib INC_StringType combined(const INC_StringType &C) const;
