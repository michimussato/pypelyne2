#python
# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Plugin script for Modo
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 6.02.31
# Copyright (c) Holger Schoenberger - Binary Alchemy
# 
######################################################################

import lx
import os
import sys
import random

import os
import sys
import platform
import random
import string
import time
import copy

from xml.etree.ElementTree import ElementTree, Element, SubElement


#####################################################################################
# This function has to be changed if an app should show info and error dialog box   #
#####################################################################################

def writeInfo(msg):
    lx.out(msg)

def writeError(msg):
    lx.eval("dialog.setup error");
    lx.eval("dialog.title {Warning}");
    lx.eval("dialog.msg {"+msg+"}");
    lx.eval("dialog.open"); 



##############################################
# JOB CLASS                                  #
##############################################

##
##class rrJob(object):
##    """Stores scene information """
##    version = ""
##    software = ""
##    renderer = ""
##    RequiredLicenses = ""
##    sceneName = ""
##    sceneDatabaseDir = ""
##    seqStart = 0
##    seqEnd = 100
##    seqStep = 1
##    seqFileOffset = 0
##    seqFrameSet = ""
##    imageWidth = 99
##    imageHeight = 99
##    imageDir = ""
##    imageFilename = ""
##    imageFramePadding = 4
##    imageExtension = ""
##    imagePreNumberLetter = ""
##    imageSingleOutput = False
##    sceneOS = ""
##    camera = ""
##    layer = ""
##    channel = ""
##    maxChannels = 0
##    channelFileName = []
##    channelExtension = []
##    isActive = False
##    sendAppBit = ""
##    preID = ""
##    waitForPreID  = ""
##    CustomA  = ""
##    CustomB  = ""
##    CustomC  = ""
##    LocalTexturesFile  = ""
##        
##    def __init__(self):
##        pass
##
##    # from infix.se (Filip Solomonsson)
##    def indent(self, elem, level=0):
##        i = "\n" + level * ' '
##        if len(elem):
##            if not elem.text or not elem.text.strip():
##                elem.text = i + " "
##            for e in elem:
##                self.indent(e, level + 1)
##                if not e.tail or not e.tail.strip():
##                    e.tail = i + " "
##            if not e.tail or not e.tail.strip():
##                e.tail = i
##        else:
##            if level and (not elem.tail or not elem.tail.strip()):
##                elem.tail = i
##        return True
##
##    def subE(self, r, e, t):
##        sub = SubElement(r, e)
##        sub.text = str(t)
##        return sub
##
##    def writeToXMLstart(self ):
##        rootElement = Element("rrJob_submitFile")
##        rootElement.attrib["syntax_version"] = "6.0"
##        self.subE(rootElement, "DeleteXML", "1")
##        return rootElement
##
##    def writeToXMLJob(self, rootElement):
##        # YOU CAN ADD OTHER NOT SCENE-INFORMATION PARAMETERS USING THIS FORMAT:
##        # self.subE(jobElement,"SubmitterParameter","PARAMETERNAME=" + PARAMETERVALUE_AS_STRING)
##
##        jobElement = self.subE(rootElement, "Job", "")
##        self.subE(jobElement, "Software", self.software)
##        self.subE(jobElement, "Renderer", self.renderer)
##        self.subE(jobElement, "RequiredLicenses", self.RequiredLicenses)
##        self.subE(jobElement, "Version", self.version)
##        self.subE(jobElement, "SceneName", self.sceneName)
##        self.subE(jobElement, "SceneDatabaseDir", self.sceneDatabaseDir)
##        self.subE(jobElement, "IsActive", self.isActive)
##        self.subE(jobElement, "SeqStart", self.seqStart)
##        self.subE(jobElement, "SeqEnd", self.seqEnd)
##        self.subE(jobElement, "SeqStep", self.seqStep)
##        self.subE(jobElement, "SeqFileOffset", self.seqFileOffset)
##        self.subE(jobElement, "SeqFrameSet", self.seqFrameSet)
##        self.subE(jobElement, "ImageWidth", int(self.imageWidth))
##        self.subE(jobElement, "ImageHeight", int(self.imageHeight))
##        self.subE(jobElement, "ImageDir", self.imageDir)
##        self.subE(jobElement, "ImageFilename", self.imageFilename)
##        self.subE(jobElement, "ImageFramePadding", self.imageFramePadding)
##        self.subE(jobElement, "ImageExtension", self.imageExtension)
##        self.subE(jobElement, "ImageSingleOutput", self.imageSingleOutput)
##        self.subE(jobElement, "ImagePreNumberLetter", self.imagePreNumberLetter)
##        self.subE(jobElement, "SceneOS", self.sceneOS)
##        self.subE(jobElement, "Camera", self.camera)
##        self.subE(jobElement, "Layer", self.layer)
##        self.subE(jobElement, "Channel", self.channel)
##        self.subE(jobElement, "SendAppBit", self.sendAppBit)
##        self.subE(jobElement, "PreID", self.preID)
##        self.subE(jobElement, "WaitForPreID", self.waitForPreID)
##        self.subE(jobElement, "CustomA", self.CustomA)
##        self.subE(jobElement, "CustomB", self.CustomB)
##        self.subE(jobElement, "CustomC", self.CustomC)
##        self.subE(jobElement, "LocalTexturesFile", self.LocalTexturesFile)
##        for c in range(0,self.maxChannels):
##           self.subE(jobElement,"ChannelFilename",self.channelFileName[c])
##           self.subE(jobElement,"ChannelExtension",self.channelExtension[c])
##        return True
##
##
##
##    def writeToXMLEnd(self, f,rootElement):
##        xml = ElementTree(rootElement)
##        self.indent(xml.getroot())
##
##        if not f == None:
##            xml.write(f)
##            f.close()
##        else:
##            print("No valid file has been passed to the function")
##            try:
##                f.close()
##            except:
##                pass
##            return False
##        return True



##############################################
# Global Functions                           #
##############################################

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
    writeError("This plugin was not installed via rrWorkstationInstaller!")


def getNewTempFileName():
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

def getRRSubmitterPath():
    ''' returns the rrSubmitter filename '''
    rrRoot = getRR_Root()
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        rrSubmitter = rrRoot+"\\win__rrSubmitter.bat"
    elif (sys.platform.lower() == "darwin"):
        rrSubmitter = rrRoot+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter"
    else:
        rrSubmitter = rrRoot+"/lx__rrSubmitter.sh"
        #writeInfo("Starting "+rrSubmitter)
    return rrSubmitter


def getOSString():
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        return "win"
    elif (sys.platform.lower() == "darwin"):
        return "osx"
    else:
        return "lx"

##    
##def submitJobsToRR(jobList):
##    tmpFileName = getNewTempFileName()
##    tmpFile = open(tmpFileName, "w")
##    if (len(jobList) == 0):
##        writeError("Error - No job to send\n (Could be an empty Output Filename)")
##        return
##    xmlObj= jobList[0].writeToXMLstart()
##    for submitjob in jobList:
##        submitjob.writeToXMLJob(xmlObj)
##    ret = jobList[0].writeToXMLEnd(tmpFile,xmlObj)
##    if not ret:
##        writeError("Error - There was a problem writing the job file to " + tmpFile.name)
##    os.system(getRRSubmitterPath()+"  \""+tmpFileName+"\"")
##
##def dublicateJobsWithNewCam(jobList, camName, baseNrJobs):
##    for c in range(0, baseNrJobs):
##        if (camName!=jobList[c].camera):
##            newJob= rrJob()
##            newJob= copy.copy(jobList[c])
##            newJob.camera = camName
##            newJob.isActive = False;
##            jobList.append(newJob)
##
##def dublicateJobsWithNewPass(jobList, passname, baseNrJobs):
##    for c in range(0, baseNrJobs):
##        if (passname!=jobList[c].channel):
##            newJob= rrJob()
##            newJob= copy.copy(jobList[c])
##            newJob.channel = passname
##            newJob.isActive = False;
##            jobList.append(newJob)
##    

