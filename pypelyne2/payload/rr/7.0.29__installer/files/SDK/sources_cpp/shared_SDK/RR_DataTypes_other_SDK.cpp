#include "RR_DataTypes_other_SDK.h"

//#include "RR_files_SDK.h"
//#include "time.h"

#if defined(RR_OS_WIN) 
	#include <Windows.h>
#elif defined (RR_OS_LINUX)
	#include <errno.h>
	#include <sys/stat.h>
	#include <stdlib.h>
#else
    #include <errno.h>
    #include <sys/stat.h>
    #include <stdlib.h>
    #include <Carbon/Carbon.h>
#endif


#ifdef  QT_CORE_LIB
	#include <QStringList> 
#endif

_rrString25 rr_AppType_asString(const rr_AppType &appType)
{
    switch (appType) {
        case rraNone: return "None";
	    case rraServer: return "Server";
	    case rraClient: return "Client";
	    case rraSubmitter: return "Submitter";
	    case rraControl: return "Control";
	    case rraPostScript: return "PostScript";
	    case rraTest: return "Test";
	    case rraLogFile: return "LogFile";
	    case rraClientWatch: return "ClientWatch";
	    case rraConfig: return "Config";
	    case rraViewer: return "Viewer";
	    case rraInstaller: return "Installer";
	    case rraHistorydb: return "HistoryDB";
        case rraScript: return "Script";
        default: return "unknown";
    }
}


#ifndef RR_OS_WIN
int rrCharLen(const rrChar *C) {
	int len=0;
	while ((*C!=0) && (len<1024)) {
		len++;
		C++;
	}
	return len;
}
#endif

unsigned long z_compressBound_copy (unsigned long sourceLen)
{
	if (sourceLen<50*1024*1024) return  sourceLen + (sourceLen >> 12) + (sourceLen >> 14) + 11 +  200  ;
	else if (sourceLen<100*1024*1024) return sourceLen*2/3;
	else return sourceLen/2;
}

void rrSleep(int ms)
{
	if (ms<=0) return;
#ifdef RR_OS_WIN
	Sleep(ms);
#else
	while (ms>=999) {
		ms-=999;
		usleep(999*1000);
	}
	usleep(ms*1000);

#endif

}


#ifndef rrPlugin
#if defined( RR_OS_WIN )
#else
#endif
					 #if defined( RR_OS_WIN )
					 #else
					 #endif
                         #if defined( RR_OS_WIN )
                         #else
                         #endif
#ifndef RR_OS_WIN
#endif
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
#else
#endif
#endif //rrPlugin




#if defined(QT_CORE_LIB)

#ifndef rrPlugin
#ifdef RR_OS_WIN
#endif
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
#else
#endif
#endif //rrPlugin




#endif //QT_CORE_LIB

