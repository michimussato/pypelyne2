

setenv MAYA_APP_DIR "$rrLocalPrefs"

if ( ! $?MAYA_PLUG_IN_PATH ) then
   setenv MAYA_PLUG_IN_PATH "${rrPlugins}plug-ins"
else 
   setenv MAYA_PLUG_IN_PATH "${rrPlugins}plug-ins:$MAYA_PLUG_IN_PATH"
endif

if ( ! $?MAYA_SCRIPT_PATH ) then
   setenv MAYA_SCRIPT_PATH "${rrPlugins}scripts"
else 
   setenv MAYA_SCRIPT_PATH "${rrPlugins}scripts:$MAYA_SCRIPT_PATH"
endif

if ( ! $?MAYA_MODULE_PATH ) then
   setenv MAYA_MODULE_PATH "${rrPlugins}modules"
else 
   setenv MAYA_MODULE_PATH "${rrPlugins}modules:$MAYA_MODULE_PATH"
endif

if ( ! $?MI_CUSTOM_SHADER_PATH ) then
   setenv MI_CUSTOM_SHADER_PATH "${rrPlugins}mentalray/include:${rrPlugins}mentalray/lib"
else 
   setenv MI_CUSTOM_SHADER_PATH "${rrPlugins}mentalray/include:${rrPlugins}mentalray/lib:$MI_CUSTOM_SHADER_PATH"
endif





###################  RenderManStudio environment variables ###################
setenv RR_RManStudio   "${rrSharedExeDir}RenderManStudio-2.0.1-maya${rrExeVersionMajor}"
/bin/echo "RenderManStudio installation path is ${RR_RManStudio}"

if ( ! $?MAYA_SCRIPT_PATH ) then
   setenv MAYA_SCRIPT_PATH "${RR_RManStudio}/scripts"
else 
   setenv MAYA_SCRIPT_PATH "${RR_RManStudio}/scripts:${MAYA_SCRIPT_PATH};"
endif
if ( ! $?MAYA_MODULE_PATH ) then
   setenv MAYA_MODULE_PATH "${RR_RManStudio}/etc"
else 
   setenv MAYA_MODULE_PATH "${RR_RManStudio}/etc:${MAYA_MODULE_PATH}"
endif

setenv MAYA_PLUG_IN_PATH      "${RR_RManStudio}/plug-ins:${MAYA_PLUG_IN_PATH};"
setenv MAYA_RENDER_DESC_PATH  "${RR_RManStudio}/etc"
setenv RATTREE                "${RR_RManStudio}"
setenv RMANTREE               "${RR_RManStudio}/rmantree"
setenv RMSTREE                "${RR_RManStudio}"
setenv XBMLANGPATH            "${RR_RManStudio}/lib/mtor/resources"


###################  VRay environment variables ###################
setenv VRAY_FOR_MAYA${rrExeVersionMajor}_MAIN_PowerPC /Applications/Autodesk/maya${rrExeVersionMajor}/vray
setenv VRAY_FOR_MAYA${rrExeVersionMajor}_MAIN_x64 /Applications/Autodesk/maya${rrExeVersionMajor}/vray
setenv VRAY_FOR_MAYA${rrExeVersionMajor}_PLUGINS_PowerPC /Applications/Autodesk/maya${rrExeVersionMajor}/vray/vrayplugins
setenv VRAY_FOR_MAYA${rrExeVersionMajor}_PLUGINS_x64 /Applications/Autodesk/maya${rrExeVersionMajor}/vray/vrayplugins
setenv VRAY_OSL_PATH_MAYA${rrExeVersionMajor}_x64 /Applications/ChaosGroup/V-Ray/Maya${rrExeVersionMajor}/opensl
setenv VRAY_TOOLS_MAYA${rrExeVersionMajor}_x64 /Applications/ChaosGroup/V-Ray/Maya${rrExeVersionMajor}/bin
setenv VRAY_PATH "/Applications/Autodesk/maya${rrExeVersionMajor}/vray/bin"
#setenv VRAY_AUTH_CLIENT_FILE_PATH ${rrPrefs}
setenv MAYA_SCRIPT_PATH "/Applications/ChaosGroup/V-Ray/Maya${rrExeVersionMajor}/bin:$MAYA_SCRIPT_PATH"




###################  Arnold/MtoA environment variables ###################
###################  required if you have not installed Arnold/MtoA locally ###################
setenv "RR_MTOA_BASE=${rrSharedExeDir}mtoadeploy_${rrExeVersionMajor}"
/bin/echo "MtoA is installed in ${RR_MTOA_BASE}"
if ( ! $?MAYA_MODULE_PATH ) then
   setenv MAYA_MODULE_PATH "${RR_MTOA_BASE}"
else 
   setenv MAYA_MODULE_PATH "${RR_MTOA_BASE}:${MAYA_MODULE_PATH};"
endif
if ( ! $?MAYA_RENDER_DESC_PATH ) then
   setenv MAYA_RENDER_DESC_PATH "${RR_MTOA_BASE}"
else 
   setenv MAYA_RENDER_DESC_PATH "${RR_MTOA_BASE}:${MAYA_RENDER_DESC_PATH};"
endif
if ( ! $?MAYA_PLUG_IN_PATH ) then
   setenv MAYA_PLUG_IN_PATH "${RR_MTOA_BASE}"
else 
   setenv MAYA_PLUG_IN_PATH "${RR_MTOA_BASE}/plug-ins:${MAYA_PLUG_IN_PATH};"
endif
if ( ! $?ARNOLD_PLUGIN_PATH ) then
   setenv ARNOLD_PLUGIN_PATH "${RR_MTOA_BASE}/shaders"
else 
   setenv ARNOLD_PLUGIN_PATH "${RR_MTOA_BASE}/shaders:${ARNOLD_PLUGIN_PATH};"
endif




############### different env variables for 32bit and 64bit ###################
## at first create the MAYA_APP_DIR folder (specified above, otherwise maya does not start) ##
## and copy the shared prefs from the network (if existing) ##


if ( $rrExeBit == "x32" ) then
   "${rrBin}rrCopy.app/Contents/MacOS/rrCopy" -oo -os -d "${rrPrefs}${rrExeVersionMajor}" "${rrLocalPrefs}${rrExeVersionMajor}"
else
   "${rrBin}rrCopy.app/Contents/MacOS/rrCopy" -oo -os -d "${rrPrefs}${rrExeVersionMajor}-x64" "${rrLocalPrefs}${rrExeVersionMajor}-x64"
endif


#do not forget the empy line at the end:
