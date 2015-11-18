#python
# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Plugin script for Modo
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 7.0.24
# Copyright (c) Holger Schoenberger - Binary Alchemy
# 
######################################################################

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

import lx
import lxu
from lxu import select
scene_service = lx.service.Scene()
current_scene = lxu.select.SceneSelection().current()



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


class rrJob(object):
         
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.version = ""
        self.software = ""
        self.renderer = ""
        self.RequiredLicenses = ""
        self.sceneName = ""
        self.sceneDatabaseDir = ""
        self.seqStart = 0
        self.seqEnd = 100
        self.seqStep = 1
        self.seqFileOffset = 0
        self.seqFrameSet = ""
        self.imageWidth = 99
        self.imageHeight = 99
        self.imageDir = ""
        self.imageFilename = ""
        self.imageFramePadding = 4
        self.imageExtension = ""
        self.imagePreNumberLetter = ""
        self.imageSingleOutput = False
        self.sceneOS = ""
        self.camera = ""
        self.layer = ""
        self.channel = ""
        self.maxChannels = 0
        self.channelFileName = []
        self.channelExtension = []
        self.isActive = False
        self.sendAppBit = ""
        self.preID = ""
        self.waitForPreID  = ""
        self.CustomA  = ""
        self.CustomB  = ""
        self.CustomC  = ""
        self.LocalTexturesFile  = ""
        self.ImageStereoL=""
        self.ImageStereoR=""
        self.isStereo= False

    # from infix.se (Filip Solomonsson)
    def indent(self, elem, level=0):
        i = "\n" + level * ' '
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + " "
            for e in elem:
                self.indent(e, level + 1)
                if not e.tail or not e.tail.strip():
                    e.tail = i + " "
            if not e.tail or not e.tail.strip():
                e.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
        return True

    def subE(self, r, e, text):
        sub = SubElement(r, e)
        sub.text = str(text).decode("utf8")
        return sub

    def writeToXMLstart(self, submitOptions ):
        rootElement = Element("rrJob_submitFile")
        rootElement.attrib["syntax_version"] = "6.0"
        self.subE(rootElement, "DeleteXML", "1")
        self.subE(rootElement, "SubmitterParameter", submitOptions)
        # YOU CAN ADD OTHER NOT SCENE-INFORMATION PARAMETERS USING THIS FORMAT:
        # self.subE(jobElement,"SubmitterParameter","PARAMETERNAME=" + PARAMETERVALUE_AS_STRING)
        return rootElement

    def writeToXMLJob(self, rootElement):
        jobElement = self.subE(rootElement, "Job", "")
        self.subE(jobElement, "Software", self.software)
        self.subE(jobElement, "Renderer", self.renderer)
        self.subE(jobElement, "RequiredLicenses", self.RequiredLicenses)
        self.subE(jobElement, "Version", self.version)
        self.subE(jobElement, "SceneName", self.sceneName)
        self.subE(jobElement, "SceneDatabaseDir", self.sceneDatabaseDir)
        self.subE(jobElement, "IsActive", self.isActive)
        self.subE(jobElement, "SeqStart", self.seqStart)
        self.subE(jobElement, "SeqEnd", self.seqEnd)
        self.subE(jobElement, "SeqStep", self.seqStep)
        self.subE(jobElement, "SeqFileOffset", self.seqFileOffset)
        self.subE(jobElement, "SeqFrameSet", self.seqFrameSet)
        self.subE(jobElement, "ImageWidth", int(self.imageWidth))
        self.subE(jobElement, "ImageHeight", int(self.imageHeight))
        self.subE(jobElement, "ImageDir", self.imageDir)
        self.subE(jobElement, "ImageFilename", self.imageFilename)
        self.subE(jobElement, "ImageFramePadding", self.imageFramePadding)
        self.subE(jobElement, "ImageExtension", self.imageExtension)
        self.subE(jobElement, "ImageSingleOutput", self.imageSingleOutput)
        self.subE(jobElement, "ImagePreNumberLetter", self.imagePreNumberLetter)
        self.subE(jobElement, "ImageStereoL", self.ImageStereoL)
        self.subE(jobElement, "ImageStereoR", self.ImageStereoR)
        self.subE(jobElement, "SceneOS", self.sceneOS)
        self.subE(jobElement, "Camera", self.camera)
        self.subE(jobElement, "Layer", self.layer)
        self.subE(jobElement, "Channel", self.channel)
        self.subE(jobElement, "SendAppBit", self.sendAppBit)
        self.subE(jobElement, "PreID", self.preID)
        self.subE(jobElement, "WaitForPreID", self.waitForPreID)
        self.subE(jobElement, "CustomA", self.CustomA)
        self.subE(jobElement, "CustomB", self.CustomB)
        self.subE(jobElement, "CustomC", self.CustomC)
        self.subE(jobElement, "LocalTexturesFile", self.LocalTexturesFile)
        for c in range(0,self.maxChannels):
           self.subE(jobElement,"ChannelFilename",self.channelFileName[c])
           self.subE(jobElement,"ChannelExtension",self.channelExtension[c])
        return True



    def writeToXMLEnd(self, f,rootElement):
        xml = ElementTree(rootElement)
        self.indent(xml.getroot())
        if not f == None:
            xml.write(f)
            f.close()
        else:
            writeError("No valid file has been passed to the function")
            try:
                f.close()
            except:
                pass
            return False
        return True



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
    return rrSubmitter


def getOSString():
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        return "win"
    elif (sys.platform.lower() == "darwin"):
        return "osx"
    else:
        return "lx"

    
def submitJobsToRR(jobList,submitOptions):
    tmpFileName = getNewTempFileName()
    tmpFile = open(tmpFileName, "w")
    xmlObj= jobList[0].writeToXMLstart(submitOptions)
    for submitjob in jobList:
        submitjob.writeToXMLJob(xmlObj)
    ret = jobList[0].writeToXMLEnd(tmpFile,xmlObj)
    if ret:
        writeInfo("Job written to " + tmpFile.name)
    else:
        writeError("Error - There was a problem writing the job file to " + tmpFile.name)
    os.system(getRRSubmitterPath()+"  \""+tmpFileName+"\"")


###########################################
# Read Modo file                          #
###########################################

            

def dublicateJobsWithNewCam(jobList, camName, baseNrJobs):
    for c in range(0, baseNrJobs):
        if (camName!=jobList[c].camera):
            newJob= rrJob()
            newJob= copy.copy(jobList[c])
            newJob.camera = camName
            newJob.isActive = False;
            jobList.append(newJob)


def applyStereoSettings(jobList, camNames, camStereo, camEye, camComp):
    for j in range(0, len(jobList)):
        for c in range(0, len(camNames)):
            if (camNames[c]==jobList[j].camera):
                if (not camStereo[c]):
                    jobList[j].imageFilename = jobList[j].imageFilename.replace("<StereoRL>", "")
                    
                
               
            

class _sceneInfo(object):
    def __init__(self):
        pService= lx.Service('platformservice')
        sService= lx.Service( "sceneservice" )
        self.version= str(pService.query("appversion"))
        self.version=self.version[:1]  + "."
        appBuild= pService.query("appbuild")
        appPath= lx.eval( "query platformservice path.path ? program" )
        appPath=appPath.upper()
        if (appPath.find("_SP")>0):
            appPath = appPath[appPath.find('_SP') + 3:]
            appPath = appPath[:1]
            if (appPath.isdigit()):
                self.version=self.version+appPath
        self.software = "Modo"
        self.sceneOS = getOSString()
        self.sceneName = lx.eval( "query sceneservice scene.file ? current" )
        rend = current_scene.AnyItemOfType(scene_service.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
        chan = current_scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
        idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_RESX)
        self.imageWidth = chan.Integer(rend, idx)
        self.imageHeight = chan.Integer(rend, idx + 1)
        idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_FIRST)
        self.seqStart = chan.Integer(rend, idx)
        idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_LAST)
        self.seqEnd = chan.Integer(rend, idx)
        idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_STEP)
        self.seqStep = chan.Integer(rend, idx)
        self.camera = rrSubmit_getNodeName(lx.eval( "render.camera ?"))
        self.ImageStereoL="L"
        self.ImageStereoR="R"


    

def rrSubmit_getNodeName(nodeName):
    lx.eval( "select.item "+nodeName)
    return lx.eval( "item.name ?")


