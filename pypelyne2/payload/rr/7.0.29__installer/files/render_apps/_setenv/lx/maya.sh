
#disable Autodesk Customer Involvement Program (CIP). Shutdown time of Maya fastened by  up to 30s if no internet connection available. And no crashes if home/.autdesk is read-only
setenv MAYA_DISABLE_CIP 1

setenv MAYA_APP_DIR "$rrLocalPrefs"

if ( ! $?MAYA_PLUG_IN_PATH ) then
   setenv MAYA_PLUG_IN_PATH "${rrPlugins}${rrExeVersionMajor}/plug-ins"
else 
   setenv MAYA_PLUG_IN_PATH "${rrPlugins}${rrExeVersionMajor}/plug-ins:$MAYA_PLUG_IN_PATH"
endif

if ( ! $?MAYA_SCRIPT_PATH ) then
   setenv MAYA_SCRIPT_PATH "${rrPlugins}${rrExeVersionMajor}/scripts"
else 
   setenv MAYA_SCRIPT_PATH "${rrPlugins}${rrExeVersionMajor}/scripts:$MAYA_SCRIPT_PATH"
endif

if ( ! $?MAYA_MODULE_PATH ) then
   setenv MAYA_MODULE_PATH "${rrPlugins}${rrExeVersionMajor}/modules"
else 
   setenv MAYA_MODULE_PATH "${rrPlugins}${rrExeVersionMajor}/modules:$MAYA_MODULE_PATH"
endif

if ( ! $?MI_CUSTOM_SHADER_PATH ) then
   setenv MI_CUSTOM_SHADER_PATH "${rrPlugins}${rrExeVersionMajor}/mentalray/include:${rrPlugins}mentalray/lib"
else 
   setenv MI_CUSTOM_SHADER_PATH "${rrPlugins}${rrExeVersionMajor}/mentalray/include:${rrPlugins}mentalray/lib:$MI_CUSTOM_SHADER_PATH"
endif


"${rrBin}rrCopy" -oo -os -d "${rrPrefs}${rrExeVersionMajor}-x64" "${rrLocalPrefs}${rrExeVersionMajor}-x64"
"${rrBin}rrCopy" -oo -os -d "${rrPrefs}${rrExeVersionMajor}" "${rrLocalPrefs}${rrExeVersionMajor}"



###################  RenderManStudio environment variables ###################
setenv RR_RManStudio   "${rrSharedExeDir}RenderManStudio-4.0-maya${rrExeVersionMinReq}"
/bin/echo "RenderManStudio installation path is ${RR_RManStudio}"

if ( ! $?MAYA_SCRIPT_PATH ) then
   setenv MAYA_SCRIPT_PATH "${RR_RManStudio}/scripts"
else 
   setenv MAYA_SCRIPT_PATH "${RR_RManStudio}/scripts:${MAYA_SCRIPT_PATH}"
endif
if ( ! $?MAYA_PLUG_IN_PATH ) then
   setenv MAYA_PLUG_IN_PATH "${RR_RManStudio}/plug-ins"
else 
   setenv MAYA_PLUG_IN_PATH "${RR_RManStudio}/plug-ins:${MAYA_PLUG_IN_PATH}"
endif
if ( ! $?MAYA_MODULE_PATH ) then
   setenv MAYA_MODULE_PATH "${RR_RManStudio}/etc"
else 
   setenv MAYA_MODULE_PATH "${RR_RManStudio}/etc:${MAYA_MODULE_PATH}"
endif


setenv MAYA_RENDER_DESC_PATH  "${RR_RManStudio}/etc"
setenv RATTREE                "${RR_RManStudio}"
setenv RMANTREE               "${RR_RManStudio}/rmantree"
setenv RMSTREE                "${RR_RManStudio}"
setenv XBMLANGPATH            "${RR_RManStudio}/lib/mtor/resources"


###################  Mayaman environment variables ###################
#setenv MAYAMANROOT "/usr/local/mayaman2.0.29"
#/bin/echo "Mayaman installation path is ${MAYAMANROOT}"
#if ( ! $?MAYA_SCRIPT_PATH ) then
#   setenv MAYA_SCRIPT_PATH "${MAYAMANROOT}/mel"
#else 
#   setenv MAYA_SCRIPT_PATH "${MAYAMANROOT}/mel:${MAYA_SCRIPT_PATH}:"
#endif
#if ( ! $?MAYA_PLUG_IN_PATH ) then
#   setenv MAYA_PLUG_IN_PATH "${MAYAMANROOT}/plugins/${rrExeVersionMajor}"
#else 
#   setenv MAYA_PLUG_IN_PATH "${MAYAMANROOT}/plugins/${rrExeVersionMajor}:${MAYA_PLUG_IN_PATH}:"
#endif




###################  Arnold/MtoA environment variables ###################
###################  required if you have not installed Arnold/MtoA locally ###################
if ( ! $?RR_MTOA_BASE ) then
   setenv RR_MTOA_BASE "${rrSharedExeDir}mtoadeploy_${rrExeVersionMajor}"
endif
/bin/echo "MtoA installation path is set to ${RR_MTOA_BASE}"
if ( ! $?MAYA_MODULE_PATH ) then
   setenv MAYA_MODULE_PATH "${RR_MTOA_BASE}"
