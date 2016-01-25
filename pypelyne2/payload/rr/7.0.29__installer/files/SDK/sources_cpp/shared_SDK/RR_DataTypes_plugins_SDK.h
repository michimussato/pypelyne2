#ifndef RRSDK_DataTypes_plugins_H
#define RRSDK_DataTypes_plugins_H

#include "RR_defines_SDK.h"
#include "RR_version_SDK.inc"
#include <float.h>
//#include <math.h>
#include "RR_defines_features_classid_SDK.h"
#include "../sharedLib/RR_DataTypes_rrString_SDK.h"


class __RRSDK;
class __RR;

#ifdef DEF_PluginsIMG
class _rrPluginsIMG;
#endif

namespace  rrJ {
	class _JobBasicsArray;
	class _JobSend;
    }  
namespace  rrCHK {
	class _SingleImageFile;
	class _SingleImageView;
    }






inline qint32 swapByte(qint32 source)
{
    return 0
        | ((source & 0x000000ff) << 24)
        | ((source & 0x0000ff00) << 8)
        | ((source & 0x00ff0000) >> 8)
        | ((source & 0xff000000) >> 24);
};


inline quint32 swapByte(quint32 source)
{
    return 0
        | ((source & 0x000000ff) << 24)
        | ((source & 0x0000ff00) << 8)
        | ((source & 0x00ff0000) >> 8)
        | ((source & 0xff000000) >> 24);
};

inline quint16 swapByte(quint16 source)
{
    return 0
        | ((source & 0x00ff) << 8)
        | ((source & 0xff00) >> 8);
};



