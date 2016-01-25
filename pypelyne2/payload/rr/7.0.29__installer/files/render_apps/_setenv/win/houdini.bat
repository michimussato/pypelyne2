@echo on

@rem change the license server name:
@rem C:\WINDOWS\system32\hserver.exe -S myLicenseServerName



rem  ###################  Arnold/HtoA environment variables ###################
rem  ###################  required if you have not installed Arnold/MtoA locally ###################

IF "%RR_HTOA_BASE%" == ""  ( set "RR_HTOA_BASE=%rrSharedExeDir%htoa%rrJobRendererVersion%_houdini%rrExeVersionMajor%" )
echo HtoA installation path is set to %RR_HTOA_BASE%
set "PATH=%PATH%;%RR_HTOA_BASE%\scripts\bin"


set "HOUDINI_PATH_BSLASH=%RR_HTOA_BASE%;%HOUDINI_PATH%;%rrBaseAppPath%\houdini"
set "HOUDINI_PATH=%HOUDINI_PATH_BSLASH:\=/%"

set "HOUDINI_OTLSCAN_PATH_BSLASH=%RR_HTOA_BASE%\otls;%HOUDINI_OTLSCAN_PATH%;%rrBaseAppPath%\houdini\otls" 
set "HOUDINI_OTLSCAN_PATH=%HOUDINI_OTLSCAN_PATH_BSLASH:\=/%"

rem set "solidangle_LICENSE=<port>@<hostname>"
