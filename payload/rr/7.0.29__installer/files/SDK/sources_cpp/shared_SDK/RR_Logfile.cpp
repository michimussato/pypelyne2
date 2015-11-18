#include "RR_Logfile.h"
#include <fstream>
#include "../shared_SDK/RR_files_SDK.h"

#ifndef rrPlugin
#endif

#ifdef  QT_CORE_LIB
#include <QMutex>
#endif

_rrLogfile::_rrLogfile()
{
    m_logFilename="";
    m_logFilename_local="";
    m_alwaysWriteLocal=false;

    m_maxLogfileSize=1*1024*1024;
    p_bufferAllocatedSize=100*1024;
    p_cutStartIfMaxReached=true;

	p_buf = (char*) calloc(1,p_bufferAllocatedSize+1);
    p_bufferUsage=0;
    p_bufferLocalWrittenUntil=0;
    m_maxTimeFlush=60;
    m_maxSizeFlush=1*1024;
    p_lastLogWritten.value=0;
    p_lastLogWriteFailed.value=0;
    p_mutexBuffer = new (QMutex);
    m_addLineEnd=true;
}

_rrLogfile::_rrLogfile(const _rrString8_500 &inlogFilename, const _rrString8_500 &inlogFilename_local,const int &inmaxFileSize,bool inalwaysWriteLocal, bool incutStartIfMaxReached)
{
    m_logFilename=inlogFilename;
    m_logFilename_local=inlogFilename_local;
    m_alwaysWriteLocal=inalwaysWriteLocal;

    m_maxLogfileSize=inmaxFileSize;
    p_bufferAllocatedSize=100*1024;
    p_cutStartIfMaxReached=incutStartIfMaxReached;

	p_buf = (char*) calloc(1,p_bufferAllocatedSize+1);
    p_bufferUsage=0;
    p_bufferLocalWrittenUntil=0;
    m_maxTimeFlush=60;
    m_maxSizeFlush=1*1024;
    p_lastLogWritten.value=0;
    p_lastLogWriteFailed.value=0;
    p_mutexBuffer = new (QMutex);
    m_addLineEnd=true;
}


_rrLogfile::~_rrLogfile()
{
    flush();
    rrDeleteAlloc(p_buf);
    rrDeletePointer(p_mutexBuffer);
}

void _rrLogfile::addLog(char const * const newLine, const int &size)
{
    if (!p_mutexBuffer->tryLock(5000)) return;
    addLog_p(newLine,size,true);
    p_mutexBuffer->unlock();
}

void _rrLogfile::addLog(const _rrString8_250 &newLine)
{
    addLog(newLine.value, newLine.length);
}

#ifdef QT_CORE_LIB
void  _rrLogfile::addLog(const QString &newLine)
{
    addLog(newLine.toLatin1().data(), newLine.length());
}

#endif



void _rrLogfile::addLog_p(char const * const newLine,  int size,const bool &writeToFile)
{
    //printf("addLog_p: %s\n",newLine);
    if (size>0) {
        if (p_bufferUsage+size+2 > p_bufferAllocatedSize) {
            //printf("addLog_p: %d %d\n",bufferUsage,bufferAllocatedSize);
            if (writeToFile) flush_p();
            if (p_bufferUsage+size+2 > p_bufferAllocatedSize) {
                size=p_bufferAllocatedSize-p_bufferUsage-3;
            }
        } 
    
        //printf("addLog_p 2 \n");
        memcpy(&p_buf[p_bufferUsage],newLine, size);
        p_bufferUsage+=size;
        if (m_addLineEnd) {
            #ifdef RR_OS_WIN
            p_buf[p_bufferUsage]='\r';
            p_bufferUsage++;
            #endif
            p_buf[p_bufferUsage]='\n';
            p_bufferUsage++;
        }
    }
    

    if (!writeToFile) return;
    //printf("addLog_p 3 \n");
    if ( (p_bufferUsage > m_maxSizeFlush) || m_maxTimeFlush<=0 || p_lastLogWritten.waitTimeIsOver(m_maxTimeFlush,true)) flush_p();
}




void _rrLogfile::flush()
{
    if (!p_mutexBuffer->tryLock(5000)) return;
    flush_p();
    p_mutexBuffer->unlock();
}


