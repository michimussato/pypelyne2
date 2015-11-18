
#include "RR_DataTypes_RR_SDK.h"
#include "RR_MessageBox_SDK.h"
#include "../sharedLib/RR_files_SDK.h"
#include "RR_version_SDK.inc"
#include "RR_Logfile_SDK.h"


#ifndef rrPlugin
#endif


#ifdef QT_CORE_LIB
	#ifndef rrPlugin
		#ifdef RR_OS_WIN
		#endif
	#endif
	//#include <QDir>
	//#include <QMutex>
	#include <QFile>
	#include <QThread>
	#if (!defined rrConsoleApp)
		//#include <QApplication>
	#endif
#endif


#if (!defined RR_OS_WIN)
	//#include <sys/utsname.h>
#endif




#ifndef rrPlugin
#ifdef NetDebugVersion
#endif
#ifdef rrConsoleApp
#endif
#ifdef NetDebugVersion		
#endif
	#ifdef RR_OS_WIN
	#endif
#ifdef RR_OS_WIN
#else
#endif
    #ifdef RRx64
    #else
    #endif
#ifdef RR_OS_MAC
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef RR_OS_WIN
#endif
#ifdef RR_OS_MAC
#endif
#ifdef RR_OS_MAC
#endif
#ifdef RR_OS_WIN
#else
#endif
    #if (defined(defrrServerconsole))
    #endif
#ifdef RR_OS_WIN
#else
#endif
#ifdef NetDebugVersion		
#endif
			#ifndef RR_OS_WIN
			#endif
#else

__RRSDK::~__RRSDK()
{
}

#endif //(!defined rrPlugin) else



#ifdef QT_CORE_LIB
QString rrConvertFileError_localSDK(QFile::FileError err)
{
	switch (err) {
		case QFile::NoError: return "No error occurred";
		case QFile::ReadError : return "An error occurred when reading from the file.";
		case QFile::WriteError : return "An error occurred when writing to the file.";
		case QFile::FatalError : return "A fatal error occurred.";
		case QFile::ResourceError : return "Resource error.";
		case QFile::OpenError : return "The file could not be opened.";
		case QFile::AbortError : return "The operation was aborted.";
		case QFile::TimeOutError : return "A timeout occurred.";
		case QFile::UnspecifiedError : return "An unspecified error occurred.";
		case QFile::RemoveError : return "The file could not be removed.";
		case QFile::RenameError : return "The file could not be renamed.";
		case QFile::PositionError : return "The position in the file could not be changed.";
		case QFile::ResizeError : return "The file could not be resized.";
		case QFile::PermissionsError : return "The file could not be accessed.";
		case QFile::CopyError : return "The file could not be copied.";
		default: return QString("Unknown Error %1").arg(err);
	}
}


void  __RRSDK::logNoUIExecute(int rrLog_level, int flags, const QString &error_msg, const QString &Location)
{
	if (app.noLogUI) return;
    if (rrHasFlag(flags,rrlLogIntoFileOnly)) return;
	QString compMsg;
	formatLogMessage(rrLog_level,flags, error_msg, Location,compMsg);
#ifdef rrConsoleApp
	puts(compMsg.toAscii().data());
#else
	if (app.isConsole) {
		puts(compMsg.toAscii().data());
	} else {
		if (rrHasFlag(flags,rrlNoMessageWindow)) return;
		if (!app.QAppIsInit) return;
		if (app.isService) return;
        if (rrLog_level>=rrlDebugMain)  return;
		
                //QObject ob;
		compMsg.replace(";   ",";");
		compMsg.replace(";  ",";");
		compMsg.replace("; ",";");
		compMsg.replace(';','\n');
		compMsg.replace("()","");
        if (rrLog_level==rrlCritical) 
             rrMessageBox::Critical(NULL,compMsg,"Ok",90,"",NULL,rrHasFlag(flags,rrlMessageBoxAlignLeft));
        else rrMessageBox::Warning(NULL,compMsg,"Ok",90,"",NULL,rrHasFlag(flags,rrlMessageBoxAlignLeft));
	}
#endif
}


