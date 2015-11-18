#ifndef RR_files_H
#define RR_files_H

#include "RR_DataTypes_other_SDK.h"


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


_rrString250		rrConvertPDToOS(const _rrString250 &inString);
_rrString500		rrConvertPDToOS(const _rrString500 &inString);

#if defined(QT_CORE_LIB)
    QString		rrGetDirName(QString dir,rrChar pd=PD);
    QString		rrGetDirNameAutoPD(QString dir);
    QString		rrGetFileName(QString dir,rrChar pd=PD);
    QString		rrGetFileNameBase(QString dir,rrChar pd=PD);
    QString		rrGetFileNameExtention(QString dir);
    QString		rrGetFileNameAutoPD(QString dir);
	bool		rrIsRootpath(const QString &path);
#endif
_rrString8_500	rrGetDirName( _rrString8_500 dir);
_rrString8_250	rrGetDirName( _rrString8_250 dir);
_rrString8_200	rrGetDirName( _rrString8_200 dir);
_rrString250		rrGetDirName( _rrString250 dir);
_rrString500		rrGetDirName( _rrString500 dir);
_rrString8_100	rrGetFileName(const _rrString8_500 &file);
_rrString8_100	rrGetFileName(const _rrString8_250 &file);
_rrString8_100	rrGetFileName(const _rrString8_200 &file);
_rrString100		rrGetFileName(const _rrString250 &file);
_rrString100		rrGetFileName(const _rrString500 &file);


//Ascii:
bool			rrDirectoryExists(_rrString8_200 strDirname);
bool			rrDirectoryExists(_rrString8_250 strDirname);
bool			rrDirectoryExists(_rrString8_500 strDirname);
bool			rrDirectoryExists(char * strDirname);
bool			rrFileExists(const _rrString8_250 &strFilename,_rrTime *FileTime =NULL, qint64 *size =NULL);
bool			rrFileExists(const _rrString8_500 &strFilename,_rrTime *FileTime =NULL, qint64 *size =NULL);
//unicode:
bool			rrDirectoryExists(_rrString500 strDirname);
inline bool		rrDirectoryExists(const _rrString250 &strDirname) {return rrDirectoryExists(_rrString500(strDirname.value));};
bool			rrFileExists(const _rrString500 &strFilename);
bool			rrFileExists(const _rrString500 &strFilename  ,_rrTime *FileTime, qint64 *size =NULL);
inline bool		rrFileExists(const _rrString250 &strFilename)										{return rrFileExists(_rrString500(strFilename.value));};
inline bool		rrFileExists(const _rrString250 &strFilename,_rrTime *FileTime, qint64 *size =NULL) {return rrFileExists(_rrString500(strFilename.value),FileTime,size);};

#if defined(QT_CORE_LIB)
    inline bool	rrFileExists(const QString strFilename) {return rrFileExists(_rrString500(strFilename));};
    bool		rrFileExists(QString strFilename,_rrTime *FileTime, qint64 *size =NULL);
    bool		rrDirectoryExists(QString strDirname);
#endif



//___________________________________________________
//     file/folder  modification (copy, delete, create, write buffer data)

#if ((!defined rrPlugin) || (defined defrrSceneParserMayaBinary) || (defined defrrSceneParserClarisseIFX))
	_rrString500	rrDeleteFile(const _rrString500 &filename);
	bool		syncCopy(_rrString8_500 CopyFrom,_rrString8_500 CopyTo, const bool &winValidateExeEnd=true, _rrString8_500 * returnError=NULL,_rrString8_500 * returnInfo=NULL, int copyDelayTime=333,const bool &logNotCopied=false);

  #ifdef RR_OS_WIN
    void		timeToFileTime( time_t t, LPFILETIME pft );
    void		fileTimeToTime( _rrTime &t, LPFILETIME pft );
  #endif

  #if defined(QT_CORE_LIB)
	QString		rrCopyFile(const QString & sourceFilename,const QString & destFilename, bool overwrite=true, const int &chunkwait=-1, bool *lastByteEmpty=NULL);
	QString		rrDeleteFile(const QString &filename);
	bool		rrCreateFolder(const QString &folderName, bool createParentfolder=true);
	bool		rrSetFileTime(const QString &filename,_rrTime * tim =NULL);
	bool		rrRenameFile(const QString  &oldFilename,const QString  &newFilename, bool overwrite=true);
	QString		rrWriteBufferToFile(QString fileName, quint8 * buffer, qint64 buffersize );
    QString		rrAddStringToFileName(QString fileName, const QString &insert);
    QString		rrPathResolve(QString fileName);
  #else
	bool		rrCopyFile(const _rrString8_500 & sourceFilename,const _rrString8_500 & destFilename, bool overwrite=true, const int &chunkwait=0, bool *lastByteEmpty=NULL);
	bool		rrDeleteFile(const _rrString8_500 &filename);
	bool		rrRenameFile(const _rrString8_500 &oldFilename,const _rrString8_500 &newFilename, bool overwrite=true);
	bool		rrCreateFolder(const _rrString8_500 &folderName, bool createParentfolder=true);
	bool		rrSetFileTime(const _rrString8_500 &filename, _rrTime * tim =NULL);
  #endif //QT_CORE_LIB

#endif

    
#if defined(QT_CORE_LIB)
    QString		rrConvertPDToOS(const QString &inString);
	QString		rrConvertPDToOS(const QString &inString,_rrOS ToOS);
	bool		isRelativePath(QString inString);
	QString		rrRemoveIllegalCharFromHtmlFile(QString inString);
	QString		rrRemoveIllegalCharFromHtmlDir(QString inString);
	QString		rrRemoveIllegalCharFromFile(QString inString,bool allowspaces=false,const bool &allowFN=false);
	QString		rrRemoveIllegalCharFromDir (QString inString,bool allowspaces=false,const bool &allowFN=false,bool allowGreaterSmaller=false );
#ifndef rrPlugin
#endif  //plugin
	bool		rrDeleteFolder(const QString &dirName);
#endif //qtcore



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

