@echo off
set "ArnoldExe=  Kick.exe Not Found  "


SETLOCAL ENABLEDELAYEDEXPANSION 

set "WGPaths=%1"
set "WGPaths=%WGPaths:"=%"
set "WGPaths=%WGPaths::semicolon:=;%" 

FOR %%i IN (%WGPaths%) DO (
  set "testPath=%%i\Addons\SItoA\Application\bin\nt-x86-64\kick.exe" 
  IF EXIST "!testPath!" set "ArnoldExe=!testPath!"
  set "testPath=%%i\Addons\SItoA\Application\Plugins\bin\nt-x86-64\kick.exe" 
  IF EXIST "!testPath!" set "ArnoldExe=!testPath!"
)

ENDLOCAL & set "ArnoldExe=%ArnoldExe%"

echo Arnold Kick is set to "%ArnoldExe%"