else 
   setenv MAYA_MODULE_PATH "${RR_MTOA_BASE}:${MAYA_MODULE_PATH}:"
endif
if ( ! $?MAYA_RENDER_DESC_PATH ) then
   setenv MAYA_RENDER_DESC_PATH "${RR_MTOA_BASE}"
else 
   setenv MAYA_RENDER_DESC_PATH "${RR_MTOA_BASE}:${MAYA_RENDER_DESC_PATH}:"
endif
if ( ! $?ARNOLD_PLUGIN_PATH ) then
   setenv ARNOLD_PLUGIN_PATH "${RR_MTOA_BASE}/shaders"
else 
   setenv ARNOLD_PLUGIN_PATH "${RR_MTOA_BASE}/shaders:${ARNOLD_PLUGIN_PATH}:"
endif
if ( ! $?MAYA_PLUG_IN_PATH ) then
   setenv MAYA_PLUG_IN_PATH "${RR_MTOA_BASE}"
else 
   setenv MAYA_PLUG_IN_PATH "${RR_MTOA_BASE}/plug-ins:${MAYA_PLUG_IN_PATH}:"
endif




###################  RedShift environment variables ###################
if ( ! $?RR_REDSHIFT_BASE ) then
   setenv RR_REDSHIFT_BASE "${rrSharedExeDir}Redshift_${rrJobRendererVersion}"
endif
/bin/echo "Redshift installation path is set to ${RR_REDSHIFT_BASE}"
setenv REDSHIFT_COREDATAPATH "${RR_REDSHIFT_BASE}"
setenv REDSHIFT_COMMON_ROOT "${RR_REDSHIFT_BASE}/Common"
setenv REDSHIFT_PLUG_IN_PATH "${RR_REDSHIFT_BASE}/${rrExeVersionMinReq}/linux"
setenv REDSHIFT_SCRIPT_PATH "${REDSHIFT_COMMON_ROOT}/scripts:${REDSHIFT_COMMON_ROOT}/scripts/override"
setenv REDSHIFT_XBMLANGPATH "${REDSHIFT_COMMON_ROOT}/icons"
setenv REDSHIFT_RENDER_DESC_PATH "${REDSHIFT_COMMON_ROOT}/rendererDesc"
if ( ! $?MAYA_RENDER_DESC_PATH ) then
   setenv MAYA_RENDER_DESC_PATH "${REDSHIFT_RENDER_DESC_PATH}"
else 
   setenv MAYA_RENDER_DESC_PATH "${REDSHIFT_RENDER_DESC_PATH}:${MAYA_RENDER_DESC_PATH}"
endif
if ( ! $?MAYA_SCRIPT_PATH ) then
   setenv MAYA_SCRIPT_PATH "${REDSHIFT_SCRIPT_PATH}"
else 
   setenv MAYA_SCRIPT_PATH "${REDSHIFT_SCRIPT_PATH}:${MAYA_SCRIPT_PATH}"
endif
if ( ! $?MAYA_PLUG_IN_PATH ) then
   setenv MAYA_PLUG_IN_PATH "${REDSHIFT_PLUG_IN_PATH}"
else 
   setenv MAYA_PLUG_IN_PATH "${REDSHIFT_PLUG_IN_PATH}:${MAYA_PLUG_IN_PATH}"
endif






###################  VRay environment variables ###################
if ( ! $?RR_VRAY_BASE ) then
    setenv RR_VRAY_BASE "${rrSharedExeDir}vray${rrExeVersionMajor}"
endif
echo VRay installation path is set to ${RR_VRAY_BASE}
setenv MAYA_PLUG_IN_PATH "${RR_VRAY_BASE}/plug-ins:${MAYA_PLUG_IN_PATH}"
setenv MAYA_SCRIPT_PATH  "${RR_VRAY_BASE}/scripts:${MAYA_SCRIPT_PATH}"
setenv MAYA_RENDER_DESC_PATH "${RR_VRAY_BASE}/rendererDesc:${MAYA_RENDER_DESC_PATH}"
setenv MAYA_MODULE_PATH  "${RR_VRAY_BASE}/modules:${MAYA_MODULE_PATH}"
setenv VRAY_FOR_MAYA${rrExeVersionMajor}_MAIN_x64    "${RR_VRAY_BASE}"
setenv VRAY_FOR_MAYA${rrExeVersionMajor}_PLUGINS_x64 "${RR_VRAY_BASE}/vrayplugins"
setenv VRAY_PATH "${RR_VRAY_BASE}/bin"
setenv VRAY_OSL_PATH_MAYA${rrExeVersionMajor}_x64 "/usr/ChaosGroup/V-Ray/Maya${rrExeVersionMajor}-x64/opensl"
setenv VRAY_PLUGINS_x64 "${RR_VRAY_BASE}/vrayplugins"
setenv VRAY_TOOLS_MAYA${rrExeVersionMajor}_x64 "${RR_VRAY_BASE}/Maya${rrExeVersionMajor}-x64/bin"

@echo ""
@echo ""









#do not forget the empy line at the end:
