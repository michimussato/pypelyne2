@echo on

Set "XSI_USERHOME=%rrLocalPrefs%%rrExeVersion%"
rem set XSI_LOG_LOAD_TIME=1


@rem The following line enables you to use imf_disp via rrViewer to see images while they are being rendered
set MI_ENABLE_PIPE_MODE=


rem set "solidangle_LICENSE=<port>@<hostname>"


IF "%WorkgroupPath%" == ""  (
@rem  set different workgroup for each XSI version:
@echo Set Workgroup path:

goto %rrExeVersionMajor%

goto unknownversion

:6
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_6"
goto done


:7
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_7"
goto done


:2010
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_2010"
goto done


:2011
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_2011"
goto done


:2012
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_2012"
goto done


:2013
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_2013"
goto done


:2014
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_2014"
goto done



:2015
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_2015"
goto done



:2016
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_2016"
goto done



:unknownversion
Set "WorkgroupPath=%rrPluginsNoOS%workgroup_%rrExeVersionMajor%"
goto done

)

:done