namespace  rrP {

//Plugins should return one of these error codes:
enum _rrpReturnCode {
	rUnknownError=0,
	rSuccessful=1,				//Successful execution
	rFileNotFound=2,			//File to read was not found (for Scene parser plugins in case they have to change the input filename to the right scene name)
	rFileFailedToOpen=3,		//Failed to open the file to read
	rUnsupportedFormat=4,		//File format is not supported
	rRRDataVersionConflict=5,	//StructureID or MinorID not supported //(RR also checks the returned StructureID and MinorID of the plugin info function)
	rCError=6,					//an unhandled/unknown C exception occured
	rMemError=7,				//plugin cannot allocate required memory
	rPluginFileMissing=8,		//RR wanted to load plugin, but it was deleted		
	rPluginLoadError=9,			//RR wanted to load plugin, but was unable to do so
	rSuccessfulIgnoreNoJobs=10,	//Do not use it
	rOtherError=11,				
	rWrongFileSize=12,			//Image file or scene file does not have expected size (as told from the file header)
	rNoImageDimensions=13,		//RR called plugin, but plugin did not return width or height
	rDataError=14,				//Some error while decoding the data
	rImageDimensionsToLarge=15,	//RR called plugin, width or height of image are to big for image buffer
	rRequireFullLoad=16,		//imgLoadHeader gets only a few kBytes to get its header information. But this specific imgLoadHeader requires a full load of the file, so it returns imgLoadHeader and is called again with full file buffer.
	rNoPluginforFileType=17,	//RR does not find a plugin for this image type
	rPythonError=18,	
	rFileSizeToSmall=19,		//File is smaller than the MinFileSize set by the plugin
	rDebugCompile=20,			//Mismatch: plugin or main app was compiled in debug, the other not
	rIsPlaceHolderFile=21,		//
	rFileFailedToSave=22,		//Failed to save the file
	rSuccessfulRetryLoad=23,	//Do not use it
	rFileBuffertoSmall=24,		//If a write to the buffer failed, the plugin should return this error
    rNoImageOutput=25,		    //For scene readers: No image output set in scene file
    rAbsolutePathsRequired=26,		  
	rLoadEndOfFileOnly=27,		//For image reader: do not load full image, load only the last 1kb.
    };

enum _rrpPluginType {
	tCpp,
	tPython,
	tTextBased,
};


struct _dataALL_Info_pre {
    unsigned short	StructureID;		//Two-way usage: RR send the plugin its version, the plugin overwrites the value and tells RR the version it was compiled with.
    unsigned short  MinorID;			
    _rrString50		pluginName;
    _rrString100		pluginAuthor;
    _rrString25		pluginVersion;
    _rrString25		RRVersion;			//Two-way usage: RR send the plugin its version, the plugin overwrites the value and tells RR the version it was compiled with.
    _rrString25		QTVersion;			//Two-way usage: RR send the plugin its version, the plugin overwrites the value and tells RR the version it was compiled with.
	bool			isDebugCompile;     //The plugin was compiled as debug
};

struct _dataALL_Info:_dataALL_Info_pre {
    __RRSDK			* RR;
#ifdef rrDEBUG
	void setDebugCompile(){ isDebugCompile=true;};
#else
	#if ((defined NDEBUG) || (defined QT_NO_DEBUG))
		void setDebugCompile(){ isDebugCompile=false;};
	#else
		void setDebugCompile(){ isDebugCompile=true;};
	#endif
#endif

#ifndef rrPlugin
#endif
    };





//####################################### Scene Parser Plugins  ############################################
//####################################### Scene Parser Plugins  ############################################
//####################################### Scene Parser Plugins  ############################################
//####################################### Scene Parser Plugins  ############################################

    
#pragma pack(4)
struct _dataPARS_Info: _dataALL_Info    {
	unsigned int			struct_align_ignore;
    _rrString50              supportedFileExt;	//supported file extensions the plugin can parse. Each extension starts with *. and ends with ; . E.g. "*.ma;*.mb;"
	};
struct _dataPARS_LoadSceneFile     {
    _rrString250				* fileName;
    rrJ::_JobBasicsArray    * const jobs;
    __RRSDK			        * const RR;
    const bool	            batchmode;
    /*constructor*/_dataPARS_LoadSceneFile(_rrString250 &inFileName, rrJ::_JobBasicsArray * const injobs , __RRSDK * const inRR,const bool &inbatchmode) :fileName(&inFileName), jobs(injobs), RR(inRR), batchmode(inbatchmode){};
    };
#pragma pack() //restore default alignment

#define         rrpPARS_Info_Name	   "pInfo"
#define         rrpPARS_Info_Def	   int  pInfo(rrP::_dataPARS_Info * const data)
typedef int (* rrpPARS_Info_Func)                (rrP::_dataPARS_Info * const data); 

#define         rrpPARS_LoadSceneFile_Name       "pLoadSceneFile"
#define         rrpPARS_LoadSceneFile_Def	 int pLoadSceneFile(rrP::_dataPARS_LoadSceneFile * const data)
typedef int  (* rrpPARS_LoadSceneFile_Func)                    (rrP::_dataPARS_LoadSceneFile * const data);




//####################################### Notification Plugins  ############################################
//####################################### Notification Plugins  ############################################
//####################################### Notification Plugins  ############################################
//####################################### Notification Plugins  ############################################

#pragma pack(4)

const unsigned int Max_dataNFY_Info_Params  =25;

struct _dataNFY_Info: _dataALL_Info  {
	unsigned int		paramMax;
    _rrString25          param[Max_dataNFY_Info_Params];
    _rrString25          paramDisplayName;
	};

struct _dataNFY_Notify     {
    __RRSDK			        * const RR;
	rrJ::_JobSend			* const job;
	/*constructor*/_dataNFY_Notify(__RRSDK * const inRR, rrJ::_JobSend * const inJob) :RR(inRR), job(inJob) {};
    };

struct _dataNFY_InitExit     {
    __RRSDK			        * const RR;
    /*constructor*/_dataNFY_InitExit(__RRSDK * const inRR) :RR(inRR){};
    };
#pragma pack() //restore default alignment



#define         rrpNFY_Info_Name	   "pInfo"
#define         rrpNFY_Info_Def	   int pInfo(rrP::_dataNFY_Info * const data)
typedef int (* rrpNFY_Info_Func)             (rrP::_dataNFY_Info * const data); 

#define         rrpNFY_Notify_Name      "pNotify"
#define         rrpNFY_Notify_Def	 int pNotify(rrP::_dataNFY_Notify * const data)
typedef int  (* rrpNFY_Notify_Func)             (rrP::_dataNFY_Notify * const data);

#define         rrpNFY_Init_Name    "pInit"
#define         rrpNFY_Init_Def	 int pInit(rrP::_dataNFY_InitExit * const data)
typedef int  (* rrpNFY_Init_Func)         (rrP::_dataNFY_InitExit * const data);

#define         rrpNFY_Exit_Name    "pExit"
#define         rrpNFY_Exit_Def	 int pExit(rrP::_dataNFY_InitExit * const data)
typedef int  (* rrpNFY_Exit_Func)         (rrP::_dataNFY_InitExit * const data);




//####################################### Server Job Plugins  ############################################
//####################################### Server Job Plugins  ############################################
//####################################### Server Job Plugins  ############################################
//####################################### Server Job Plugins  ############################################

#pragma pack(4)

//server plugins are executed if the job enters the stage
const qint16 JobExecFirstCheck				= 1 << 1;   //job was received, next is first check to find outpout dir and existing files is not done yet
const qint16 JobExecScriptPreRender			= 1 << 2;   //pre-render-scripts are executed next
const qint16 JobExecPreviewRender			= 1 << 3;	//job starts to render now (either preview or jumps to complete render)
const qint16 JobExecScriptAfterPreview   	= 1 << 10;	//script executed after preview frames are done
const qint16 JobExecWaitForApprovalMain		= 1 << 4;	//Job is waiting for approval
const qint16 JobExecMainRender				= 1 << 5;	//Job starts the main render phase 
const qint16 JobExecScriptPostRender    	= 1 << 6;	//post-scripts are now executed
const qint16 JobExecWaitForApprovalDone		= 1 << 7;	//Job is waiting for approval
const qint16 JobExecScriptFinished			= 1 << 8;	//Job is executing post-done-scripts next
const qint16 JobExecFinished				= 1 << 9;	//Job is completely finished
const qint16 JobExecALL						= 0x0FFF;	//all flags


struct _dataJOB_Info: _dataALL_Info    {
	quint32		executedWhenFlags;
	};

struct _dataJOB_Execute     {
    __RRSDK			        * const RR;
	rrJ::_JobSend			* const job;
	/*constructor*/_dataJOB_Execute(__RRSDK * const inRR, rrJ::_JobSend * const inJob) :RR(inRR), job(inJob) {};
    };

struct _dataJOB_InitExit     {
    __RRSDK			        * const RR;
    /*constructor*/_dataJOB_InitExit(__RRSDK * const inRR) :RR(inRR){};
    };
#pragma pack() //restore default alignment



#define         rrpJOB_Info_Name	  "pInfo"
#define         rrpJOB_Info_Def	   int pInfo(rrP::_dataJOB_Info * const data)
typedef int (* rrpJOB_Info_Func)             (rrP::_dataJOB_Info * const data); 

#define         rrpJOB_Execute_Name     "pExecute"
#define         rrpJOB_Execute_Def	 int pExecute(rrP::_dataJOB_Execute * const data)
typedef int  (* rrpJOB_Execute_Func)             (rrP::_dataJOB_Execute * const data);

#define         rrpJOB_Init_Name    "pInit"
#define         rrpJOB_Init_Def	 int pInit(rrP::_dataJOB_InitExit * const data)
typedef int  (* rrpJOB_Init_Func)         (rrP::_dataJOB_InitExit * const data);

#define         rrpJOB_Exit_Name    "pExit"
#define         rrpJOB_Exit_Def	 int pExit(rrP::_dataJOB_InitExit * const data)
typedef int  (* rrpJOB_Exit_Func)         (rrP::_dataJOB_InitExit * const data);




//####################################### Image Plugins  ############################################
//####################################### Image Plugins  ############################################
//####################################### Image Plugins  ############################################


#define saveF(fnr) ( _isnan(fnr) ? (0) :  fnr )
#define float2quint8(fnr) ( ((fnr<=0) || _isnan(fnr)) ? (0) :  (fnr>=1.0f) ? (0xFF) : (int(fnr*255.0f)) )
#define float2quint16(fnr) ( ((fnr<=0) || _isnan(fnr)) ? (0) :  (fnr>=1.0f) ? (0xFFFF) : (int(fnr*65535.0f)) )


struct _float_swap {
	union
	{
		float *f;
		quint32 *i;
	};
	void swap(){*i = (((*i & 0x000000FF)<<24)|((*i & 0x0000FF00)<<8)| ((*i & 0x00FF0000)>>8)|((*i & 0xFF000000)>>24));   };
};

#pragma pack(1)



struct _Rgba8 {
    union 
    {
		struct {quint8 r,g,b,a;};
		quint32 col; //0xAABBGGRR
    };
	void fromFloatR(const float &f);
	void fromFloatG(const float &f);
	void fromFloatB(const float &f);
	void fromFloatA(const float &f);
	void fromFloatRGBA_sw(const float &ir, const float &ig, const float &ib, const float &ia, const bool &showSuperWhite);
	void fromFloatR(float f,const bool &swap);
	void fromFloatG(float f,const bool &swap);
	void fromFloatB(float f,const bool &swap);
	void fromFloatA(float f,const bool &swap);
	inline void swapBGR() {col =  (col&0xFF000000)|((col&0x0000FF)<<16)|((col&0x0000FF00))| ((col&0x00FF0000)>>16);}; //0xAARRGGBB => 0xAABBGGRR
	inline void swapGBR() {col =  (col&0xFF000000)|((col&0x00FF0000)>>8)|((col&0x0000FF00)>>8)| ((col&0x000000FF)<<16);}; //0xAAGGRRBB => 0xAABBGGRR
	_Rgba8(const quint32 &icol=0xFFCCCCCC):col(icol){};
	_Rgba8 fromARGB(quint32 color) {col=color; swapBGR(); return *this;};
    };

struct _Rgba16 {
    union 
    {
		struct {quint16 r,g,b,a;};
		quint64 col; //0xAAAABBBBGGGGRRRR
            };
	void fromFloatR(const float &f);
	void fromFloatG(const float &f);
	void fromFloatB(const float &f);
	void fromFloatA(const float &f);
	void fromFloatR(float f,const bool &swap);
	void fromFloatG(float f,const bool &swap);
	void fromFloatB(float f,const bool &swap);
	void fromFloatA(float f,const bool &swap);
    inline void swapBGR() {col =  (col&0xFFFF000000000000LL)|((col&0x0000000000FFFFLL)<<32)|((col&0x00000000FFFF0000LL))| ((col&0x0000FFFF00000000LL)>>32);}; //0xAARRGGBB => 0xAABBGGRR
    inline void swapGBR() {col =  (col&0xFFFF000000000000LL)|((col&0x0000FFFF00000000LL)>>16)|((col&0x00000000FFFF0000LL)>>16)| ((col&0x000000000000FFFFLL)<<32);}; //0xAAGGRRBB => 0xAABBGGRR

    _Rgba16(){col=0xFFFFCCCCCCCCCCCCLL;};
	_Rgba16(quint64 color) {col=color;};
    };

struct _Rgbaf {
		struct {float r,g,b,a;};
		void swapBytes();
		//float col[4]; //0xAABBGGRR
    };

#pragma pack()



enum _rrChannel {
	_rrCR=0,
	_rrCG=1,
	_rrCB=2,
	_rrCA=3
    };



#pragma pack(4)

struct _imgHeaderInfo {
    private:
	    quint16 _thisStructSize;  //size of this struct
    public:
	    _imgHeaderInfo() {_thisStructSize=sizeof(_imgHeaderInfo); clear();};
	    inline quint16 _imgHeaderInfoSize() {return _thisStructSize;};
        qint32  width;
        qint32  height;
        bool    hasAlpha;      //RGB or RGBA?
        qint8   bitDepth;	  //8, 16 or 32(float)
        bool    fixedFileSize;   //=file size does not vary, uncompressed files
	    _rrString250 infoString; //Human readable information about the format e.g. SGI RLA-compressed
							    //If an error occurs or format is not supported: " ERR: Unsupported color specification!" or " ERR: File size too small!" or " ERR: compression not supported!" or ....
        qint32  dataStartOffset; //Start of the image data. The file pointer is set to dataStartOffset before any imgDecode function is called. If imgLoadHeader does not set this value, dataStartOffset is set to the current position after imgLoadHeader
	    void clear() { dataStartOffset=-1; width=0; height=0;	hasAlpha=false; bitDepth=8; fixedFileSize=false; infoString.clear(); };
    };



struct _imgFileBuffer {
		#ifdef DEF_PluginsIMG
		friend class ::_rrPluginsIMG;
		#endif
	    RR_DISABLE_COPY(_imgFileBuffer)
	private:
        quint8  * m_buf;
        qint64  m_bufferAllocatedSize;
        qint64  m_sizeLoaded; //has to be signed in case read returns -1
        qint64  m_filesize;
        qint64  m_bufPos;
    public:
        bool   m_swapBytes; //change big endian <> low endian in all read/write functions

	    _imgFileBuffer(unsigned int  newSize);
	    ~_imgFileBuffer();
	    void   setSizeLoaded(qint64 newSize); //used by RR while loading the file
	    bool   setFileSize(unsigned int  newSize);


	    bool readUint8 (quint8  &res);
	    bool readSint8 (qint8   &res);
	    bool readUint16(quint16 &res,const bool &swap=false);
	    bool readSint16(qint16  &res,const bool &swap=false);
	    bool readUint24(quint32 &res,const bool &swap=false);
	    bool readUint32(quint32 &res,const bool &swap=false);
	    bool readSint32(qint32  &res,const bool &swap=false);
	    bool readfloat (float   &res,const bool &swap=false);
	    bool readdouble(double  &res);
	    bool readBuffer(quint8 * const buffer, const qint32 &readSize);

	    bool readUint8P (quint8  &res,const qint32 &position);
	    bool readSint8P (qint8   &res,const qint32 &position);
	    bool readUint16P(quint16 &res,const qint32 &position,const bool &swap=false);
	    bool readSint16P(qint16  &res,const qint32 &position,const bool &swap=false);
	    bool readUint32P(quint32 &res,const qint32 &position,const bool &swap=false);
	    bool readSint32P(qint32  &res,const qint32 &position,const bool &swap=false);
	    bool readfloatP (float   &res,const qint32 &position,const bool &swap=false);
	    bool readdoubleP(double  &res,const qint32 &position);
	    bool readBufferP(quint8 * const buffer, const qint32 &readSize,const qint32 &position);


        inline void resetBufferSize() {m_sizeLoaded=0; m_filesize=0;}; //called before imgEncodeX functions
        inline qint64 maxBufferSize() const {return m_bufferAllocatedSize;};
	    bool writeUint8 (const quint8  &res);
	    bool writeSint8 (const qint8   &res);
	    bool writeUint16(quint16 res,const bool &swap=false);
	    bool writeSint16(qint16  res,const bool &swap=false);
	    bool writeUint24(quint32 res,const bool &swap=false);
	    bool writeUint32(quint32 res,const bool &swap=false);
	    bool writeSint32(qint32  res,const bool &swap=false);
	    bool writefloat (float   res,const bool &swap=false);
	    bool writedouble(const double  &res);
		bool writeString(const char * res);
	    bool writeBuffer(quint8 * const buffer, const qint32 &writeSize);


        inline quint8 * buffer() {return  m_buf; };
        inline quint8 * buffer(const qint64 &position) {return &m_buf[position]; };
        inline quint8 * bufferCurrentPos() {return &m_buf[m_bufPos]; };
        inline qint64	getBufferAllocatedSize() {return m_bufferAllocatedSize;};
        inline qint64   getFileSize()  {return m_filesize;};
        inline qint64	getBufPosition() {return m_bufPos;};
        inline qint64	getSizeLoaded() {return m_sizeLoaded;};
		//RR does not load the whole file for the function "imgLoadHeader", so there is a difference between getSizeLoaded() and getFileSize()
		//But the file is loaded completely before the imgDecodeX functions

	    bool   setBufPosition(const qint64 &position);
		bool   setBufPositionWrite(const qint64 &position,bool setSize=false);
	    bool   offsetBufPosition(qint64 offset);

    };



struct _imgPluginBuffer {
	quint8 buffer[1*1024*1024];
	bool readfromFileBuffer(_imgFileBuffer * const fileBuf, const qint16 &headerSize);
    void clear() {memset(buffer,0,1*1024*1024);}; 
    };


const quint8 _imgLoadGammaAdjusted	=0x0001;
const quint8 _imgLoadSuperWhite	=0x0001 << 1;




struct _imgRGBABuffer_all {
	    friend class rrCHK::_SingleImageFile;
		friend class rrCHK::_SingleImageView;
		friend class ::__RR;
		#ifdef DEF_PluginsIMG
		friend class ::_rrPluginsIMG;
		#endif
	    RR_DISABLE_COPY(_imgRGBABuffer_all)

//################ variables: ################
    public:
	    _imgRGBABuffer_all(const quint32 &numberOfPixel, const qint8   &inPixelByteSize);
		_imgRGBABuffer_all(const quint32 &width,const quint32 &height, const qint8   &inPixelByteSize);

        bool        m_hasAlpha;
        _imgHeaderInfo m_headerInfo;
        quint8      m_loadFlags; //was: gammaAdjusted;

    protected:
        qint8       m_pixelByteSize;
        quint32     m_bufSize; //buffer size in pixels (not bytes!!!)
        qint32      m_width;
        qint32      m_height;
        quint32     m_totalPixels;


    public:
        inline  quint32 bufPos(const qint32 &x, const qint32 &y) const {return ((y*m_width)+x);};
	    bool	doesImageSizeFit (const quint32 wid,const quint32 hei) const;
        inline	qint32	width() const { return m_width;};
        inline	qint32	height() const {return m_height;};
        inline	quint32	totalPixels() const { return m_totalPixels;};
        inline  qint32   getBufferAllocatedSize() const {return m_bufSize*m_pixelByteSize;};
        inline	void	setWidth (const qint32 &newWidth ) {m_width =newWidth;  m_totalPixels=m_height*m_width; if (m_totalPixels>m_bufSize) {setWidth (m_bufSize/m_height);}  };
        inline	void	setHeight(const qint32 &newHeight) {m_height=newHeight; m_totalPixels=m_height*m_width; if (m_totalPixels>m_bufSize) {setHeight(m_bufSize/m_width);}  };
        bool	gammaAdjusted() { return ((m_loadFlags & _imgLoadGammaAdjusted)>0);};
        void	setgammaAdjusted(const bool value) {if (value) m_loadFlags|=_imgLoadGammaAdjusted; else m_loadFlags&= ~_imgLoadGammaAdjusted; };
        bool	superwhite() { return ((m_loadFlags & _imgLoadSuperWhite)>0);};
        void	setsuperwhite(const bool value) {if (value) m_loadFlags|=_imgLoadSuperWhite; else m_loadFlags&= ~_imgLoadSuperWhite; };
};




struct _imgRGBABuffer8: _imgRGBABuffer_all {
	    friend class rrCHK::_SingleImageFile;
		friend class rrCHK::_SingleImageView;
		friend class ::__RR;
		#ifdef DEF_PluginsIMG
		friend class ::_rrPluginsIMG;
		#endif
		
	    RR_DISABLE_COPY(_imgRGBABuffer8)
    public:
	    _imgRGBABuffer8(const quint32 &numberOfPixel);
		_imgRGBABuffer8(const quint32 &width,const quint32 &height);
	    ~_imgRGBABuffer8();