void __RRSDK::writeLog(int rrLog_level, int flags, const QString &error_msg, const QString &Location)
{
	if (rrLog_level==rrlCritical) p_criticalErrorOccured=true;
	if ((cfg) && (cfg->iLog_Level_enabled[rrLog_level])) {
		logNoUIExecute(rrLog_level,flags, error_msg, Location);
		logFileWrite(rrLog_level, flags, error_msg, Location);
	}
	
}


void __RRSDK::formatLogMessage(int rrLog_level, int flags, QString error_msg, const QString &Location, QString &Result)
{
	error_msg= rrToRRUTF8(error_msg,false);
	_rrTime tim; 	tim.setCurrentTime();
	Result.clear();
	if (!rrHasFlag(flags,rrlNoTimeDisplay)) {
#ifdef defrrtestFtp
		Result=tim.daytimeAsString()+m_logfileDateSeperator;
#else
		Result=tim.asString()+m_logfileDateSeperator;
#endif
	}

    bool showDebugLocation= (rrLog_level==rrlCritical) || (rrLog_level==rrlError)  || cfg->iLog_Level_enabled[rrlDebugShowLocations];
    bool showStackTrace= (rrLog_level==rrlCritical) || (rrLog_level==rrlError)  || cfg->iLog_Level_enabled[rrlDebugShowStackTrace];
    QString preString;
    if ((error_msg.length()>2) && (error_msg.at(1)=='|')) {
        preString= error_msg.left(2);
        error_msg.remove(0,2);
        if (error_msg.at(0)==' ') error_msg.remove(0,1);
    }


	switch (rrLog_level) {
		case rrlCritical: 
            error_msg="CRF Critical Failure - "+error_msg;  
            break;
		case rrlError:    
            error_msg="ERR "+error_msg; 

            break;
		case rrlWarning:  
            error_msg="WRN "+error_msg; 
            break;
		default: 
            if ((error_msg.length()>3) && (error_msg.at(3)==' ') && (error_msg.at(2).isUpper()) ) {
                //has a 2 letter start like DGB
                //error_msg=error_msg;
            }
            else error_msg="    "+error_msg;
    }

    Result=Result+preString+' '+error_msg;
    if (Result.endsWith('\n')) Result.truncate(Result.length()-1);
    Result.replace("\n","\n                    ");
    if (rrHasFlag(flags,rrlLogNoDebugInfo))  {
        showDebugLocation=false;
        showStackTrace=false;
    }
    if (showDebugLocation) 
        Result+=";;   ("+Location+")"; 
#ifndef rrPlugin
		#ifdef RRx64
		#else
		#endif
#endif


}
#else //QT_CORE_LIB
#endif


void  __RRSDK::logNoUIExecute_noQT(int rrLog_level, int error_ID, const _rrString250 &error_msg, const _rrString250 &Location)
{
	if (app.noLogUI) return;
	if (error_ID & rrlLogIntoFileOnly) return;
	_rrString250 compMsg;
	formatLogMessage_noQT(rrLog_level,error_ID, error_msg, Location,compMsg);
#if (defined(rrConsoleApp) && (!defined(rrPlugin))) 
	_rrString8_250 compMsg8;
	compMsg.toChar(compMsg8.value,compMsg8.ArraySize);
	puts(compMsg8.value);
#else
	if (app.isConsole) {
		_rrString8_250 compMsg8;
		compMsg.toChar(compMsg8.value,compMsg8.ArraySize);
		puts(compMsg8.value);
	} else {
		//without QT we do not have a way to print messages
	}
#endif
}


void __RRSDK::writeLog_noQT(int rrLog_level, int flags, const _rrString250 &error_msg, const _rrString250 &Location)
{
	if (rrLog_level==rrlCritical) p_criticalErrorOccured=true;
	if ((cfg) && (cfg->iLog_Level_enabled[rrLog_level])) {
		logNoUIExecute_noQT(rrLog_level,flags, error_msg, Location);
		//logFileWrite(rrLog_level, flags, error_msg, Location); 
	}
	
}


