#ifndef RR_LogFile_H
#define RR_LogFile_H

#include "../shared_SDK/RR_DataTypes_other_SDK.h"


class QMutex;
class QString;



class _rrLogfile {
    RR_DISABLE_COPY(_rrLogfile) //buffer!!
public:
    _rrLogfile();
    _rrLogfile(const _rrString8_500 &m_logFilename, const _rrString8_500 &m_logFilename_local="" ,const int &maxFileSize=1*1024*1024,bool m_alwaysWriteLocal=false,bool p_cutStartIfMaxReached=true);
    ~_rrLogfile();
    void addLog(char const * const newLine, const int &size);
    void addLog(const _rrString8_250 &newLine);
    void addLog(const QString &newLine);
    int  bufferUsage() {return p_bufferUsage;};
    void flush();


    _rrString8_500 m_logFilename;
    _rrString8_500 m_logFilename_local;
    bool    m_alwaysWriteLocal; //otherwise only if main logfile is not accessible
    int     m_maxLogfileSize;
    int     m_maxTimeFlush;			//limit to decide when to write the memory buffer into a file
    int     m_maxSizeFlush;			//limit to decide when to write the memory buffer into a file
    int     m_maxBufferUsageFlush;	//limit to decide when to write the memory buffer into a file
    bool    m_addLineEnd;
	char *  buf() {return p_buf;};
    QMutex  * mutexBuffer() {return p_mutexBuffer;};


private:
    _rrTime p_lastLogWritten;
    _rrTime p_lastLogWriteFailed;
    bool    p_cutStartIfMaxReached;
    int     p_bufferAllocatedSize;
    int     p_bufferUsage;
    int     p_bufferLocalWrittenUntil;
    char *  p_buf;
    QMutex  * p_mutexBuffer;



    void trimLogFile(_rrString8_500 fileName, qint64 curFileSize);
    bool writetoLogFile(_rrString8_500 fileName, bool setlastLogTime, bool mainLog, int bufStartAt=0);
    void addSelfError(const _rrString8_500 &errMsg, const bool &addErrorCode=true);
    void addLog_p(char const * const newLine,  int size,const bool &writeToFile=true);
    void flush_p();
};




#endif