	    void	write     (const qint32 &x, const qint32 &y	,const quint8 &r, const quint8 &g,const quint8 &b, const quint8 &a);
	    //void	write	  (const qint32 &x, const qint32 &y	,const quint32 &rgba);
	    void	write	  (const qint32 &x, const qint32 &y	,const _Rgba8  &rgba);
	    void	writeMulti(const qint32 &x, const qint32 &y	,const char * const bufferFrom,qint32 numberOfPixel);
	    void	write     (const qint32 pixelIndex			,const quint8 &r, const quint8 &g,const quint8 &b, const quint8 &a);
	    //void	write     (const qint32 pixelIndex			,const quint32 &rgba);
	    void	write     (const qint32 pixelIndex			,const _Rgba8  &rgba);
        void	writeMix  (const qint32 &x, const qint32 &y	,const rrP::_Rgba8 &color, const float &opacity);
	    void	writeMulti(const qint32 pixelIndex			,const char * const bufferFrom,qint32 numberOfPixel);
	    void	writeByte (const quint32 bufferPos			,const quint8 color);
	    void	write	  (const qint32 &x, const qint32 &y	,const quint8 &color,const _rrChannel &channel);



	    _Rgba8  read(const qint32 &x, const qint32 &y) const;
	    _Rgba8  read(const quint32 pixelIndex) const;

	    void  read(_Rgba8 &out,const qint32 &x, const qint32 &y) const;
	    void  read(_Rgba8 &out,const quint32 pixelIndex) const;

        void	clear();
	    bool	copyTo(_imgRGBABuffer8 &dest,bool copyImgData=true);
        inline  _Rgba8 * buffer() const {return (_Rgba8 *) m_buf;};
        inline  _Rgba8 * buffer(const int &pixelIndex) const {return (_Rgba8 *) &m_buf[pixelIndex];};
        inline  _Rgba8 * buffer(const qint32 &x, const qint32 &y) const {return (_Rgba8 *) &m_buf[bufPos(x,y)];};
        inline	void	fillColor(const quint8 &color=0x60) {memset(m_buf,color,m_bufSize*m_pixelByteSize); } ;

		void createLetterBox(rrP::_imgRGBABuffer8 *imgBuffer,const int &Yoffset,int screenHeight);
		void freeLetterBox();


//################ variables: ################
    private:
        _Rgba8 * m_buf;
	#ifdef RRx32
        _Rgba8 * m_bufx64; //just a placeholder to keep memory size equal
	#endif
        quint32 *m_bufOrgAlloc;
	#ifdef RRx32
        quint32 * m_bufOrgAllocx64;//just a placeholder to keep memory size equal
	#endif
    };





struct _imgRGBABuffer16: _imgRGBABuffer_all {
	    RR_DISABLE_COPY(_imgRGBABuffer16)
	    public:
	    _imgRGBABuffer16(quint32 numberOfPixel);
	    ~_imgRGBABuffer16();

	    void	write     (const qint32 &x, const qint32 &y	,const quint16 &r, const quint16 &g,const quint16 &b, const quint16 &a);
	    void	write	  (const qint32 &x, const qint32 &y	,const _Rgba16  &rgba);
	    void	writeMulti(const qint32 &x, const qint32 &y	,const char * const bufferFrom,qint32 numberOfPixel);
	    void	write     (const qint32 pixelIndex			,const quint16 &r, const quint16 &g,const quint16 &b, const quint16 &a);
	    void	write     (const qint32 pixelIndex			,const _Rgba16  &rgba);
	    void	writeMulti(const qint32 pixelIndex			,const char * const bufferFrom,qint32 numberOfPixel);
    	
	    void	writeShort(const quint32 bufferPos			,const quint16 color);
	    void	write	  (const qint32 &x, const qint32 &y	,const quint16 &color,const _rrChannel &channel);

	    _Rgba16  read(const qint32 &x, const qint32 &y) const;
	    _Rgba16  read(const quint32 pixelIndex) const;

	    void  read(_Rgba16 * &out,const qint32 &x, const qint32 &y) const;
	    void  read(_Rgba16 * &out,const quint32 pixelIndex) const;

        void	clear();
	    bool	copyTo(_imgRGBABuffer16 &dest,bool copyImgData=true);
        inline  _Rgba16 * buffer() const {return (_Rgba16 *) m_buf;};
        inline  _Rgba16 * buffer(const int &pos) const {return (_Rgba16 *) &m_buf[pos];};
        inline  _Rgba16 * buffer(const qint32 &x, const qint32 &y) const {return (_Rgba16 *) &m_buf[bufPos(x,y)];};
        inline	void	fillColor(const quint8 &color=0x60) {memset(m_buf,color,m_bufSize*m_pixelByteSize); } ;



	//################ variables: ################
    private:
        _Rgba16 * m_buf;
	#ifdef RRx32
        _Rgba16 * m_bufx64;
	#endif
    };


struct _imgRGBABufferf: _imgRGBABuffer_all {
	    RR_DISABLE_COPY(_imgRGBABufferf)

