//######################################################################
//#
//# Royal Render Plugin script for Lightwave 
//# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
//# Last change: v 6.02.12
//# Copyright (c) Holger Schoenberger - Binary Alchemy
//# 
//######################################################################


@version 1.0
@warnings
@script generic

getRR_Root
{
    rrPath = getenv( "RR_ROOT" );
    return rrPath;
}

generic
{
    scene = Scene();
    sceneName =scene.filename;
    contentFolder = getdir( "Content" );
    version = hostVersion();
    args = string( " \"", sceneName , "\" -SDD \"", contentFolder, "\"  -Version \"", version, "\"" );

    exitcodeFilename = string( tempPath, "submitexitcode.txt" );
    rrPath=getRR_Root();
    exec= "";

    if (platform() == MACINTOSH) {
        exec= string( rrPath ,"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter");
    } else  if (platform() == LINUX ) {
        exec= string( rrPath ,"/lx__rrSubmitter.sh");
    } else {
        exec= string( rrPath ,"\\win__rrSubmitter.bat");
    }

    spawn( exec, args  );
}