void __RRSDK::formatLogMessage_noQT(int rrLog_level, int flags, const _rrString250 &error_msg, const _rrString250 &Location, _rrString250 &Result)
{
	
	_rrTime tim; 	tim.setCurrentTime();
	Result.clear();
	if (!rrHasFlag(flags,rrlNoTimeDisplay)) {
		Result=tim.asRR8String().value;
		Result=+";   ";
	}
	switch (rrLog_level) {
#ifndef rrPlugin
#else
		case rrlCritical: Result+="Critical Failure - ";
						  Result+=error_msg;  
						  if ((!rrHasFlag(flags,rrlLogNoDebugInfo)) || (cfg->iLog_Level_enabled[rrlDebugShowLocations] )) 
							  Result+=";;   (";
							  Result+=Location;
							  Result+=");";
							  Result+=app.displayName.value;
							  Result+=rrVersion; 
						  break;
		case rrlError:    Result+="Error - "; Result+=error_msg;  if ((!rrHasFlag(flags,rrlLogNoDebugInfo)) || (cfg->iLog_Level_enabled[rrlDebugShowLocations] )) Result+=";;   ("; Result+=Location; Result+=");"; Result+=app.displayName.value; Result+=rrVersion; break;
		case rrlWarning:  Result+="Warning - "; // NO BREAK, continue
		default: 
			if (((rrLog_level>=rrlDebugMain) || cfg->iLog_Level_enabled[rrlDebugShowLocations]) && (!Location.isEmpty()) && (!rrHasFlag(flags,rrlLogNoDebugInfo))) 
			{Result+=error_msg; Result+=";;   ("; Result+=Location; Result+=")"; }
			else Result+=error_msg;
#endif
		}
}





#ifdef QT_CORE_LIB

void __RRSDK::logFileWriteError(int rrLog_level, int flags, const QString &error_msg, const QString &Location)
{
    if (rrLog_level!=rrlCritical && rrLog_level!=rrlError) return;
    if (app.noLogFile) return;
//    if (!licIsVersion70()) return;

    QString compMsg;
    formatLogMessage(rrLog_level,flags, error_msg, Location,compMsg);
#ifdef RR_OS_WIN
    compMsg+="\r\n";
    compMsg="["+app.machineName+"]\r\n"+compMsg;
#else
    compMsg+='\n';
    compMsg="["+app.machineName+"]\n"+compMsg;
#endif
    m_logFileError->addLog(compMsg);
}

void __RRSDK::logFileWrite(int rrLog_level, int flags, const QString &error_msg, const QString &Location)
{
    if (!cfg->iLog_Level_enabled[rrLog_level]) return;
    if (rrLog_level==rrlCritical || error_msg.contains("Access violation") || error_msg.contains("PAGE_FAULT")  || error_msg.contains("std::bad_alloc:bad allocation")) {
		p_criticalErrorOccured=true;
		app.noLogFile=false;
		m_logFile->m_maxTimeFlush=0;
	}
	if (app.noLogFile)  return;
	//if (flags==rrlLogFileError) return; //Prevent loop from error message written in logFile->flush();_prv

	if (rrLog_level==rrlCritical || rrLog_level==rrlError) {
        logFileWriteError(rrLog_level, flags,error_msg, Location);
	}
    

	try {
		QString compMsg;
		formatLogMessage(rrLog_level,flags, error_msg, Location,compMsg);
        m_logFile->addLog(compMsg);
	}
	catch (...)
	{
	}
}

#endif


bool    & __RRSDK::cfgGetB(const char * name) const
{
	for (int i=0;i<cfg->m_count;i++) {
		if (cfg->params[i].name==name) {
			if (cfg->params[i].type !=rrgCfgBool) {
				return cfg->notFoundB;
			}
			return cfg->params[i].b;
		}
	}
	return cfg->notFoundB;
}

qint16  & __RRSDK::cfgGetI(const char * name) const
{
	for (int i=0;i<cfg->m_count;i++)	{
		if (cfg->params[i].name==name) {
			if (cfg->params[i].type !=rrgCfgInt) {
				return cfg->notFoundI;
			}
			return cfg->params[i].i;
		}
	}
	return cfg->notFoundI;
}

_rrString100 & __RRSDK::cfgGetS(const char * name) const
{
	for (int i=0;i<cfg->m_count;i++) {
		if (cfg->params[i].name==name) {
			if (cfg->params[i].type !=rrgCfgQString) {
				return cfg->notFoundS;
			}
			return cfg->params[i].s;
		}
	}
	return cfg->notFoundS;

}

float   & __RRSDK::cfgGetF(const char * name) const
{
	for (int i=0;i<cfg->m_count;i++) {
		if (cfg->params[i].name==name) {
			if (cfg->params[i].type !=rrgCfgFloat) {
				return cfg->notFoundF;
			}
			return cfg->params[i].f;
		}
	}
	return cfg->notFoundF;
}



bool    & __RRSDK::cfgGetB(const char * name) 
{
	for (int i=0;i<cfg->m_count;i++) {
		if (cfg->params[i].name==name) {
			if (cfg->params[i].type !=rrgCfgBool) {
				#ifdef QT_CORE_LIB
				writeLog(rrlError,0,"config param "+QString(name)+" is not a boolean!","RR,cfgGetB");
				#endif
				return cfg->notFoundB;
			}
			return cfg->params[i].b;
		}
	}
	#ifdef QT_CORE_LIB
	writeLog(rrlError,0,"config param not found: "+QString(name),"RR,cfgGetB");
	#endif
	return cfg->notFoundB;
}

qint16  & __RRSDK::cfgGetI(const char * name) 
{
	for (int i=0;i<cfg->m_count;i++)	{
		if (cfg->params[i].name==name) {
			if (cfg->params[i].type !=rrgCfgInt) {
				#ifdef QT_CORE_LIB
				writeLog(rrlError,0,"config param "+QString(name)+" is not an integer!","RR,cfgGetI");
				#endif
				return cfg->notFoundI;
			}
			return cfg->params[i].i;
		}
	}
	#ifdef QT_CORE_LIB
	writeLog(rrlError,0,"config param not found: "+QString(name),"RR,cfgGetI");
	#endif
	return cfg->notFoundI;
}

_rrString100 & __RRSDK::cfgGetS(const char * name) 
{
	for (int i=0;i<cfg->m_count;i++) {
		if (cfg->params[i].name==name) {
			if (cfg->params[i].type !=rrgCfgQString) {
				#ifdef QT_CORE_LIB
				writeLog(rrlError,0,"config param "+QString(name)+" is not a string!","cfgGetS");
				#endif
				return cfg->notFoundS;
			}
			return cfg->params[i].s;
		}
	}
	#ifdef QT_CORE_LIB
	writeLog(rrlError,0,"config param not found: "+QString(name),"RR,cfgGetS");
	#endif
	return cfg->notFoundS;

}

float   & __RRSDK::cfgGetF(const char * name) 
{
	for (int i=0;i<cfg->m_count;i++) {
		if (cfg->params[i].name==name) {
			if (cfg->params[i].type !=rrgCfgFloat) {
				#ifdef QT_CORE_LIB
				writeLog(rrlError,0,"config param "+QString(name)+" is not a float!","RR,cfgGetF");
				#endif
				return cfg->notFoundF;
			}
			return cfg->params[i].f;
		}
	}
	#ifdef QT_CORE_LIB
	writeLog(rrlError,0,"config param not found: "+QString(name),"RR,cfgGetF");
	#endif
	return cfg->notFoundF;
}



_rrString100 __RRSDK::getServerConnectName(const bool &BackupServer)
{
	if (BackupServer && (!cfgGetS(cfgnServerName).isEmpty())) {
		if (cfgGetB(cfgnUseServerIP)) return cfgGetS(cfgnBackupServerIP1);
		else return cfgGetS(cfgnBackupServerName);
	} 
    _rrString100 IP=cfgGetS(cfgnServerIP1);
	if (cfgGetB(cfgnUseServerIP) && (!IP.isEmpty())) return IP;
	else return cfgGetS(cfgnServerName);
}