	    //friend class rrCHK::_SingleImageFile;
		//friend class rrCHK::_SingleImageView;
		//friend class ::__RR;
		#ifdef DEF_PluginsIMG
		friend class ::_rrPluginsIMG;
		#endif
		

	    public:
	    _imgRGBABufferf(quint32 numberOfPixel);
	    ~_imgRGBABufferf();

	    void	write     (const qint32 &x, const qint32 &y	,const float &r, const float &g,const float &b, const float &a);
	    void	write	  (const qint32 &x, const qint32 &y	,const _Rgbaf  &rgba);
	    void	writeMulti(const qint32 &x, const qint32 &y	,const char * const bufferFrom,qint32 numberOfPixel);
	    void	write     (const qint32 pixelIndex			,const float &r, const float &g,const float &b, const float &a);
	    void	write     (const qint32 pixelIndex			,const _Rgbaf  &rgba);
	    void	writeMulti(const qint32 pixelIndex			,const char * const bufferFrom,qint32 numberOfPixel);
    	
	    void	writeFloat(const quint32 bufferPos			,const float color);
	    void	write	  (const qint32 &x, const qint32 &y	,const float &color,const _rrChannel &channel);

	    _Rgbaf  read(const qint32 &x, const qint32 &y) const;
	    _Rgbaf  read(const quint32 pixelIndex) const;

	    void  read(_Rgbaf * &out,const qint32 &x, const qint32 &y) const;
	    void  read(_Rgbaf * &out,const quint32 pixelIndex) const;

        void	clear();
	    bool	copyTo(_imgRGBABufferf &dest,bool copyImgData=true);
        inline  _Rgbaf * buffer() const {return (_Rgbaf *) m_buf;};
        inline  _Rgbaf * buffer(const int &pos) const {return (_Rgbaf *) &m_buf[pos];};
        inline  _Rgbaf * buffer(const qint32 &x, const qint32 &y) const {return (_Rgbaf *) &m_buf[bufPos(x,y)];};
        inline	void	fillColor(const quint8 &color=0x60) {memset(m_buf,color,m_bufSize*m_pixelByteSize); } ;

	//################ variables: ################
    private:
        _Rgbaf * m_buf;
	#ifdef RRx32
        _Rgbaf * m_bufx64;
	#endif
	};




const unsigned short IMGFuncDecode8  = 1 << 1;
const unsigned short IMGFuncEncode8  = 1 << 2;
const unsigned short IMGFuncDecode16 = 1 << 3;
const unsigned short IMGFuncEncode16 = 1 << 4;
const unsigned short IMGFuncDecodef  = 1 << 5;
const unsigned short IMGFuncEncodef  = 1 << 6;
const unsigned short IMGFuncEncodeGamma = 1 << 7;
typedef unsigned short IMGFuncFlags;


struct _dataIMG_Info: _dataALL_Info    {
	unsigned int	minFileSize;
	_rrString50		supportedFileExt;	//supported file extensions the plugin can parse. Each extension starts with *. and ends with ; . E.g. "*.ma;*.mb;"
	IMGFuncFlags	flags;
	};
struct _dataIMG_LoadHeader    {
    rrP::_imgFileBuffer * const in;
    rrP::_imgHeaderInfo * const outInfo;
    rrP::_imgPluginBuffer * const pluginCustomData;
    __RRSDK * const RR;
    /*constructor*/_dataIMG_LoadHeader( rrP::_imgFileBuffer * const inin, rrP::_imgHeaderInfo * const inoutInfo, rrP::_imgPluginBuffer * const inpluginCustomData, __RRSDK * const inRR)
    /*constructor*/    :in(inin), outInfo(inoutInfo), pluginCustomData (inpluginCustomData), RR(inRR){};
    };
struct _dataIMG_Decode8    {
    rrP::_imgFileBuffer * const in;
    rrP::_imgRGBABuffer8 * const out;
    rrP::_imgPluginBuffer * const pluginCustomData;
    __RRSDK * const RR;
    /*constructor*/_dataIMG_Decode8( rrP::_imgFileBuffer * const inin, rrP::_imgRGBABuffer8 * const inout, rrP::_imgPluginBuffer * const inpluginCustomData, __RRSDK * const inRR)
    /*constructor*/    :in(inin), out(inout), pluginCustomData (inpluginCustomData), RR(inRR){};
    };
struct _dataIMG_Decode16    {
    rrP::_imgFileBuffer * const in;
    rrP::_imgRGBABuffer16 * const out;
    rrP::_imgPluginBuffer * const pluginCustomData;
    __RRSDK * const RR;
    /*constructor*/_dataIMG_Decode16( rrP::_imgFileBuffer * const inin, rrP::_imgRGBABuffer16 * const inout, rrP::_imgPluginBuffer * const inpluginCustomData, __RRSDK * const inRR)
    /*constructor*/    :in(inin), out(inout), pluginCustomData (inpluginCustomData), RR(inRR){};
    };
struct _dataIMG_Decodef    {
    rrP::_imgFileBuffer * const in;
    rrP::_imgRGBABufferf * const out;
    rrP::_imgPluginBuffer * const pluginCustomData;
    __RRSDK * const RR;
    /*constructor*/ _dataIMG_Decodef( rrP::_imgFileBuffer * const inin, rrP::_imgRGBABufferf * const inout, rrP::_imgPluginBuffer * const inpluginCustomData, __RRSDK * const inRR)
    /*constructor*/    :in(inin), out(inout), pluginCustomData (inpluginCustomData), RR(inRR){};
    };
struct _dataIMG_Encode8    {
    rrP::_imgFileBuffer * const out;
    rrP::_imgRGBABuffer8 * const in;
    rrP::_imgPluginBuffer * const pluginCustomData;
    __RRSDK * const RR;
    /*constructor*/_dataIMG_Encode8( rrP::_imgFileBuffer * const inout, rrP::_imgRGBABuffer8 * const inin, rrP::_imgPluginBuffer * const inpluginCustomData, __RRSDK * const inRR)
    /*constructor*/   : out(inout), in(inin), pluginCustomData (inpluginCustomData),  RR(inRR){};
    };
struct _dataIMG_Encode16    {
    rrP::_imgFileBuffer * const out;
    rrP::_imgRGBABuffer16 * const in;
    rrP::_imgPluginBuffer * const pluginCustomData;
    __RRSDK * const RR;
    /*constructor*/_dataIMG_Encode16( rrP::_imgFileBuffer * const inout, rrP::_imgRGBABuffer16 * const inin, rrP::_imgPluginBuffer * const inpluginCustomData, __RRSDK * const inRR)
       : out(inout), in(inin), pluginCustomData (inpluginCustomData),  RR(inRR){};
    };
struct _dataIMG_Encodef    {
    rrP::_imgFileBuffer * const out;
    rrP::_imgRGBABufferf * const in;
    rrP::_imgPluginBuffer * const pluginCustomData;
    __RRSDK * const RR;
    /*constructor*/_dataIMG_Encodef( rrP::_imgFileBuffer * const inout, rrP::_imgRGBABufferf * const inin, rrP::_imgPluginBuffer * const inpluginCustomData, __RRSDK * const inRR)
       : out(inout), in(inin), pluginCustomData (inpluginCustomData),  RR(inRR){};
    };


#pragma pack()  

#define         rrpIMG_Info_Name	       "imgInfo"
#define         rrpIMG_Info_Def		    int imgInfo(rrP::_dataIMG_Info * const data)
typedef int  (* rrpIMG_Info_Func)                  (rrP::_dataIMG_Info * const data); 

#define         rrpIMG_LoadHeader_Name	   "imgLoadHeader"
#define         rrpIMG_LoadHeader_Def	int imgLoadHeader(rrP::_dataIMG_LoadHeader * const data)
typedef int  (* rrpIMG_LoadHeader_Func)                  (rrP::_dataIMG_LoadHeader * const data); 

#define         rrpIMG_Decode8_Name	       "imgDecode8"
#define         rrpIMG_Decode8_Def	    int imgDecode8(rrP::_dataIMG_Decode8 * const data)
typedef int  (* rrpIMG_Decode8_Func)                  (rrP::_dataIMG_Decode8 * const data); 

#define         rrpIMG_Decode16_Name	   "imgDecode16"
#define         rrpIMG_Decode16_Def	    int imgDecode16(rrP::_dataIMG_Decode16 * const data)
typedef int  (* rrpIMG_Decode16_Func)                  (rrP::_dataIMG_Decode16 * const data); 

#define         rrpIMG_Decodef_Name	       "imgDecodef"
#define         rrpIMG_Decodef_Def	    int imgDecodef(rrP::_dataIMG_Decodef * const data)
typedef int  (* rrpIMG_Decodef_Func)                  (rrP::_dataIMG_Decodef * const data); 

#define         rrpIMG_Encode8_Name	       "imgEncode8"
#define         rrpIMG_Encode8_Def	    int imgEncode8(rrP::_dataIMG_Encode8 * const data)
typedef int  (* rrpIMG_Encode8_Func)                  (rrP::_dataIMG_Encode8 * const data); 

#define         rrpIMG_Encode16_Name	   "imgEncode16"
#define         rrpIMG_Encode16_Def	    int imgEncode16(rrP::_dataIMG_Encode16 * const data)
typedef int  (* rrpIMG_Encode16_Func)                  (rrP::_dataIMG_Encode16 * const data); 

#define         rrpIMG_Encodef_Name	       "imgEncodef"
#define         rrpIMG_Encodef_Def	    int imgEncodef(rrP::_dataIMG_Encodef * const /*data*/)
typedef int  (* rrpIMG_Encodef_Func)                  (rrP::_dataIMG_Encodef * const data); 

} //endNamespace


#endif 

