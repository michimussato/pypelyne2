#ifndef RR_files_H
#define RR_files_H

#include "../shared_SDK/RR_defines_SDK.h"
#include "../sharedLib/RR_DataTypes_rrString_SDK.h"
#include "../sharedLib/RR_DataTypes_time_SDK.h"


#define noQT_DirSearch

#if ((!defined rrPlugin) || (defined defrrSceneParserMayaBinary)  || (defined defrrSceneParserClarisseIFX))
    #if defined(RR_OS_WIN) 
		//#include <Windows.h>
	#endif

	#ifdef noQT_DirSearch
			#if (!defined(RR_OS_WIN) )
			//#include <sys/types.h>
			//#include <dirent.h>
			#endif
		#else
			//#include <QFileInfoList>
			//#include <QDir>
		#endif

#endif



//___________________________________________________
//     simple dir/file/path name/exist checks


DllExport_sharedLib _rrString250		rrConvertPDToOS(const _rrString250 &inString);
DllExport_sharedLib _rrString500		rrConvertPDToOS(const _rrString500 &inString);

#if defined(QT_CORE_LIB)
    DllExport_sharedLib QString		rrGetDirName(QString dir,rrChar pd=PD);
    DllExport_sharedLib QString		rrGetDirNameAutoPD(QString dir);
    DllExport_sharedLib QString		rrGetFileName(QString dir,rrChar pd=PD);
    DllExport_sharedLib QString		rrGetFileNameBase(QString dir,rrChar pd=PD);
    DllExport_sharedLib QString		rrGetFileNameExtention(QString dir);
    DllExport_sharedLib QString		rrGetFileNameAutoPD(QString dir);
	DllExport_sharedLib bool		rrIsRootpath(const QString &path);
#endif
DllExport_sharedLib _rrString8_500	rrGetDirName( _rrString8_500 dir);
DllExport_sharedLib _rrString8_250	rrGetDirName( _rrString8_250 dir);
DllExport_sharedLib _rrString8_200	rrGetDirName( _rrString8_200 dir);
DllExport_sharedLib _rrString250		rrGetDirName( _rrString250 dir);
DllExport_sharedLib _rrString500		rrGetDirName( _rrString500 dir);
DllExport_sharedLib _rrString8_100	rrGetFileName(const _rrString8_500 &file);
DllExport_sharedLib _rrString8_100	rrGetFileName(const _rrString8_250 &file);
DllExport_sharedLib _rrString8_100	rrGetFileName(const _rrString8_200 &file);
DllExport_sharedLib _rrString100		rrGetFileName(const _rrString250 &file);
DllExport_sharedLib _rrString100		rrGetFileName(const _rrString500 &file);


//Ascii:
DllExport_sharedLib bool			rrDirectoryExists(_rrString8_200 strDirname);
DllExport_sharedLib bool			rrDirectoryExists(_rrString8_250 strDirname);
DllExport_sharedLib bool			rrDirectoryExists(_rrString8_500 strDirname);
DllExport_sharedLib bool			rrDirectoryExists(const  char * strDirname);
DllExport_sharedLib bool			rrFileExists(const _rrString8_250 &strFilename,_rrTime *FileTime =NULL, qint64 *size =NULL);
DllExport_sharedLib bool			rrFileExists(const _rrString8_500 &strFilename,_rrTime *FileTime =NULL, qint64 *size =NULL);
//unicode:
DllExport_sharedLib bool			rrDirectoryExists(_rrString500 strDirname);
DllExport_sharedLib inline bool		rrDirectoryExists(const _rrString250 &strDirname) {return rrDirectoryExists(_rrString500(strDirname.value));};
DllExport_sharedLib bool			rrFileExists(const _rrString500 &strFilename);
DllExport_sharedLib bool			rrFileExists(const _rrString500 &strFilename  ,_rrTime *FileTime, qint64 *size =NULL);
DllExport_sharedLib inline bool		rrFileExists(const _rrString250 &strFilename)										{return rrFileExists(_rrString500(strFilename.value));};
DllExport_sharedLib inline bool		rrFileExists(const _rrString250 &strFilename,_rrTime *FileTime, qint64 *size =NULL) {return rrFileExists(_rrString500(strFilename.value),FileTime,size);};

#if defined(QT_CORE_LIB)
    DllExport_sharedLib inline bool	rrFileExists(const QString strFilename) {return rrFileExists(_rrString500(strFilename));};
    DllExport_sharedLib bool		rrFileExists(QString strFilename,_rrTime *FileTime, qint64 *size =NULL);
    DllExport_sharedLib bool		rrDirectoryExists(QString strDirname);
#endif



//___________________________________________________
//     file/folder  modification (copy, delete, create, write buffer data)

#if ((!defined rrPlugin) || (defined defrrSceneParserMayaBinary) || (defined defrrSceneParserClarisseIFX))
	DllExport_sharedLib _rrString500	rrDeleteFile(const _rrString500 &filename);

  #ifdef RR_OS_WIN
    DllExport_sharedLib void		timeToFileTime( time_t t, LPFILETIME pft );
    DllExport_sharedLib void		fileTimeToTime( _rrTime &t, LPFILETIME pft );
  #endif

  #if defined(QT_CORE_LIB)
	DllExport_sharedLib QString		rrCopyFile(const QString & sourceFilename,const QString & destFilename, bool overwrite=true, const int &chunkwait=-1, bool *lastByteEmpty=NULL);
	DllExport_sharedLib QString		rrDeleteFile(const QString &filename);
	DllExport_sharedLib bool		rrCreateFolder(const QString &folderName, bool createParentfolder=true);
	DllExport_sharedLib bool		rrSetFileTime(const QString &filename,_rrTime * tim =NULL);
	DllExport_sharedLib bool		rrRenameFile(const QString  &oldFilename,const QString  &newFilename, bool overwrite=true);
	DllExport_sharedLib QString		rrWriteBufferToFile(QString fileName, quint8 * buffer, qint64 buffersize );
    DllExport_sharedLib QString		rrAddStringToFileName(QString fileName, const QString &insert);
    DllExport_sharedLib QString		rrPathResolve(QString fileName);
  #else
	DllExport_sharedLib bool		rrCopyFile(const _rrString8_500 & sourceFilename,const _rrString8_500 & destFilename, bool overwrite=true, const int &chunkwait=0, bool *lastByteEmpty=NULL);
	DllExport_sharedLib bool		rrDeleteFile(const _rrString8_500 &filename);
	DllExport_sharedLib bool		rrRenameFile(const _rrString8_500 &oldFilename,const _rrString8_500 &newFilename, bool overwrite=true);
	DllExport_sharedLib bool		rrCreateFolder(const _rrString8_500 &folderName, bool createParentfolder=true);
	DllExport_sharedLib bool		rrSetFileTime(const _rrString8_500 &filename, _rrTime * tim =NULL);
  #endif //QT_CORE_LIB

#endif

#if defined(QT_CORE_LIB)
    DllExport_sharedLib QString		rrConvertPDToOS(const QString &inString);
	DllExport_sharedLib QString		rrConvertPDToOS(const QString &inString,_rrOS ToOS);
	DllExport_sharedLib bool		isRelativePath(QString inString);
	DllExport_sharedLib QString		rrRemoveIllegalCharFromHtmlFile(QString inString);
	DllExport_sharedLib QString		rrRemoveIllegalCharFromHtmlDir(QString inString);
	DllExport_sharedLib QString		rrRemoveIllegalCharFromFile(QString inString,bool allowspaces=false,const bool &allowFN=false);
	DllExport_sharedLib QString		rrRemoveIllegalCharFromDir (QString inString,bool allowspaces=false,const bool &allowFN=false,bool allowGreaterSmaller=false );
#ifndef rrPlugin
#endif  //plugin
	DllExport_sharedLib bool		rrDeleteFolder(const QString &dirName);
#endif //qtcore



DllExport_sharedLib bool writeToLogFile(const _rrString8_250 &fileName,_rrString8_evenSize<3000> msg, bool overwrite=false, bool addTime=true);




#ifndef rrPlugin
  #ifdef RR_OS_MAC
  #else
  #endif
#endif //rrPlugin






	
//___________________________________________________
//     rrFileLocker

#if defined(QT_CORE_LIB)
#ifndef rrPlugin
#endif  //plugin
#endif //qtcore









#endif