def rrSubmit_fillGlobalSceneInfo(newJob,sceneInfo):
    newJob.version= sceneInfo.version
    newJob.software = sceneInfo.software
    newJob.sceneOS = sceneInfo.sceneOS
    newJob.sceneName = sceneInfo.sceneName
    newJob.seqStart =  sceneInfo.seqStart
    newJob.seqEnd= sceneInfo.seqEnd
    newJob.seqStep= sceneInfo.seqStep
    newJob.imageWidth= sceneInfo.imageWidth
    newJob.imageHeight= sceneInfo.imageHeight
    newJob.camera = sceneInfo.camera
    newJob.ImageStereoL = sceneInfo.ImageStereoL
    newJob.ImageStereoR = sceneInfo.ImageStereoR
    newJob.imageFilename = ""
    

    

def rrSubmit_GetImageExtension(imageExtension):
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
        return imageExtension



def rrSubmit_AddPattern(imageFilename,sceneInfo):
    rend = current_scene.AnyItemOfType(scene_service.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
    chan = current_scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
    idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_OUTPAT)
    outPattern = chan.String(rend, idx)
    if (outPattern==None or (len(outPattern)==0)):
        outPattern="<FFFF>"
    outPattern= outPattern.replace("[<LR>]","<StereoRL>")
    outPattern= outPattern.replace("<LR>","<StereoRL>")
    outPattern= outPattern.replace("[<output>]","<Layer>")
    outPattern= outPattern.replace("<output>","<Layer>")
    outPattern= outPattern.replace("[<camera>]","<Camera>")
    outPattern= outPattern.replace("[<pass>]","<Channel>")
    outPattern= outPattern.replace("<pass>","<Channel>")
    outPattern= outPattern.replace("<F>","#")
    outPattern= outPattern.replace("<FF>","##")
    outPattern= outPattern.replace("<FFF>","###")
    outPattern= outPattern.replace("<FFFF>","####")
    outPattern= outPattern.replace("<FFFFF>","#####")
    outPattern= outPattern.replace("<FFFFFF>","######")
    outPattern= outPattern.replace(".ext","")
    imageFilename = imageFilename + outPattern
    return imageFilename


#Get all pass groups with all passes and per-pass renderlayer  overrides:
class passGroup:
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.name = ""
        self.passes = []
        self.layer = []
        self.layerEnabled = []

def getPassInfo(passGroupList):
    scService = lx.Service( "sceneservice" )
    allItems= scService.query("item.N")
    for obj in range(allItems):
        scService.select("item.id",str(obj))
        if (str(scService.query('item.type'))== "group"):
            gTags=scService.query("render.tags")
            if (gTags!=None and gTags=="render"):
                newPassGr= passGroup()
                newPassGr.name=scService.query('item.name')
                #print ("Pass Group "+newPassGr.name)
                passInternal=scService.query("pass.itemMembers")
                if (passInternal==None):
                    continue
                if (type(passInternal)==str):
                    passInternal=(passInternal,)
                #print ("Pass Group "+newPassGr.name+"   "+str(type(passInternal)))
                for pas in passInternal:
                    name=lx.eval("item.name ? item:{%s}" % pas)
                    newPassGr.passes.append(name)
                    #print ("    -pass "+name)
                    scServiceP = lx.Service( "sceneservice" )
                    allAC= scServiceP.query("actionItem.N")
                    for act in range(allAC):
                        if (name!=lx.eval( "query sceneservice actionItem.name  ? %s" % act)):
                            continue
                        allChan=lx.eval( "query sceneservice actionItem.channels  ? %s" % act)
                        if (type(allChan)==str):
                            allChan=(allChan,)
                        if (type(allChan)==tuple):
                            for chn in allChan:
                                if (chn.startswith("renderOutput") and chn.endswith(":enable")):
                                    chnValue=lx.eval( "query sceneservice actionItem.chanValue  ? {%s}" % chn)
                                    chn= chn[:chn.find(":")]
                                    chn=lx.eval( "query sceneservice item.name  ? %s" % chn)
                                    newPassGr.layer.append(chn)
                                    newPassGr.layerEnabled.append(chnValue=="1")
                                    #print("      override:     "+chn+"  "+str(chnValue))
                passGroupList.append(newPassGr)



