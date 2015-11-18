# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Plugin script for Cinema R13+
# Author:  Michael Auerswald - 908video.de ,  Holger Schoenberger - Binary Alchemy
# Last change: v 7.0.24
# Copyright (c)  Holger Schoenberger 
# #win:   rrInstall_Copy:         plugins\
# #linux: rrInstall_Copy:         plugins\
# #mac:   rrInstall_Copy:         ..\..\..\plugins\
# #win:   rrInstall_Delete:       plugins\rrSubmit_Cinema 4d_11.0+.cof
# #linux: rrInstall_Delete:       plugins\rrSubmit_Cinema 4d_11.0+.cof
# #mac:   rrInstall_Delete:       ..\..\..\plugins\rrSubmit_Cinema 4d_11.0+.cof
# #win:   rrInstall_Delete:       plugins\rrSubmit_Cinema 4d_13.0+.cof
# #linux: rrInstall_Delete:       plugins\rrSubmit_Cinema 4d_13.0+.cof
# #mac:   rrInstall_Delete:       ..\..\..\plugins\rrSubmit_Cinema 4d_13.0+.cof
# 
######################################################################

import c4d
from c4d import gui, plugins
import os
import sys
import tempfile
import logging
import time
from subprocess import call
from xml.etree.ElementTree import ElementTree, Element, SubElement

#########################################################
# To enable tile rendering for sequences as well, set  SHOWTILEDIALOG = True  #
#########################################################

SHOWTILEDIALOG = False


##############################################
# GLOBAL LOGGER                              #
##############################################

LOGGER = logging.getLogger('rrSubmit')
LOGGER.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
LOGGER.addHandler(ch)

##############################################
# GLOBAL FUNCTIONS                           #
##############################################
PLUGIN_ID = 1027715
TILES = 1

def isWin():
    if c4d.GeGetCurrentOS() == c4d.GE_WIN:
        LOGGER.debug("OS: Windows")
        return True
    elif c4d.GeGetCurrentOS() == c4d.GE_MAC:
        LOGGER.debug("OS: Mac")
        return False
    else:
        LOGGER.debug("OS: not found (this should not happen)")
        return False

def rrGetRR_Root():
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
    LOGGER.warning("No RR_ROOT environment variable set!\n Please execute rrWorkstationInstaller and restart the machine.")
    return"";

def PD():
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        return "\\"
    elif (sys.platform.lower() == "darwin"):
        return "/"
    else:
        return "/"
    
##############################################
# JOB CLASS                                  #
##############################################


class rrJob(object):
         
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.version = ""
        self.software = "Cinema 4D"
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
        self.imageFileName = ""
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
        self.isTiledMode= False

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

    def subE(self, r, e, t):
        sub = SubElement(r, e)
        sub.text = str(t)
        return sub

    def writeToXMLstart(self ):
        rootElement = Element("rrJob_submitFile")
        rootElement.attrib["syntax_version"] = "6.0"
        self.subE(rootElement, "DeleteXML", "1")
        self.subE(rootElement, "decodeUTF8", "_")
        return rootElement

    def writeToXMLJob(self, rootElement):
        # YOU CAN ADD OTHER NOT SCENE-INFORMATION PARAMETERS USING THIS FORMAT:
        # self.subE(rootElement,"SubmitterParameter","PARAMETERNAME=" + PARAMETERVALUE_AS_STRING)
        if (self.isTiledMode):
            self.subE(rootElement,"SubmitterParameter","TileFrame=0~0")
            self.subE(rootElement,"SubmitterParameter","PPAssembleTiles=0~1")

        jobElement = self.subE(rootElement, "Job", "")
        self.subE(jobElement, "Software", self.software)
        self.subE(jobElement, "Renderer", self.renderer)
        self.subE(jobElement, "Version", self.versionInfo)
        self.subE(jobElement, "SceneName", self.sceneFilename)
        self.subE(jobElement, "IsActive", "1")
        self.subE(jobElement, "Layer", self.layerName)
        self.subE(jobElement, "SeqStart", self.seqStart)
        self.subE(jobElement, "SeqEnd", self.seqEnd)
        self.subE(jobElement, "SeqStep", self.seqStep)
        self.subE(jobElement, "ImageWidth", int(self.width))
        self.subE(jobElement, "ImageHeight", int(self.height))
        self.subE(jobElement, "ImageFilename", self.imageName)
        self.subE(jobElement, "ImageFramePadding", self.imageFramePadding)
        self.subE(jobElement, "ImageExtension", self.imageFormat)
        self.subE(jobElement, "SceneOS", self.osString)
        self.subE(jobElement, "Camera", self.camera)
        for c in range(0,self.maxChannels):
           self.subE(jobElement,"ChannelFilename",self.channelFileName[c])
           self.subE(jobElement,"ChannelExtension",self.channelExtension[c])
        
#        self.subE(jobElement, "Channel", self.channel)
#        self.subE(jobElement, "preID", self.preID)
#        self.subE(jobElement, "WaitForPreID", self.WaitForPreID)
        return True



    def writeToXMLEnd(self, f,rootElement):
        xml = ElementTree(rootElement)
        self.indent(xml.getroot())

        if not f == None:
            xml.write(f, encoding="utf-8")
            LOGGER.debug("XML written to " + f.name)
            f.close()
        else:
            print("No valid file has been passed to the function")
            try:
                f.close()
            except:
                pass
            return False
        return True

##############################################
# CINEMA                                     #
##############################################


class RRDialog(c4d.gui.GeDialog):
    ''' asks for input when in tiled mode '''
    tiles = 1

    def CreateLayout(self):
        self.SetTitle("Tiled RRSubmit v 7.0.24")
        self.GroupBegin(20001, c4d.BFH_SCALEFIT | c4d.BFV_FIT, 2, 0, "")
        self.AddStaticText(0, c4d.BFH_LEFT, 0, 0, "Tiles:", 0)
        self.AddEditNumberArrows(20100, c4d.BFH_LEFT)
        self.GroupEnd()
        self.AddButton(20101, c4d.BFH_SCALE | c4d.BFV_SCALE, 75, 15, "Run")
        self.SetLong(20100, self.tiles, 1, 100)
        return True

    def Command(self, id, msg):
        global TILES
        if id == 20100:
            self.tiles = self.GetLong(20100)
        if id == 20101:
            TILES = self.tiles
            self.Close()
        return True


class RRSubmit(c4d.plugins.CommandData):

    job = rrJob()
    job.clear()
    isMP = False
    renderSettings = None
    isMPSinglefile = False
    languageStrings = {}

    def submitToRR(self, submitjob, useConsole, PID=None, WID=None):
        ''' writes XML Job file into a temporary file, then calls the appropriate method to either pass it to the rrSubmitter or rrSubmitterconsole '''
        tmpDir = tempfile.gettempdir()
        doc = c4d.documents.GetActiveDocument()
        xmlObj= submitjob.writeToXMLstart()

        if TILES > 1:  # tiled documents
            submitjob.isTiledMode = True
            LOGGER.debug("tiled documents " + str(TILES))
            filelist = self.saveTiledDocument(doc, TILES, submitjob.sceneFilename)
            i = 0
            base, ext = os.path.splitext(submitjob.imageName)
            tmpFile = open(tmpDir + os.sep + "rrTmpSubmit.xml", "w")
            for f in filelist:
                LOGGER.debug("tiled document  "+str(f))
                submitjob.sceneFilename = f
                submitjob.imageName = base + "_tile" + str(i) + ext
                i += 1
                junk, rest = os.path.split(f)
                fname, junk = os.path.splitext(rest)
                submitjob.writeToXMLJob(xmlObj)
                pass
        else:  # single document
            rvalue = gui.QuestionDialog("Save Scene?")
            if rvalue:
                c4d.documents.SaveDocument(doc, submitjob.sceneFilename, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, c4d.FORMAT_C4DEXPORT)
            # Send XML to RR Submitter
            tmpFile = open(tmpDir + os.sep + "rrTmpSubmit.xml", "w")
            submitjob.writeToXMLJob(xmlObj)

        ret = submitjob.writeToXMLEnd(tmpFile,xmlObj)
        if ret:
            LOGGER.debug("Job written to " + tmpFile.name)
        else:
            LOGGER.warning("There was a problem writing the job file to " + tmpFile.name)
        if useConsole == True:
            self.submitRRConsole(tmpFile.name, PID, WID)
        else:
            self.submitRR(tmpFile.name)

    def submitRR(self, filename):
        ''' calls rrSubmit and passes the XML job file as a parameter '''
        c4d.storage.GeExecuteProgram(rrGetRR_Root() + self.getRRSubmitter(), filename)
        return True

    def submitRRConsole(self, filename, PID=None, WID=None):
        ''' calls rrSubmitterconsole and passes the XML job file as a parameter '''
        if WID is not None:
            #c4d.storage.GeExecuteProgramEx(rrGetRR_Root() + self.getRRSubmitterConsole(), filename + " -PreID " + PID + " -WaitForID " + WID)
            call([self.getRRRoot() + self.getRRSubmitterConsole(), filename, "-PID", PID, "-WID", WID])
        elif PID is not None:
            #c4d.storage.GeExecuteProgramEx(rrGetRR_Root() + self.getRRSubmitterConsole(), filename + " -PreID " + PID)
            call([self.getRRRoot() + self.getRRSubmitterConsole(), filename, "-PID", PID])
        else:
            c4d.storage.GeExecuteProgram(rrGetRR_Root() + self.getRRSubmitterConsole(), filename)
        return True

    def getRRSubmitter(self):
        ''' returns the rrSubmitter filename '''
        if isWin() == True:
            rrSubmitter = "\\win__rrSubmitter.bat"
        else:
            rrSubmitter = "/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter"
        return rrSubmitter

    def getRRSubmitterConsole(self):
        ''' returns the rrSubmitterconsole filename '''
        if isWin() == True:
            rrSubmitterConsole = "\\bin\\win\\rrSubmitterconsole.exe"
        else:
            rrSubmitterConsole = "/bin/mac/rrSubmitterConsole.app/Contents/MacOS/rrSubmitterconsole"
        return rrSubmitterConsole

    def setImageFormat(self):
        ''' evaluates the image format extension from the currently selected render settings '''
        if (self.isRegular or (not self.isMP)) :
            self.job.imageFormatID = self.renderSettings[c4d.RDATA_FORMAT]
        else:
            self.job.imageFormatID = self.renderSettings[c4d.RDATA_MULTIPASS_SAVEFORMAT]
            
        if self.job.imageFormatID == c4d.FILTER_TIF:
            self.job.imageFormat = ".tif"
        elif self.job.imageFormatID == c4d.FILTER_PNG:
            self.job.imageFormat = ".png"
        elif self.job.imageFormatID == c4d.FILTER_IES:
            self.job.imageFormat = ".ies"
        elif self.job.imageFormatID == c4d.FILTER_PSB:
            self.job.imageFormat = ".psb"
        elif self.job.imageFormatID == 1016606:
            self.job.imageFormat = ".exr"
        elif self.job.imageFormatID == 1023737:
            self.job.imageFormat = ".dpx"
        elif self.job.imageFormatID == 777209673:
            self.job.imageFormat = ".sgi"
        elif self.job.imageFormatID == c4d.FILTER_TGA:
            self.job.imageFormat = ".tga"
        elif self.job.imageFormatID == c4d.FILTER_BMP:
            self.job.imageFormat = ".bmp"
        elif self.job.imageFormatID == c4d.FILTER_IFF:
            self.job.imageFormat = ".iff"
        elif self.job.imageFormatID == c4d.FILTER_JPG:
            self.job.imageFormat = ".jpg"
        elif self.job.imageFormatID == c4d.FILTER_PICT:
            self.job.imageFormat = ".pict"
        elif self.job.imageFormatID == c4d.FILTER_PSD:
            self.job.imageFormat = ".psd"
        elif self.job.imageFormatID == c4d.FILTER_RLA:
            self.job.imageFormat = ".rla"
        elif self.job.imageFormatID == c4d.FILTER_RPF:
            self.job.imageFormat = ".rpf"
        elif self.job.imageFormatID == c4d.FILTER_B3D:
            self.job.imageFormat = ".b3d"
        elif self.job.imageFormatID == c4d.FILTER_TIF_B3D:
            self.job.imageFormat = ".tif"
        elif self.job.imageFormatID == c4d.FILTER_HDR:
            self.job.imageFormat = ".hdr"
        elif self.job.imageFormatID == c4d.FILTER_QTVRSAVER_PANORAMA:
            self.job.imageFormat = ".qtvr"
        elif self.job.imageFormatID == c4d.FILTER_QTVRSAVER_OBJECT:
            self.job.imageFormat = ".qtvr"
        elif self.job.imageFormatID == 1785737760:
            self.job.imageFormat = ".jp2"
        elif self.job.imageFormatID == 1903454566:
            self.job.imageFormat = ".mov"
            self.job.imageSingleOutput = True
        elif self.job.imageFormatID == c4d.FILTER_MOVIE:
            self.job.imageFormat = ".mov"
            self.job.imageSingleOutput = True
        elif self.job.imageFormatID == c4d.FILTER_AVI:
            self.job.imageFormat = ".avi"
            self.job.imageSingleOutput = True
        LOGGER.debug("File Format: " + self.job.imageFormat)

        if self.job.imageSingleOutput == True:
            LOGGER.debug("SingleOutput: yes")
        else:
            LOGGER.debug("SingleOutput: no")

        self.job.imageFormatIDMultiPass = self.renderSettings[c4d.RDATA_MULTIPASS_SAVEFORMAT]

        if self.job.imageFormatIDMultiPass == c4d.FILTER_TIF:
            self.job.imageFormatMultiPass = ".tif"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_PNG:
            self.job.imageFormatMultiPass = ".png"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_IES:
            self.job.imageFormatMultiPass = ".ies"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_PSB:
            self.job.imageFormatMultiPass = ".psb"
        elif self.job.imageFormatIDMultiPass == 1016606:
            self.job.imageFormatMultiPass = ".exr"
        elif self.job.imageFormatIDMultiPass == 1023737:
            self.job.imageFormatMultiPass = ".dpx"
        elif self.job.imageFormatIDMultiPass == 777209673:
            self.job.imageFormatMultiPass = ".sgi"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_TGA:
            self.job.imageFormatMultiPass = ".tga"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_BMP:
            self.job.imageFormatMultiPass = ".bmp"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_IFF:
            self.job.imageFormatMultiPass = ".iff"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_JPG:
            self.job.imageFormatMultiPass = ".jpg"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_PICT:
            self.job.imageFormatMultiPass = ".pict"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_PSD:
            self.job.imageFormatMultiPass = ".psd"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_RLA:
            self.job.imageFormatMultiPass = ".rla"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_RPF:
            self.job.imageFormatMultiPass = ".rpf"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_B3D:
            self.job.imageFormatMultiPass = ".b3d"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_TIF_B3D:
            self.job.imageFormatMultiPass = ".tif"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_HDR:
            self.job.imageFormatMultiPass = ".hdr"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_QTVRSAVER_PANORAMA:
            self.job.imageFormatMultiPass = ".qtvr"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_QTVRSAVER_OBJECT:
            self.job.imageFormatMultiPass = ".qtvr"
        elif self.job.imageFormatIDMultiPass == 1785737760:
            self.job.imageFormatMultiPass = ".jp2"
        elif self.job.imageFormatIDMultiPass == 1903454566:
            self.job.imageFormatMultiPass = ".mov"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_MOVIE:
            self.job.imageFormatMultiPass = ".mov"
        elif self.job.imageFormatIDMultiPass == c4d.FILTER_AVI:
            self.job.imageFormatMultiPass = ".avi"
        return True

    def setSeq(self):
        doc = c4d.documents.GetActiveDocument()
        ''' gets the beginning, end and step size for the current frame sequence from the render settings '''
        seqMode = self.renderSettings[c4d.RDATA_FRAMESEQUENCE]
        if seqMode == c4d.RDATA_FRAMESEQUENCE_MANUAL:
            startTime = self.renderSettings[c4d.RDATA_FRAMEFROM]
            endTime = self.renderSettings[c4d.RDATA_FRAMETO]
            frameRate = self.job.frameRateRender
            self.job.seqStart = startTime.GetFrame(int(frameRate))
            self.job.seqEnd = endTime.GetFrame(int(frameRate))
        elif seqMode == c4d.RDATA_FRAMESEQUENCE_CURRENTFRAME:
            startTime = self.renderSettings[c4d.RDATA_FRAMEFROM]
            endTime = startTime
            frameRate = self.job.frameRateRender
            self.job.seqStart = startTime.GetFrame(int(frameRate))
            self.job.seqEnd = endTime.GetFrame(int(frameRate))
        elif seqMode == c4d.RDATA_FRAMESEQUENCE_PREVIEWRANGE:
            startTime = doc.GetLoopMinTime()
            endTime = doc.GetLoopMaxTime()
            frameRate = self.job.frameRateRender
            self.job.seqStart = startTime.GetFrame(int(frameRate))
            self.job.seqEnd = endTime.GetFrame(int(frameRate))
        else: 
            startTime = doc.GetMinTime()
            endTime = doc.GetMaxTime()
            frameRate = self.job.frameRateRender
            self.job.seqStart = startTime.GetFrame(int(frameRate))
            self.job.seqEnd = endTime.GetFrame(int(frameRate))

        self.job.seqStep = self.renderSettings[c4d.RDATA_FRAMESTEP]
        if self.job.seqStep == None:
            self.job.seqStep = 1
        return True
    
    def setNameFormat(self, imagefilename, imageformat):
        if self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_0:
            # name0000.ext
            imageformat = imageformat
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_1:
            # name0000
            imageformat = ""
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_2:
            # name.0000
            self.job.imageFormat = ""
            imageformat = imageformat + "."
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_3:
            # name000.ext
            imageformat = imageformat
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_4:
            # name000
            imageformat = ""
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_5:
            # name.0000
            imageformat = ""
            imagefilename =imagefilename + "."
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_6:
            # name.0000.ext
            imagefilename = imagefilename+ "."
        if ((len(imagefilename)>0) and imagefilename[-1].isdigit()):
            imagefilename = imagefilename+ "_"
        return imagefilename, imageformat

    def getChannelName(self,displayName):
        retStr=""
        for key in self.languageStrings:
            if (self.languageStrings[key] == displayName):
                retStr=str(key);
        return retStr


    def setFileout(self):
        if self.isMP == True:
            LOGGER.debug("MultiPass: yes")
            self.job.layerName = "MultiPass"
            self.job.imageName = self.renderSettings[c4d.RDATA_MULTIPASS_FILENAME]
        else:
            LOGGER.debug("MultiPass: no")
            self.job.layerName = ""
            self.job.imageName = self.renderSettings[c4d.RDATA_PATH]

        if (self.isRegular or (not self.isMP)) :
            self.job.imageNamingID = self.renderSettings[c4d.RDATA_NAMEFORMAT]
        else:
            self.job.imageNamingID = self.renderSettings[c4d.RDATA_MULTIPASS_SAVEFORMAT]
        
            
        addStereoString="";
        if (self.renderSettings[c4d.RDATA_STEREO]):
            dirName=os.path.dirname(self.job.imageName)
            fileName=os.path.basename(self.job.imageName)

            if (  (self.renderSettings[c4d.RDATA_STEREO_CALCRESULT]==c4d.RDATA_STEREO_CALCRESULT_S)):
                addStereoString=self.languageStrings['STREAM']+" "+self.languageStrings['STEREO_ANA_COL_RIGHT']
            elif ((self.renderSettings[c4d.RDATA_STEREO_CALCRESULT]==c4d.RDATA_STEREO_CALCRESULT_R)):
                addStereoString=self.languageStrings['STREAM']+" "+self.languageStrings['MERGEDSTREAM']
            elif ((self.renderSettings[c4d.RDATA_STEREO_CALCRESULT]==c4d.RDATA_STEREO_CALCRESULT_SR)):
                addStereoString=self.languageStrings['STREAM']+" "+self.languageStrings['MERGEDSTREAM']
            elif ((self.renderSettings[c4d.RDATA_STEREO_CALCRESULT]==c4d.RDATA_STEREO_CALCRESULT_SINGLE)):
                if ((self.renderSettings[c4d.RDATA_STEREO_SINGLECHANNEL]==1)):
                    addStereoString=self.languageStrings['STREAM']+" "+self.languageStrings['STEREO_ANA_COL_LEFT']
                else:
                    addStereoString=self.languageStrings['STREAM']+" "+self.languageStrings['STEREO_ANA_COL_RIGHT']
            if (self.renderSettings[c4d.RDATA_STEREO_SAVE_FOLDER]):
                self.job.imageName= dirName+"/"+addStereoString+"/"+fileName
            else:
                self.job.imageName= dirName+"/"+addStereoString+"_"+fileName
                
        if (self.isMP and not self.isMPSinglefile):
            passNames= { }
            MP = self.renderSettings.GetFirstMultipass()
            channelName=self.getChannelName(MP.GetName())
            if ((len(channelName)>1) and (not MP.GetBit(c4d.BIT_VPDISABLED)) ):
                filenameComb= self.job.imageName+ "_" + channelName
                fileext=self.job.imageFormatMultiPass
                filenameComb, fileext = self.setNameFormat(filenameComb,fileext)
                self.job.channelExtension.append(fileext)
                self.job.channelFileName.append(filenameComb)
                self.job.maxChannels= self.job.maxChannels+1
            while MP.GetNext():
                MP = MP.GetNext()
                channelName=self.getChannelName(MP.GetName())
                if ((len(channelName)>1) and (not MP.GetBit(c4d.BIT_VPDISABLED)) ):
                    filenameComb= self.job.imageName+ "_" + channelName
                    fileext=self.job.imageFormatMultiPass
                    filenameComb, fileext = self.setNameFormat(filenameComb,fileext)
                    self.job.channelExtension.append(fileext)
                    self.job.channelFileName.append(filenameComb)
                    self.job.maxChannels= self.job.maxChannels+1

        self.job.imageName, self.job.imageFormat = self.setNameFormat(self.job.imageName,self.job.imageFormat)

        if (self.renderSettings[c4d.RDATA_STEREO] and (self.renderSettings[c4d.RDATA_STEREO_CALCRESULT]==c4d.RDATA_STEREO_CALCRESULT_S)):
            curMaxChannels=self.job.maxChannels
            tempName=self.job.imageName
            tempName = tempName.replace(self.languageStrings['STEREO_ANA_COL_RIGHT'],self.languageStrings['STEREO_ANA_COL_LEFT'])            
            self.job.channelFileName.append(tempName)
            self.job.channelExtension.append(self.job.imageFormat)
            self.job.maxChannels= self.job.maxChannels+1
            for po in range(0, curMaxChannels):
                tempName=self.job.channelFileName[po]
                tempName = tempName.replace(self.languageStrings['STEREO_ANA_COL_RIGHT'],self.languageStrings['STEREO_ANA_COL_LEFT'])            
                self.job.channelFileName.append(tempName)
                self.job.channelExtension.append(self.job.channelExtension[po])
                self.job.maxChannels= self.job.maxChannels+1

        if (self.renderSettings[c4d.RDATA_STEREO]):
            tempName=self.job.imageName
            if (self.renderSettings[c4d.RDATA_STEREO_SAVE_FOLDER]):
                tempName = tempName.replace(addStereoString+"/","<removeVar "+addStereoString+"/"+">")
            else:
                tempName = tempName.replace(addStereoString+"_","<removeVar "+addStereoString+"_"+">")
            self.job.imageName=tempName
            

            
        
        if self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_0:
            # name0000.ext
            self.job.imageFramePadding = 4
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_1:
            # name0000
            self.job.imageFramePadding = 4
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_2:
            # name.0000
            self.job.imageFramePadding = 4
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_3:
            # name000.ext
            self.job.imageFramePadding = 3
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_4:
            # name000
            self.job.imageFramePadding = 3
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_5:
            # name.0000
            self.job.imageFramePadding = 3
        elif self.job.imageNamingID == c4d.RDATA_NAMEFORMAT_6:
            # name.0000.ext
            self.job.imageFramePadding = 4
        return True

    def saveTiledDocument(self, doc, tiles, filename):
        ''' experimental function to store tiled versions of a single document'''
        basename, ext = os.path.splitext(filename)
        filelist = []

        # store original state
        oRegion = self.renderSettings[c4d.RDATA_RENDERREGION]
        oRegionLeft = self.renderSettings[c4d.RDATA_RENDERREGION_LEFT]
        oRegionTop = self.renderSettings[c4d.RDATA_RENDERREGION_TOP]
        oRegionRight = self.renderSettings[c4d.RDATA_RENDERREGION_RIGHT]
        oRegionBottom = self.renderSettings[c4d.RDATA_RENDERREGION_BOTTOM]

        left = oRegionLeft
        top = oRegionTop
        right = oRegionRight
        bottom = oRegionBottom

        width = self.job.width - left - right

        step, rest = divmod(width, tiles)

        for i in range(0, tiles):
            self.renderSettings[c4d.RDATA_RENDERREGION] = True
            self.renderSettings[c4d.RDATA_RENDERREGION_LEFT] = int(left + (step * i))

            self.renderSettings[c4d.RDATA_RENDERREGION_RIGHT] = int(((tiles - 1) * step) - (self.renderSettings[c4d.RDATA_RENDERREGION_LEFT]))
            if self.renderSettings[c4d.RDATA_RENDERREGION_RIGHT] < right:
                self.renderSettings[c4d.RDATA_RENDERREGION_RIGHT] = int(right)

            self.renderSettings[c4d.RDATA_RENDERREGION_TOP] = int(top)
            self.renderSettings[c4d.RDATA_RENDERREGION_BOTTOM] = int(bottom)
            tiledname = basename + "_tile" + str(i) + ext
            c4d.documents.SaveDocument(doc, tiledname, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, c4d.FORMAT_C4DEXPORT)
            filelist.append(tiledname)

        # back to previous state
        self.renderSettings[c4d.RDATA_RENDERREGION] = oRegion
        self.renderSettings[c4d.RDATA_RENDERREGION_LEFT] = oRegionLeft
        self.renderSettings[c4d.RDATA_RENDERREGION_TOP] = oRegionTop
        self.renderSettings[c4d.RDATA_RENDERREGION_RIGHT] = oRegionRight
        self.renderSettings[c4d.RDATA_RENDERREGION_BOTTOM] = oRegionBottom
        return filelist

    def convert_umlaut(self, inStr):
        return inStr

    def getLanguage(self):
        self.languageStrings = {}
        language = "US"
        lID= 0
        lanDesc= c4d.GeGetLanguage(lID)
        while lanDesc!=None:
            if (lanDesc["default_language"]):
                language=lanDesc["extensions"]
                break
            lID= lID+1
            lanDesc=c4d.GeGetLanguage(lID)
        CinemaPath= os.path.dirname(os.path.dirname(__file__))
        CinemaPath=CinemaPath+PD() + "resource"+PD()+"modules"+PD()+"newman"+PD()+PD()+"strings_"+str(language).lower()+PD()+"c4d_strings.str"
        strfile = open(CinemaPath)
        for sline in strfile :
            sline= sline.rstrip()
            svalue=""
            if (sline.find(";")>0 and sline.find("\"")>0):
                sline=sline.split("\"")
                svalue=sline[1].rstrip()
                sline=sline[0].rstrip()
                if (sline.find("IDS_PV_STEREO_CHANNEL")>0):
                    self.languageStrings['STEREO_CHANNEL'] = svalue
                elif (sline.find("IDS_PV_STEREO_ANA_COL_LEFT")>0):
                    self.languageStrings['STEREO_ANA_COL_LEFT'] = svalue
                elif (sline.find("IDS_PV_STEREO_ANA_COL_RIGHT")>0):
                    self.languageStrings['STEREO_ANA_COL_RIGHT'] = svalue
        strfile.close()   
        CinemaPath= os.path.dirname(os.path.dirname(__file__))
        CinemaPath=CinemaPath+PD() + "resource"+PD()+"modules"+PD()+"c4dplugin"+PD()+PD()+"strings_"+str(language).lower()+PD()+"c4d_strings.str"
        strfile = open(CinemaPath)
        for sline in strfile :
            sline= sline.rstrip()
            svalue=""
            if (sline.find(";")>0 and sline.find("\"")>0):
                sline=sline.split("\"")
                svalue=sline[1].rstrip()
                sline=sline[0].rstrip()
                if (sline.find("IDS_STREAM")>0):
                    self.languageStrings['STREAM'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MERGEDSTREAM")>0):
                    self.languageStrings['MERGEDSTREAM'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_AMBIENT")>0):
                    self.languageStrings['ambient'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_ATMOSPHERE")>0):
                    self.languageStrings['atmos'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_ATMOSPHERE_MULTIPLY")>0):
                    self.languageStrings['atmosmul'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_TRANSPARENCY")>0):
                    self.languageStrings['refr'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_REFLECTION")>0):
                    self.languageStrings['refl'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_RADIOSITY")>0):
                    self.languageStrings['gi'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_CAUSTICS")>0):
                    self.languageStrings['caustics'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_DEPTH")>0):
                    self.languageStrings['depth'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_SHADOW")>0):
                    self.languageStrings['shadow'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_SPECUALR")>0):
                    self.languageStrings['specular'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_DIFFUSE")>0):
                    self.languageStrings['diffuse'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_ILLUMINATION")>0):
                    self.languageStrings['illum'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_SPECULAR")>0):
                    self.languageStrings['matspeccol'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_SPECULAR_COLOR")>0):
                    self.languageStrings['matspec'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_ENVIRONMENT")>0):
                    self.languageStrings['matenv'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_REFLECTION")>0):
                    self.languageStrings['matrefl'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_TRANSPARENCY")>0):
                    self.languageStrings['mattrans'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_LUMINANCE")>0):
                    self.languageStrings['matlum'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_DIFFUSION")>0):
                    self.languageStrings['matdif'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_COLOR")>0):
                    self.languageStrings['matcolor'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_AMBIENTOCCLUSION")>0):
                    self.languageStrings['ao'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MOTIONVECTOR")>0):
                    self.languageStrings['motion'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_UV")>0):
                    self.languageStrings['uv'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_MATERIAL_NORMAL")>0):
                    self.languageStrings['normal'] = self.convert_umlaut( svalue)
                if (sline.find("IDS_MULTIPASS_RGBA")>0):
                    self.languageStrings['rgb'] = self.convert_umlaut( svalue)
        strfile.close()   



    def Execute(self, doc):
        print "rrSubmit v 7.0.24"
        
        # read current render settings
        self.getLanguage()
        self.renderSettings = doc.GetActiveRenderData()

        # collects some data and populates the job with initial settings
        self.isRegular = self.renderSettings[c4d.RDATA_SAVEIMAGE]
        self.isMP = self.renderSettings[c4d.RDATA_MULTIPASS_SAVEIMAGE] and self.renderSettings[c4d.RDATA_MULTIPASS_ENABLE]  # is Multipass enabled?
        self.isMPSinglefile = self.renderSettings[c4d.RDATA_MULTIPASS_SAVEONEFILE] 
        
        self.job.sceneFilename = doc.GetDocumentPath() + os.sep + doc.GetDocumentName()
        self.job.width = self.renderSettings[c4d.RDATA_XRES]
        self.job.height = self.renderSettings[c4d.RDATA_YRES]
        self.job.versionInfo = str(int(c4d.GetC4DVersion() / 1000))
        if isWin() == True:
            self.job.osString = "win"
        else:
            self.job.osString = "mac"
        self.job.camera = doc.GetRenderBaseDraw().GetSceneCamera(doc).GetName()
        self.job.frameRateDoc = doc.GetFps()
        self.job.frameRateRender = self.renderSettings[c4d.RDATA_FRAMERATE]
        if self.job.frameRateDoc != self.job.frameRateRender:
            ret = gui.QuestionDialog("Document (" + str(self.job.frameRateDoc) + ") and Render Settings (" + str(self.job.frameRateRender) + ") are not using the same framerate - do you wish to continue anyway?")
            if not ret:
                return False

        rendererID = self.renderSettings[c4d.RDATA_RENDERENGINE]
        if (rendererID==c4d.RDATA_RENDERENGINE_STANDARD): 
            self.job.renderer=""
        elif (rendererID==c4d.RDATA_RENDERENGINE_PREVIEWSOFTWARE):
            self.job.renderer="preview"
        elif (rendererID==c4d.RDATA_RENDERENGINE_PHYSICAL):
            self.job.renderer="Physical"
        elif (rendererID==c4d.RDATA_RENDERENGINE_PREVIEWHARDWARE):
            self.job.renderer="Hardware"
        elif (rendererID==c4d.RDATA_RENDERENGINE_CINEMAN):
            self.job.renderer="CineMan"
        elif (rendererID==1029525):
            self.job.renderer="Octane"
        elif (rendererID==1029988):
            self.job.renderer="Arnold"
        else:
            self.job.renderer= "RID"+str(rendererID)
        


        self.setSeq()
        self.setImageFormat()
        self.setFileout()

        if ((SHOWTILEDIALOG) or (self.job.seqStart==self.job.seqEnd)):
            self.dialog = RRDialog()
            ret = self.dialog.Open(dlgtype=c4d.DLG_TYPE_MODAL_RESIZEABLE, pluginid=PLUGIN_ID)
            print ret
            if not ret: 
                return False

        self.submitToRR(self.job, False, PID=None, WID=None)

        return True

if __name__ == '__main__':
    result = plugins.RegisterCommandPlugin(PLUGIN_ID, "rrSubmit", 0, None, "rrSubmit", RRSubmit())
