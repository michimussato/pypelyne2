
#include "RR_files_SDK.h"
#include <sys/stat.h>


#if defined(QT_CORE_LIB)
	//#include <QStringList>
	#include <QDir>
#endif 

#include <fstream>

#if defined(RR_OS_WIN) 
	//#include <Windows.h>
#else
    #include <errno.h>
	//#include <stdio.h>
	//#include <stddef.h>
//#include <sys/types.h>
    #include <fcntl.h>
    #include <utime.h>
    #include <stdint.h>
	//#include <stdlib.h>
	//#include <unistd.h>
	//#include <pwd.h>
#endif



//#define disallowDeleteFiles 
#ifndef rrPlugin
#endif







                  
bool rrFileExists(const _rrString500 &strFilename,_rrTime *FileTime, qint64 *size) {
  #ifdef RR_OS_WIN
    DWORD       fileAttr;
	fileAttr = GetFileAttributesW(strFilename.value);
    if ((fileAttr == INVALID_FILE_ATTRIBUTES) || ((fileAttr & FILE_ATTRIBUTE_DIRECTORY)>0)) return false;
    HANDLE fHandle=CreateFileW(strFilename.value,0,GENERIC_READ & FILE_SHARE_DELETE &  FILE_SHARE_READ & FILE_SHARE_WRITE, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL );

    if (fHandle==INVALID_HANDLE_VALUE) return false;
    if (FileTime!=NULL) {
        FILETIME created;
        FILETIME accessed;
        FILETIME lastWrite;
        if (GetFileTime(fHandle,&created,&accessed,&lastWrite)!=0) {
            FileTime->from_FILETIME(lastWrite.dwLowDateTime,lastWrite.dwHighDateTime);
        } else {
            FileTime->value=0;
        }
    }
    if (size!=NULL) {
        LARGE_INTEGER fileSize;
        if (GetFileSizeEx(fHandle,&fileSize)==0) {
            CloseHandle(fHandle);
            return false;
        }
        *size=fileSize.QuadPart;
    }
    CloseHandle(fHandle);
    return true;
  #else
	_rrString8_500 nameChar;
	strFilename.toChar(nameChar.value,nameChar.ArraySize);
	return rrFileExists(nameChar,FileTime, size);
  #endif
}



bool rrFileExists(const _rrString500 &strFilename) {
  #ifdef RR_OS_WIN
	DWORD       fileAttr;
	fileAttr = GetFileAttributesW(strFilename.value);
    if ((fileAttr == INVALID_FILE_ATTRIBUTES) || ((fileAttr & FILE_ATTRIBUTE_DIRECTORY)>0)) return false;
	return true;
  #else
	_rrString8_500 nameChar;
	strFilename.toChar(nameChar.value,nameChar.ArraySize);
	struct stat stFileInfo;
	if(stat(nameChar.value,&stFileInfo) == 0  &&  ((stFileInfo.st_mode & S_IFDIR)==0)) {
		return true;
	} else {
		return false;
	}
  #endif
}


#ifdef QT_CORE_LIB
bool rrFileExists(QString strFilename,_rrTime *FileTime, qint64 *size)
{
	return rrFileExists(_rrString500(strFilename),FileTime,size);
};
#endif


bool rrFileExists(const _rrString8_250 &strFilename, _rrTime *FileTime, qint64 *size) {
  #ifdef RR_OS_WIN
    DWORD       fileAttr;
	fileAttr = GetFileAttributesA(strFilename.value);
    if ((fileAttr == INVALID_FILE_ATTRIBUTES) || ((fileAttr & FILE_ATTRIBUTE_DIRECTORY)>0)) return false;
    HANDLE fHandle=CreateFileA(strFilename.value,0,GENERIC_READ & FILE_SHARE_DELETE &  FILE_SHARE_READ & FILE_SHARE_WRITE, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL );

    if (fHandle==INVALID_HANDLE_VALUE) return false;
    if (FileTime!=NULL) {
        FILETIME created;
        FILETIME accessed;
        FILETIME lastWrite;
        if (GetFileTime(fHandle,&created,&accessed,&lastWrite)!=0) {
            FileTime->from_FILETIME(lastWrite.dwLowDateTime,lastWrite.dwHighDateTime);
        } else {
            FileTime->value=0;
        }
    }
    if (size!=NULL) {
        LARGE_INTEGER fileSize;
        if (GetFileSizeEx(fHandle,&fileSize)==0) {
            CloseHandle(fHandle);
            return false;
        }
        *size=fileSize.QuadPart;
    }
    CloseHandle(fHandle);
    return true;
  #else
  struct stat stFileInfo;
  if(stat(strFilename.value,&stFileInfo) == 0 &&  ((stFileInfo.st_mode & S_IFDIR)==0)) {
	  if (FileTime!=NULL) *FileTime= _rrTime::convertStatFileTime(stFileInfo.st_mtime);
	  if (size!=NULL) *size= stFileInfo.st_size;
	  return true;
  } else {
	  if (FileTime!=NULL) FileTime->value=0;
	  if (size!=NULL) *size=0;
	  return false;
  }
   #endif
}

bool rrFileExists(const _rrString8_500 &strFilename,_rrTime *FileTime, qint64 *size) {
   #ifdef RR_OS_WIN
    DWORD       fileAttr;
	fileAttr = GetFileAttributesA(strFilename.value);
    if ((fileAttr == INVALID_FILE_ATTRIBUTES) || ((fileAttr & FILE_ATTRIBUTE_DIRECTORY)>0)) return false;
    HANDLE fHandle=CreateFileA(strFilename.value,0,GENERIC_READ & FILE_SHARE_DELETE &  FILE_SHARE_READ & FILE_SHARE_WRITE, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL );

    if (fHandle==INVALID_HANDLE_VALUE) return false;
    if (FileTime!=NULL) {
        FILETIME created;
        FILETIME accessed;
        FILETIME lastWrite;
        if (GetFileTime(fHandle,&created,&accessed,&lastWrite)!=0) {
            FileTime->from_FILETIME(lastWrite.dwLowDateTime,lastWrite.dwHighDateTime);
        } else {
            FileTime->value=0;
        }
    }
    if (size!=NULL) {
        LARGE_INTEGER fileSize;
        if (GetFileSizeEx(fHandle,&fileSize)==0) {
            CloseHandle(fHandle);
            return false;
        }
        *size=fileSize.QuadPart;
    }
    CloseHandle(fHandle);
    return true;
  #else
    struct stat stFileInfo;
  if(stat(strFilename.value,&stFileInfo) == 0 &&  ((stFileInfo.st_mode & S_IFDIR)==0)) {
	  if (FileTime!=NULL) *FileTime= _rrTime::convertStatFileTime(stFileInfo.st_mtime);
	  if (size!=NULL) *size= stFileInfo.st_size;
	  return true;
  } else {
	  if (FileTime!=NULL) FileTime->value=0;
	  if (size!=NULL) *size=0;
	  return false;
  }
    #endif
}






#ifndef rrPlugin
#ifndef RR_OS_WIN
#endif // ! RR_OS_WIN
#if defined(QT_CORE_LIB)
#ifdef RR_OS_WIN
        #ifdef _MSC_VER
        #else
        #endif
        #if (defined(RR_OS_WIN) && defined(_MSC_VER))
        #else
        #endif
#else
#endif
#else //QTCore
#ifdef RR_OS_WIN
        #ifdef _MSC_VER
        #else
        #endif
        #if (defined(RR_OS_WIN) && defined(_MSC_VER))
        #else
        #endif
#else
#endif
#endif //#if defined(QT_CORE_LIB) #else
#if defined(QT_CORE_LIB)
#ifdef RR_OS_WIN
#else
#endif
	#ifdef RR_OS_WIN
	#else
	#endif
#ifdef disallowDeleteFiles
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#else  //QTCore
#ifdef RR_OS_WIN
#else
#endif
#ifdef disallowDeleteFiles
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#endif //QTcore
#ifdef RR_OS_WIN
#endif //windows
#endif //plugin
#if defined(QT_CORE_LIB)
#ifdef RR_OS_WIN
#else 
#endif
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
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#if defined(QT_CORE_LIB)
#endif //QT_CORE_LIB
#if defined(QT_CORE_LIB)
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifndef rrPlugin
#endif //rrPlugin


bool rrDeleteFolder(const QString &dirName)
{
	QDir dir(dirName);
	return dir.rmdir(dirName);
}

#endif //QT_CORE_LIB



_rrString250 rrConvertPDToOS(const _rrString250 &inString)
{
	_rrString250 helper;
	helper=inString;
#ifdef RR_OS_WIN
	helper.replace(PD_LX,PD_WIN);
	//helper.replace(PD_MAC,PD_WIN);
#elif defined RR_OS_MAC
        helper.replace(PD_WIN,PD_LX);
	//helper.replace(PD_LX,PD_MAC);
#else
	helper.replace(PD_WIN,PD_LX);
	//helper.replace(PD_MAC,PD_LX);
#endif
	return helper;
}

_rrString500 rrConvertPDToOS(const _rrString500 &inString)
{
	_rrString500 helper;
	helper=inString;
#ifdef RR_OS_WIN
	helper.replace(PD_LX,PD_WIN);
	//helper.replace(PD_MAC,PD_WIN);
#elif defined RR_OS_MAC
        helper.replace(PD_WIN,PD_LX);
	//helper.replace(PD_LX,PD_MAC);
#else
	helper.replace(PD_WIN,PD_LX);
	//helper.replace(PD_MAC,PD_LX);
#endif
	return helper;
}



#ifndef rrPlugin
#ifdef disallowDeleteFiles
#endif
#ifdef RR_OS_WIN
#else
#endif
#endif //rrPlugin





#ifndef rrPlugin
#ifdef RR_OS_MAC
#endif //OSX_MAC
#endif














#ifndef rrPlugin
#if defined(QT_CORE_LIB)
#ifdef RR_OS_WIN
#else
#endif
		    #ifdef RR_OS_WIN
		    #else
		    #endif
    #if (defined(RR_OS_WIN) && defined(_MSC_VER))
    #else
    #endif
            #ifdef RR_OS_WIN
            #else
            #endif
#ifdef RR_OS_WIN
#else
#endif
#endif  //QT_CORE_LIB
#endif //ifndef plugin





bool writeToLogFile(const _rrString8_250 &fileName,_rrString8_3000 msg, bool overwrite, bool addTime)
{
	_rrTime zeit(true);
	_rrString8_3000 msg_neu="";
    if (addTime) {
	    msg_neu=zeit.asRR8String().value;
	    msg_neu+=": ";
    }
	msg_neu+=msg;
    msg_neu+="\n";

	std::ios_base::openmode openMode;
	if (overwrite) 
		 openMode=std::ofstream::out;
	else openMode=std::ofstream::app;

	std::ofstream myfile(fileName.value, openMode);
	if (myfile.is_open()) {
		std::string line;
		line=msg_neu.value;
		myfile << line;
		myfile.close();
		return true;
	}
	return false;
}


