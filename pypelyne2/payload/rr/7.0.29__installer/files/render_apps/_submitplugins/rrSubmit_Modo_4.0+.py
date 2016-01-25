#python
# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Plugin script for Modo
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 7.0.06
# Copyright (c) Holger Schoenberger - Binary Alchemy
# 
######################################################################

import lx
import os
import sys
import random



def showDialog(message):
    lx.eval("dialog.setup error");
    lx.eval("dialog.title {Warning}");
    lx.eval("dialog.msg {"+message+"}");
    lx.eval("dialog.open"); 

def getRR_Root():
    if os.environ.has_key('RR_ROOT'):
        return os.environ['RR_ROOT']
    HCPath="%"
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        HCPath="%RRLocationWin%"
    elif (sys.platform.lower() == "darwin"):
        HCPath="%RRLocationMac%"
    else:
        HCPath="%RRLocationLx%"
    if HCPath[0]!="%":
        return HCPath
    showDialog("No RR_ROOT environment variable set!\n Please execute rrWorkstationInstaller and restart.")


def writeNodeStr(fileID,name,text):
    text=text.replace("&","&amp;")
    text=text.replace("<","&lt;")
    text=text.replace(">","&gt;")
    text=text.replace("\"","&quot;")
    text=text.replace("'","&apos;")
    text=text.replace(unichr(228),"&#228;")
    text=text.replace(unichr(246),"&#246;")
    text=text.replace(unichr(252),"&#252;")
    text=text.replace(unichr(223),"&#223;")
    text=text.replace(unichr(196),"&#196;")
    text=text.replace(unichr(214),"&#214;")
    text=text.replace(unichr(220),"&#220;")
    fileID.write("    <"+name+">  "+text+"   </"+name+">\n")

def writeNodeInt(fileID,name,number):
    fileID.write("    <"+name+">  "+str(number)+"   </"+name+">\n")

def writeNodeBool(fileID,name,value):
    if value:
        fileID.write("    <"+name+">   1   </"+name+">\n")
    else:
        fileID.write("    <"+name+">   0   </"+name+">\n")


def setNewTempFileName():
    random.seed()
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        if os.environ.has_key('TEMP'):
            nam=os.environ['TEMP']
        else:
            nam=os.environ['TMP']
        nam+="\\"
    else:
        nam="/tmp/"
    nam+="rrSubmitModo_"
    nam+=str(random.randrange(1000,10000,1))
    nam+=".xml"
    return nam

def rrSubmit():
    SceneName = lx.eval( "query sceneservice scene.file ? current" )
    if ((SceneName==None) or (len(SceneName)==0)):
        showDialog("Scene was never saved.")
        return
    sceneWasChanged = lx.eval( "query sceneservice scene.changed ? current" )
    if (sceneWasChanged):
        lx.out( "Saving scene..." )
        lx.eval( "scene.save" )
    sceneVersion= lx.eval( "query platformservice appversion ?")
    sceneVersion=str(sceneVersion)
    sceneBuild= lx.eval( "query platformservice appbuild ?")
    sceneVersion=sceneVersion[:1]  + "."
    if (sceneBuild>=42548):
        sceneVersion=sceneVersion + "3"

    lx.eval( "select.itemType polyRenders")
    seqStart = lx.eval( "item.channel first ?")
    seqEnd= lx.eval( "item.channel last ?")
    seqStep= lx.eval( "item.channel step ?")

    TempFileName=setNewTempFileName()
    fileID=0
    fileID = file(TempFileName, "w")
    fileID.write("<rrJob_submitFile syntax_version=\"6.0\">\n")
    fileID.write("<DeleteXML>1</DeleteXML>\n")


