
//INC_StringType	rrString8_UnevenSize
//INC_CharType		char
//INC_strlen		strlen
//INC_CharSize	1



template <int aSize> 
int  INC_StringType<aSize>::lastIndexOf(const INC_CharType &C, int from )  const
{
	int i=length-1; 
	if ((from>=0) && (from<length)) i=from;  
	for (; i>=0; i--) {if (value[i]==C) return i;} 
	return -1; 
} 


template <int aSize> 
int  INC_StringType<aSize>::indexOf(const INC_CharType &C, int from ) const
{
	int i=0; if ((from<length)) i=from;  for (; i<length; i++) {if (value[i]==C) return i;} return -1; 
} 



template <int aSize> 
int  INC_StringType<aSize>::indexOf(const INC_StringType &t, int from ) const	
{ 
			if (t.length+from > length) return -1; 
			if (t.length==length) { 
				if (compare(t)==0) return 0; 
				else return -1; 
			} 
			INC_StringType upN(t); 
			upN.makeUpper(); 
			INC_StringType upH=*this; 
			upH.makeUpper();  
			int haystack=0; 
			int needle=0; 
			for (int i=0; i<upN.length; i++) { 
				needle+= upN.value[i]; 
				haystack+= upH.value[from+i]; 
			} 
			haystack-= upH.value[upN.length-1+from]; 
			for (int i=upN.length+from; i<=upH.length; i++) { 
				haystack+= upH.value[i-1]; 
				if (haystack==needle) 
					if (memcmp(&upH.value[i-upN.length],upN.value,upN.length*INC_CharSize)==0) return i- upN.length; 
				haystack-= upH.value[i-upN.length]; 
			} 
			return -1;  
}; 



    

template <int aSize> 
int  INC_StringType<aSize>::indexOfCaseSen(const INC_StringType &t, int from ) const	{
			if (t.length+from > length) return -1; 
			if (t.length==length) { 
				if (compare(t)==0) return 0; 
				else return -1; 
			} 
			INC_StringType upN(t); 
			INC_StringType upH=*this; 
			int haystack=0; 
			int needle=0; 
			for (int i=0; i<upN.length; i++) { 
				needle+= upN.value[i]; 
				haystack+= upH.value[from+i]; 
			} 
			haystack-= upH.value[upN.length-1+from]; 
			for (int i=upN.length+from; i<=upH.length; i++) { 
				haystack+= upH.value[i-1]; 
				if (haystack==needle) 
					if (memcmp(&upH.value[i-upN.length],upN.value,upN.length*INC_CharSize)==0) return i- upN.length; 
				haystack-= upH.value[i-upN.length]; 
			} 
			return -1;  
			}
	


template <int aSize> 
void INC_StringType<aSize>::trim()		{ 
		while ((length>0)  && ((value[length-1]==0) || (value[length-1]=='\r') || (value[length-1]=='\n') || (value[length-1]=='\t') || (value[length-1]==' '))) 
		{ length--; }
		quint16 st=0; 
					while ((st<length)  && ((value[st]==0)|| (value[st]=='\r')|| (value[st]=='\n')|| (value[st]=='\t')|| (value[st]==' '))) { st++;}; 
					if (st>0) { length-=st; for (quint16 i=0; i<length; i++ ) value[i]=value[st+i]; } 
					value[length]=0; 
					}
	

    

template <int aSize> 
bool INC_StringType<aSize>::startsWith(const INC_CharType &c) const				{return ((length>0) && (value[0]==c) ); }
	

template <int aSize> 
bool INC_StringType<aSize>::startsWith(const char *c) const	{ 
											if (length==0 || c==NULL) return false; 
											INC_StringType upa(c); 
											if ((upa.length>length) || (upa.length==0)) return false; 
											upa.makeUpper(); 
											INC_StringType upb=*this; 
											upb.makeUpper(); 
											return (memcmp(&upb.value,upa.value,upa.length*INC_CharSize)==0); 
											}

template <int aSize> 
bool INC_StringType<aSize>::startsWith(const char *c,int len) const	{ 
											if (length==0 || c==NULL) return false; 
											if ((len>length) || (len==0)) return false; 
											INC_StringType upa(c,len); 
											upa.makeUpper(); 
											INC_StringType upb=*this; 
											upb.makeUpper(); 
											return (memcmp(&upb.value,upa.value,upa.length*INC_CharSize)==0); 
											}


template <int aSize> 
bool INC_StringType<aSize>::startsWithCaseSen(const char *c) const	{ 
											if (length==0 || c==NULL) return false; 
											int len=strlen(c);
											return (memcmp(&value[0],c,len*INC_CharSize)==0);
											}


template <int aSize> 
bool INC_StringType<aSize>::startsWith(INC_StringType upa) const	{ 
											if (length==0) return false; 
											if ((upa.length>length) || (upa.length==0)) return false; 
											upa.makeUpper(); 
											INC_StringType upb=*this; 
											upb.makeUpper(); 
											return (memcmp(upb.value,upa.value,upa.length*INC_CharSize)==0); 
	}

template <int aSize> 
bool INC_StringType<aSize>::endsWith(const INC_CharType &c) const					{return ((length>0) && (value[length-1]==c) ); }
	

template <int aSize> 
bool INC_StringType<aSize>::endsWith(const char * c,int len) const			
{ 
											if (length==0 || c==NULL) return false; 
											if ((len>length) || (len==0)) return false; 
											INC_StringType upa(c); 
											upa.makeUpper(); 
											INC_StringType upb=*this; 
											upb.makeUpper(); 
											return (memcmp(&upb.value[upb.length-upa.length],upa.value,upa.length*INC_CharSize)==0);
} 
	

template <int aSize> 
bool INC_StringType<aSize>::endsWith(const char *c) const	
{ 
											if (length==0 || c==NULL) return false; 
											INC_StringType upa(c); 
											if ((upa.length>length) || (upa.length==0)) return false; 
											upa.makeUpper(); 
											INC_StringType upb=*this; 
											upb.makeUpper(); 
											return (memcmp(&upb.value[upb.length-upa.length],upa.value,upa.length*INC_CharSize)==0);
	}


template <int aSize> 
bool INC_StringType<aSize>::endsWith(const INC_StringType &c) const	{ 
											if (length==0) return false; 
											if ((c.length>length) || (c.length==0)) return false; 
											INC_StringType upa(c); 
											upa.makeUpper(); 
											INC_StringType upb=*this; 
											upb.makeUpper(); 
											return (memcmp(&upb.value[upb.length-upa.length],upa.value,upa.length*INC_CharSize)==0); 
	}


template <int aSize> 
INC_StringType<aSize> & INC_StringType<aSize>::replace(const INC_CharType &o,const INC_CharType &n) { 
		INC_StringType upH=*this; 
		upH.makeUpper();  
		INC_CharType O= toupper(o); 
		for (int i=0; i<length; i++) {if (upH.value[i]==O) value[i]=n;} 
		return (*this);
	}
	

template <int aSize> 
INC_StringType<aSize> & INC_StringType<aSize>::replace(const INC_StringType &o,const INC_StringType &n) { 
		int p=indexOf(o); 
		while (p>=0) { 
			INC_StringType cpy(*this); 
			this->length=0; 
			add(cpy.value,p); 
			add(n.value,n.length); 
			add(&cpy.value[p+o.length],cpy.length -p-o.length); 
			p=indexOf(o,p+n.length); 
		} 
		return (*this);
	}


template <int aSize> 
INC_StringType<aSize>  & INC_StringType<aSize>::replaceCaseSen(const INC_StringType &o,const INC_StringType &n) { 
		                                    int p=indexOfCaseSen(o); 
		                                    while (p>=0) { 
			                                    INC_StringType cpy(*this); 
			                                    this->length=0; 
			                                    add(cpy.value,p); 
			                                    add(n.value,n.length); 
			                                    add(&cpy.value[p+o.length],cpy.length -p-o.length); 
			                                    p=indexOfCaseSen(o,p+n.length); 
		                                    } 
		                                    return (*this);
	                                    }


template <int aSize> 
INC_StringType<aSize>  INC_StringType<aSize>::remove(const INC_CharType &o) { 
		INC_StringType upH=*this; 
		upH.makeUpper();  
		INC_CharType O= toupper(o); 
		for (int i=length-1; i>=0; i--) { 
			if (upH.value[i]==O) {
				INC_StringType cpy(*this); 
				this->length=0; 
				add(cpy.value,i); 
				add(&cpy.value[i+1],cpy.length -i-1); 
			}
		} 
		return (*this);
		}
	

template <int aSize> 
void INC_StringType<aSize>::remove(const int &start, const int &length) { 
		INC_StringType cpy(*this); 
		this->length=0;   
		add(cpy.value,start); 
		add(&cpy.value[start+length],cpy.length -start-length); 
		}
	

template <int aSize> 
INC_StringType<aSize>  & INC_StringType<aSize>::remove(const INC_StringType &o) { 
		int p=indexOf(o); 
		while (p>=0) { 
			INC_StringType cpy(*this); 
			this->length=0; 
			add(cpy.value,p); 
			add(&cpy.value[p+o.length],cpy.length -p-o.length); 
			p=indexOf(o,p); 
		} 
		return (*this);
		}
	

template <int aSize> 
INC_StringType<aSize>  & INC_StringType<aSize>::removeCaseSens(const INC_StringType &o) { 
		int p=indexOfCaseSen(o); 
		while (p>=0) { 
			INC_StringType cpy(*this); 
			this->length=0; 
			add(cpy.value,p); 
			add(&cpy.value[p+o.length],cpy.length -p-o.length); 
			p=indexOfCaseSen(o,p); 
		} 
		return (*this);
}










		

template <int aSize> 
bool INC_StringType<aSize>::isEqualSameCase(const INC_StringType &t)	const		
{ 
	return ((length==t.length) && memcmp(&value[0],&t.value[0],length*INC_CharSize)==0); 
}  
    	

template <int aSize> 
bool INC_StringType<aSize>::isEqual(const INC_StringType &t)	const		
{ 
	if (length!=t.length) return false; for (uint i=0; i<length;i++) if (toupper( t.value[i])!=toupper( value[i])) return false; return true;
}  
    	

template <int aSize> 
bool INC_StringType<aSize>::isEqualSameCase(const INC_CharType *C, int Clen)	const	
{ 
	return ((length==Clen) && memcmp(&value[0],C,length*INC_CharSize)==0); 
} 
    	

template <int aSize> 
bool INC_StringType<aSize>::isEqual(const INC_CharType *C, int Clen)	const	
{ 
	if (length!=Clen) return false; for (uint i=0; i<length;i++) if (toupper( C[i])!=toupper( value[i])) return false; return true;
}  
    	



template <int aSize> 
int INC_StringType<aSize>::compare(const INC_StringType &t) const 
{ 
		                                    uint len=length; if (t.length<len) len=t.length;  
		                                    INC_StringType upa(t); 
		                                    upa.length=len; 
		                                    upa.makeUpper(); 
		                                    INC_StringType upb=*this; 
		                                    upb.length=len; 
		                                    upb.makeUpper();  
											int comp=memcmp(upb.value,upa.value,len*INC_CharSize); 
											if (comp==0) {if (length==t.length) return 0; 
												else if (length<t.length) return -1; 
												else return 1;} 
											else return comp;
} 



template <int aSize> 
void INC_StringType<aSize>::insert(const int &pos, const INC_StringType &strg) 
{ 
		                                    INC_StringType cpy(*this); 
		                                    this->length=0;   
		                                    add(cpy.value,pos); 
		                                    add(strg.value,strg.length); 
		                                    add(&cpy.value[pos],cpy.length -pos); 
		                                    }



template <int aSize> 
INC_StringType<aSize> INC_StringType<aSize>::mid(const int &start, const int &len) 
{ 
		                                    INC_StringType ret; 
		                                    ret.add(&value[start],len); 
		                                    return  ret; 
} 



template <int aSize> 
INC_StringType<aSize> INC_StringType<aSize>::left(int len) 
{ 
		                                    INC_StringType ret; 
                                            if (len>length) len=length;
		                                    ret.add(&value[0],len); 
		                                    return  ret; 
}  




template <int aSize> 
void INC_StringType<aSize>::clear()							
{
	length=0; memset(&value[0],0,(ArraySize+1)*INC_CharSize); 
}


template <int aSize> 
void INC_StringType<aSize>::clearUnused()						
{
	memset(&value[length],0,(ArraySize-length+1)*INC_CharSize); 
}


template <int aSize> 
bool INC_StringType<aSize>::isEmpty() const					
{
	return length==0;
}

template <int aSize> 
bool INC_StringType<aSize>::hasData() const					
{
	return length!=0;
}


template <int aSize> 
void INC_StringType<aSize>::setLength(const qint16 &len)		
{
	if (len<0) length=0; else if (len>ArraySize) length=ArraySize; else length=len; value[length]=0; 
}


template <int aSize> 
void INC_StringType<aSize>::calcLength()						
{
	length=ArraySize; for (int i=0; i<ArraySize; i++) {
		if (value[i]==0) {length=i; break;}
	} 
	value[length]=0; 
} 



template <int aSize> 
void INC_StringType<aSize>::makeUpper()						
{
	for (uint i=0; i<length;i++) value[i]=toupper( value[i]); 
}


template <int aSize> 
void INC_StringType<aSize>::makeLower()					    
{
	for (uint i=0; i<length;i++) {value[i]=tolower( value[i]);} 
}






template <int aSize> 
void INC_StringType<aSize>::add(const INC_StringType &C) 
{ 
	if (C.length<=0) return; 
	uint Clen=C.length;
	if ((length+Clen)>ArraySize) Clen=ArraySize-length;  
	for (uint i=0; i<Clen;i++) value[length+i]=C.value[i]; 
	length+=Clen; 
	value[length]=0; 
}


template <int aSize> 
void INC_StringType<aSize>::add(const INC_CharType * C, uint Clen) 
{ 
	if (C==NULL || Clen<=0) return; 
	if ((length+Clen)>ArraySize) Clen=ArraySize-length;  
	for (uint i=0; i<Clen;i++) value[length+i]=C[i]; 
	length+=Clen; 
	value[length]=0; 
}


template <int aSize> 
void INC_StringType<aSize>::add(const char * C) 
{ 
	if (C==NULL) return; 
	uint Clen=(quint16) strlen(C); 
	if (Clen<=0) return ; 
	if ((length+Clen)>ArraySize) Clen=ArraySize-length;  
	for (uint i=0; i<Clen;i++) value[length+i]=quint8(C[i]);
	length+=Clen; 
	value[length]=0;
}


template <int aSize> 
INC_StringType<aSize> INC_StringType<aSize>::combined(const char * C)   const 
{ 
	INC_StringType comb(*this); 
	comb.add(C); 
	return comb;
}


template <int aSize> 
INC_StringType<aSize> INC_StringType<aSize>::combined(const INC_StringType &C)  const
{ 
	INC_StringType comb(*this); 
	comb+=C; 
	return comb;
}
