# Render script for 3dsmax
#  v 7.0.24
#  Copyright (c)  Holger Schoenberger - Binary Alchemy

import datetime
import time
import sys
import logging
import MaxPlus
import os

logFile_available=False

def flushLog():
    pass


def logMessageGen(lvl, msg, tries):
    try:
        if (len(lvl)==0):
            if (logFile_available):
                logger = logging.getLogger()
                logging.info(datetime.datetime.now().strftime("' %H:%M.%S") + " rrMax      : " + str(msg))
                logger.handlers[0].close()
            #print(datetime.datetime.now().strftime("' %H:%M.%S") + " rrMax      : " + str(msg))
        else:
            if (logFile_available):
                logger = logging.getLogger()
                logging.info(datetime.datetime.now().strftime("' %H:%M.%S") + " rrMax - " + str(lvl) + ": " + str(msg))
                logger.handlers[0].close()
            #print(datetime.datetime.now().strftime("' %H:%M.%S") + " rrMax - " + str(lvl) + ": " + str(msg))
    except IOError:
        if (tries<3):
            time.sleep(0.35)
            logMessageGen(lvl, msg, tries+1)
        
        

def logMessage(msg):
    logMessageGen("",msg,1)

def logMessageSET(msg):
    logMessageGen("SET",msg,1)

def logMessageDebug(msg):
    if (True):
        logMessageGen("DBG", msg,1)

def logMessageError(msg):
    logMessageGen("ERR", str(msg)+"\n\n",1)
    logMessageGen("ERR", "Error reported, aborting render script",1)
    flushLog();
    sys.exit();
    #raise NameError("\nError reported, aborting render script\n")    


def argValid(argValue):
    return ((argValue!= None) and (len(str(argValue))>0))
    

class argParser:
    def getParam(self,argFindName):
        import ConfigParser
        argFindName=argFindName.lower()
        try:
            argValue = self.config.get('Max', argFindName)
        except ConfigParser.NoOptionError:
            return ""
        if (argValue== None):
            return ""
        argValue=argValue.strip()
        if (argValue.startswith("*")):
            return ""
        if (argValue.lower()=="true"):
            argValue=True
        elif (argValue.lower()=="false"):
            argValue=False
        logMessage("Flag  "+argFindName.ljust(15)+": '"+str(argValue)+"'");
        return argValue
        
        
    def readArguments(self):
        import ConfigParser
        self.config = ConfigParser.RawConfigParser()
        configFilename=os.environ['TEMP']+"\\kso_3dsmax.ini"
        logMessage("configFilename: "+configFilename);
        self.config.read(configFilename )
        self.SName=self.getParam("Scene")
        self.RendererMode=self.getParam("RendererMode")
        self.KSOMode=self.getParam("KSOMode")
        self.KSOPort=self.getParam("KSOPort")
        self.RPMPass=self.getParam("RPMPass")
        self.StateSet=self.getParam("StateSet")
        self.FName=self.getParam("FName")
        self.FNameVar=self.getParam("FNameVar")
        self.FExt=self.getParam("FExt")
        self.FPadding=self.getParam("FPadding")
        self.FNameChannelAdd=self.getParam("FNameChannelAdd")
        self.FrStart=self.getParam("SeqStart")
        self.FrEnd=self.getParam("SeqEnd")
        self.FrStep=self.getParam("SeqStep")
        self.FrOffset=self.getParam("SeqOffset")
        self.Camera=self.getParam("Camera")
        self.ResX=self.getParam("ResX")
        self.ResY=self.getParam("ResY")
        self.IgnoreError=self.getParam("IgnoreErr")
        self.RegionX1=self.getParam("RegionX1")
        self.RegionX2=self.getParam("RegionX2")
        self.RegionY1=self.getParam("RegionY1")
        self.RegionY2=self.getParam("RegionY2")
        self.RenderThreads=self.getParam("RenderThreads")
        self.PyModPath=self.getParam("PyModPath")
        self.logFile=self.getParam("LogFile")
        self.ElementsFolder=self.getParam("ElementsFolder")
        self.VRayMemLimit=self.getParam("VRayMemLimit")
        self.VRayMemLimitPercent=self.getParam("VRayMemLimitPercent")
        self.ClientTotalMemory=self.getParam("ClientTotalMemory")
        self.GBuffer=self.getParam("GBuffer")
                
        

globalArg = argParser() #required for KSO rendering


def checkCreateFolder(filedir, verbose):
    if (not os.path.exists(filedir)):
        if (verbose):
            logMessage("creating folder '%s'" % filedir)
        os.mkdir(filedir)






def applyOutput_default(arg,frameNr, verbose):
    logMessageDebug("applyOutput_default "+str(frameNr)+"  "+str(verbose));
    #note: The render output will be set with frame number 00000, but these settings have to be overwritten before each frame with the right frame number
    render = MaxPlus.RenderSettings
    outFile= render.GetOutputFile()
    logMessageDebug("applyOutput_default - "+outFile)
    tempExt=os.path.splitext(render.GetOutputFile())[1]
    if (len(tempExt)==0):
        tempExt=arg.FExt
    mainFileName=arg.FName+str(frameNr).zfill(int(arg.FPadding))+tempExt
    logMessageDebug("applyOutput_default - "+mainFileName)
    if verbose:
        logMessageSET("main output to '" +arg.FName+tempExt +"'")
    render.SetOutputFile( arg.FName+tempExt)
    filedir=os.path.dirname(arg.FName)
    checkCreateFolder(filedir,True)
    render.SetSaveFile( True )
    if (arg.ElementsFolder and arg.renderChannels and argValid(arg.FNameVar) and MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).GetElementsActive()").Get()):
        logMessageDebug("applyOutput_default - elements")
        nrOfElements=MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).NumRenderElements()").Get()
        if verbose:
            logMessage("elements found: "+str(nrOfElements))
        for elemNr in xrange(0,nrOfElements):
            elemName=MaxPlus.Core.EvalMAXScript("((maxOps.GetCurRenderElementMgr()).GetRenderElement "+str(elemNr)+").elementName").Get()
            elemName=elemName.replace(" ","_")
            logMessageDebug("applyOutput_default - "+elemName)
            if (MaxPlus.Core.EvalMAXScript("(( (maxOps.GetCurRenderElementMgr()).GetRenderElementFileName "+str(elemNr)+")==undefined)").Get()):
                fileout=""
            else:
                FVal=MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).GetRenderElementFileName "+str(elemNr))
                fileout=FVal.Get()
            tempExt=os.path.splitext(fileout)[1]
            if (len(tempExt)==0):
                tempExt=arg.FExt
            fileout=arg.FNameVar+str(frameNr).zfill(int(arg.FPadding))+tempExt
            fileout=fileout.replace("<Channel>",elemName)
            if verbose:
                logMessageSET("element %20s output to '%s'" % (elemName,fileout))
            filedir=os.path.dirname(fileout)
            fileout=fileout.replace("\\","\\\\")
            logMessageDebug("applyOutput_default -  "+fileout)
            MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).SetRenderElementFilename "+str(elemNr)+"  \""+fileout+"\"")
            checkCreateFolder(filedir,verbose)
    logMessageDebug("applyOutput_default - exit "+mainFileName)
    return mainFileName


def applyRendererOptions_default(arg):
    logMessage("Rendering with Max Default Scanline");
    applyOutput_default(arg,0,True)
    



def applyOutput_VRay(arg,frameNr, verbose):
    logMessageDebug("applyOutput_VRay "+str(frameNr)+"  "+str(verbose));
    #note: The render output will be set with frame number 0000, but these settings have to be overwritten before each frame with the right frame number
    if (arg.RendererMode=="GIPrePass"):
        return arg.FName+str(frameNr).zfill(int(arg.FPadding))+arg.FExt

    render = MaxPlus.RenderSettings
    if (not arg.vraySeperateRenderChannels) and (render.GetSaveFile() or (not arg.vrayRawFile)):
        return applyOutput_default(arg,frameNr, verbose)

    mainFileName=""
    
    
    if (render.GetSaveFile()):
        logMessageDebug("applyOutput_VRay - render.GetSaveFile()");
        #get the extension of the main output
        tempExt=os.path.splitext(render.GetOutputFile())[1]
        if (len(tempExt)==0):
            tempExt= arg.FExt
        mainFileName= arg.FName+str(frameNr).zfill(int(arg.FPadding))+tempExt
        if verbose:
            logMessageSET("main output to '" +arg.FName+tempExt +"'")
        render.SetOutputFile( arg.FName+tempExt)
        filedir=os.path.dirname(arg.FName)
        checkCreateFolder(filedir,True)

    VRayExt=arg.FExt
    if (arg.vraySeperateRenderChannels):
        logMessageDebug("applyOutput_VRay - vraySeperateRenderChannels");
        if (MaxPlus.Core.EvalMAXScript("(renderers.production.output_splitfilename==undefined)").Get()):
            pass
        else:
            FVal=MaxPlus.Core.EvalMAXScript("renderers.production.output_splitfilename")
            VRayExt=os.path.splitext(FVal.Get())[1]
        if (len(VRayExt)==0):
            VRayExt=arg.FExt
        fileout=arg.FName+VRayExt
        if (verbose):
            logMessageSET("VRay render channel output to "+fileout)
        filedir=os.path.dirname(fileout)
        fileout=fileout.replace("\\","\\\\")
        MaxPlus.Core.EvalMAXScript("renderers.production.output_splitfilename=\""+fileout+"\"")
        checkCreateFolder(filedir,verbose)
        if (MaxPlus.Core.EvalMAXScript("renderers.production.output_splitRGB").Get()):
            mainFileName= arg.FNameVar+str(frameNr).zfill(int(arg.FPadding))+arg.FExt
            mainFileName=mainFileName.replace("<Channel>","RGB_color")


    if (arg.vrayRawFile):
        logMessageDebug("applyOutput_VRay - output_saveRawFile");
        fileout=arg.FName+arg.FExt
        fileout=fileout.replace("\\","\\\\")
        MaxPlus.Core.EvalMAXScript("renderers.production.output_rawFileName=\""+fileout+"\"")
        mainFileName= arg.FName+str(frameNr).zfill(int(arg.FPadding))+arg.FExt


    #it is not required to set the filename for VRay buffers IF output_splitfilename is enabled
    #but in case that is Disabled or there is a 3dsmax buffer, we need to set it

    seperateElementFiles= argValid(arg.FNameVar) and MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).GetElementsActive()").Get()
    if (not render.GetSaveFile()) and (not arg.vraySeperateRenderChannels):
        seperateElementFiles=False
    if ((not arg.vrayFramebuffer) and MaxPlus.Core.EvalMAXScript("renderers.production.output_on").Get()):
        seperateElementFiles=False
        
    if (seperateElementFiles and arg.ElementsFolder):
        logMessageDebug("applyOutput_VRay - Elements");
        nrOfElements=MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).NumRenderElements()").Get()
        if verbose:
            logMessage("elements found: "+str(nrOfElements))
        for elemNr in xrange(0,nrOfElements):
            elemName=MaxPlus.Core.EvalMAXScript("((maxOps.GetCurRenderElementMgr()).GetRenderElement "+str(elemNr)+").elementName").Get()
            elemName=elemName.replace(" ","_")
            if (arg.vraySeperateRenderChannels):
                fileout=arg.FNameVar+str(frameNr).zfill(int(arg.FPadding))+VRayExt
            else:
                if (MaxPlus.Core.EvalMAXScript("(( (maxOps.GetCurRenderElementMgr()).GetRenderElementFileName "+str(elemNr)+")==undefined)").Get()):
                    fileout=""
                else:
                    FVal=MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).GetRenderElementFileName "+str(elemNr))
                    fileout=FVal.Get()
                tempExt=os.path.splitext(fileout)[1]
                if (len(tempExt)==0):
                    tempExt=arg.FExt
                fileout=arg.FNameVar+str(frameNr).zfill(int(arg.FPadding))+tempExt
            fileout=fileout.replace("<Channel>",elemName)
            if verbose:
                logMessageSET("element %20s output to '%s'" % (elemName,fileout))
            filedir=os.path.dirname(fileout)
            fileout=fileout.replace("\\","\\\\")
            checkCreateFolder(filedir, verbose)
            MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).SetRenderElementFilename "+str(elemNr)+"  \""+fileout+"\"")
    return  mainFileName





