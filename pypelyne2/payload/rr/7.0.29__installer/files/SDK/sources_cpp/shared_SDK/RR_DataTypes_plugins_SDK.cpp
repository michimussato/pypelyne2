
#include "RR_DataTypes_plugins_SDK.h"
#include <math.h>

#if !defined(max)
#define max(a, b)       ((a) > (b) ? (a) : (b))
#define min(a, b)       ((a) < (b) ? (a) : (b))
#endif

#if (!defined(RR_OS_WIN) && !defined(_isnan))
    #define _isnan isnan
#endif


namespace rrP {


//####################################### _imgFileBuffer ############################################
//####################################### _imgFileBuffer ############################################
//####################################### _imgFileBuffer ############################################



_imgFileBuffer::_imgFileBuffer(unsigned int  newSize)
 :m_bufferAllocatedSize(newSize)
{ 
	m_sizeLoaded=0;
	m_bufPos=0;
	m_buf = new quint8[newSize+4]; 
	if (m_buf==NULL) m_bufferAllocatedSize=0;
	m_swapBytes=false;
	m_filesize=0;
} 
_imgFileBuffer::~_imgFileBuffer()
{ 
	rrDeleteArray(m_buf);
}

bool _imgFileBuffer::setFileSize(unsigned int  newSize)
{
	if (newSize>m_bufferAllocatedSize) {
		//filesize=BufferAllocatedSize; 
		m_filesize=newSize;
		return false;
	} else {
		m_filesize=newSize;
		return true;
	}
}

void _imgFileBuffer::setSizeLoaded(qint64 newSize)
{
	if (newSize>m_bufferAllocatedSize) m_sizeLoaded=m_bufferAllocatedSize;
	else if (newSize<0) m_sizeLoaded=0;
	else m_sizeLoaded=newSize;
}



bool _imgFileBuffer::setBufPosition(const qint64 &position)
{
	if ((position<0) ||(position>m_sizeLoaded)) return false;
	m_bufPos=position;
	return true;
}

bool  _imgFileBuffer::offsetBufPosition(qint64 offset)
{
	if (offset==0) return true;
	if (offset>=0) {
		if (m_bufPos+offset>=m_sizeLoaded) {
			m_bufPos=m_sizeLoaded;
			return false;
		}
	} else {
		if (m_bufPos+offset<0) return false;
	}
	m_bufPos+=offset;
	return true;
}


bool _imgFileBuffer::readUint8 (quint8  &res)	{if (m_bufPos+(qint32) sizeof(quint8)>m_sizeLoaded) return false; res=* ((quint8 *) &m_buf[m_bufPos]); m_bufPos+=sizeof(quint8); return true;}
bool _imgFileBuffer::readSint8 (qint8   &res)	{if (m_bufPos+(qint32) sizeof(qint8)>m_sizeLoaded) return false; res=* ((qint8 *) &m_buf[m_bufPos]); m_bufPos+=sizeof(qint8); return true;}
bool _imgFileBuffer::readdouble(double  &res)	{if (m_bufPos+(qint32) sizeof(double)>m_sizeLoaded) return false; res=* ((double *) &m_buf[m_bufPos]); m_bufPos+=sizeof(double); return true;}

bool _imgFileBuffer::readfloat (float   &res,const bool & swap) {
	if (m_bufPos+(qint32) sizeof(float)>m_sizeLoaded) return false; 
	res=* ((float *) &m_buf[m_bufPos]); 
	if (m_swapBytes!=swap) {
		quint32 *resP;
		resP=(quint32 *) &res;
		*resP = (((*resP&0x000000FF)<<24)|((*resP&0x0000FF00)<<8)| ((*resP&0x00FF0000)>>8)|((*resP&0xFF000000)>>24));
	}
	m_bufPos+=sizeof(float); 
	return true;
}

bool _imgFileBuffer::readUint16(quint16 &res,const bool & swap)	{
	if (m_bufPos+(qint32) sizeof(quint16)>m_sizeLoaded) {res=0; return false; }
	res=* ((quint16 *) &m_buf[m_bufPos]); 
	if (m_swapBytes!=swap) res = ( ((res & 0x00FF)<< 8) 
			     | ((res & 0xFF00)>> 8));
	m_bufPos+=sizeof(quint16); 
	return true;}

bool _imgFileBuffer::readSint16(qint16  &res,const bool & swap)	{
	if (m_bufPos+(qint32) sizeof(qint16)>m_sizeLoaded) return false; 
	res=* ((qint16 *) &m_buf[m_bufPos]); 
	if (m_swapBytes!=swap) res = ( ((res&0x00FF)<<8)| ((res&0xFF00)>>8));
	m_bufPos+=sizeof(qint16);
	return true; }

bool _imgFileBuffer::readUint24(quint32 &res,const bool & swap)	{
	if (m_bufPos+3>m_sizeLoaded) return false; 
	res=* ((quint32 *) &m_buf[m_bufPos]); 
	//res= res >> 8;
	if (m_swapBytes!=swap)res = (((res&0x0000FF)<<16)|((res&0x0000FF00))| ((res&0x00FF0000)>>16));
	m_bufPos+=3; 
	return true;}


bool _imgFileBuffer::readUint32(quint32 &res,const bool & swap)	{
	if (m_bufPos+(qint32) sizeof(quint32)>m_sizeLoaded) 
		return false; 
	res=* ((quint32 *) &m_buf[m_bufPos]); 
	if (m_swapBytes!=swap)res = (((res&0x000000FF)<<24)|((res&0x0000FF00)<<8)| ((res&0x00FF0000)>>8)|((res&0xFF000000)>>24));
	m_bufPos+=sizeof(quint32); 
	return true;}

bool _imgFileBuffer::readSint32(qint32  &res,const bool & swap)	{
	if (m_bufPos+(qint32) sizeof(qint32)>m_sizeLoaded) return false; 
	res=* ((qint32 *) &m_buf[m_bufPos]); 
	if (m_swapBytes!=swap) res = (((res&0x000000FF)<<24)|((res&0x0000FF00)<<8)| ((res&0x00FF0000)>>8)|((res&0xFF000000)>>24));
	m_bufPos+=sizeof(qint32); 
	return true;}


bool _imgFileBuffer::readBuffer(quint8 * const buffer, const qint32 &readSize) {
    if (m_bufPos+ readSize>m_sizeLoaded) {
        return false; 
    }
    if (buffer==NULL) {
        return false; 
    }
	memcpy(buffer,&m_buf[m_bufPos],readSize);
	m_bufPos+=readSize; 
	return true;
}



bool _imgPluginBuffer::readfromFileBuffer(_imgFileBuffer * const fileBuf, const qint16 &headerSize)
{
	if (headerSize<=0) return false;
	return fileBuf->readBuffer(buffer,headerSize);
}




bool _imgFileBuffer::readUint8P (quint8  &res,const qint32 &position)	{if (position+(qint32) sizeof(quint8)>m_sizeLoaded) return false; res=* ((quint8 *) &m_buf[position]); return true;}
bool _imgFileBuffer::readSint8P (qint8   &res,const qint32 &position)	{if (position+(qint32) sizeof(qint8)>m_sizeLoaded) return false; res=* ((qint8 *) &m_buf[position]); return true;}
bool _imgFileBuffer::readdoubleP(double  &res,const qint32 &position)	{if (position+(qint32) sizeof(double)>m_sizeLoaded) return false; res=* ((double *) &m_buf[position]); return true;}

bool _imgFileBuffer::readfloatP (float   &res,const qint32 &position,const bool & swap) {
	if (position+(qint32) sizeof(float)>m_sizeLoaded) return false; 
	res=* ((float *) &m_buf[position]); 
	if (m_swapBytes!=swap) {
		quint32 *resP;
		resP=(quint32 *) &res;
		*resP = (((*resP&0x000000FF)<<24)|((*resP&0x0000FF00)<<8)| ((*resP&0x00FF0000)>>8)|((*resP&0xFF000000)>>24));
	}
	return true;
}

bool _imgFileBuffer::readUint16P(quint16 &res,const qint32 &position,const bool & swap)	{
	if (position+(qint32) sizeof(quint16)>m_sizeLoaded) return false; 
	res=* ((quint16 *) &m_buf[position]); 
	if (m_swapBytes!=swap) res = ( ((res & 0x00FF)<< 8) 
			     | ((res & 0xFF00)>> 8));
	return true;}

bool _imgFileBuffer::readSint16P(qint16  &res,const qint32 &position,const bool & swap)	{
	if (position+(qint32) sizeof(qint16)>m_sizeLoaded) return false; 
	res=* ((qint16 *) &m_buf[position]); 
	if (m_swapBytes!=swap) res = ( ((res&0x00FF)<<8)| ((res&0xFF00)>>8));
	return true; }

bool _imgFileBuffer::readUint32P(quint32 &res,const qint32 &position,const bool & swap)	{
	if (position+(qint32) sizeof(quint32)>m_sizeLoaded) 
		return false; 
	res=* ((quint32 *) &m_buf[position]); 
	if (m_swapBytes!=swap)res = (((res&0x000000FF)<<24)|((res&0x0000FF00)<<8)| ((res&0x00FF0000)>>8)|((res&0xFF000000)>>24));
	return true;}

bool _imgFileBuffer::readSint32P(qint32  &res,const qint32 &position,const bool & swap)	{
	if (position+(qint32) sizeof(qint32)>m_sizeLoaded) return false; 
	res=* ((qint32 *) &m_buf[position]); 
	if (m_swapBytes!=swap) res = (((res&0x000000FF)<<24)|((res&0x0000FF00)<<8)| ((res&0x00FF0000)>>8)|((res&0xFF000000)>>24));
	return true;}


bool _imgFileBuffer::readBufferP(quint8 * const buffer, const qint32 &readSize,const qint32 &position) {
	if (position+ readSize>m_sizeLoaded) return false; 
	if (buffer==NULL) return false; 
	memcpy(buffer,&m_buf[position],readSize);
	return true;
}


bool _imgFileBuffer::writeUint8 (const quint8  &res)
{
    if (m_filesize+int(sizeof(quint8))>=m_bufferAllocatedSize) return false;
	memcpy(&m_buf[m_bufPos],&res,sizeof(quint8));
	m_bufPos+=sizeof(quint8);
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writeSint8 (const qint8   &res)
{
    if (m_filesize+int(sizeof(quint8))>=m_bufferAllocatedSize) return false;
	memcpy(&m_buf[m_bufPos],&res,sizeof(quint8));
	m_bufPos+=sizeof(quint8);
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writeUint16(quint16 res,const bool &swap)
{
    if (m_filesize+int(sizeof(quint16))>=m_bufferAllocatedSize) return false;
	if (m_swapBytes!=swap) res = ( ((res&0x00FF)<<8)| ((res&0xFF00)>>8));
	memcpy(&m_buf[m_bufPos],&res,sizeof(quint16));
	m_bufPos+=sizeof(quint16);
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writeSint16(qint16  res,const bool &swap)
{
    if (m_filesize+int(sizeof(qint16))>=m_bufferAllocatedSize) return false;
	if (m_swapBytes!=swap) res = ( ((res&0x00FF)<<8)| ((res&0xFF00)>>8));
	memcpy(&m_buf[m_bufPos],&res,sizeof(qint16));
	m_bufPos+=sizeof(qint16);
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writeUint24(quint32 res,const bool &swap)
{
    if (m_filesize+3>=m_bufferAllocatedSize) return false;
	if (m_swapBytes!=swap)res = (((res&0x0000FF)<<16)|((res&0x0000FF00))| ((res&0x00FF0000)>>16));
	memcpy(&m_buf[m_bufPos],&res,3);
	m_bufPos+=3;
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writeUint32(quint32 res,const bool &swap)
{
    if (m_filesize+int(sizeof(quint32))>=m_bufferAllocatedSize) return false;
	if (m_swapBytes!=swap) res = (((res&0x000000FF)<<24)|((res&0x0000FF00)<<8)| ((res&0x00FF0000)>>8)|((res&0xFF000000)>>24));
	memcpy(&m_buf[m_bufPos],&res,sizeof(quint32));
	m_bufPos+=sizeof(quint32);
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writeSint32(qint32  res,const bool &swap)
{
    if (m_filesize+int(sizeof(qint32))>=m_bufferAllocatedSize) return false;
	if (m_swapBytes!=swap) res = (((res&0x000000FF)<<24)|((res&0x0000FF00)<<8)| ((res&0x00FF0000)>>8)|((res&0xFF000000)>>24));
	memcpy(&m_buf[m_bufPos],&res,sizeof(qint32));
	m_bufPos+=sizeof(qint32);
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writefloat (float   res,const bool &swap)
{
    if (m_filesize+int(sizeof(float))>=m_bufferAllocatedSize) return false;
	if (m_swapBytes!=swap) {
		_float_swap sw;
		sw.f=&res;
		sw.swap();
	}
	memcpy(&m_buf[m_bufPos],&res,sizeof(float));
	m_bufPos+=sizeof(float);
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writedouble(const double  &res)
{
    if (m_filesize+int(sizeof(double))>=m_bufferAllocatedSize) return false;
	memcpy(&m_buf[m_bufPos],&res,sizeof(double));
	m_bufPos+=sizeof(double);
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}
bool _imgFileBuffer::writeString(const char * res)
{
	if (res==NULL) return false;
	int len =(int) strlen(res);
	return writeBuffer((quint8 *) res,len);
}
bool _imgFileBuffer::writeBuffer(quint8 * const buffer, const qint32 &writeSize)
{
    if (m_filesize+writeSize>=m_bufferAllocatedSize) return false;
	memcpy(&m_buf[m_bufPos],buffer,writeSize);
	m_bufPos+=writeSize;
	if (m_bufPos>m_sizeLoaded) {
		m_filesize=m_bufPos;
		m_sizeLoaded=m_bufPos;
	}
	return true;
}



bool _imgFileBuffer::setBufPositionWrite(const qint64 &position,bool setSize)
{
    if ((position<0) ||(quint32(position)>quint64(m_bufferAllocatedSize))) return false;
	m_bufPos=position;
	if (setSize && position>m_sizeLoaded) {
		m_filesize=position;
		m_sizeLoaded=position;
	}
	return true;
}



//############################################## rrP::_Rgba8 ##########################################################
//############################################## rrP::_Rgba8 ##########################################################
//############################################## rrP::_Rgba8 ##########################################################



//HDR colors:
//1.0  1.0  l.0 white
//0.0  0.0  l.0 blue   2  1
//.85  0.0  .85 purple 3 
//1.0  0.0  0.0 red 4
//.85  .85  0.0 yellow 5
//0.0  1.0  0.0 green 6
//0.0  1.0  1.0 cyan 7 
//1.0  1.0  l.0 white 8  7

const float swGradient[8][3] = { 
						{1.0f ,1.0f ,1.0f }, //white
						{0.0f ,0.0f ,1.0f }, //blue
						{0.85f,0.0f ,0.85f}, //purple
						{1.0f ,0.0f, 0.0f }, //red
						{0.85f,0.85f,0.0f }, //yellow
						{0.0f ,1.0f ,0.0f }, //green
						{0.0f ,1.0f ,1.0f }, //cyan
						{1.0f ,1.0f ,1.0f }, //white
						};
						
			
#define gradientScale 4.0f

void _Rgba8::fromFloatRGBA_sw(const float &ir, const float &ig, const float &ib, const float &ia, const bool &showSuperWhite)
{
	a=float2quint8(ia);
	float maxLum=max(max(saveF(ir),saveF(ib)),saveF(ig));
	if (!showSuperWhite || (maxLum<=1.0f)) {
		r=float2quint8(ir);
		g=float2quint8(ig);
		b=float2quint8(ib);
	} else if ((maxLum<=1.0f+1.0f/gradientScale) ) {
		maxLum-=1.0f;
		maxLum*=gradientScale;
		int fl=int(maxLum);
		if (fl==1) {
			maxLum=1.0f;
		} else 
			maxLum-=float(fl);
		float inv_maxLum=1.0f-maxLum;

		float f;
		f=ir*inv_maxLum + swGradient[0][0]*maxLum;
		r=float2quint8(f);
		f=ig*inv_maxLum + swGradient[0][1]*maxLum;
		g=float2quint8(f);
		f=ib*inv_maxLum + swGradient[0][2]*maxLum;
		b=float2quint8(f);
	} else {
		maxLum-=1.0f+1.0f/gradientScale;
		maxLum*=gradientScale;
		maxLum=fmod(maxLum,7.0f);
		int fl=int(maxLum);
		if (fl>6) fl=6;
		maxLum-=float(fl);
		if (maxLum>1.0) maxLum=1.0f;
		float inv_maxLum=1.0f-maxLum;
		float f;
		
		f=swGradient[fl][0]*inv_maxLum + swGradient[fl+1][0]*maxLum;
		r=float2quint8(f);
		f=swGradient[fl][1]*inv_maxLum + swGradient[fl+1][1]*maxLum;
		g=float2quint8(f);
		f=swGradient[fl][2]*inv_maxLum + swGradient[fl+1][2]*maxLum;
		b=float2quint8(f);
	}
}





void  _Rgba8::fromFloatR(const float &f)
{
	r=float2quint8(f);
}
void _Rgba8::fromFloatG(const float &f)
{
	g=float2quint8(f);
}
void _Rgba8::fromFloatB(const float &f)
{
	b=float2quint8(f);
}
void _Rgba8::fromFloatA(const float &f)
{
	a=float2quint8(f);
}


void  _Rgba8::fromFloatR(float f,const bool &swap)
{
	if (swap) {
		_float_swap sw;
		sw.f=&f;
		sw.swap();
	}
	fromFloatR(f);
}

void  _Rgba8::fromFloatG(float f,const bool &swap)
{
	if (swap) {
		_float_swap sw;
		sw.f=&f;
		sw.swap();
	}
	fromFloatG(f);
}

void  _Rgba8::fromFloatB(float f,const bool &swap)
{
	if (swap) {
		_float_swap sw;
		sw.f=&f;
		sw.swap();
	}
	fromFloatB(f);
}

void  _Rgba8::fromFloatA(float f,const bool &swap)
{
	if (swap) {
		_float_swap sw;
		sw.f=&f;
		sw.swap();
	}
	fromFloatA(f);
}


//############################################## rrP::_Rgba16 ##########################################################
//############################################## rrP::_Rgba16 ##########################################################
//############################################## rrP::_Rgba16 ##########################################################


void  _Rgba16::fromFloatR(const float &f)
{
	r=float2quint16(f);
}
void _Rgba16::fromFloatG(const float &f)
{
	g=float2quint16(f);
}
void _Rgba16::fromFloatB(const float &f)
{
	b=float2quint16(f);
}
void _Rgba16::fromFloatA(const float &f)
{
	a=float2quint16(f);
}


void  _Rgba16::fromFloatR(float f,const bool &swap)
{
	if (swap) {
		_float_swap sw;
		sw.f=&f;
		sw.swap();
	}
	fromFloatR(f);
}

void  _Rgba16::fromFloatG(float f,const bool &swap)
{
	if (swap) {
		_float_swap sw;
		sw.f=&f;
		sw.swap();
	}
	fromFloatG(f);
}

void  _Rgba16::fromFloatB(float f,const bool &swap)
{
	if (swap) {
		_float_swap sw;
		sw.f=&f;
		sw.swap();
	}
	fromFloatB(f);
}

void  _Rgba16::fromFloatA(float f,const bool &swap)
{
	if (swap) {
		_float_swap sw;
		sw.f=&f;
		sw.swap();
	}
	fromFloatA(f);
}


//############################################## rrP::_Rgbaf ##########################################################
//############################################## rrP::_Rgbaf ##########################################################
//############################################## rrP::_Rgbaf ##########################################################

void  _Rgbaf::swapBytes()
{
	_float_swap sw;
	sw.f=&r;
	sw.swap();
	sw.f=&g;
	sw.swap();
	sw.f=&b;
	sw.swap();
	sw.f=&a;
	sw.swap();
}



//############################################## _imgRGBABuffer8 ##########################################################
//############################################## _imgRGBABuffer8 ##########################################################
//############################################## _imgRGBABuffer8 ##########################################################


_imgRGBABuffer_all::_imgRGBABuffer_all(const quint32 &numberOfPixel, const qint8   &inPixelByteSize)
 {
    m_pixelByteSize=inPixelByteSize;
	m_hasAlpha=false;
	m_width=1;
	m_height=1;
	m_totalPixels=1;
	m_loadFlags=0;

	if (numberOfPixel<=0) m_bufSize=1;
	else m_bufSize=numberOfPixel;
}


_imgRGBABuffer_all::_imgRGBABuffer_all(const quint32 &width,const quint32 &height, const qint8   &inPixelByteSize)
{
    m_pixelByteSize=inPixelByteSize;
	m_hasAlpha=false;
	m_width=width;
	m_height=height;
	m_loadFlags=0;

	m_totalPixels= height*width;
	m_bufSize=m_totalPixels;
}



bool _imgRGBABuffer_all::doesImageSizeFit(const quint32 wid,const quint32 hei) const
{
	return (wid*hei)<=m_bufSize;
}







//############################################## _imgRGBABuffer8 ##########################################################
//############################################## _imgRGBABuffer8 ##########################################################
//############################################## _imgRGBABuffer8 ##########################################################




_imgRGBABuffer8::_imgRGBABuffer8(const quint32 &numberOfPixel)
 :_imgRGBABuffer_all(numberOfPixel,4)
{ 
    m_buf=NULL;

#ifdef RR_OS_WIN
    __try {
#endif
    m_bufOrgAlloc= new quint32[m_bufSize+4];
#ifdef RR_OS_WIN
    } __except(true) {
        m_bufSize=0;
		m_width=0;
		m_height=0;
		m_buf =NULL;
		return;
    }
#endif
    if (m_bufOrgAlloc==NULL) {
		m_bufSize=0;
		m_width=0;
		m_height=0;
		m_buf =NULL;
		return;
	}
	m_buf =  (_Rgba8 *) &m_bufOrgAlloc[1]; //offset required for png export as channels are shifted by one

} 

_imgRGBABuffer8::_imgRGBABuffer8(const quint32 &width,const quint32 &height)
 :_imgRGBABuffer_all(width,height,4)
{ 
    m_buf=NULL;
	m_bufOrgAlloc= new quint32[m_bufSize+4]; 
	if (m_bufOrgAlloc==NULL) {
		m_bufSize=0;
		m_width=0;
		m_height=0;
		m_buf =NULL;
		return;
	}
	m_buf = (_Rgba8 *) &m_bufOrgAlloc[1]; //offset required for some export if channels are shifted by one
} 


_imgRGBABuffer8::~_imgRGBABuffer8()
{ 
	rrDeleteArray(m_bufOrgAlloc);
}


void _imgRGBABuffer8::clear()
{ 
	memset(m_buf,0x60,m_bufSize*m_pixelByteSize);
	m_loadFlags=0;
}

void _imgRGBABuffer8::writeByte (const quint32 bufferPos ,const quint8 color)
{
	if (bufferPos>=m_bufSize*m_pixelByteSize) return;
	((quint8 *) m_buf)[bufferPos]=color;
}

void	_imgRGBABuffer8::write	  (const qint32 &x, const qint32 &y	,const quint8 &color,const _rrChannel &channel)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	rrP::_Rgba8 * rgba;
	rgba= (rrP::_Rgba8 *) &m_buf[bpos];
	switch (channel) {
		case _rrCA:rgba->a=color; break;
		case _rrCB:rgba->b=color; break;
		case _rrCG:rgba->g=color; break;
		case _rrCR:rgba->r=color; break;
	}
}

void _imgRGBABuffer8::write(const qint32 &x, const qint32 &y,const quint8 &r, const quint8 &g,const quint8 &b, const quint8 &a)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	_Rgba8 * col=(_Rgba8 *) &m_buf[bpos];
	col->r=r;
	col->g=g;
	col->b=b;
	col->a=a;
}


void _imgRGBABuffer8::write(const qint32 &x, const qint32 &y,const rrP::_Rgba8 &rgba)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	m_buf[bpos]=rgba;
}


void _imgRGBABuffer8::writeMix  (const qint32 &x, const qint32 &y	,const rrP::_Rgba8 &color, const float &opacity)
{
    if (opacity<=0) return;
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
    float invOp=1.0f-opacity;
    m_buf[bpos].r= quint8(m_buf[bpos].r*invOp  + color.r*opacity);
    m_buf[bpos].g= quint8(m_buf[bpos].g*invOp  + color.g*opacity);
    m_buf[bpos].b= quint8(m_buf[bpos].b*invOp  + color.b*opacity);
}


void _imgRGBABuffer8::write(const qint32 pixelIndex,const quint8 &r, const quint8 &g,const quint8 &b, const quint8 &a)
{
	if (pixelIndex>=(int) m_bufSize) return;
	_Rgba8 *col=(_Rgba8 *) &m_buf[pixelIndex];
	col->r=r;
	col->g=g;
	col->b=b;
	col->a=a;
}

void _imgRGBABuffer8::write(const qint32 pixelIndex,const rrP::_Rgba8 &rgba)
{
	if (pixelIndex>=(qint32) m_bufSize) return;
	m_buf[pixelIndex]=rgba;
}

void	_imgRGBABuffer8::writeMulti(const qint32 pixelIndex			,const char * const bufferFrom,qint32 numberOfPixel)
{
	if (pixelIndex>=(int) m_bufSize) return;
	if (pixelIndex+numberOfPixel>=(int) m_bufSize) numberOfPixel=m_bufSize-pixelIndex-1;
	if (numberOfPixel<=0)  return;
	memcpy(&m_buf[pixelIndex],bufferFrom,numberOfPixel*m_pixelByteSize);
	return;
}

void _imgRGBABuffer8::writeMulti(const qint32 &x, const qint32 &y,const  char * const bufferFrom,qint32 numberOfPixel)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	if (bpos+numberOfPixel>=m_bufSize) numberOfPixel=m_bufSize-bpos-1;
	if (numberOfPixel<=0)  return;
	memcpy(&m_buf[bpos],bufferFrom,numberOfPixel*m_pixelByteSize);
	return;
}


_Rgba8 _imgRGBABuffer8::read(const qint32 &x, const qint32 &y) const
{
	if (x>=m_width) return _Rgba8();
	if (y>=m_height)  return _Rgba8();
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return _Rgba8();
	return m_buf[bpos];
}

_Rgba8 _imgRGBABuffer8::read(const quint32 pixelIndex) const
{
	if (pixelIndex>=m_bufSize) return _Rgba8();
	return (_Rgba8) m_buf[pixelIndex];
}


void _imgRGBABuffer8::read(_Rgba8 &out,const qint32 &x, const qint32 &y) const
{
	if (x>=m_width) { out=m_buf[0]; return;}
	if (y>=m_height)  { out=m_buf[0]; return;}
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) { out=m_buf[0]; return;}
	out=m_buf[bpos];
}

void _imgRGBABuffer8::read(_Rgba8 &out,const quint32 pixelIndex) const
{
	if (pixelIndex>=m_bufSize) { out=m_buf[0]; return;}
	out= m_buf[pixelIndex];
}





bool _imgRGBABuffer8::copyTo(_imgRGBABuffer8 &dest,bool copyImgData)
{
	if (qint64(dest.m_bufSize) < m_totalPixels ) return false;
	dest.setWidth(m_width);
	dest.setHeight(m_height);
	dest.m_hasAlpha =m_hasAlpha;
	dest.m_headerInfo =m_headerInfo;
	dest.m_loadFlags=m_loadFlags;
	if (copyImgData) memcpy(dest.m_buf,this->m_buf,m_totalPixels*m_pixelByteSize);
	return true;
}


void _imgRGBABuffer8::createLetterBox(rrP::_imgRGBABuffer8 *imgBuffer,const int &Yoffset,int screenHeight)
{
	if (screenHeight+Yoffset > imgBuffer->m_height) {
		screenHeight=imgBuffer->m_height - Yoffset;
	}
	m_totalPixels= imgBuffer->m_width * screenHeight;
	m_buf= &imgBuffer->m_buf[Yoffset* imgBuffer->m_width ];
	m_bufSize = m_totalPixels;
	rrDeleteArray(m_bufOrgAlloc);
}

void _imgRGBABuffer8::freeLetterBox()
{
	m_width=0;
	m_height=0;
	m_totalPixels=0;
	m_bufSize=0;
	m_buf = NULL;
}


//############################################## _imgRGBABuffer16 ##########################################################
//############################################## _imgRGBABuffer16 ##########################################################
//############################################## _imgRGBABuffer16 ##########################################################


_imgRGBABuffer16::_imgRGBABuffer16(quint32 numberOfPixel)
:_imgRGBABuffer_all(numberOfPixel,4*2)
{ 

	m_buf = new _Rgba16[numberOfPixel]; 
	if (m_buf==NULL) {
		m_bufSize=0;
		m_width=0;
		m_height=0;
		numberOfPixel=0;
		m_buf =NULL;
		return;
	}
} 

_imgRGBABuffer16::~_imgRGBABuffer16()
{ 
	rrDeleteArray(m_buf);
}

void _imgRGBABuffer16::clear()
{ 
	memset(m_buf,0x60,m_bufSize*m_pixelByteSize);
	m_loadFlags=0;
}

void _imgRGBABuffer16::writeShort (const quint32 bufferPos ,const quint16 color)
{
	if (bufferPos>=m_bufSize*m_pixelByteSize) return;
	((quint16 *) m_buf)[bufferPos]=color;
}

void	_imgRGBABuffer16::write	  (const qint32 &x, const qint32 &y	,const quint16 &color,const _rrChannel &channel)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	rrP::_Rgba16 * rgba;
	rgba= (rrP::_Rgba16 *) &m_buf[bpos];
	switch (channel) {
		case _rrCA:rgba->a=color; break;
		case _rrCB:rgba->b=color; break;
		case _rrCG:rgba->g=color; break;
		case _rrCR:rgba->r=color; break;
	}
}

void _imgRGBABuffer16::write(const qint32 &x, const qint32 &y,const quint16 &r, const quint16 &g,const quint16 &b, const quint16 &a)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	_Rgba16 * col=(_Rgba16 *) &m_buf[bpos];
	col->r=r;
	col->g=g;
	col->b=b;
	col->a=a;
}


void _imgRGBABuffer16::write(const qint32 &x, const qint32 &y,const rrP::_Rgba16 &rgba)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	m_buf[bpos]=rgba;
}


void _imgRGBABuffer16::write(const qint32 pixelIndex,const quint16 &r, const quint16 &g,const quint16 &b, const quint16 &a)
{
	if (pixelIndex>=(int) m_bufSize) return;
	_Rgba16 *col=(_Rgba16 *) &m_buf[pixelIndex];
	col->r=r;
	col->g=g;
	col->b=b;
	col->a=a;
}

void _imgRGBABuffer16::write(const qint32 pixelIndex,const rrP::_Rgba16 &rgba)
{
	if (pixelIndex>=(qint32) m_bufSize) return;
	m_buf[pixelIndex]=rgba;
}

void	_imgRGBABuffer16::writeMulti(const qint32 pixelIndex			,const char * const bufferFrom,qint32 numberOfPixel)
{
	if (pixelIndex>=(int) m_bufSize) return;
	if (pixelIndex+numberOfPixel>=(int) m_bufSize) numberOfPixel=m_bufSize-pixelIndex-1;
	if (numberOfPixel<=0)  return;
	memcpy(&m_buf[pixelIndex],bufferFrom,numberOfPixel*m_pixelByteSize);
	return;
}

void _imgRGBABuffer16::writeMulti(const qint32 &x, const qint32 &y,const  char * const bufferFrom,qint32 numberOfPixel)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	if (bpos+numberOfPixel>=m_bufSize) numberOfPixel=m_bufSize-bpos-1;
	if (numberOfPixel<=0)  return;
	memcpy(&m_buf[bpos],bufferFrom,numberOfPixel*m_pixelByteSize);
	return;
}


_Rgba16 _imgRGBABuffer16::read(const qint32 &x, const qint32 &y) const
{
	if (x>=m_width) return _Rgba16();
	if (y>=m_height)  return _Rgba16();
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return _Rgba16();
	return m_buf[bpos];
}

_Rgba16 _imgRGBABuffer16::read(const quint32 pixelIndex) const
{
	if (pixelIndex>=m_bufSize) return _Rgba16();
	return (_Rgba16) m_buf[pixelIndex];
}


void _imgRGBABuffer16::read(_Rgba16 * &out,const qint32 &x, const qint32 &y) const
{
	if (x>=m_width) { out=(_Rgba16 *) &m_buf[0]; return;}
	if (y>=m_height)  { out=(_Rgba16 *) &m_buf[0]; return;}
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) { out=(_Rgba16 *) &m_buf[0]; return;}
	out= (_Rgba16 *) &m_buf[bpos];
}

void _imgRGBABuffer16::read(_Rgba16 * &out,const quint32 pixelIndex) const
{
	if (pixelIndex>=m_bufSize) { out=(_Rgba16 *) &m_buf[0]; return;}
	out= (_Rgba16 *) &m_buf[pixelIndex];
}





bool _imgRGBABuffer16::copyTo(_imgRGBABuffer16 &dest,bool copyImgData)
{
	if (qint64(dest.m_bufSize) < m_totalPixels ) return false;
	dest.setWidth(m_width);
	dest.setHeight(m_height);
	dest.m_hasAlpha =m_hasAlpha;
	dest.m_headerInfo =m_headerInfo;
	dest.m_loadFlags=m_loadFlags;
	if (copyImgData) memcpy(dest.m_buf,this->m_buf,m_totalPixels*m_pixelByteSize);
	return true;
}



