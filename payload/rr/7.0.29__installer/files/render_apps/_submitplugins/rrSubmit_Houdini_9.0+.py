# Royal Render Plugin script for Houdini 9+
# Author: Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 6.02.12
# Copyright (c) Holger Schoenberger - Binary Alchemy
# rrInstall_Copy: ../houdini/scripts/menu/
# rrInstall_Change_File: ../houdini/MainMenuCommon, before "</mainMenu>", "<addScriptItem id=\"h.royalrender\">\n	<parent>render_menu</parent>\n	<label>Submit RRender</label>\n	<scriptPath>$HFS/houdini/scripts/menu/rrSubmit_Houdini_9.0+.py</scriptPath>\n	<scriptArgs></scriptArgs>\n	<insertAfter/>\n  </addScriptItem>\n\n"


import sys
import os



def getRR_Root():
    if os.environ.has_key('RR_ROOT'):
        return os.environ['RR_ROOT']
    HCPath= "%"
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        HCPath="%RRLocationWin%"
    elif (sys.platform.lower() == "darwin"):
        HCPath="%RRLocationMac%"
    else:
        HCPath="%RRLocationLx%"
    if HCPath[0]!="%":
        return HCPath
    #raise (NameError, "No RR_ROOT environment variable set!\n")


def rrSubmit():
    hou.hipFile.save()
    sceneFile = hou.hipFile.name()
    rrRoot = getRR_Root()
    if ((sceneFile==None) or (len(sceneFile)==0)):
        return
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        os.system(rrRoot+"\\win__rrSubmitter.bat  \""+sceneFile+"\"")
    elif (sys.platform.lower() == "darwin"):
        os.system(rrRoot+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter  \""+sceneFile+"\"")
    else:
        os.system(rrRoot+"/lx__rrSubmitter.sh  \""+sceneFile+"\"")

    
rrSubmit()