void _rrLogfile::flush_p()
{
    //printf("flush_p \n");
    if (writetoLogFile(m_logFilename, true, true)) {
        if (m_alwaysWriteLocal && !m_logFilename_local.isEmpty()) {
            writetoLogFile(m_logFilename_local, false, false, p_bufferLocalWrittenUntil);
            p_bufferLocalWrittenUntil=0;
        }
        p_bufferUsage=0;
    } else {
        //writetoLogFile failed
        if (!m_logFilename_local.isEmpty()) {
            if (writetoLogFile(m_logFilename_local, false, false, p_bufferLocalWrittenUntil)) {
                p_bufferLocalWrittenUntil=p_bufferUsage;
            }
        }
    }
}


void _rrLogfile::trimLogFile(_rrString8_500 fileName, qint64 curFileSize)
{
    int newFileSize= m_maxLogfileSize/2;
    char * tmpbuf = (char*) calloc(1,newFileSize+1);
    if (tmpbuf==NULL) return;
	std::ios_base::openmode openMode=std::ofstream::in |std::ofstream::binary;
	std::fstream myfile(fileName.value, openMode);
    if (!myfile.is_open()) {
        rrDeleteAlloc(tmpbuf);
        return;
    }
    myfile.seekg(curFileSize-newFileSize);
    myfile.read(tmpbuf, newFileSize);
    myfile.close();

    openMode=std::ofstream::out |std::ofstream::binary;
	myfile.open(fileName.value, openMode);
    if (!myfile.is_open()) {
        rrDeleteAlloc(tmpbuf);
        return;
    }
    myfile.write(tmpbuf, newFileSize);
    myfile.flush();
    myfile.close();
    rrDeleteAlloc(tmpbuf);
}



void _rrLogfile::addSelfError(const _rrString8_500 &errMsg, const bool &addErrorCode)
{
    //printf("addSelfError \n");
    _rrString8_500 msg=_rrTime(true).asRR8String().value;
    msg+=" LOGFILE ERROR: ";
    msg+=errMsg;
    if (addErrorCode) {
        msg+="  ";
        msg+=rrLastOSError8().value;
    }
    addLog_p(msg.value,msg.length, false);
}



bool _rrLogfile::writetoLogFile(_rrString8_500 fileName,  bool setlastLogTime, bool mainLog, int bufStartAt)
{
    //printf("writetoLogFile %s\n",fileName.value);
    if (fileName.isEmpty()) return false;
    if (p_bufferUsage-bufStartAt<=0) return true;

    qint64 fSize;
    bool fExist= rrFileExists(fileName,NULL,&fSize);
#ifndef rrPlugin
#endif

    if (setlastLogTime) p_lastLogWritten.setCurrentTime();
	std::ios_base::openmode openMode=std::ofstream::app | std::ofstream::binary;
	std::ofstream myfile;
    if (!fExist) {
        myfile.open(fileName.value, openMode);
        if (myfile.is_open()) {
            #ifndef rrPlugin
            #endif
        } else {
            if (p_lastLogWriteFailed.value==0) {
                if (mainLog) {
					p_lastLogWriteFailed.setCurrentTime();
					_rrString8_500 msg=rrGetDirName(fileName);
					if (rrDirectoryExists(msg)) {
	                    msg="Log folder was found, but unable to write logfile '";
					} else {
	                    msg="Log folder was NOT found, unable to write logfile '";
					}
					msg+=fileName;
					msg+="'.";
					addSelfError(msg);
				}
            }
            return false;
        }
    } else {
        if (fSize>m_maxLogfileSize) {
            if (p_cutStartIfMaxReached) {
                trimLogFile(fileName,fSize);
            }
            else return true; //max file size reached, stop adding stuff
        }
        myfile.open(fileName.value, openMode);
        if (myfile.is_open()) {
            
        } else {
            if (p_lastLogWriteFailed.value==0) {
                if (mainLog) {
					p_lastLogWriteFailed.setCurrentTime();
					_rrString8_500 msg="Unable to write to logfile '";
					msg+=fileName;
					msg+="'.";
					addSelfError(msg);
				}
            }
            myfile.close();
            return false;
        }
    }

    if (mainLog && p_lastLogWriteFailed.value!=0) {
        addSelfError("Logfile is working again.",false);
        p_lastLogWriteFailed.value=0;
    }

    int wsize= p_bufferUsage-bufStartAt;
    myfile.write(&p_buf[bufStartAt], wsize );
    myfile.close();


    #ifndef rrPlugin
    #endif

    return true;
}
