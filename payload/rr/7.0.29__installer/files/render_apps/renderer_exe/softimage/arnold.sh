
setenv WGPaths "$1"
setenv ArnoldExe  "kick not found"

foreach x (`echo $WGPaths | tr ";" " "`)  
   setenv testPath "${x}/Addons/SItoA/Application/Plugins/bin/linux/x64/kick"
   if -f "$testPath" then
   setenv ArnoldExe "$testPath"
   endif
   setenv testPath "${x}/Addons/SItoA/Application/bin/linux/x64/kick"
   if -f "$testPath" then
   setenv ArnoldExe "$testPath"
   endif
end


echo Arnold is installed in: $ArnoldExe

#do not forget the empy line at the end: 
