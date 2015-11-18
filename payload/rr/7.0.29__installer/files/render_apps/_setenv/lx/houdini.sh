
###################  Arnold/HtoA environment variables ###################
###################  required if you have not installed Arnold/HtoA locally ###################
if ( ! $?RR_HTOA_BASE ) then
   setenv RR_HTOA_BASE "${rrSharedExeDir}htoa${rrJobRendererVersion}_houdini${rrExeVersionMajor}"
endif
/bin/echo "HtoA installation path is set to ${RR_HTOA_BASE}"

if ( ! $?HOUDINI_PATH ) then
   setenv HOUDINI_PATH "${RR_HTOA_BASE}:${rrBaseAppPath}/houdini"
else 
   setenv HOUDINI_PATH "${RR_HTOA_BASE}:$HOUDINI_PATH:${rrBaseAppPath}/houdini"
endif  

if ( ! $?HOUDINI_OTLSCAN_PATH ) then
   setenv HOUDINI_OTLSCAN_PATH "${RR_HTOA_BASE}/otls:${rrBaseAppPath}\houdini"
else 
   setenv HOUDINI_OTLSCAN_PATH "${RR_HTOA_BASE}/otls:$HOUDINI_OTLSCAN_PATH:${rrBaseAppPath}/houdini/otls"
endif  





#do not forget the empy line at the end:
