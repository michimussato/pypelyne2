REM    Set this path to the UNC path RRender:
REM    e.g.   set "RR_ROOT_INSTALLER=\\Fileserver\Share\RoyalRender"
set "RR_ROOT_INSTALLER="

call "%RR_ROOT_INSTALLER%\win__global.bat"
start "" "%RR_ROOT_INSTALLER%\bin\win\rrWorkstation_installer.exe"  %RRCMD% %* 