#one job to render all layers, but no passes
def rrSubmit_CreateAllLayerJob(jobList,sceneInfo,passGroups):
    newJob= rrJob()
    rrSubmit_fillGlobalSceneInfo(newJob,sceneInfo)
    nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
    firstFound=False
    newJob.layer="** All **"
    for L in range(0, nbOutputs):
        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
        lx.eval( "select.item "+objID)
        imgName= lx.eval( "item.channel renderOutput$filename ? " );
        if ((imgName==None) or (len(imgName)==0)):
            continue
        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
        if (not isEnabled):
            continue
        layerName= lx.eval("item.name ?")
        if (layerName!="Final Color Output"):
            continue
        newJob.imageExtension=lx.eval( "item.channel renderOutput$format ?" );
        if (newJob.imageExtension==None):
            writeError("You have not set an image extension for '"+layerName+"'\n. Please use the browse... button")
        newJob.imageExtension=rrSubmit_GetImageExtension(newJob.imageExtension)
        imgName= rrSubmit_AddPattern(imgName,sceneInfo)
        imgName= imgName.replace("<Channel>","")
        imgName= imgName.replace("<Layer>",layerName)
        newJob.imageFilename=imgName
        firstFound=True
        break
    
    for L in range(0, nbOutputs):
        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
        lx.eval( "select.item "+objID)
        imgName= lx.eval( "item.channel renderOutput$filename ? " );
        if ((imgName==None) or (len(imgName)==0)):
            continue
        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
        if (not isEnabled):
            continue
        layerName= lx.eval("item.name ?")
        if (layerName=="Final Color Output"):
            continue
        if (not firstFound):
            newJob.imageExtension=lx.eval( "item.channel renderOutput$format ?" );
            if (newJob.imageExtension==None):
                writeError("You have not set an image extension for '"+layerName+"'\n. Please use the browse... button")
            newJob.imageExtension=rrSubmit_GetImageExtension(newJob.imageExtension)
            imgName= rrSubmit_AddPattern(imgName,sceneInfo)
            imgName= imgName.replace("<Channel>","")
            imgName= imgName.replace("<Layer>",layerName)
            newJob.imageFilename=imgName
            firstFound=True
        else:
            imgExt=lx.eval( "item.channel renderOutput$format ?" );
            if (imgExt==None):
                writeError("You have not set an image extension for '"+layerName+"'\n. Please use the browse... button")
            imgExt=rrSubmit_GetImageExtension(imgExt)
            imgName= rrSubmit_AddPattern(imgName,sceneInfo)
            imgName= imgName.replace("<Channel>","")
            imgName= imgName.replace("<Layer>",layerName)
            newJob.channelFileName.append(imgName)
            newJob.channelExtension.append(imgExt)
            newJob.maxChannels= newJob.maxChannels + 1
    jobList.append(newJob)


#loop all render layers and add them as job
#Renders one Layer with all pass groups and passes
def rrSubmit_CreateLayerJobs(jobList,sceneInfo,passGroups):
    nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
    for L in range(0, nbOutputs):
        newJob= rrJob()
        rrSubmit_fillGlobalSceneInfo(newJob,sceneInfo)
        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
        lx.eval( "select.item "+objID)
        newJob.imageFilename= lx.eval( "item.channel renderOutput$filename ? " );
        if ((newJob.imageFilename==None) or (len(newJob.imageFilename)==0)):
            continue
        newJob.layer=lx.eval("item.name ?")
        #isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
        #if (not isEnabled):
        #    continue
        newJob.imageExtension=lx.eval( "item.channel renderOutput$format ?" );
        if (newJob.imageExtension==None):
            writeError("You have not set an image extension for '"+newJob.layer+"'\n. Please use the browse... button")
        newJob.imageExtension=rrSubmit_GetImageExtension(newJob.imageExtension)
        newJob.imageFilename= rrSubmit_AddPattern(newJob.imageFilename,sceneInfo)
        for pg in range(0, len(passGroupList)):
            for p in range(0,len(passGroupList[pg].passes)):
                imgName= newJob.imageFilename
                imgName= imgName.replace("<Channel>",passGroupList[pg].passes[p])
                newJob.channelFileName.append(imgName)
                newJob.channelExtension.append(newJob.imageExtension)
                newJob.maxChannels= newJob.maxChannels + 1
        newJob.imageFilename= newJob.imageFilename.replace("<Channel>","")
        jobList.append(newJob)


#create a job per pass group
#renders all passes of this group and all layers
def rrSubmit_CreatePassJobs(jobList,sceneInfo,passGroup):
    newJob= rrJob()
    rrSubmit_fillGlobalSceneInfo(newJob,sceneInfo)
    newJob.channel=passGroup.name
    newJob.isActive=True
    newJob.layer="** All **"
    nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
    for L in range(0, nbOutputs):
        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
        lx.eval( "select.item "+objID)
        imgName= lx.eval( "item.channel renderOutput$filename ? " );
        if ((imgName==None) or (len(imgName)==0)):
            continue
        layerName= lx.eval("item.name ?")
        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
        overrideFound=False
        for p in range(1,len(passGroup.layer)):
            if (layerName!=passGroup.layer[p]):
                continue
            if (not overrideFound):
                #print("Pass "+passGroup.name+"+Layer "+layerName+" found first override "+str(passGroup.layerEnabled[p]))
                isEnabled=passGroup.layerEnabled[p]
                overrideFound=True
            elif passGroup.layerEnabled[p]:
                #print("Pass "+passGroup.name+"+Layer "+layerName+" found another override "+str(passGroup.layerEnabled[p]))
                isEnabled=True
        if (not isEnabled):
            continue
        #print("Pass "+passGroup.name+"+Layer "+newJob.rrSubmit_CreatePassJobs(jobList,sceneInfo,passGroup):layer+" is enabled")
        
        if (layerName!="Final Color Output"):
            continue
        imgName= rrSubmit_AddPattern(imgName,sceneInfo)
        imgName= imgName.replace("<Layer>","<Layer-replaceVar "+layerName +">")
        imgExt=lx.eval( "item.channel renderOutput$format ?" );
        if (imgExt==None):
            writeError("You have not set an image extension for '"+layerName+"'\n. Please use the browse... button")
        imgExt=rrSubmit_GetImageExtension(imgExt)
        if (len(newJob.imageFilename)==0):
            newJob.imageFilename= imgName
            newJob.imageExtension= imgExt
        else:
            newJob.channelFileName.append(imgName)
            newJob.channelExtension.append(imgExt)
            newJob.maxChannels= newJob.maxChannels + 1
        break
    
    for L in range(0, nbOutputs):
        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
        lx.eval( "select.item "+objID)
        imgName= lx.eval( "item.channel renderOutput$filename ? " );
        if ((imgName==None) or (len(imgName)==0)):
            continue
        layerName= lx.eval("item.name ?")
        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
        overrideFound=False
        for p in range(1,len(passGroup.layer)):
            if (layerName!=passGroup.layer[p]):
                continue
            if (not overrideFound):
                #print("Pass "+passGroup.name+"+Layer "+layerName+" found first override "+str(passGroup.layerEnabled[p]))
                isEnabled=passGroup.layerEnabled[p]
                overrideFound=True
            elif passGroup.layerEnabled[p]:
                #print("Pass "+passGroup.name+"+Layer "+layerName+" found another override "+str(passGroup.layerEnabled[p]))
                isEnabled=True
        if (not isEnabled):
            continue
        #print("Pass "+passGroup.name+"+Layer "+newJob.rrSubmit_CreatePassJobs(jobList,sceneInfo,passGroup):layer+" is enabled")
        if (layerName=="Final Color Output"):
            continue
        imgName= rrSubmit_AddPattern(imgName,sceneInfo)
        imgName= imgName.replace("<Layer>","<Layer-replaceVar "+layerName +">")
        imgExt=lx.eval( "item.channel renderOutput$format ?" );
        if (imgExt==None):
            writeError("You have not set an image extension for '"+layerName+"'\n. Please use the browse... button")
        imgExt=rrSubmit_GetImageExtension(imgExt)
        if (len(newJob.imageFilename)==0):
            newJob.imageFilename= imgName
            newJob.imageExtension= imgExt
        else:
            newJob.channelFileName.append(imgName)
            newJob.channelExtension.append(imgExt)
            newJob.maxChannels= newJob.maxChannels + 1
            
    maxChannelsOld = newJob.maxChannels
    for p in range(1,len(passGroup.passes)):
            imgName= newJob.imageFilename
            imgExt= newJob.imageExtension
            imgName= imgName.replace("<Channel>",passGroup.passes[p])
            newJob.channelFileName.append(imgName)
            newJob.channelExtension.append(imgExt)
            newJob.maxChannels= newJob.maxChannels + 1
            for c in range(0,maxChannelsOld):
                imgName= newJob.channelFileName[c]
                imgExt= newJob.channelExtension[c]
                imgName= imgName.replace("<Channel>",passGroup.passes[p])
                newJob.channelFileName.append(imgName)
                newJob.channelExtension.append(imgExt)
                newJob.maxChannels= newJob.maxChannels + 1
    newJob.imageFilename= newJob.imageFilename.replace("<Channel>","<Channel-replaceVar "+passGroup.passes[0]+">")
    for c in range(0,maxChannelsOld):
        imgName= newJob.channelFileName[c]
        imgName= imgName.replace("<Channel>",passGroup.passes[0])
        newJob.channelFileName[c]= imgName
    jobList.append(newJob)