def moveOutput_VRay(arg,frameNr, verbose):
    if ((not arg.ElementsFolder) or (not arg.vraySeperateRenderChannels)):
        return
    import shutil
    VRayExt=arg.FExt
    if (arg.vraySeperateRenderChannels):
        VRayExt=os.path.splitext(MaxPlus.Core.EvalMAXScript("renderers.production.output_splitfilename").Get())[1]
        if (len(VRayExt)==0):
            VRayExt=arg.FExt
    FNameVar_Rendered= arg.FNameVar;
    FNameVar_Rendered= FNameVar_Rendered.replace("<Channel>\\","")
    if (argValid(arg.FNameVar) and MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).GetElementsActive()").Get()):
        nrOfElements=MaxPlus.Core.EvalMAXScript("(maxOps.GetCurRenderElementMgr()).NumRenderElements()").Get()
        for elemNr in xrange(0,nrOfElements):
            elemName=MaxPlus.Core.EvalMAXScript("((maxOps.GetCurRenderElementMgr()).GetRenderElement "+str(elemNr)+").elementName").Get()
            elemName=elemName.replace(" ","_")
            fileout_Rendered=FNameVar_Rendered+str(frameNr).zfill(int(arg.FPadding))+VRayExt
            fileout_Should  =arg.FNameVar     +str(frameNr).zfill(int(arg.FPadding))+VRayExt
            fileout_Rendered=fileout_Rendered.replace("<Channel>",elemName)
            fileout_Should  =fileout_Should  .replace("<Channel>",elemName)

            if (not os.path.isfile(fileout_Rendered)):
                logMessageGen("WRN", "Element file to be moved to subfolder not found: "+fileout_Rendered,1)
                continue;
            if (verbose):
                logMessage("Moving element '"+fileout_Rendered+"' => '"+fileout_Should+"'")
            shutil.move(fileout_Rendered,fileout_Should)
        



def applyRendererOptions_Vray(arg):
    logMessage("Rendering with VRay");
    MaxPlus.Core.EvalMAXScript("renderers.production.system_vrayLog_level=2")
    MaxPlus.Core.EvalMAXScript("renderers.production.system_vrayLog_file=\"%TEMP%\\\\VRayLog.txt\"")
    if (argValid(arg.VRayMemLimit)):
        logMessageSET("VRay mem limit to "+str(arg.VRayMemLimit))
        MaxPlus.Core.EvalMAXScript("renderers.production.system_raycaster_memLimit="+str(arg.VRayMemLimit))
    elif (argValid(arg.VRayMemLimitPercent) and argValid(arg.ClientTotalMemory)):
        memory=int(arg.ClientTotalMemory)*int(arg.VRayMemLimitPercent)/100
        logMessageSET("VRay mem limit to "+str(arg.VRayMemLimitPercent)+"% of "+str(arg.ClientTotalMemory)+" => "+str(memory))
        MaxPlus.Core.EvalMAXScript("renderers.production.system_raycaster_memLimit="+str(memory))
    
    arg.vrayOverrideResolution=not MaxPlus.Core.EvalMAXScript("renderers.production.output_getsetsfrommax").Get()
    logMessage("VRay Override 3dsMax Resolution: "+str(arg.vrayOverrideResolution))
    if (arg.vrayOverrideResolution):
        if (argValid(arg.ResX)):
            logMessageSET("width to " +str(arg.ResX))
            MaxPlus.Core.EvalMAXScript("renderers.production.output_width="+str(arg.ResX))
        if (argValid(arg.ResY)):
            logMessageSET("height to " +str(arg.ResY))
            MaxPlus.Core.EvalMAXScript("renderers.production.output_height="+str(arg.ResY))
    arg.vrayFramebuffer= MaxPlus.Core.EvalMAXScript("renderers.production.output_on").Get()
    arg.vraySeperateRenderChannels= MaxPlus.Core.EvalMAXScript("renderers.production.output_splitgbuffer").Get()
    arg.vrayRawFile= MaxPlus.Core.EvalMAXScript("renderers.production.output_saveRawFile").Get()
    
    if (arg.vrayFramebuffer):
        if (not arg.vrayRawFile) and (not arg.vraySeperateRenderChannels) :
            arg.vrayFramebuffer=False
            arg.renderChannels=False
    if (not arg.vrayFramebuffer):
        arg.vraySeperateRenderChannels=False
        MaxPlus.Core.EvalMAXScript("renderers.production.output_splitgbuffer=false")
        MaxPlus.Core.EvalMAXScript("renderers.production.output_saveRawFile=false")
    logMessage("VRay Framebuffer used: "+str(arg.vrayFramebuffer))
    logMessage("VRay Seperate Render Channels: "+str(arg.vraySeperateRenderChannels))
    logMessage("VRay Raw image: "+str(arg.vrayRawFile))
    
    if (not argValid(arg.RendererMode)):
        arg.RendererMode="default"
        if (arg.FExt==".vrmap"):
            arg.RendererMode="GIPrePass"
    logMessage("VRay render mode is "+arg.RendererMode)
    logMessage("VRay GI irradiance mode: #"+str(MaxPlus.Core.EvalMAXScript("renderers.production.adv_irradmap_mode").Get()))
    if (arg.RendererMode=="GIPrePass"):
        arg.FExt=".vrmap"
        if (not MaxPlus.Core.EvalMAXScript("renderers.production.gi_on").Get()):
            logMessageSET("VRay GI mode enabled")
            MaxPlus.Core.EvalMAXScript("renderers.production.gi_on=true")
        fileout=arg.FName+arg.FExt
        fileout=fileout.replace("\\","\\\\")
        logMessageSET("VRay GI vrmap prepass to "+fileout)
        MaxPlus.Core.EvalMAXScript("renderers.production.adv_irradmap_autoSaveFileName=\""+ fileout + "\"")
        logMessageSET("VRay GI vrmap/animation prepass")
        MaxPlus.Core.EvalMAXScript("renderers.production.adv_irradmap_mode=6")
        logMessage("VRay GI irradiance mode: #"+str(MaxPlus.Core.EvalMAXScript("renderers.production.adv_irradmap_mode").Get()))
        logMessageSET("VRay Seperate Render Channels On")
        MaxPlus.Core.EvalMAXScript("renderers.production.output_splitgbuffer=false")
        logMessageSET("VRay Framebuffer Off")
        MaxPlus.Core.EvalMAXScript("renderers.production.output_on=true")
        logMessageSET("Main 3dsmax save file Off")
        render = MaxPlus.RenderSettings
        render.SetSaveFile( False )
    else:
        if (MaxPlus.Core.EvalMAXScript("renderers.production.adv_irradmap_mode").Get()==6):
            #the scene was saved with GI prepass animation, so change it to GI animation render
            loadFileName=MaxPlus.Core.EvalMAXScript("renderers.production.adv_irradmap_loadFileName").Get()
            if (not argValid(loadFileName)):
                logMessageGen("WRN","Warning: There is no irradiance map set to be loaded, switching to GI mode single frame", 1)                
                logMessageSET("VRay GI mode to single frame")
                MaxPlus.Core.EvalMAXScript("renderers.production.adv_irradmap_mode=0")
            else:
                logMessageSET("VRay GI mode to animation render")
                MaxPlus.Core.EvalMAXScript("renderers.production.adv_irradmap_mode=7")
        
    applyOutput_VRay(arg,0,True)
        