#First write an *all* layer
    nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
    for L in range(0, nbOutputs):
        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
        lx.eval( "select.item "+objID)
        ImageFilename= lx.eval( "item.channel renderOutput$filename ? " );
        if ((ImageFilename==None) or (len(ImageFilename)==0)):
            continue
        
        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
        if (not isEnabled):
            continue
        
        imageExtension=lx.eval( "item.channel renderOutput$format ?" );
        if (imageExtension=="$FLEX"):
            imageExtension=".flx"
        elif (imageExtension=="$Targa"):
            imageExtension=".tga"
        elif (imageExtension=="BMP"):
            imageExtension=".bmp"
        elif (imageExtension=="HDR"):
            imageExtension=".hdr"
        elif (imageExtension=="JP2"):
            imageExtension=".jp2"
        elif (imageExtension=="JP216"):
            imageExtension=".jp2"
        elif (imageExtension=="JP216Lossless"):
            imageExtension=".jp2"
        elif (imageExtension=="JPG"):
            imageExtension=".jpg"
        elif (imageExtension=="PNG"):
            imageExtension=".png"
        elif (imageExtension=="PNG16"):
            imageExtension=".png"
        elif (imageExtension=="PSD"):
            imageExtension=".psd"
        elif (imageExtension=="SGI"):
            imageExtension=".sgi"
        elif (imageExtension=="TIF"):
            imageExtension=".tif"
        elif (imageExtension=="TIF16BIG"):
            imageExtension=".tif"
        elif (imageExtension=="TIF16"):
            imageExtension=".tif"
        elif (imageExtension=="openexr"):
            imageExtension=".exr"
        elif (imageExtension=="openexr_32"):
            imageExtension=".exr"
        elif (imageExtension=="openexr_tiled16"):
            imageExtension=".exr"
        elif (imageExtension=="openexr_tiled32"):
            imageExtension=".exr"
        else:
            imageExtension="."+imageExtension
        
        lx.eval( "select.itemType polyRenders")       
        Stereo= lx.eval("item.channel polyRender$stereo ?");
        if (Stereo==1):
            ImageFilename = ImageFilename + "L"


        fileID.write("<Job>\n")
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            writeNodeStr(fileID,"SceneOS", "win")
        elif (sys.platform.lower() == "darwin"):
            writeNodeStr(fileID,"SceneOS", "mac")
        else:
            writeNodeStr(fileID,"SceneOS", "lx")
        writeNodeStr(fileID,"Software", "Modo")
        if (Stereo==1):
            writeNodeStr(fileID,"Renderer", "Stereo")
        writeNodeInt(fileID,"Version",  sceneVersion)
        writeNodeStr(fileID,"SceneName", SceneName)
        writeNodeBool(fileID,"IsActive", True )
        writeNodeInt(fileID,"SeqStart",seqStart)
        writeNodeInt(fileID,"SeqEnd",seqEnd)
        writeNodeInt(fileID,"SeqStep",seqStep)
        writeNodeStr(fileID,"Layer","** All **")
        writeNodeStr(fileID,"ImageFilename",ImageFilename)
        writeNodeStr(fileID,"ImageExtension",imageExtension)

        for ch in range(L+1, nbOutputs):
            objID= lx.eval( "query sceneservice renderOutput.id ? "+str(ch))
            lx.eval( "select.item "+objID)
            ImageFilename= lx.eval( "item.channel renderOutput$filename ? " );
            if ((ImageFilename==None) or (len(ImageFilename)==0)):
                continue
            isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
            if (not isEnabled):
                continue
            imageExtension=lx.eval( "item.channel renderOutput$format ? " );
            if (imageExtension=="$FLEX"):
                imageExtension=".flx"
            elif (imageExtension=="$Targa"):
                imageExtension=".tga"
            elif (imageExtension=="BMP"):
                imageExtension=".bmp"
            elif (imageExtension=="HDR"):
                imageExtension=".hdr"
            elif (imageExtension=="JP2"):
                imageExtension=".jp2"
            elif (imageExtension=="JP216"):
                imageExtension=".jp2"
            elif (imageExtension=="JP216Lossless"):
                imageExtension=".jp2"
            elif (imageExtension=="JPG"):
                imageExtension=".jpg"
            elif (imageExtension=="PNG"):
                imageExtension=".png"
            elif (imageExtension=="PNG16"):
                imageExtension=".png"
            elif (imageExtension=="PSD"):
                imageExtension=".psd"
            elif (imageExtension=="SGI"):
                imageExtension=".sgi"
            elif (imageExtension=="TIF"):
                imageExtension=".tif"
            elif (imageExtension=="TIF16BIG"):
                imageExtension=".tif"
            elif (imageExtension=="TIF16"):
                imageExtension=".tif"
            elif (imageExtension=="openexr"):
                imageExtension=".exr"
            elif (imageExtension=="openexr_32"):
                imageExtension=".exr"
            elif (imageExtension=="openexr_tiled16"):
                imageExtension=".exr"
            elif (imageExtension=="openexr_tiled32"):
                imageExtension=".exr"
            else:
                imageExtension="."+imageExtension
            writeNodeStr(fileID,"ChannelFilename",ImageFilename)
            writeNodeStr(fileID,"ChannelExtension",imageExtension)        
        fileID.write("</Job>\n")
        #we only need to write "*all*" once:
        break;