###########################################
# Read Modo file                          #
###########################################

##
##class _sceneInfo(object):
##    def __init__(self):
##        self.version= lx.eval( "query platformservice appversion ?")
##        self.version=str(self.version)
##        sceneBuild= lx.eval( "query platformservice appbuild ?")
##        self.version=self.version[:1]  + "."
##        self.software = "Modo"
##        self.sceneOS = getOSString()
##        self.sceneName = lx.eval( "query sceneservice scene.file ? current" )
##        lx.eval( "select.itemType polyRenders")
##        self.seqStart = lx.eval( "item.channel first ?")
##        self.seqEnd= lx.eval( "item.channel last ?")
##        self.seqStep= lx.eval( "item.channel step ?")
##        self.imageWidth= lx.eval( "render.res 0 ?")
##        self.imageHeight= lx.eval( "render.res 1 ?")
##        self.camera = rrSubmit_getNodeName(lx.eval( "render.camera ?"))
##        self.imageFilename = ""
##        lx.eval( "select.itemType polyRenders")
##        self.isStereo= lx.eval("render.stereo ?");
##        self.stereoEye= 0;
##        self.stereoComposite= 4;
##        if self.isStereo:
##            self.stereoEye= lx.eval("render.stereoEye ?");
##            self.stereoComposite= lx.eval("render.stereoComposite ?");
##        
##    
##
##def rrSubmit_getNodeName(nodeName):
##    lx.eval( "select.item "+nodeName)
##    return lx.eval( "item.name ?")
##
##
##def rrSubmit_fillGlobalSceneInfo(newJob,sceneInfo):
##    newJob.version= sceneInfo.version
##    newJob.software = sceneInfo.software
##    newJob.sceneOS = sceneInfo.sceneOS
##    newJob.sceneName = sceneInfo.sceneName
##    newJob.seqStart =  sceneInfo.seqStart
##    newJob.seqEnd= sceneInfo.seqEnd
##    newJob.seqStep= sceneInfo.seqStep
##    newJob.imageWidth= sceneInfo.imageWidth
##    newJob.imageHeight= sceneInfo.imageHeight
##    newJob.camera = sceneInfo.camera
##    newJob.imageFilename = ""
##    
##
##    
##
##def rrSubmit_GetImageExtension(imageExtension):
##        if (imageExtension=="$FLEX"):
##            imageExtension=".flx"
##        elif (imageExtension=="$Targa"):
##            imageExtension=".tga"
##        elif (imageExtension=="BMP"):
##            imageExtension=".bmp"
##        elif (imageExtension=="HDR"):
##            imageExtension=".hdr"
##        elif (imageExtension=="JP2"):
##            imageExtension=".jp2"
##        elif (imageExtension=="JP216"):
##            imageExtension=".jp2"
##        elif (imageExtension=="JP216Lossless"):
##            imageExtension=".jp2"
##        elif (imageExtension=="JPG"):
##            imageExtension=".jpg"
##        elif (imageExtension=="PNG"):
##            imageExtension=".png"
##        elif (imageExtension=="PNG16"):
##            imageExtension=".png"
##        elif (imageExtension=="PSD"):
##            imageExtension=".psd"
##        elif (imageExtension=="SGI"):
##            imageExtension=".sgi"
##        elif (imageExtension=="TIF"):
##            imageExtension=".tif"
##        elif (imageExtension=="TIF16BIG"):
##            imageExtension=".tif"
##        elif (imageExtension=="TIF16"):
##            imageExtension=".tif"
##        elif (imageExtension=="openexr"):
##            imageExtension=".exr"
##        elif (imageExtension=="openexr_32"):
##            imageExtension=".exr"
##        elif (imageExtension=="openexr_tiled16"):
##            imageExtension=".exr"
##        elif (imageExtension=="openexr_tiled32"):
##            imageExtension=".exr"
##        else:
##            imageExtension="."+imageExtension
##        return imageExtension
##
##
##
##def rrSubmit_AddPattern(imageFilename,sceneInfo):
##    lx.eval( "select.itemType polyRenders")
##    outPattern = lx.eval( "item.channel outPat ?")
##    outPattern= outPattern.replace("[<LR>]","<StereoRL>")
##    outPattern= outPattern.replace("<LR>","<StereoRL>")
##    outPattern= outPattern.replace("[<output>]","<Layer>")
##    outPattern= outPattern.replace("<output>","<Layer>")
##    outPattern= outPattern.replace("[<camera>]","<Camera>")
##    outPattern= outPattern.replace("[<pass>]","<Channel DefaultPass>")
##    outPattern= outPattern.replace("<pass>","<Channel DefaultPass>")
##    outPattern= outPattern.replace("<F>","#")
##    outPattern= outPattern.replace("<FF>","##")
##    outPattern= outPattern.replace("<FFF>","###")
##    outPattern= outPattern.replace("<FFFF>","####")
##    outPattern= outPattern.replace("<FFFFF>","#####")
##    outPattern= outPattern.replace("<FFFFFF>","######")
##    outPattern= outPattern.replace(".ext","")
##    if (sceneInfo.isStereo!=1):
##        outPattern= outPattern.replace("<StereoRL>","")
##    imageFilename = imageFilename + outPattern
##    return imageFilename
##
##
##def rrSubmit_CreateAllJob(jobList,sceneInfo):
##    newJob= rrJob()
##    rrSubmit_fillGlobalSceneInfo(newJob,sceneInfo)
##    nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
##    for L in range(0, nbOutputs):
##        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
##        lx.eval( "select.item "+objID)
##        newJob.imageFilename= lx.eval( "item.channel renderOutput$filename ? " );
##        if ((newJob.imageFilename==None) or (len(newJob.imageFilename)==0)):
##            continue
##        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
##        if (not isEnabled):
##            continue
##        newJob.layer=lx.eval("item.name ?")
##        newJob.imageExtension=lx.eval( "item.channel renderOutput$format ?" );
##        newJob.imageExtension=rrSubmit_GetImageExtension(newJob.imageExtension)
##        newJob.imageFilename=rrSubmit_AddPattern(newJob.imageFilename,sceneInfo)
##        newJob.imageFilename= newJob.imageFilename.replace("<Layer>",newJob.layer)
##        
##        newJob.isActive = True;
##        newJob.layer = "** All **";
##
##        for ch in range(L+1, nbOutputs):
##            objID= lx.eval( "query sceneservice renderOutput.id ? "+str(ch))
##            lx.eval( "select.item "+objID)
##            imageFilename= lx.eval( "item.channel renderOutput$filename ? " );
##            writeInfo (lx.eval( "item.channel renderOutput$effect ? " ))
##            if ((imageFilename==None) or (len(imageFilename)==0)):
##                continue
##            isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
##            if (not isEnabled):
##                continue
##            layername=lx.eval("item.name ?")
##            imageExtension= lx.eval( "item.channel renderOutput$format ? " );
##            imageExtension= rrSubmit_GetImageExtension(imageExtension)
##            imageFilename=rrSubmit_AddPattern(imageFilename,sceneInfo)
##            imageFilename= imageFilename.replace("<Layer>",layername )
##            newJob.channelFileName.append(imageFilename)
##            newJob.channelExtension.append(imageExtension)
##            newJob.maxChannels= newJob.maxChannels+1
##        jobList.append(newJob)
##        #we only need to write "*all*" once, so break
##        break;
##
##
##
##def rrSubmit_CreateLayerJobs(jobList,sceneInfo):
###    scService = lx.Service( "sceneservice" )
###    nbOutputs= scService.query("renderOutput.N")
###    for objID in range(nbOutputs):
###        newJob= rrJob()
###        rrSubmit_fillGlobalSceneInfo(newJob, sceneInfo)
###        scService.select("renderOutput.id",str(objID))
###        newJob.layer=scService.query('item.name')
##    nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
##    for L in range(0, nbOutputs):
##        newJob= rrJob()
##        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
##        lx.eval( "select.item "+objID)
##        newJob.imageFilename= lx.eval( "item.channel renderOutput$filename ? " );
##        if ((newJob.imageFilename==None) or (len(newJob.imageFilename)==0)):
##            continue
##        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
##        if (not isEnabled):
##            continue
##        newJob.layer=lx.eval("item.name ?")
##        newJob.imageExtension=lx.eval( "item.channel renderOutput$format ?" );
##        newJob.imageExtension=rrSubmit_GetImageExtension(newJob.imageExtension)
##        newJob.imageFilename=rrSubmit_AddPattern(newJob.imageFilename,sceneInfo)
###        newJob.imageFilename= newJob.imageFilename.replace("<Layer>",newJob.layer)
##        
##        jobList.append(newJob)
##
##
##def rrSubmit():
##    writeInfo ("rrSubmit v 6.02.31")
##    SceneName = lx.eval( "query sceneservice scene.file ? current" )
##    if ((SceneName==None) or (len(SceneName)==0)):
##        writeError("Scene was never saved.")
##        return
##    sceneWasChanged = lx.eval( "query sceneservice scene.changed ? current" )
##    if (sceneWasChanged):
##        lx.out( "Saving scene..." )
##        lx.eval( "scene.save" )
##
##    jobList= []
###    start = time.clock()
##    sceneInfo = _sceneInfo()
##    rrSubmit_CreateAllJob(jobList,sceneInfo)
###    end = time.clock()
###    writeInfo (str( end - start))
##
##    baseNrJobs= len(jobList)
##    scService = lx.Service( "sceneservice" )
##    nbItems= scService.query("item.N")
##    for obj in range(nbItems):
##        scService.select("item.id",str(obj))
##        if (str(scService.query('item.type'))== "group"):
##            name=scService.query('item.name')
##            dublicateJobsWithNewPass(jobList,name,baseNrJobs)
##
##    baseNrJobs= len(jobList)
##    scService = lx.Service( "sceneservice" )
##    nbItems= scService.query("item.N")
##    for obj in range(nbItems):
##        scService.select("item.id",str(obj))
##        if (str(scService.query('item.type'))== "camera"):
##            name=scService.query('item.name')
##            dublicateJobsWithNewCam(jobList,name,baseNrJobs)
##
##
##    submitJobsToRR(jobList)
##    return


def rrSubmit(): 
    writeInfo ("rrSubmit v 6.02.31")
    SceneName = lx.eval( "query sceneservice scene.file ? current" )
    if ((SceneName==None) or (len(SceneName)==0)):
        writeError("Scene was never saved.")
        return
    sceneWasChanged = lx.eval( "query sceneservice scene.changed ? current" )
    if (sceneWasChanged):
        lx.out( "Saving scene..." )
        lx.eval( "scene.save" )

    rrRoot = getRR_Root()
    if ((SceneName==None) or (len(SceneName)==0)):
        return
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        os.system(rrRoot+"\\win__rrSubmitter.bat  \""+SceneName+"\"")
    elif (sys.platform.lower() == "darwin"):
        os.system(rrRoot+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter  \""+SceneName+"\"")
    else:
        os.system(rrRoot+"/lx__rrSubmitter.sh  \""+SceneName+"\"")




rrSubmit()