def writeRenderPlaceholder(filename):
    logMessageGen("---",filename, 1);
    import socket
    hostName=socket.gethostname()
    hostName=hostName[:100]
    file = open(filename,"wb")
    file.write("rrDB") #Magic ID
    file.write("\x01\x0B") #DataType ID
    for x in range(0, len(hostName)):
        file.write(hostName[x])
        file.write("\x00")     #unicode
    for x in range(len(hostName),51):
        file.write("\x00\x00")
    file.write(chr(len(hostName)))
    file.write("\x00")
    file.write("\x00\x00")
    file.close();

    

def render_frame(FrStart,FrEnd,FrStep,arg):
    FrStart=int(FrStart)
    FrEnd=int(FrEnd)
    FrStep=int(FrStep)
    MaxPlus.RenderSettings.SetNThFrame(1)
    #we have to loop single frames as max will not print any "frame done in between"
    for frameNr in xrange(FrStart,FrEnd+1,FrStep):
        MaxPlus.RenderSettings.SetStart(frameNr/MaxPlus.Core.EvalMAXScript('frameRate').GetInt()*4800)
        MaxPlus.RenderSettings.SetEnd(frameNr/MaxPlus.Core.EvalMAXScript('frameRate').GetInt()*4800)
        logMessage("Starting to render frame #"+str(frameNr)+" ...")
        flushLog()
        beforeFrame=datetime.datetime.now()
        if (arg.Renderer=="VRay"):
            fileName=applyOutput_VRay(arg,frameNr,False)
        else:
            fileName=applyOutput_default(arg,frameNr,False)

        logMessageDebug("render_frame - fileName "+fileName)
        if (len(fileName)>1):
            writeRenderPlaceholder(fileName)

        logMessageDebug("render_frame - renderCmdLine start")
        
        renderCmdLine="render  vfb: false "
        renderCmdLine=renderCmdLine+" frame: "+str(frameNr)
        if (argValid(arg.Camera)):
            renderCmdLine=renderCmdLine+" camera: (getnodebyname(\""+arg.Camera+"\")) "
        if (arg.regionEnabled):
             renderCmdLine=renderCmdLine+" renderType: #region region: #("+str(arg.RegionX1)+","+str(arg.RegionY1)+","+str(arg.RegionX2)+","+str(arg.RegionY2)+") "
        else:
            renderCmdLine=renderCmdLine+" renderType: #normal "

        if (argValid(arg.GBufferString)):
            renderCmdLine=renderCmdLine+" channels:#("+arg.GBufferString+")"
            
            
        
        if ((arg.RendererMode=="default" or arg.RendererMode=="") and (MaxPlus.RenderSettings.GetSaveFile()) and fileName!="" ):
            renderCmdLine=renderCmdLine+" outputfile:\""+fileName.replace("\\","/")+"\"";
            
        logMessageDebug ("executing  "+renderCmdLine)
        FPVal=MaxPlus.Core.EvalMAXScript(renderCmdLine)
        logMessageDebug ("renderer result: "+str(FPVal.Get()))
        afterFrame=datetime.datetime.now()
        afterFrame=afterFrame-beforeFrame;
        logMessage("Frame #"+str(frameNr)+" done ")
        logMessage("Frame Time: "+str(afterFrame)+"  h:m:s.ms")
        if (arg.Renderer=="VRay"):
            moveOutput_VRay(arg,frameNr,True)
        flushLog()
    return True



def ksoRenderFrame(FrStart,FrEnd,FrStep ):
    global globalArg
    render_frame(FrStart,FrEnd,FrStep,globalArg)
    logMessage("rrKSO Frame(s) done #"+str(FrEnd)+" ")
    logMessage("                                                            ")
    logMessage("                                                            ")
    logMessage("                                                            ")
    flushLog()
    



def rrKSOStartServer(arg):
    logMessage("rrKSO startup...")
    if ((arg.KSOPort== None) or (len(str(arg.KSOPort))<=1)):
        arg.KSOPort=7774
    HOST, PORT = "localhost", int(arg.KSOPort)
    server = kso_tcp.rrKSOServer((HOST, PORT), kso_tcp.rrKSOTCPHandler)
    flushLog()
    logMessage("rrKSO server started")
    flushLog()
    kso_tcp.rrKSONextCommand=""
    while server.continueLoop:
        try:
            logMessageDebug("rrKSO waiting for new command...")
            server.handle_request()
            time.sleep(1) # handle_request() seem to return before handle() completed execution
        except Exception, e:
            logMessageError( e)
            server.continueLoop= False;
            import traceback
            logMessageError(traceback.format_exc())
        logMessage("                                                            ")
        logMessage("                                                            ")
        logMessage("rrKSO NextCommand ______________________________________________________________________________________________")
        logMessage("rrKSO NextCommand '"+ kso_tcp.rrKSONextCommand+"'")   
        logMessage("rrKSO NextCommand ______________________________________________________________________________________________")
        flushLog()
        if (len(kso_tcp.rrKSONextCommand)>0):
            if ((kso_tcp.rrKSONextCommand=="ksoQuit()") or (kso_tcp.rrKSONextCommand=="ksoQuit()\n")):
                server.continueLoop=False
                kso_tcp.rrKSONextCommand=""
            else:
                exec (kso_tcp.rrKSONextCommand)
                kso_tcp.rrKSONextCommand=""
    logMessage("rrKSO closed")


def render_KSO(arg):
    rrKSOStartServer(arg)
    
def render_default(arg):
    render_frame(arg.FrStart,arg.FrEnd,arg.FrStep,arg)



    
    
##############################################################################
#MAIN "FUNCTION":
##############################################################################
timeStart=datetime.datetime.now()
logMessageDebug('----------------------startup-----------------')
arg=argParser()
arg.readArguments()
if (not argValid(arg.logFile)):
    arg.logFile= os.environ['TEMP']+"\\rrMaxRender.log"
logging.basicConfig(filename=arg.logFile,level=logging.INFO,format='%(message)s')
logger = logging.getLogger()
logger.handlers[0].flush()
logger.handlers[0].close()
logFile_available=True
logMessage("###########################################################################")
flushLog()

if (argValid(arg.PyModPath)):
    import sys
    sys.path.append(arg.PyModPath)