def get_items_by_type(itype):
    ''' returns all items in the scene of type itype '''
    items = []
    # lookup the item type
    item_type = scene_service.ItemTypeLookup(itype)
    # get a count of itype items in the scene
    numitems = current_scene.ItemCount(item_type)
    for x in range(numitems):
        items.append(current_scene.ItemByIndex(item_type, x))
    return items


        


##############################################################################
    #MAIN "FUNCTION":
##############################################################################

writeInfo ("rrSubmit v 7.0.24")
SceneName = lx.eval( "query sceneservice scene.file ? current" )
if ((SceneName==None) or (len(SceneName)==0)):
    writeError("Scene was never saved.")
    sys.exit(0)
sceneWasChanged = lx.eval( "query sceneservice scene.changed ? current" )
if (sceneWasChanged):
    lx.eval("dialog.setup saveOK");
    lx.eval("dialog.title {rrSubmit}");
    lx.eval("dialog.msg {This scene was not changed, would you like to save it?}");
    try:
        lx.eval("dialog.open");
        QRes= lx.eval("dialog.result ?")
    except:
        QRes= lx.eval("dialog.result ?")
    if (QRes=="cancel"):
        sys.exit(0)
    if (QRes=="ok"):
        lx.out( "Saving scene..." )
        lx.eval( "scene.save" )
        


jobList= []
sceneInfo = _sceneInfo()

#get pass groups and enable/disable for each output layer
passGroupList=[];
getPassInfo(passGroupList)

#create jobs for each render layer, it renders all pass groups
rrSubmit_CreateAllLayerJob(jobList,sceneInfo,passGroupList)
#print (len(jobList))

#create jobs for each render layer, it renders all pass groups
rrSubmit_CreateLayerJobs(jobList,sceneInfo,passGroupList)
#print (len(jobList))

#create jobs for each pass group, render all Layer
for pg in range(0, len(passGroupList)):
    rrSubmit_CreatePassJobs(jobList,sceneInfo,passGroupList[pg])
#print (len(jobList))

                      

#Get camera list and dublicate jobs for each camera
baseNrJobs= len(jobList)
cameraNames=[]
cameraStereo=[]
cameraEye=[]
cameraComposite=[]
cameras=get_items_by_type("camera")
for cam in cameras:
    cameraNames.append(cam.UniqueName())
    chan = current_scene.Channels(None, 0.0)
    idx = cam.ChannelLookup(lx.symbol.sICHAN_CAMERA_STEREO)
    cameraStereo.append(chan.Integer(cam, idx))
    idx = cam.ChannelLookup(lx.symbol.sICHAN_CAMERA_STEREO_EYE)
    cameraEye.append(chan.Integer(cam, idx))
    idx = cam.ChannelLookup(lx.symbol.sICHAN_CAMERA_STEREO_COMP)
    cameraComposite.append(chan.Integer(cam, idx))
    dublicateJobsWithNewCam(jobList,cam.UniqueName(),baseNrJobs)

#replace stereo <LR> if there is no stereo
applyStereoSettings(jobList,cameraNames,cameraStereo,cameraEye,cameraComposite)

    
submitOptions=""
if (len(jobList)==0):
    writeError("No render layer enabled or no output set for a layer.")
else:
    submitJobsToRR(jobList,submitOptions)