//############################################## _imgRGBABufferf ##########################################################
//############################################## _imgRGBABufferf ##########################################################
//############################################## _imgRGBABufferf ##########################################################



_imgRGBABufferf::_imgRGBABufferf(quint32 numberOfPixel)
:_imgRGBABuffer_all(numberOfPixel,4*4)
{ 
	m_hasAlpha=false;
	m_width=1;
	m_height=1;
	m_totalPixels=1;
	m_loadFlags=0;

	m_buf = new _Rgbaf[numberOfPixel]; 
	if (m_buf==NULL) {
		m_bufSize=0;
		m_width=0;
		m_height=0;
		numberOfPixel=0;
		m_buf =NULL;
		return;
	}

} 

_imgRGBABufferf::~_imgRGBABufferf()
{ 
	rrDeleteArray(m_buf);
}

void _imgRGBABufferf::clear()
{ 
	memset(m_buf,0x60,m_bufSize*m_pixelByteSize);
	m_loadFlags=0;
}

void _imgRGBABufferf::writeFloat (const quint32 bufferPos ,const float color)
{
	if (bufferPos>=m_bufSize*m_pixelByteSize) return;
	((float *) m_buf)[bufferPos]=color;
}

void	_imgRGBABufferf::write	  (const qint32 &x, const qint32 &y	,const float &color,const _rrChannel &channel)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	rrP::_Rgbaf * rgba;
	rgba= (rrP::_Rgbaf *) &m_buf[bpos];
	switch (channel) {
		case _rrCA:rgba->a=color; break;
		case _rrCB:rgba->b=color; break;
		case _rrCG:rgba->g=color; break;
		case _rrCR:rgba->r=color; break;
	}
}

void _imgRGBABufferf::write(const qint32 &x, const qint32 &y,const float &r, const float &g,const float &b, const float &a)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	_Rgbaf * col=(_Rgbaf *) &m_buf[bpos];
	col->r=r;
	col->g=g;
	col->b=b;
	col->a=a;
}


void _imgRGBABufferf::write(const qint32 &x, const qint32 &y,const rrP::_Rgbaf &rgba)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	m_buf[bpos]=rgba;
}


void _imgRGBABufferf::write(const qint32 pixelIndex,const float &r, const float &g,const float &b, const float &a)
{
	if (pixelIndex>=(int) m_bufSize) return;
	_Rgbaf *col=(_Rgbaf *) &m_buf[pixelIndex];
	col->r=r;
	col->g=g;
	col->b=b;
	col->a=a;
}

void _imgRGBABufferf::write(const qint32 pixelIndex,const rrP::_Rgbaf &rgba)
{
	if (pixelIndex>=(qint32) m_bufSize) return;
	m_buf[pixelIndex]=rgba;
}

void	_imgRGBABufferf::writeMulti(const qint32 pixelIndex			,const char * const bufferFrom,qint32 numberOfPixel)
{
	if (pixelIndex>=(int) m_bufSize) return;
	if (pixelIndex+numberOfPixel>=(int) m_bufSize) numberOfPixel=m_bufSize-pixelIndex-1;
	if (numberOfPixel<=0)  return;
	memcpy(&m_buf[pixelIndex],bufferFrom,numberOfPixel*m_pixelByteSize);
	return;
}