logMessage("Importing rrKSO...")
import kso_tcp


logMessage( "Loading Scene '" + str(arg.SName)+"'...")
fm = MaxPlus.FileManager
if not fm.Open(str(arg.SName), True, True, True):
    logMessageError("Unable to open scene file")
    
logMessage ("Gamma Settings:  In: "+str(MaxPlus.GammaMgr.GetFileInGamma()) +"  Out: " +str(MaxPlus.GammaMgr.GetFileOutGamma()))    


if (argValid(arg.StateSet)):
    logMessageSET("pass to '" + str(arg.StateSet) +"'")
    MaxPlus.Core.EvalMAXScript("sceneStateMgr.restoreAllParts \""+arg.StateSet+"\"")
#else:
    #arg.StateSet= Check if an state set is active
    #logMessage("Using current pass '" + arg.StateSet +"'")


        
if (argValid(arg.RPMPass)):
    logMessageSET("RPM pass to '" + str(arg.RPMPass) +"'")
    MaxPlus.Core.EvalMAXScript("RPass_nr =0;  for i= 1 to RPMdata.GetPassCount() do  (  if ("+arg.RPMPass+"==RPMdata.GetPassName(i))    then RPass_nr=i  );  if RPass_nr>0    then RPMData.RMRestValues RPass_nr    else quitMax #noPrompt")


    
    
FPVal=MaxPlus.Core.EvalMAXScript("classof renderers.production as string")
arg.Renderer=  FPVal.Get()
logMessage("renderer used: '" + arg.Renderer +"'")
if (arg.Renderer.find("V_Ray")>=0):
    arg.Renderer="VRay"
elif (arg.Renderer.find("Brazil")>=0):
    arg.Renderer="Brazil"
logMessage("renderer used: '" + arg.Renderer +"'")    


MaxPlus.RenderSettings.SetSkipFrames( False)
MaxPlus.RenderSettings.SetTimeType(3)
MaxPlus.RenderSettings.SetFileNumberBase (int(arg.FrOffset))
MaxPlus.RenderSettings.SetShowVFB(False)
MaxPlus.RenderSettings.SetAreaType(0)


if (argValid(arg.Camera)):
    logMessageSET("camera to " +arg.Camera)
    camNode=MaxPlus.INode.GetINodeByName(arg.Camera)
    if (str(camNode)=="None"):
        logMessage("Unable to find camera node with name " +arg.Camera)
        arg.Camera=""
    
    MaxPlus.RenderSettings.SetUseActiveView(False)
    MaxPlus.ViewportManager.SetActiveViewport(0)
    MaxPlus.RenderSettings.SetViewID(0)
    MaxPlus.Viewport.SetViewCamera(MaxPlus.ViewportManager.GetViewportByID(0),camNode)
    MaxPlus.RenderSettings.SetCamera(camNode)   
else:
    logMessage("Rendering active viewport number "+str( MaxPlus.RenderSettings.GetViewID()))

MaxPlus.Core.EvalMAXScript("redrawViews()")
viewID=MaxPlus.RenderSettings.GetViewID()
logMessage("Rendering camera/view #"+str(viewID)+" '"+str(MaxPlus.ViewportManager.getViewportLabel(viewID))+"'")


camFileName=arg.Camera
camFileName= camFileName.replace(" ","_")


if (not argValid(arg.FPadding)):
    arg.FPadding=4;

arg.ElementsFolder=False # this works for 3dsmax elements only. And artists are not used to it.
if (not argValid(arg.ElementsFolder)):
    arg.ElementsFolder=True

if (not argValid(arg.FExt)):
    arg.FExt=""

if (not argValid(arg.FNameVar)):
    arg.FNameVar=arg.FName


arg.FNameVar= arg.FNameVar.replace("<channel>","<Channel>")
arg.FNameVar= arg.FNameVar.replace("<camera>",camFileName)
arg.FNameVar= arg.FNameVar.replace("<Camera>",camFileName)
arg.FNameVar= arg.FNameVar.replace("<Layer>",arg.StateSet)
arg.FNameVar= arg.FNameVar.replace("<layer>",arg.StateSet)