#ifdef RR_OS_WIN
_rrString8_500	GetExceptionString( DWORD uiExceptionCode )
{
	switch( uiExceptionCode )
	{
		case EXCEPTION_ACCESS_VIOLATION:
            return( "EXCEPTION: The thread tried to read from or write to a virtual address for which it does not have the appropriate access. (Possible NULL Pointer)");
		case EXCEPTION_ARRAY_BOUNDS_EXCEEDED:
 			return( "EXCEPTION: The thread tried to access an array element that is out of bounds and the underlying hardware supports bounds checking.");
		case EXCEPTION_BREAKPOINT:
 			return( "EXCEPTION: A breakpoint was encountered.");
		case EXCEPTION_DATATYPE_MISALIGNMENT:
 			return( "EXCEPTION: The thread tried to read or write data that is misaligned on hardware that does not provide alignment. For example, 16-bit values must be aligned on 2-byte boundaries; 32-bit values on 4-byte boundaries, and so on.");
		case EXCEPTION_FLT_DENORMAL_OPERAND:
 			return( "EXCEPTION: One of the operands in a floating-point operation is denormal. A denormal value is one that is too small to represent as a standard floating-point value.");
		case EXCEPTION_FLT_DIVIDE_BY_ZERO:
 			return( "EXCEPTION: The thread tried to divide a floating-point value by a floating-point divisor of zero.");
		case EXCEPTION_FLT_INEXACT_RESULT:
 			return( "EXCEPTION: The result of a floating-point operation cannot be represented exactly as a decimal fraction.");
		case EXCEPTION_FLT_INVALID_OPERATION:
 			return( "EXCEPTION: This exception represents any floating-point exception not included in this list.");
		case EXCEPTION_FLT_OVERFLOW:
 			return( "EXCEPTION: The exponent of a floating-point operation is greater than the magnitude allowed by the corresponding type.");
		case EXCEPTION_FLT_STACK_CHECK:
 			return( "EXCEPTION: The stack overflowed or underflowed as the result of a floating-point operation.");
		case EXCEPTION_FLT_UNDERFLOW:
 			return( "EXCEPTION: The exponent of a floating-point operation is less than the magnitude allowed by the corresponding type.");
		case EXCEPTION_ILLEGAL_INSTRUCTION:
 			return( "EXCEPTION: The thread tried to execute an invalid instruction.");
		case EXCEPTION_IN_PAGE_ERROR:
 			return( "EXCEPTION: The thread tried to access a page that was not present, and the system was unable to load the page. For example, this exception might occur if a network connection is lost while running a program over the network.");
		case EXCEPTION_INT_DIVIDE_BY_ZERO:
 			return( "EXCEPTION: The thread tried to divide an integer value by an integer divisor of zero.");
		case EXCEPTION_INT_OVERFLOW:
 			return( "EXCEPTION: The result of an integer operation caused a carry out of the most significant bit of the result.");
		case EXCEPTION_INVALID_DISPOSITION:
 			return( "EXCEPTION: An exception handler returned an invalid disposition to the exception dispatcher. Programmers using a high-level language such as C should never encounter this exception.");
		case EXCEPTION_NONCONTINUABLE_EXCEPTION:
 			return( "EXCEPTION: The thread tried to continue execution after a noncontinuable exception occurred.");
		case EXCEPTION_PRIV_INSTRUCTION:
 			return( "EXCEPTION: The thread tried to execute an instruction whose operation is not allowed in the current machine mode."); 
		case EXCEPTION_SINGLE_STEP:
 			return( "EXCEPTION: A trace trap or other single-instruction mechanism signaled that one instruction has been executed.");
		case EXCEPTION_STACK_OVERFLOW:
 			return( "EXCEPTION: The thread used up its stack.");
		default:
			_rrString8_500 winMsg;
            winMsg.length=quint16(FormatMessageA(FORMAT_MESSAGE_FROM_HMODULE | FORMAT_MESSAGE_IGNORE_INSERTS,
                           GetModuleHandleA("ntdll.dll"),
                           uiExceptionCode,
                           MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
						   winMsg.value,
						   winMsg.ArraySize,
                           NULL));
			if (winMsg.length<=0) {
				winMsg.length= sprintf_s(&winMsg.value[0],500,"EXCEPTION code %d.",uiExceptionCode);
				winMsg+="No system message found";
				//winMsg+=rrLastOSError();
			} else {
				if (winMsg.value[winMsg.length-1]==10) winMsg.length--;
				if (winMsg.value[winMsg.length-1]==13) winMsg.length--;
				winMsg.value[winMsg.length]=0;
			}
			return winMsg;

			break;
	}
}
#endif

_rrString500 rrLastOSError(int errorCode)
{
#ifdef RR_OS_WIN
    _rrString500 ret;
	if (errorCode == -1) {
        errorCode = GetLastError();
		}
    switch (errorCode) {
    case 0:
		ret="No Error.";
        break;
	/*case -1073741819:
		ret="General protection fault (Probably 'Memory Access Violation'?).";
		break;*/
	case 126:
		ret="A DLL is missing.";
		break;
	default: {
			_rrString500 winMsg;
            winMsg.length=quint16(FormatMessageW(FORMAT_MESSAGE_FROM_SYSTEM,
                           NULL,
                           errorCode,
                           MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
						   winMsg.value,
						   winMsg.ArraySize,
                           NULL));
			if (winMsg.value[winMsg.length-1]==10) winMsg.length--;
			if (winMsg.value[winMsg.length-1]==13) winMsg.length--;
			winMsg.value[winMsg.length]=0;
	#if (defined(RR_OS_WIN) && defined(_MSC_VER))
			if (winMsg.length>0) {
				ret.length= swprintf_s(ret.value,ret.ArraySize,L"Error %d: %s.",errorCode, winMsg.value);
			} else {
                ret=GetExceptionString(errorCode).value;
				if (ret.length==0) ret.length= swprintf_s(ret.value,ret.ArraySize,L"Error %d.",errorCode);
			}
	#else
			if (winMsg.length>0) {
				ret.length= swprintf(ret.value,"Error %d: %s.",errorCode, winMsg.value);
			} else {
				ret.length= swprintf(ret.value,"Error %d.",errorCode);
			}
	#endif
    break; }
	}
	while (ret.indexOf('\n')>=0) ret.value[ret.indexOf('\n')]=' ';
	while (ret.indexOf('\r')>=0) ret.value[ret.indexOf('\r')]=' ';
	return ret;
#else
	_rrString500 ret;
	ret =rrLastOSError8(errorCode).value;
	return ret;
#endif
}





_rrString8_250 rrLastOSError8(int errorCode)
{
    _rrString8_250 ret;
#ifdef RR_OS_WIN
	if (errorCode == -1) {
        errorCode = GetLastError();
		}
#else
	if (errorCode == -1) {
        errorCode = errno;
		}
#endif


    switch (errorCode) {
    case 0:
		ret="No Error.";
        break;

#ifdef RR_OS_WIN
	/*case -1073741819:
		ret="General protection fault (Probably 'Memory Access Violation'?).";
		break;*/
	case 126:
		ret="A DLL is missing.";
		break;
    default: {

			_rrString8_500 winMsg;
            winMsg.length=quint16(FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM,
                           NULL,
                           errorCode,
                           MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
						   winMsg.value,
						   winMsg.ArraySize,
                           NULL));
			if (winMsg.value[winMsg.length-1]==10) winMsg.length--;
			if (winMsg.value[winMsg.length-1]==13) winMsg.length--;
			winMsg.value[winMsg.length]=0;
	#if (defined(RR_OS_WIN) && defined(_MSC_VER))
			if (winMsg.length>230) {
				_rrString8_500 retLong;
				retLong.length= sprintf_s(retLong.value,500,"Error %d: %s.",errorCode, winMsg.value);
				ret=retLong.value;
			} else if (winMsg.length>0) {
				ret.length= sprintf_s(ret.value,250,"Error %d: %s.",errorCode, winMsg.value);
			} else {
                ret=GetExceptionString(errorCode).value;
                if (ret.length==0) ret.length= ret.length= sprintf_s(ret.value,250,"Error %d.",errorCode);
			}
	#else
			if (winMsg.length>230) {
				_rrString500 retLong;
				retLong.length= sprintf(retLong.value,"Error %d: %s.",errorCode, winMsg.value);
				ret=retLong.value;
			} else if (winMsg.length>0) {
				ret.length= sprintf(ret.value,"Error %d: %s.",errorCode, winMsg.value);
			} else {
				ret.length= sprintf(ret.value,"Error %d.",errorCode);
			}
	#endif
#elif defined (RR_OS_MAC)
   default: {
        if (strerror_r(errorCode, ret.value, 250)!=0) ret.clear();
        ret.calcLength();
        if (ret.isEmpty()) {
            ret.length=sprintf(ret.value,"Error %d.",errorCode);
        }

#else

    default: {
        char * buf;
        buf=strerror_r(errorCode, ret.value, 250);
        if (buf==NULL) ret.clear();
        if (buf!=ret.value) ret=buf; else ret.calcLength();
        if (ret.isEmpty()) {
            ret.length=sprintf(ret.value,"Error %d.",errorCode);
		} else {
			_rrString8_250 ret2=ret;
                        ret.length=sprintf(ret.value,"%s (#%d)",ret2.value,errorCode);
		}
#endif
    break; }
    }
	while (ret.indexOf('\n')>=0) ret.value[ret.indexOf('\n')]=' ';
	while (ret.indexOf('\r')>=0) ret.value[ret.indexOf('\r')]=' ';
	return ret;
}

