# Royal Render Plugin script for Houdini 12.5+
# Author: Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 7.0.11
# Copyright (c) Holger Schoenberger - Binary Alchemy
# rrInstall_Copy: ../houdini/scripts/
# rrInstall_Change_File: ../houdini/MainMenuCommon.xml, before "</mainMenu>", "<addScriptItem id=\"h.royalrender\">\n	<parent>render_menu</parent>\n	<label>Submit RRender</label>\n	<scriptPath>$HFS/houdini/scripts/rrSubmit_Houdini_12.5+.py</scriptPath>\n	<scriptArgs></scriptArgs>\n	<insertAfter/>\n  </addScriptItem>\n\n"


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
    RenVer_Arnold=""
    try:
        import arnold
        RenVer_Arnold=" -customRenVer_Arnold "+AiGetVersionString()
    except:
        pass
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        os.system(rrRoot+"\\win__rrSubmitter.bat  \""+sceneFile+"\"  "+RenVer_Arnold)
    elif (sys.platform.lower() == "darwin"):
        os.system(rrRoot+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter  \""+sceneFile+"\" "+RenVer_Arnold)
    else:
        os.system(rrRoot+"/lx__rrSubmitter.sh  \""+sceneFile+"\" "+RenVer_Arnold)

    
rrSubmit()
