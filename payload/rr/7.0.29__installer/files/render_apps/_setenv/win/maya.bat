@echo on

rem #disable Autodesk Customer Involvement Program (CIP). Shutdown time of Maya fastened by  up to 30s if no internet connection available. And no crashes if home/.autdesk is read-only

Set MAYA_DISABLE_CIP=1



Set "MAYA_APP_DIR=%rrLocalPrefs%"
set "PATH=%rrPlugins%%rrExeVersionMajor%\plug-ins;%PATH%"
set "MAYA_PLUG_IN_PATH=%rrPlugins%%rrExeVersionMajor%\plug-ins;%MAYA_PLUG_IN_PATH%"
set "MAYA_SCRIPT_PATH=%rrPlugins%%rrExeVersionMajor%\scripts;%MAYA_SCRIPT_PATH%;"
set "MAYA_MODULE_PATH=%rrPlugins%%rrExeVersionMajor%\modules;%MAYA_MODULE_PATH%;"
set "MI_CUSTOM_SHADER_PATH=%rrPlugins%%rrExeVersionMajor%\mentalray\include;%rrPlugins%%rrExeVersionMajor%\mentalray\lib;%MI_CUSTOM_SHADER_PATH%;"
set "MAYA_RENDER_DESC_PATH=%rrPlugins%%rrExeVersionMajor%\rendererDesc;%MAYA_RENDER_DESC_PATH%;"
"%rrBin%rrCopy.exe" -oo -os -d "%rrPrefs%%rrExeVersionMajor%-x64"  "%rrLocalPrefs%%rrExeVersionMajor%-x64"
"%rrBin%rrCopy.exe" -oo -os -d "%rrPrefs%%rrExeVersionMajor%"  "%rrLocalPrefs%%rrExeVersionMajor%"

@echo ""
@echo ""


rem  ###################  RenderManStudio environment variables ###################
set "RR_RManStudio=%rrSharedExeDir%RenderManStudio-2.0.1-maya%rrExeVersionMinReq%"
echo RenderManStudio installation path is set to %RR_RManStudio%
set "MAYA_SCRIPT_PATH=%RR_RManStudio%\scripts\;%MAYA_SCRIPT_PATH%;"
set "MAYA_PLUG_IN_PATH=%RR_RManStudio%\plug-ins\;%MAYA_PLUG_IN_PATH%;"
set "MAYA_RENDER_DESC_PATH=%RR_RManStudio%\etc;%MAYA_RENDER_DESC_PATH%"
Set "MAYA_MODULE_PATH=%RR_RManStudio%\etc;%MAYA_MODULE_PATH%"
Set "RATTREE=%RR_RManStudio%"
Set "RMANTREE=%RR_RManStudio%\rmantree"
Set "RMSTREE=%RR_RManStudio%"
Set "XBMLANGPATH=%RR_RManStudio%\lib\mtor\resources"

@echo ""
@echo ""


rem  ###################  MAYAMANROOT environment variables ###################
rem set "MAYAMANROOT=C:\Program Files (x86)\mayaman2.0.29"
rem set "MAYA_SCRIPT_PATH=%MAYAMANROOT%\mel\;%MAYA_SCRIPT_PATH%;"
rem set "MAYA_PLUG_IN_PATH=%MAYAMANROOT%\plugins\%rrExeVersionMajor%;%MAYA_PLUG_IN_PATH%;"

@echo ""
@echo ""


rem  ###################  3Delight environment variables ###################
rem set DELIGHT=C:\Program Files\3Delight
rem set DL_DISPLAYS_PATH=%DELIGHT%\displays
rem set DL_SHADERS_PATH=.:%DELIGHT%\shaders
rem set PATH=%PATH%;%DELIGHT%\bin
rem set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%DELIGHT%\maya\plugins
rem set MAYA_RENDER_DESC_PATH=%MAYA_RENDER_DESC_PATH%;%DELIGHT%\maya\render_desc
rem set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%DELIGHT%\maya\scripts


@echo ""
@echo ""


rem  ###################  VRay environment variables ###################
rem  ###################  required if you have not installed VRay locally ###################
rem IF "%RR_VRAY_BASE%" == ""  ( set "RR_VRAY_BASE=%rrSharedExeDir%vray%rrExeVersionMajor%" )
rem echo VRay installation path is set to '%RR_VRAY_BASE%'

rem "%RR_VRAY_BASE%\bin\setvrlservice.exe" -server=YourServerName
rem "%rrBin%rrCopy.exe" -oo -os -d "%RR_VRAY_BASE%\copy_maya" "%rrBaseAppPath%"

rem set "MAYA_PLUG_IN_PATH=%RR_VRAY_BASE%\plug-ins\;%MAYA_PLUG_IN_PATH%;"
rem set "MAYA_SCRIPT_PATH=%RR_VRAY_BASE%\scripts\;%MAYA_SCRIPT_PATH%;"
rem set "MAYA_RENDER_DESC_PATH=%RR_VRAY_BASE%\rendererDesc;%MAYA_RENDER_DESC_PATH%;
rem set "MAYA_MODULE_PATH=%RR_VRAY_BASE%\modules;%MAYA_MODULE_PATH%;"
rem set "VRAY_FOR_MAYA%rrExeVersionMajor%_MAIN_x64=%RR_VRAY_BASE%"
rem set "VRAY_FOR_MAYA%rrExeVersionMajor%_PLUGINS_x64=%RR_VRAY_BASE%\vrayplugins"
rem set "VRAY_PLUGINS_x64=%RR_VRAY_BASE%\vrayplugins"
rem set "VRAY_OSL_PATH_MAYA%rrExeVersionMajor%_x64=%RR_VRAY_BASE%\Maya %rrExeVersionMajor% for x64\opensl"
rem set "VRAY_TOOLS_MAYA%rrExeVersionMajor%_x64=%RR_VRAY_BASE%\Maya %rrExeVersionMajor% for x64\bin"
rem set "PATH=%RR_VRAY_BASE%\bin;%RR_VRAY_BASE%\Maya %rrExeVersionMajor% for x64\bin;%PATH%"

@echo ""
@echo ""



rem  ###################  Arnold/MtoA environment variables ###################
IF "%RR_MTOA_BASE%" == ""  ( set "RR_MTOA_BASE=%rrSharedExeDir%mtoadeploy_%rrExeVersionMajor%" )
echo MtoA installation path is set to '%RR_MTOA_BASE%'
set "PATH=%RR_MTOA_BASE%\bin;%PATH%"
set "PATH=%PATH%;%rrBaseAppPath%\plug-ins\xgen\bin;%rrBaseAppPath%\bin"
Set "MAYA_MODULE_PATH=%RR_MTOA_BASE%;%MAYA_MODULE_PATH%"
set "MAYA_RENDER_DESC_PATH=%RR_MTOA_BASE%;%MAYA_RENDER_DESC_PATH%"
set "MAYA_PLUG_IN_PATH=%RR_MTOA_BASE%\plug-ins;%MAYA_PLUG_IN_PATH%"
set "ARNOLD_PLUGIN_PATH=%RR_MTOA_BASE%\shaders;%ARNOLD_PLUGIN_PATH%"
set "ARNOLD_PROCEDURAL_PATH=%RR_MTOA_BASE%\procedurals;%ARNOLD_PROCEDURAL_PATH%"
rem set "solidangle_LICENSE=<port>@<hostname>"
"%rrBin%rrCopy.exe" -oo -os  "%RR_MTOA_BASE%\procedurals\xgen_procedural.dll"  "%RR_MTOA_BASE%\shaders\xgen_procedural.dll"

@echo ""
@echo ""


rem  ###################  RedShift environment variables ###################
IF "%RR_REDSHIFT_BASE%" == ""  ( set "RR_REDSHIFT_BASE=%rrSharedExeDir%Redshift_%rrJobRendererVersion%" )
echo RedShift Maya plugin installation path is set to  '%RR_REDSHIFT_BASE%'
set "REDSHIFT_COREDATAPATH=%RR_REDSHIFT_BASE%"
set "REDSHIFT_COMMON_ROOT=%RR_REDSHIFT_BASE%\Plugins\Maya\Common"
set "REDSHIFT_PLUG_IN_PATH=%RR_REDSHIFT_BASE%\Plugins\Maya\%rrExeVersionMinReq%\nt-x86-64
set "REDSHIFT_SCRIPT_PATH=%REDSHIFT_COMMON_ROOT%\scripts;%REDSHIFT_COMMON_ROOT%\scripts\override
set "REDSHIFT_XBMLANGPATH=%REDSHIFT_COMMON_ROOT%\icons
set "REDSHIFT_RENDER_DESC_PATH=%REDSHIFT_COMMON_ROOT%\rendererDesc
set "MAYA_RENDER_DESC_PATH=%REDSHIFT_RENDER_DESC_PATH%;%MAYA_RENDER_DESC_PATH%"
set "MAYA_SCRIPT_PATH=%REDSHIFT_SCRIPT_PATH%;%MAYA_SCRIPT_PATH%"
set "MAYA_PLUG_IN_PATH=%REDSHIFT_PLUG_IN_PATH%;%MAYA_PLUG_IN_PATH%"
set "PATH=%REDSHIFT_PLUG_IN_PATH%;%PATH%"
rem set "redshift_LICENSE=5053@licenseserverName"


rem  ###################  PhoenixFD environment variables ###################
set "PHX_FOR_MAYA%rrExeVersionMinReq%_MAIN_x64=%rrPlugins%%rrExeVersionMajor%\plug-ins\phoenixfd"
set "MAYA_PLUG_IN_PATH=%rrPlugins%%rrExeVersionMajor%\plug-ins\phoenixfd\plug-ins;%MAYA_PLUG_IN_PATH%"



rem  ###################  Yeti environment variables ###################
IF "%RR_YETI_BASE%" == ""  ( set "RR_YETI_BASE=%rrPlugins%%rrJobVersionMajor%\yeti" )
echo Yeti installation path is set to '%RR_YETI_BASE%'
set ARNOLD_PROCS_PATH=%RR_YETI_BASE%\bin;%ARNOLD_PROCS_PATH%
set MTOA_EXTENSIONS_PATH=%RR_YETI_BASE%\plug-ins;%MTOA_EXTENSIONS_PATH%
set peregrinel_LICENSE=5053@localhost
set MAYA_PLUG_IN_PATH=%RR_YETI_BASE%\plug-ins;%MAYA_PLUG_IN_PATH%



@echo ""
@echo ""


