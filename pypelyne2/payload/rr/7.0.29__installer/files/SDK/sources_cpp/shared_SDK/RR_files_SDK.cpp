
#include "RR_files_SDK.h"
#include <sys/stat.h>

#if defined(QT_CORE_LIB)
	//#include <QStringList>
	#include <QDir>
#endif 

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
}

bool rrFileExists(const _rrString8_500 &strFilename,_rrTime *FileTime, qint64 *size) {
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
}





#if ((!defined rrPlugin) || (defined defrrSceneParserMayaBinary)  || (defined defrrSceneParserClarisseIFX))
#ifndef RR_OS_WIN
// Compute the greatest common divisor of U and V using Euclid's  algorithm.  U and V must be nonzero.
static inline size_t gcd (size_t u, size_t v)
{
  do
	{
	  size_t t = u % v;
	  u = v;
	  v = t;
	}
  while (v);
  return u;
}
// Compute the least common multiple of U and V.  U and V must be nonzero.
static inline size_t lcm (size_t u, size_t v)
{
  return u * (v / gcd (u, v));
}
static inline char * ptr_align (void const *ptr, size_t alignment)
{
  char const *p0 = (char const *) ptr;
  char const *p1 = p0 + alignment - 1;
  return (char *) (p1 - (size_t) p1 % alignment);
}
#endif // ! RR_OS_WIN





#define maxChunkSize 1*1024*1024


#if defined(QT_CORE_LIB)


QString	rrCopyFile(const QString & sourceFilename,const QString & destFilename, bool overwrite, const int &chunkwait, bool *lastByteEmpty)
{
    if (rrFileExists(destFilename)) {
		if (!overwrite) return QString();
		QString ret=rrDeleteFile(destFilename);
		if (!ret.isEmpty()) return ret;
	}
	_rrTime sourceTime;

	if (!rrFileExists(sourceFilename,&sourceTime)) return QString("Source file does not exist.");


#ifdef RR_OS_WIN
    if (chunkwait>=0) {
        char * buf=(char * ) malloc(maxChunkSize);
		if (buf==NULL) return QString("No memory left.");
        size_t size;
        #ifdef _MSC_VER
        FILE* source;
        int errno_t=_wfopen_s(&source,sourceFilename.utf16(), L"rb");
		if (errno_t!=0) {
        #else
        FILE* source = fopen(sourceFilename.toLatin1().data(), "rb");
		if (source==NULL) {
        #endif
	        free(buf);
			return QString("Unable to open input file.");
		}

        FILE* dest;
        #if (defined(RR_OS_WIN) && defined(_MSC_VER))
           errno_t=_wfopen_s(&dest,destFilename.utf16() , L"wb");
		   if (errno_t!=0) {
        #else
            dest = fopen(destFilename.toLatin1().data() , "wbx");
		if (source==NULL) {
        #endif
			free(buf);
			fclose(source);
			return QString("Unable to open output file.");
		}

        while (size = fread(buf, 1, maxChunkSize, source)) {
            if (lastByteEmpty!=NULL) {
				if (size>10) {
					*lastByteEmpty= (buf[size-1]==0 && buf[size-7]==0 && buf[size-10]==0);
				} else *lastByteEmpty= (buf[size-1]==0);
            }
            fwrite(buf, 1, size, dest);
            if (chunkwait>0) rrSleep(chunkwait);
        }
        free(buf);
        fclose(source);
        fclose(dest);
    } else {
        if (!CopyFileW((wchar_t*) sourceFilename.utf16(), (wchar_t*) destFilename.utf16(), !overwrite)) {
            return rrLastOSError();
        }
    }
	rrSetFileTime(destFilename,&sourceTime);
#else
	QString ret;

	char *buf = NULL;
	char *buf_alloc = NULL;
	char *name_alloc = NULL;
	int dest_desc;
	int source_desc;
	struct stat statSrc;

	source_desc = open (sourceFilename.toLatin1().data(), O_RDONLY);
	if (source_desc < 0) {
		ret="Cannot open source file for reading: "+rrLastOSError();
		return ret;
	}

	if (fstat (source_desc, &statSrc) != 0)	{
		ret="Cannot fstat source file: "+rrLastOSError();
		goto close_src_desc;
	}



	{
        ssize_t buf_size = maxChunkSize;
		if (S_ISREG (statSrc.st_mode) && (statSrc.st_size < buf_size)) { //reduce buffer to max file size
			buf_size = statSrc.st_size + 1;
			buf_size += (4*1024) - 1; //adjust buffer to 4096 block size
			buf_size -= buf_size % (4*1024);
			if (buf_size == 0) buf_size = 4*1024;
		}
		size_t buf_alignment = lcm (sysconf(_SC_PAGESIZE), sizeof (uintptr_t));
		size_t buf_alignment_slop = sizeof (uintptr_t) + buf_alignment - 1;
		buf_alloc = (char*) malloc (buf_size + buf_alignment_slop);
		buf = ptr_align (buf_alloc, buf_alignment);
		if (buf==NULL) {
            ret="No memory left";
			goto close_src_desc;
		}

		int open_flags = O_WRONLY | O_CREAT;
		mode_t dst_mode= S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH;
		dst_mode= dst_mode | statSrc.st_mode;
		dest_desc = open (destFilename.toLatin1().data(), open_flags, dst_mode);

		if (dest_desc < 0) {
            ret="Cannot create target file: "+rrLastOSError()+"!  '"+destFilename+"'";
			goto close_src_desc;
		}

		{

			for (;;)
			{
				ssize_t n_read = read (source_desc, buf, buf_size);
				if (n_read < 0)
				{
					if (errno == EINTR) continue;
					ret="Error reading source: "+rrLastOSError();
					goto close_src_and_dst_desc;
				}
				if (n_read == 0) break;
                if (lastByteEmpty!=NULL) {
                    *lastByteEmpty= (buf[n_read-1]==0);
                }
				//for (;;)
				//{
					ssize_t result = write (dest_desc, buf, n_read);
					if (errno == EINTR) continue;
					if (result!=n_read) {
						ret="Error writing destination: "+rrLastOSError();
						goto close_src_and_dst_desc;
					}
					//break;
				//}
				/* A short read on a regular file means EOF.  */
				if ((n_read != buf_size) && S_ISREG(statSrc.st_mode)) break;
                if (chunkwait>0) rrSleep(chunkwait);
			}

			//preserve timestamps
			struct utimbuf utimbuf;
			utimbuf.actime = statSrc.st_atime;
			utimbuf.modtime = statSrc.st_mtime;
			if (utime (destFilename.toLatin1().data(), &utimbuf) != 0) {
				ret="Error setting file time of destination file: "+rrLastOSError();
				goto close_src_and_dst_desc;
			}
		}
	}

	close_src_and_dst_desc:
	if (close (dest_desc) < 0) {
		ret="Error closing destination file: "+rrLastOSError();
	}
	close_src_desc:
	if (close (source_desc) < 0) {
		ret="Unable to close source: "+rrLastOSError();
	}

	free (buf_alloc);
	free (name_alloc);
	return ret;
#endif
	return QString();
}

#else //QTCore

bool rrCopyFile(const _rrString8_500 & sourceFilename,const _rrString8_500 & destFilename, bool overwrite, const int &chunkwait, bool *lastByteEmpty)
{
    if (rrFileExists(destFilename)) {
		if (!overwrite) return true;
		if (!rrDeleteFile(destFilename)) return false;
	}

	_rrTime sourceTime;
	if (!rrFileExists(sourceFilename,&sourceTime)) 
		return false;

#ifdef RR_OS_WIN
    if (chunkwait>=0) {
        char * buf=(char * ) malloc(maxChunkSize);
        size_t size;
        #ifdef _MSC_VER
        FILE* source;
        fopen_s(&source,sourceFilename.value, "rb");
        #else
        FILE* source = fopen(sourceFilename.value, "rb");
        #endif
		if (source==NULL) {
			free(buf);
			return false;
		}

        FILE* dest;
        #if (defined(RR_OS_WIN) && defined(_MSC_VER))
           fopen_s(&dest,destFilename.value , "wb");
        #else
            dest = fopen(destFilename.value , "wbx");
        #endif
		if (source==NULL) {
			fclose(source);
			free(buf);
			return false;
		}
        while (size = fread(buf, 1, maxChunkSize, source)) {
            if (lastByteEmpty!=NULL) {
                *lastByteEmpty=buf[size-1]==0;
            }
            fwrite(buf, 1, size, dest);
            if (chunkwait>0) rrSleep(chunkwait);
        }
        fclose(source);
        fclose(dest);
        free(buf);
        rrSetFileTime(destFilename,&sourceTime);
    } else {
	    if (!CopyFileA(sourceFilename.value, destFilename.value, !overwrite)) {
    		return false;
        }
	}
	
	
#else
	bool ret=true;

	char *buf = NULL;
	char *buf_alloc = NULL;
	char *name_alloc = NULL;
	int dest_desc;
	int source_desc;
	struct stat statSrc;

	source_desc = open (sourceFilename.value, O_RDONLY);
	if (source_desc < 0) {
		return false;
	}

	if (fstat (source_desc, &statSrc) != 0)	{
		ret=false;
		goto close_src_desc;
	}

	{
		int open_flags = O_WRONLY | O_CREAT;
		mode_t dst_mode= S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH;
		dst_mode= dst_mode | statSrc.st_mode;
		dest_desc = open (destFilename.value, open_flags, dst_mode);

		if (dest_desc < 0) {
			ret=false;
			goto close_src_desc;
		}

		{
			ssize_t buf_size = 512*1024; //use 512 KB buffer
			if (S_ISREG (statSrc.st_mode) && (statSrc.st_size < buf_size)) { //reduce buffer to max file size
				buf_size = statSrc.st_size + 1;
				buf_size += (4*1024) - 1; //adjust buffer to 4096 block size
				buf_size -= buf_size % (4*1024);
				if (buf_size == 0) buf_size = 4*1024;
			}
			size_t buf_alignment = lcm (sysconf(_SC_PAGESIZE), sizeof (uintptr_t));
			size_t buf_alignment_slop = sizeof (uintptr_t) + buf_alignment - 1;
			buf_alloc = (char*) malloc (buf_size + buf_alignment_slop);
			buf = ptr_align (buf_alloc, buf_alignment);

			for (;;)
			{
				ssize_t n_read = read (source_desc, buf, buf_size);
				if (n_read < 0)
				{
					if (errno == EINTR) continue;
					ret=false;
					goto close_src_and_dst_desc;
				}
				if (n_read == 0) break;
                if (lastByteEmpty!=NULL) {
                    *lastByteEmpty=buf[n_read-1]==0;
                }
				for (;;)
				{
					ssize_t result = write (dest_desc, buf, n_read);
					if (errno == EINTR) continue;
					if (result!=n_read) {
						ret=false;
						goto close_src_and_dst_desc;
					}
					break;
				}
				/* A short read on a regular file means EOF.  */
				if ((n_read != buf_size) && S_ISREG(statSrc.st_mode)) break;
                if (chunkwait>0) rrSleep(chunkwait);
			}

			//preserve timestamps
			struct utimbuf utimbuf;
			utimbuf.actime = statSrc.st_atime;
			utimbuf.modtime = statSrc.st_mtime;
			if (utime (destFilename.value, &utimbuf) != 0) {
				ret=false;
				goto close_src_and_dst_desc;
			}
		}
	}

	close_src_and_dst_desc:
	if (close (dest_desc) < 0) {
		ret=false;
	}
	close_src_desc:
	if (close (source_desc) < 0) {
		ret=false;
	}

	free (buf_alloc);
	free (name_alloc);
	return ret;
#endif
	return true;
}

#endif //#if defined(QT_CORE_LIB) #else





#include <time.h>

#if defined(QT_CORE_LIB)
bool rrSetFileTime(const QString &filename,_rrTime * tim)
{
	_rrTime jetzte;

	if (tim != NULL) jetzte=*tim;
	else jetzte.setCurrentTime();

#ifdef RR_OS_WIN
	FILETIME newFileTime;
	time_t t;
	t=jetzte.value;


	timeToFileTime(t,&newFileTime);

	HANDLE hFile = CreateFileW((wchar_t*) filename.utf16(),
        FILE_WRITE_ATTRIBUTES,FILE_SHARE_READ|FILE_SHARE_WRITE,
        NULL,
        OPEN_EXISTING,
        FILE_FLAG_NO_BUFFERING,
        NULL);

	if(hFile == INVALID_HANDLE_VALUE)
		return false;

    BOOL bVal = SetFileTime(hFile,&newFileTime,&newFileTime,&newFileTime);
	CloseHandle(hFile);
    
	return bVal;
#else
			//preserve timestamps
	struct utimbuf utimbuf;
	utimbuf.actime = jetzte.value;
	utimbuf.modtime = jetzte.value;
	if (utime (filename.toLatin1().data(), &utimbuf) != 0) {
		return false;
	}

#endif
	
	return true;
}

QString rrAddStringToFileName(QString fileName, const QString &insert)
{
    int p=(fileName.lastIndexOf('.'));
    if ((p>0) && (p>fileName.lastIndexOf(PD))) {
        fileName.insert(p,insert);
    } else fileName.append(insert);
    return fileName;
}

QString rrPathResolve(QString fileName)
{
    rrChar PDl;
    if (fileName.contains('\\')) PDl='\\';
    else PDl='/';
    QString pdLpp=QString("..")+PDl;
    if (!fileName.contains(pdLpp)) return fileName;
    QString firstp= fileName.left(fileName.indexOf(pdLpp));
    fileName.remove(0,fileName.indexOf(pdLpp));
    while (fileName.startsWith(pdLpp)) {
        fileName.remove(0,3);
        firstp=rrGetDirName(firstp,PDl);
    }
    fileName=firstp+fileName;
    return fileName;
}




QString rrWriteBufferToFile(QString fileName, quint8 * buffer, qint64 buffersize )
{
		FILE *outFile;
	#ifdef RR_OS_WIN
		fopen_s(&outFile,fileName.toLatin1().data(), "wb");
	#else
		outFile = fopen(fileName.toLatin1().data(), "wb");
	#endif
		if (!(outFile)) {
			return QString("Unable to write/open file: "+rrLastOSError());
		}
		if (buffersize>0) {
			qint64 chunkSize=4*1024*1024; //4mb chunks;
			size_t writ;
			qint64 writeLeft= buffersize;
			quint8 * buf=buffer;
			do  {
				size_t toWrite;
				if (writeLeft<chunkSize) toWrite=writeLeft; else toWrite=chunkSize;
				writ=fwrite(buf, toWrite,1, outFile);
				if (writ!=1) {
					fclose(outFile);
					return QString("Unable to write %1b (%2/%3 done): %4").arg(toWrite).arg(buffersize-writeLeft).arg(buffersize).arg(rrLastOSError());
				}
				writeLeft-= chunkSize;
				buf= &buf[chunkSize];
			} while (writeLeft>0);
		}
		fclose(outFile);
		return QString();
}


QString	rrDeleteFile(const QString &filename)
{
#ifdef disallowDeleteFiles
    printf("Command to delete file '%s'. Skipped.",filename.toLatin1().data());
    return QString("Command to delete file '%1'. Skipped.").arg(filename);
#endif
    if (!rrFileExists(filename)) return QString();

#ifdef RR_OS_WIN
    SetFileAttributesW((wchar_t*) filename.utf16(),FILE_ATTRIBUTE_NORMAL);
    if (!DeleteFileW((wchar_t*) filename.utf16()))
#else
	  if (unlink(filename.toLatin1().data())!=0)
#endif
		{
			return QString("Unable to delete file, %1.").arg(rrLastOSError());
		}

	return QString();
}


bool rrCreateFolder(const QString &folderName, bool createParentfolder)
{
#ifdef RR_OS_WIN
	if (folderName.size()<=3) return true; 
#else
	if (folderName.size()<=1) return true; 
#endif
	if (rrDirectoryExists(folderName)) return true;
	if (createParentfolder) {
		QString parentfolder=rrGetDirName(folderName);
		if (parentfolder==folderName) return false;
		if (!rrCreateFolder(parentfolder,true)) return false;
	} 
#ifdef RR_OS_WIN
	return CreateDirectoryW(	(wchar_t*) folderName.utf16(),0);
#else
	return (mkdir(folderName.toLatin1().data(), 0777) == 0);
#endif
}

bool rrRenameFile(const QString &oldFilename,const QString &newFilename, bool overwrite)
{
	if (rrFileExists(newFilename)) {
		if (!overwrite) return true;
		if (!rrDeleteFile(newFilename).isEmpty()) return false;
	}
	if (!rrFileExists(oldFilename)) 
		return false;
	bool sucess=false;
#ifdef RR_OS_WIN
	sucess=(MoveFileW((wchar_t *) oldFilename.utf16(),(wchar_t *) newFilename.utf16()) != 0);
#else
	sucess=(::rename(oldFilename.toLatin1().data(),newFilename.toLatin1().data()) == 0);
#endif
	/*qint64 size1,size2;
	if (sucess && rrFileExists(oldFilename,NULL,&size1) && rrFileExists(newFilename,NULL,&size2) && (size1==size2)) {
		//rrDeleteFile(newFilename);
	}*/
	return sucess;
}



#else  //QTCore


bool rrSetFileTime(const _rrString8_500 &filename, _rrTime * tim)
{
	_rrTime jetzte;

	if (tim != NULL) jetzte=*tim;
	else jetzte.setCurrentTime();

#ifdef RR_OS_WIN
	FILETIME newFileTime;
	time_t t;
	t=jetzte.value;

	timeToFileTime(t,&newFileTime);

	HANDLE hFile = CreateFileA(filename.value,
        FILE_WRITE_ATTRIBUTES,FILE_SHARE_READ|FILE_SHARE_WRITE,
        NULL,
        OPEN_EXISTING,
        FILE_FLAG_NO_BUFFERING,
        NULL);

	if(hFile == INVALID_HANDLE_VALUE)
		return false;

    BOOL bVal = SetFileTime(hFile,&newFileTime,&newFileTime,&newFileTime);
	CloseHandle(hFile);
    
	return (bVal!=0);
#else
			//preserve timestamps
	struct utimbuf utimbuf;
	utimbuf.actime = jetzte.value;
	utimbuf.modtime = jetzte.value;
	if (utime (filename.value, &utimbuf) != 0) {
		return false;
	}

#endif
	
	return true;
}



bool rrDeleteFile(const _rrString8_500 &filename)
{
#ifdef disallowDeleteFiles
    printf("Command to delete file '%s'. Skipped.",filename.value);
    return false;
#endif

  struct stat stFileInfo;
  if(stat(filename.value,&stFileInfo) != 0) { //file does not exist
	  return true;
  }
#ifdef RR_OS_WIN
  SetFileAttributesA(filename.value,FILE_ATTRIBUTE_NORMAL);
  if (!DeleteFileA(filename.value))
#else
	  if (unlink(filename.value)!=0)
#endif
		{
			return false;
		}

	return true;
}


bool rrRenameFile(const _rrString8_500 &oldFilename,const _rrString8_500 &newFilename, bool overwrite)
{
	if (rrFileExists(newFilename)) {
		if (!overwrite) return true;
		if (!rrDeleteFile(newFilename)) return false;
	//	if (!rrDeleteFile(_rrString250(newFilename.value)).isEmpty()) return false;
	}
	if (!rrFileExists(oldFilename)) 
		return false;
	bool sucess=false;
#ifdef RR_OS_WIN
	sucess=(MoveFileA(oldFilename.value,newFilename.value) != 0);
#else
	sucess=(::rename(oldFilename.value,newFilename.value) == 0);
#endif
	/*qint64 size1,size2;
	if (sucess && rrFileExists(oldFilename,NULL,&size1) && rrFileExists(newFilename,NULL,&size2) && (size1==size2)) {
		rrDeleteFile(newFilename);
	}*/
	return sucess;
}


bool rrCreateFolder(const _rrString8_500 &folderName, bool createParentfolder)
{
#ifdef RR_OS_WIN
	if (folderName.length<=3) return true; 
#else
	if (folderName.length<=1) return true; 
#endif
	if (rrDirectoryExists(folderName)) return true;
	if (createParentfolder) {
		_rrString8_500 parentfolder=rrGetDirName(folderName);
		if (parentfolder==folderName) return false;
		if (!rrCreateFolder(parentfolder,true)) return false;
	} 
#ifdef RR_OS_WIN
	return (CreateDirectoryA(	folderName.value,0)!=0);
#else
	return (mkdir(folderName.value, 0777) == 0);
#endif
}


#endif //QTcore


#ifdef RR_OS_WIN
void timeToFileTime( time_t t, LPFILETIME pft )
{
    LONGLONG ll = UInt32x32To64(t, 10000000) + 116444736000000000;
    pft->dwLowDateTime = (DWORD) (ll & 0xFFFFFFFF);
    pft->dwHighDateTime = ll >>32;
}

void fileTimeToTime( _rrTime &t, LPFILETIME pft )
{
	t.value =pft->dwHighDateTime;
	t.value=t.value<< 32;
	t.value+=pft->dwLowDateTime;
	t.value/=10000000;
}
#endif //windows


#endif //plugin





#if defined(QT_CORE_LIB)
bool rrIsRootpath(const QString &path)
{
#ifdef RR_OS_WIN
	if (path.length()<=3) return true; // C:/
	if (path.at(1)==':') {
		return false;
	} else {
		if (path.contains('/')) {
			int pos=path.indexOf('/',2); // we got  //, so search for //FILESERVER/
			if (pos<0) return true;      // it is //FILESERVER
			pos=path.indexOf('/',pos+1); //  search for //FILESERVER/share/
			if (pos<0) return true;		 //it is //FILESERVER/share
										//we got //FILESERVER/share/
			return (path.length()==pos+1);
		} else {
			int pos=path.indexOf('\\',2); // we got  //, so search for //FILESERVER/
			if (pos<0) return true;      // it is //FILESERVER
			pos=path.indexOf('\\',pos+1); //  search for //FILESERVER/share/
			if (pos<0) return true;		 //it is //FILESERVER/share
										//we got //FILESERVER/share/
			return (path.length()==pos+1);
		}
	}
#else 
	return (path.length()<=1);
#endif
	return false;
}


bool rrDirectoryExists(QString strDirname)
{
    if (strDirname.length()<3) return false;
    if (strDirname.at(strDirname.length()-1)==PD) {
		strDirname.truncate(strDirname.length()-1);
	}
#ifdef RR_OS_WIN
	DWORD fileAttrib = GetFileAttributesW((wchar_t*) strDirname.utf16());
	return ((fileAttrib != INVALID_FILE_ATTRIBUTES) && ((fileAttrib & FILE_ATTRIBUTE_DIRECTORY)>0));
#else
	struct stat status;
	return ((stat( strDirname.toLatin1().data(), &status ) ==0) && ( status.st_mode & S_IFDIR ));
#endif
}

#endif //QT_CORE_LIB




bool rrDirectoryExists(_rrString8_200 strDirname)
{
    if (strDirname.length<3) return false;
    if (strDirname.value[strDirname.length-1]==PD) {
		strDirname.value[strDirname.length-1]=0;
	}
#ifdef RR_OS_WIN
	DWORD fileAttrib = GetFileAttributesA(strDirname.value);
	return ((fileAttrib != INVALID_FILE_ATTRIBUTES) && ((fileAttrib & FILE_ATTRIBUTE_DIRECTORY)>0));
#else
	struct stat status;
    return ((stat( strDirname.value, &status ) ==0) && ( status.st_mode & S_IFDIR ));
#endif
}


bool rrDirectoryExists(_rrString8_250 strDirname)
{
    if (strDirname.length<3) return false;
    if (strDirname.value[strDirname.length-1]==PD) {
		strDirname.value[strDirname.length-1]=0;
	}
#ifdef RR_OS_WIN
	DWORD fileAttrib = GetFileAttributesA(strDirname.value);
	return ((fileAttrib != INVALID_FILE_ATTRIBUTES) && ((fileAttrib & FILE_ATTRIBUTE_DIRECTORY)>0));
#else
	struct stat status;
    return ((stat( strDirname.value, &status ) ==0) && ( status.st_mode & S_IFDIR ));
#endif
}


bool rrDirectoryExists(_rrString500 strDirname)
{
	if (strDirname.length<3) return false;
	if (strDirname.value[strDirname.length-1]==PD) {
		strDirname.setLength(strDirname.length-1);
	}
#ifdef RR_OS_WIN
	DWORD fileAttrib = GetFileAttributesW(strDirname.value);
	return ((fileAttrib != INVALID_FILE_ATTRIBUTES) && ((fileAttrib & FILE_ATTRIBUTE_DIRECTORY)>0));
#else
	struct stat status;
	return ((stat( strDirname.to_rrString8_250().value, &status ) ==0) && ( status.st_mode & S_IFDIR ));
#endif
}


bool rrDirectoryExists(_rrString8_500 strDirname)
{
    if (strDirname.length<3) return false;
    if (strDirname.value[strDirname.length-1]==PD) {
		strDirname.value[strDirname.length-1]=0;
	}
#ifdef RR_OS_WIN
	DWORD fileAttrib = GetFileAttributesA(strDirname.value);
	return ((fileAttrib != INVALID_FILE_ATTRIBUTES) && ((fileAttrib & FILE_ATTRIBUTE_DIRECTORY)>0));
#else
	struct stat status;
    return ((stat( strDirname.value, &status ) ==0) && ( status.st_mode & S_IFDIR ));
#endif
}


bool rrDirectoryExists(char * strDirname)
{
	return rrDirectoryExists((_rrString8_500) strDirname);
}


_rrString100  rrGetFileName(const _rrString500 &file)
{
    _rrString100 ret;
    int p=file.lastIndexOf(PD);
    if (p>=0) {
        ret.add(&file.value[p+1],file.length-p-1);
    } else ret=file.value;
    return ret;
}



_rrString100  rrGetFileName(const _rrString250 &file)
{
	_rrString100 ret;
	int p=file.lastIndexOf(PD);
	if (p>=0) {
		ret.add(&file.value[p+1],file.length-p-1);
	} else ret=file.value;
	return ret;
}


_rrString8_100 rrGetFileName(const _rrString8_200 &file)
{
	_rrString8_100 ret;
	int p=file.lastIndexOf(PD);
	if (p>=0) {
		ret.add(&file.value[p+1],file.length-p-1);
	} else ret=file.value;

	return ret;
}


_rrString8_100 rrGetFileName(const _rrString8_250 &file)
{
	_rrString8_100 ret;
	int p=file.lastIndexOf(PD);
	if (p>=0) {
		ret.add(&file.value[p+1],file.length-p-1);
	} else ret=file.value;

	return ret;
}

_rrString8_100 rrGetFileName(const _rrString8_500 &file)
{
	_rrString8_100 ret;
	int p=file.lastIndexOf(PD);
	if (p>=0) {
		ret.add(&file.value[p+1],file.length-p-1);
	} else ret=file.value;

	return ret;
}

#if defined(QT_CORE_LIB)
QString rrGetFileName(QString file,rrChar pd)
{
	int p=file.lastIndexOf(pd);
	if (p>1) {
		file.remove(0,p+1);
	}
	return file;
}

QString rrGetFileNameAutoPD(QString dir)
{
    rrChar pd;
    if (dir.contains('/')) pd='/'; else pd='\\';
    return rrGetFileName(dir,pd);
}

QString rrGetFileNameBase(QString file,rrChar pd)
{
	int p=file.lastIndexOf(pd);
	if (p>1) {
		file.remove(0,p+1);
	}
	p=file.lastIndexOf('.');
	if (p>1) {
		file.truncate(p);
	}
	return file;
}


QString rrGetFileNameExtention(QString file)
{
	int p=file.lastIndexOf('.');
	if (p>1) {
		file.remove(0,p);
	}
	return file;
}

#endif //QT_CORE_LIB



_rrString8_500 rrGetDirName(_rrString8_500 dir)
{
	if (dir.length<3) return dir;
	if (dir.value[dir.length-1]==PD) {
		dir.setLength(dir.length-1);
	}
	bool isUNC;
	isUNC= (dir.value[1]==PD);
	int p=dir.lastIndexOf(PD);
	if (p>1) {
		if ((!isUNC) || (dir.lastIndexOf(PD,p-1)>1))
			dir.setLength(dir.lastIndexOf(PD));
	}
	dir+=PD;
	return dir;
}



_rrString8_250 rrGetDirName(_rrString8_250 dir)
{
	if (dir.length<3) return dir;
	if (dir.value[dir.length-1]==PD) {
		dir.setLength(dir.length-1);
	}
	bool isUNC;
	isUNC= (dir.value[1]==PD);
	int p=dir.lastIndexOf(PD);
	if (p>1) {
		if ((!isUNC) || (dir.lastIndexOf(PD,p-1)>1))
			dir.setLength(dir.lastIndexOf(PD));
	}
	dir+=PD;
	return dir;
}



_rrString250 rrGetDirName(_rrString250 dir)
{
	if (dir.length<3) return dir;
	if (dir.value[dir.length-1]==PD) {
		dir.setLength(dir.length-1);
	}
	bool isUNC;
	isUNC= (dir.value[1]==PD);
	int p=dir.lastIndexOf(PD);
	if (p>1) {
		if ((!isUNC) || (dir.lastIndexOf(PD,p-1)>1))
			dir.setLength(dir.lastIndexOf(PD));
	}
	dir+=PD;
	return dir;
}



_rrString500 rrGetDirName(_rrString500 dir)
{
	if (dir.length<3) return dir;
	if (dir.value[dir.length-1]==PD) {
		dir.setLength(dir.length-1);
	}
	bool isUNC;
	isUNC= (dir.value[1]==PD);
	int p=dir.lastIndexOf(PD);
	if (p>1) {
		if ((!isUNC) || (dir.lastIndexOf(PD,p-1)>1))
			dir.setLength(dir.lastIndexOf(PD));
	}
	dir+=PD;
	return dir;
}


_rrString8_200 rrGetDirName(_rrString8_200 dir)
{
	if (dir.length<3) return dir;
	if (dir.value[dir.length-1]==PD) {
		dir.setLength(dir.length-1);
	}
	bool isUNC;
	isUNC= (dir.value[1]==PD);
	int p=dir.lastIndexOf(PD);
	if (p>1) {
		if ((!isUNC) || (dir.lastIndexOf(PD,p-1)>1))
			dir.setLength(dir.lastIndexOf(PD));
	}
	dir+=PD;
	return dir;
}





#if defined(QT_CORE_LIB)


QString rrGetDirName(QString dir,rrChar pd)
{ 
	if (dir.size()<3) return dir;
	if (dir.endsWith(pd)) {
		dir.resize(dir.size()-1);
	}
	bool isUNC;
	isUNC= (dir.at(1)==pd);
	int p=dir.lastIndexOf(pd);
	if (p>1) {
		if ((!isUNC) || (dir.lastIndexOf(pd,p-1)>1))
			dir.resize(dir.lastIndexOf(pd));
		dir+=pd;
	} else {
		dir="";
	}
	
	return dir;
}

QString rrGetDirNameAutoPD(QString dir)
{ 
    rrChar pd=PD;
    if (dir.contains('/')) pd='/';
    else pd='\\';
	if (dir.size()<3) return dir;
	if (dir.endsWith(pd)) {
		dir.resize(dir.size()-1);
	}
	bool isUNC;
	isUNC= (dir.at(1)==pd);
	int p=dir.lastIndexOf(pd);
	if (p>1) {
		if ((!isUNC) || (dir.lastIndexOf(pd,p-1)>1))
			dir.resize(dir.lastIndexOf(pd));
		dir+=pd;
	} else {
		dir="";
	}
	
	return dir;
}

bool isRelativePath(QString inString)
{
	if (inString.size()<3) return true;
	if (inString.at(0)==PD) return false;
	if ((inString.at(1)==':') && (inString.at(2)==PD))  return false;
	if (inString.startsWith("<Database>",Qt::CaseInsensitive)) return false;
	return true;
}

/*bool	rrMakePath(QString strDirname)
{
	QDir Dirr(strDirname);
	return Dirr.mkpath(Dirr.absolutePath());
}*/

QString rrRemoveIllegalCharFromHtmlFile(QString inString)
{
	inString.remove('!');
	inString.remove('&');
	inString.remove('$');
    inString.remove('\'');
	for (int i=0; i<inString.size(); i++) {
		if (inString.at(i)>128)  inString.replace(i,1,"_");
	}
	return rrRemoveIllegalCharFromFile(inString);
}
QString rrRemoveIllegalCharFromHtmlDir(QString inString)
{
	inString.remove('!');
	inString.remove('&');
	inString.remove('$');
    inString.remove('\'');
	for (int i=0; i<inString.size(); i++) {
		if (inString.at(i)>128)  inString.replace(i,1,"_");
	}
	return rrRemoveIllegalCharFromDir(inString);
}


QString rrRemoveIllegalCharFromDir(QString inString,bool allowspaces,const bool &allowFN)
{
#ifdef RR_OS_WIN
	inString.remove('/');
	while (inString.lastIndexOf("\\\\")>2) inString.remove(inString.lastIndexOf("\\\\"),1);
	inString=inString.replace(" \\","\\").replace("\\ ","\\");
#else
	inString.remove('\\');
	while (inString.lastIndexOf("//")>2) inString.remove(inString.lastIndexOf("//"),1);
	inString=inString.replace(" /","/").replace("/ ","/");
#endif
	inString.remove('\n');
	inString.remove('\r');
	inString.remove('\t');
	inString.remove('|');
	if (!allowspaces) inString.remove(' ');
	while (inString.lastIndexOf(':')>2) inString.remove(inString.lastIndexOf(':'),1);
	//inString.remove(':');
	inString.remove(';');
	inString.remove('#');
	//inString.remove('.');
//	inString.remove(')');
//	inString.remove('(');
	inString.remove('}');
	inString.remove('{');
	inString.remove('"');
    //inString.remove('\'');
	inString.remove('@');
	//inString.remove('%');
	inString.remove('=');
	inString.remove('?');
	inString.remove('`');
	//inString.remove('+');
	inString.remove('~');
	inString.remove('*');
	if (allowFN) inString.replace("<FN>","*FN*").replace("<FN1>","*FN1*").replace("<FN2>","*FN2*").replace("<FN3>","*FN3*").replace("<FN4>","*FN4*").replace("<FN5>","*FN5*").replace("<FN6>","*FN6*").replace("<FN7>","*FN7*");
	inString.remove('>');
	inString.remove('<');
	if (allowFN) inString.replace("*FN*","<FN>").replace("*FN1*","<FN1>").replace("*FN2*","<FN2>").replace("*FN3*","<FN3>").replace("*FN4*","<FN4>").replace("*FN5*","<FN5>").replace("*FN6*","<FN6>").replace("*FN7*","<FN7>");
	inString.remove('^');

	for (int i=0; i<inString.size(); i++) {
		if ((inString.at(i)<32)) {
			inString.remove(i,1);
			i--;
		}
	}


	return inString;
}



QString rrRemoveIllegalCharFromDir(QString inString,bool allowspaces,const bool &allowFN,bool allowGreaterSmaller )
{
#ifdef RR_OS_WIN
	inString.remove('/');
	while (inString.lastIndexOf("\\\\")>2) inString.remove(inString.lastIndexOf("\\\\"),1);
	inString=inString.replace(" \\","\\").replace("\\ ","\\");
#else
	inString.remove('\\');
	while (inString.lastIndexOf("//")>2) inString.remove(inString.lastIndexOf("//"),1);
	inString=inString.replace(" /","/").replace("/ ","/");
#endif
	inString.remove('\n');
	inString.remove('\r');
	inString.remove('\t');
	inString.remove('|');
	if (!allowspaces) inString.remove(' ');
	while (inString.lastIndexOf(':')>2) inString.remove(inString.lastIndexOf(':'),1);
	//inString.remove(':');
	inString.remove(';');
	inString.remove('#');
	//inString.remove('.');
//	inString.remove(')');
//	inString.remove('(');
	inString.remove('}');
	inString.remove('{');
	inString.remove('"');
    //inString.remove('\'');
	//inString.remove('@');
	//inString.remove('%');
	inString.remove('=');
	inString.remove('?');
	inString.remove('`');
	//inString.remove('+');
	inString.remove('~');
	inString.remove('*');
	if (!allowGreaterSmaller) {
		if (allowFN) inString.replace("<FN>","*FN*").replace("<FN1>","*FN1*").replace("<FN2>","*FN2*").replace("<FN3>","*FN3*").replace("<FN4>","*FN4*").replace("<FN5>","*FN5*").replace("<FN6>","*FN6*").replace("<FN7>","*FN7*");
		inString.remove('>');
		inString.remove('<');
		if (allowFN) inString.replace("*FN*","<FN>").replace("*FN1*","<FN1>").replace("*FN2*","<FN2>").replace("*FN3*","<FN3>").replace("*FN4*","<FN4>").replace("*FN5*","<FN5>").replace("*FN6*","<FN6>").replace("*FN7*","<FN7>");
	}
	inString.remove('^');

	for (int i=0; i<inString.size(); i++) {
		if ((inString.at(i)<32) ) {
			inString.remove(i,1);
			i--;
		}
	}


	return inString;
}


QString rrRemoveIllegalCharFromFile(QString inString,bool allowspaces,const bool &allowFN)
{
	inString.remove('\n');
	inString.remove('\r');
	inString.remove('\t');
	inString.remove('\\');
	inString.remove('/');
	inString.remove('|');
	if (!allowspaces) inString.remove(' ');
	inString.replace(':','_');
	inString.remove(';');
	inString.remove('#');
	//inString.remove('.');
//	inString.remove(')');
//	inString.remove('(');
	inString.remove('}');
	inString.remove('{');
	inString.remove('"');
	//inString.remove('@');
//	inString.remove('!');
	//inString.remove('%');
//	inString.remove('&');
	inString.remove('=');
	inString.remove('?');
	inString.remove('`');
	//inString.remove('+');
	inString.remove('~');
	inString.remove('*');
	if (allowFN) inString.replace("<FN>","*FN*").replace("<FN1>","*FN1*").replace("<FN2>","*FN2*").replace("<FN3>","*FN3*").replace("<FN4>","*FN4*").replace("<FN5>","*FN5*").replace("<FN6>","*FN6*").replace("<FN7>","*FN7*");
	inString.remove('>');
	inString.remove('<');
	if (allowFN) inString.replace("*FN*","<FN>").replace("*FN1*","<FN1>").replace("*FN2*","<FN2>").replace("*FN3*","<FN3>").replace("*FN4*","<FN4>").replace("*FN5*","<FN5>").replace("*FN6*","<FN6>").replace("*FN7*","<FN7>");
	inString.remove('^');
	for (int i=0; i<inString.size(); i++) {
		if ((inString.at(i)<32)) {
			inString.remove(i,1);
			i--;
		}
	}

	return inString;
}





QString rrConvertPDToOS(const QString &inString)
{
	QString helper;
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


QString rrConvertPDToOS(const QString &inString,_rrOS ToOS)
{
	QString helper;
	helper=inString;
	switch (ToOS) {
		case rrosWindows:
			helper.replace(PD_LX,PD_WIN);
			break;
		case rrosLinux:
			helper.replace(PD_WIN,PD_LX);
			break;
		case rrosMac:
			helper.replace(PD_WIN,PD_LX);
			break;
		default:
#ifdef RR_OS_WIN
			helper.replace(PD_LX,PD_WIN);
#elif defined RR_OS_MAC
                        helper.replace(PD_WIN,PD_LX);
#else
			helper.replace(PD_WIN,PD_LX);
#endif
			break;
	}
	return helper;
}


#ifndef rrPlugin
                     #if ((defined defrrClientconsole) || (defined defrrClient))
                     #endif
        #if ((defined defrrClientconsole) || (defined defrrClient))
        #endif
        #if ((defined defrrClientconsole) || (defined defrrClient))
        #endif
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