void _imgRGBABufferf::writeMulti(const qint32 &x, const qint32 &y,const  char * const bufferFrom,qint32 numberOfPixel)
{
	if ((x>=m_width) || (x<0) || (y>=m_height) || (y<0)) return;
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return;
	if (bpos+numberOfPixel>=m_bufSize) numberOfPixel=m_bufSize-bpos-1;
	if (numberOfPixel<=0)  return;
	memcpy(&m_buf[bpos],bufferFrom,numberOfPixel*m_pixelByteSize);
	return;
}


_Rgbaf _imgRGBABufferf::read(const qint32 &x, const qint32 &y) const
{
	if (x>=m_width) return _Rgbaf();
	if (y>=m_height)  return _Rgbaf();
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) return _Rgbaf();
	return m_buf[bpos];
}

_Rgbaf _imgRGBABufferf::read(const quint32 pixelIndex) const
{
	if (pixelIndex>=m_bufSize) return _Rgbaf();
	return (_Rgbaf) m_buf[pixelIndex];
}


void _imgRGBABufferf::read(_Rgbaf * &out,const qint32 &x, const qint32 &y) const
{
	if (x>=m_width) { out=(_Rgbaf *) &m_buf[0]; return;}
	if (y>=m_height)  { out=(_Rgbaf *) &m_buf[0]; return;}
	quint32 bpos=bufPos(x,y);
	if (bpos>=m_bufSize) { out=(_Rgbaf *) &m_buf[0]; return;}
	out= (_Rgbaf *) &m_buf[bpos];
}

void _imgRGBABufferf::read(_Rgbaf * &out,const quint32 pixelIndex) const
{
	if (pixelIndex>=m_bufSize) { out=(_Rgbaf *) &m_buf[0]; return;}
	out= (_Rgbaf *) &m_buf[pixelIndex];
}





bool _imgRGBABufferf::copyTo(_imgRGBABufferf &dest,bool copyImgData)
{
	if (qint64(dest.m_bufSize) < m_totalPixels ) return false;
	dest.setWidth(m_width);
	dest.setHeight(m_height);
	dest.m_hasAlpha =m_hasAlpha;
	dest.m_headerInfo =m_headerInfo;
	dest.m_loadFlags=m_loadFlags;
	if (copyImgData) memcpy(dest.m_buf,this->m_buf,m_totalPixels*m_pixelByteSize);
	return true;
}



}// end namespace