arg.FName=arg.FNameVar
if (arg.FName.find("<Channel>")>0):
    if ((arg.FName.find("\\<Channel>\\")>0) or (arg.FName.find("\\<Channel <Channel>>\\")>0)):
        arg.ElementsFolder=True
        arg.FName= arg.FName.replace("<Channel <Channel>>\\","")
        arg.FName= arg.FName.replace("<Channel .<Channel>. >","")
        arg.FName= arg.FName.replace("<Channel .<Channel>.>","")
        arg.FName= arg.FName.replace("<Channel>\\","")
        arg.FName= arg.FName.replace(".<Channel>.","")
        arg.FName= arg.FName.replace("<Channel>","")
    else:
        arg.ElementsFolder=False
        arg.FName= arg.FName.replace("<Channel <Channel>>","")
        arg.FName= arg.FName.replace("<Channel .<Channel>. >","")
        arg.FName= arg.FName.replace("<Channel .<Channel>.>","")
        arg.FName= arg.FName.replace(".<Channel>.","")
        arg.FName= arg.FName.replace("<Channel>","")
else:
    arg.FNameVar=arg.FName
    if (arg.ElementsFolder):
        arg.FNameVar=os.path.dirname(arg.FNameVar)+"\\<Channel>\\"+os.path.basename(arg.FNameVar)+"<Channel>"
    else:
        arg.FNameVar=arg.FNameVar+"<Channel>"

arg.FNameVar= arg.FNameVar.replace("<Channel <Channel>>","<Channel>")
arg.FNameVar= arg.FNameVar.replace("<Channel .<Channel>. >",".<Channel>.")
arg.FNameVar= arg.FNameVar.replace("<Channel .<Channel>.>",".<Channel>.")
arg.FNameVar= arg.FNameVar.replace("..<Channel>.",".<Channel>.")

#if (argValid(arg.FNameChannelAdd)):
 #   arg.FName   =arg.FName   +arg.FNameChannelAdd
    #arg.FNameVar=arg.FNameVar+arg.FNameChannelAdd
logMessage("Main    output is '"+arg.FName+"' ")
logMessage("Element output is '"+arg.FNameVar+"'  ")


#if (argValid(arg.IgnoreError)):
    #logMessageSET("Ignore Error to " +str(arg.IgnoreError))
    #MaxPlus.RenderSettings.ShouldContinueOnError(arg.IgnoreError)
#else:
    #logMessageSET("Ignore Error to True" )
    #MaxPlus.RenderSettings.ShouldContinueOnError(True)


if (argValid(arg.ResX)):
    logMessageSET("width to " +str(arg.ResX))
    MaxPlus.RenderSettings.SetWidth(int(arg.ResX))
if (argValid(arg.ResY)):
    logMessageSET("height to " +str(arg.ResY))
    MaxPlus.RenderSettings.SetHeight(int(arg.ResY))


arg.GBufferString=""
if (argValid(arg.GBuffer) and arg.GBuffer):
    arg.GBufferString="#zDepth, #UVCoords, #objectID, #normal"



arg.regionEnabled=False
if ((arg.RegionX1!= None) and (len(str(arg.RegionX1))>0)):
    arg.regionEnabled=True
    arg.RegionX1=int(arg.RegionX1)
    arg.RegionX2=int(arg.RegionX2)+1
    logMessage("region rendering X: "+str(arg.RegionX1)+"-"+str(arg.RegionX2))
    if ((arg.RegionY1!= None) and (len(str(arg.RegionY1))>0)):
        arg.RegionY1=int(arg.RegionY1)
        arg.RegionY2=int(arg.RegionY2)+1
        logMessage("region rendering Y: "+str(arg.RegionY1)+"-"+str(arg.RegionY2))
    else:
        arg.RegionY1=0
        arg.RegionY2=int(MaxPlus.RenderSettings.GetHeight())+1
        logMessage("region rendering Y: "+str(arg.RegionY1)+"-"+str(arg.RegionY2))
        

arg.renderChannels=True


if (arg.Renderer=="VRay"):
    applyRendererOptions_Vray(arg)
else:
    applyRendererOptions_default(arg)



timeEnd=datetime.datetime.now()
timeEnd=timeEnd - timeStart;
logMessage("Scene load time: "+str(timeEnd)+"  h:m:s.ms")
logMessage("Scene init done, starting to render... ")
flushLog()

globalArg=arg #copy for kso render
if (argValid(arg.KSOMode) and arg.KSOMode): 
    render_KSO(arg)
else:
    render_default(arg)
    
logMessage("Render done")
logMessage("                                        ")
logMessage("                                        ")
logMessage("                                        ")
logMessage("                                        ")
flushLog()