#Now write layers separately
    nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
    for L in range(0, nbOutputs):
        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
        lx.eval( "select.item "+objID)
        ImageFilename= lx.eval( "item.channel renderOutput$filename ? " );
        if ((ImageFilename==None) or (len(ImageFilename)==0)):
            continue

        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
        if (not isEnabled):
            continue
        layerName= lx.eval( "query sceneservice renderOutput.name ? "+str(L) );
        
        imageExtension=lx.eval( "item.channel renderOutput$format ? " );
        if (imageExtension=="$FLEX"):
            imageExtension=".flx"
        elif (imageExtension=="$Targa"):
            imageExtension=".tga"
        elif (imageExtension=="BMP"):
            imageExtension=".bmp"
        elif (imageExtension=="HDR"):
            imageExtension=".hdr"
        elif (imageExtension=="JP2"):
            imageExtension=".jp2"
        elif (imageExtension=="JP216"):
            imageExtension=".jp2"
        elif (imageExtension=="JP216Lossless"):
            imageExtension=".jp2"
        elif (imageExtension=="JPG"):
            imageExtension=".jpg"
        elif (imageExtension=="PNG"):
            imageExtension=".png"
        elif (imageExtension=="PNG16"):
            imageExtension=".png"
        elif (imageExtension=="PSD"):
            imageExtension=".psd"
        elif (imageExtension=="SGI"):
            imageExtension=".sgi"
        elif (imageExtension=="TIF"):
            imageExtension=".tif"
        elif (imageExtension=="TIF16BIG"):
            imageExtension=".tif"
        elif (imageExtension=="openexr"):
            imageExtension=".exr"
        else:
            imageExtension=".unknown"

        lx.eval( "select.itemType polyRenders")
        Stereo= lx.eval("item.channel polyRender$stereo ?");
        if (Stereo==1):
            ImageFilename = ImageFilename + "L"  


        fileID.write("<Job>\n")
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            writeNodeStr(fileID,"SceneOS", "win")
        elif (sys.platform.lower() == "darwin"):
            writeNodeStr(fileID,"SceneOS", "mac")
        else:
            writeNodeStr(fileID,"SceneOS", "lx")
        writeNodeStr(fileID,"Software", "Modo")
        if (Stereo==1):
            writeNodeStr(fileID,"Renderer", "Stereo")
        writeNodeInt(fileID,"Version",  sceneVersion)
        writeNodeStr(fileID,"SceneName", SceneName)
        writeNodeBool(fileID,"IsActive", False )
        writeNodeInt(fileID,"SeqStart",seqStart)
        writeNodeInt(fileID,"SeqEnd",seqEnd)
        writeNodeInt(fileID,"SeqStep",seqStep)
        writeNodeStr(fileID,"Layer",layerName)
        writeNodeStr(fileID,"ImageFilename",ImageFilename)
        writeNodeStr(fileID,"ImageExtension",imageExtension)
        fileID.write("</Job>\n")
        
    fileID.write("</rrJob_submitFile>\n")
    fileID.close()
    RR_ROOT=getRR_Root()
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        os.system("\""+RR_ROOT+"\\win__rrSubmitter.bat\"  "+TempFileName)
    elif (sys.platform.lower() == "darwin"):
        os.system("\""+RR_ROOT+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter\"  "+TempFileName)
    else:
        os.system("\""+RR_ROOT+"/lx__rrSubmitter.sh\"  "+TempFileName)
    return

rrSubmit()
