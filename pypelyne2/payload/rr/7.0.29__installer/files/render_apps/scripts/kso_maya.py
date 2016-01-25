#  Render script for Maya    
#  Last Change: v 7.0.24
#  Copyright (c)  Holger Schoenberger - Binary Alchemy

import datetime
import time
import sys
import maya.cmds as cmds
import maya.mel




def flushLog():
    sys.stdout.flush()        
    sys.stderr.flush()    
    
def logMessageGen(lvl, msg):
    if (len(lvl)==0):
        print(datetime.datetime.now().strftime("' %H:%M.%S") + " rrMaya      : " + str(msg))
    else:
        print(datetime.datetime.now().strftime("' %H:%M.%S") + " rrMaya - " + str(lvl) + ": " + str(msg))


def logMessage(msg):
    logMessageGen("",msg)

    
def logMessageDebug( msg):
    if (False):
        logMessageGen("DGB", msg)

def logMessageError(msg):
    logMessageGen("ERR", str(msg)+"\n\n")
    logMessage("                                   ... ")
    logMessage("                                   ..  ")
    logMessage("                                   ... ")
    time.sleep(2) #some delay as some log messages seem to be cut off
    flushLog()
    raise NameError("\nError reported, aborting render script\n")
    

def logSetAttr(setParam,setValue):
    logMessageGen("SET",str(setParam)+" = "+str(setValue))
    if cmds.objExists(setParam):
        maya.mel.eval("removeRenderLayerAdjustmentAndUnlock "+str(setParam)+";")
        cmds.setAttr(setParam,setValue)
    else:
        logMessageGen("WRN","Unable to set value. "+str(setParam)+" does not exist!")
    flushLog()
        

def setAttr(setParam,setValue):
    if cmds.objExists(setParam):
        maya.mel.eval("removeRenderLayerAdjustmentAndUnlock "+str(setParam)+";")
        cmds.setAttr(setParam,setValue)
    else:
        logMessageGen("WRN","Unable to set value. "+str(setParam)+" does not exist!")
        

def logSetAttrType(setParam,setValue,setType):
    logMessageGen("SET",str(setParam)+" = "+str(setValue))
    if cmds.objExists(setParam):
        maya.mel.eval("removeRenderLayerAdjustmentAndUnlock "+str(setParam)+";")
        cmds.setAttr(setParam,setValue, type=setType)
    else:
        logMessageGen("WRN","Unable to set value. "+str(setParam)+" does not exist!")

def argValid(argValue):
    return ((argValue!= None) and (len(str(argValue))>0))



def getParam(allArgList, argFindName):
    argFindName=argFindName.lower()
    for argComb in allArgList:
        arg= argComb.split(":")
        if (len(arg)<2):
            continue
        argName=arg[0].strip().lower()
        argValue=arg[1]
        if (len(arg)>2):  # e.g. C:\program files\...
            argValue+=":" + arg[2]
        if (len(arg)>3):
            argValue+=":" + arg[3]
        argValue=argValue.strip()
        if (argName==argFindName):
            if (argValue.lower()=="true"):
                argValue=True
            elif (argValue.lower()=="false"):
                argValue=False
            logMessage("Flag  "+argFindName.ljust(15)+": '"+str(argValue)+"'");
            return argValue
    return ""


class argParser:
    def readArguments(self,argAll):
        #argAll is *almost* a JSON string, but it is not to keep the commandline cleaner and less error prone
        logMessageDebug(argAll)
        allArgList= argAll.split(",")
        self.Renderer=getParam(allArgList,"Renderer")
        self.KSOMode=getParam(allArgList,"KSOMode")
        self.KSOPort=getParam(allArgList,"KSOPort")
        self.SName=getParam(allArgList,"SName")
        self.Database=getParam(allArgList,"Db")
        self.Layer=getParam(allArgList,"Layer")
        self.FDir=getParam(allArgList,"FDir")
        self.FName=getParam(allArgList,"FName")
        self.FNameNoVar=getParam(allArgList,"FNameNoVar")
        self.FPadding=getParam(allArgList,"FPadding")
        self.FrStart=getParam(allArgList,"FrStart")
        self.FrEnd=getParam(allArgList,"FrEnd")
        self.FrStep=getParam(allArgList,"FrStep")
        self.FrOffset=getParam(allArgList,"FrOffset")
        self.FExt=getParam(allArgList,"FExt")
        self.FExtOverride=getParam(allArgList,"FExtOverride")
        self.FOverrideFormat=getParam(allArgList,"FOverrideFormat")
        self.FSingleOutput=getParam(allArgList,"FSingleOutput")
        self.Camera=getParam(allArgList,"Camera")
        self.Threads=getParam(allArgList,"Threads")
        self.Verbose=getParam(allArgList,"Verbose")
        self.ResX=getParam(allArgList,"ResX")
        self.ResY=getParam(allArgList,"ResY")
        self.RegionX1=getParam(allArgList,"RegionX1")
        self.RegionX2=getParam(allArgList,"RegionX2")
        self.RegionY1=getParam(allArgList,"RegionY1")
        self.RegionY2=getParam(allArgList,"RegionY2")
        self.RenderThreads=getParam(allArgList,"RenderThreads")
        self.RenderDemo=getParam(allArgList,"RenderDemo")
        self.PyModPath=getParam(allArgList,"PyModPath")
        self.AA1=getParam(allArgList,"AA1")
        self.AA2=getParam(allArgList,"AA2")
        self.AA3=getParam(allArgList,"AA3")
        self.AA4=getParam(allArgList,"AA4")
        self.RenderDisplace= getParam(allArgList,"RenderDisplace")
        self.RenderMotionBlur= getParam(allArgList,"RenderMotionBlur")
        self.ArchiveExportEnabled= getParam(allArgList,"ArchiveExport")
        self.ArchiveExportName= getParam(allArgList,"ArchiveExportName")
        self.OverwriteRenderCmd= getParam(allArgList,"OverwriteRenderCmd")
        self.CudaDevices= getParam(allArgList,"CudaDevices")
        

globalArg = argParser() #required for KSO rendering


def renderFrames(arg,FrStart,FrEnd,FrStep,FrOffset,Renderer, Layer):
    try:
        if (not argValid(arg.FPadding)):
            arg.FPadding=4
        arg.FPadding= int(arg.FPadding)
        FrStart=int(FrStart)
        FrStart=int(FrStart)
        FrEnd=int(FrEnd)
        FrStep=int(FrStep)
        logMessage("Changing scene frame to frame #"+str(FrStart)+" ...")
        cmds.currentTime( FrStart, edit=True )    
        setAttr('defaultRenderGlobals.byFrameStep',FrStep)
        setAttr('defaultRenderGlobals.byExtension',int(FrStep))    
        if (Renderer == "vray"):
            setAttr('vraySettings.frameStep',FrStep)
        maya.mel.eval('setImageSizePercent(-1.)')
        setAttr('defaultRenderGlobals.renderAll',1)
        

        for frameNr in xrange(FrStart,FrEnd+1,FrStep):
            logMessage("Starting to render frame #"+str(frameNr)+" ...")
            if (argValid(arg.FNameNoVar)):
                if (Renderer == "vray" and not arg.FNameNoVar.endswith('.')):
                    kso_tcp.writeRenderPlaceholder_nr(arg.FDir+"/"+arg.FNameNoVar+".", frameNr, arg.FPadding, arg.FExt)
                else:
                    kso_tcp.writeRenderPlaceholder_nr(arg.FDir+"/"+arg.FNameNoVar, frameNr, arg.FPadding, arg.FExt)
            beforeFrame=datetime.datetime.now()
            setAttr('defaultRenderGlobals.startFrame',frameNr)
            setAttr('defaultRenderGlobals.endFrame',frameNr)
            setAttr('defaultRenderGlobals.startExtension',int(frameNr)+int(FrOffset))
            if (Renderer == "vray"):
                setAttr('vraySettings.startFrame',frameNr)
                setAttr('vraySettings.endFrame',frameNr)
            flushLog()
            maya.mel.eval('mayaBatchRenderProcedure(0, "", "'+str(Layer)+'", "'+str(Renderer)+'", "")')
            flushLog()
            afterFrame=datetime.datetime.now()
            afterFrame=afterFrame-beforeFrame
            logMessage("Frame #"+str(frameNr)+" done. Frame Time: "+str(afterFrame)+"  h:m:s.ms")
            flushLog()
        
    except Exception as e:
        logMessageError(str(e))

    



def ksoRenderFrame(FrStart,FrEnd,FrStep ):
    global globalArg
    renderFrames(globalArg,FrStart,FrEnd,FrStep, globalArg.FrOffset, globalArg.Renderer, globalArg.Layer)
    flushLog()
    logMessage("rrKSO Frame(s) done #"+str(FrEnd)+" ")
    logMessage("                                                            ")
    logMessage("                                                            ")
    logMessage("                                                            ")
    flushLog()
    



def rrKSOStartServer(arg):
    try:
        logMessage("rrKSO startup...")
        if ((arg.KSOPort== None) or (len(str(arg.KSOPort))<=0)):
            arg.KSOPort=7774
        HOST, PORT = "localhost", int(arg.KSOPort)
        server = kso_tcp.rrKSOServer((HOST, PORT), kso_tcp.rrKSOTCPHandler)
        flushLog()
        time.sleep(0.3)
        logMessage("rrKSO server started")
        flushLog()
        kso_tcp.rrKSONextCommand=""
        while server.continueLoop:
            try:
                logMessageDebug("rrKSO waiting for new command...")
                server.handle_request()
                time.sleep(1) # handle_request() seem to return before handle() completed execution
            except Exception, e:
                logMessageError(e)
                server.continueLoop= False;
                import traceback
                logMessageError(traceback.format_exc())
            logMessage("rrKSONextCommand '"+ kso_tcp.rrKSONextCommand+"'")   
            logMessage("                                                         ...")
            logMessage("                                                          . ")
            logMessage("                                                         ...")
            flushLog()
            if (len(kso_tcp.rrKSONextCommand)>0):
                if ((kso_tcp.rrKSONextCommand=="ksoQuit()") or (kso_tcp.rrKSONextCommand=="ksoQuit()\n")):
                    server.continueLoop=False
                    kso_tcp.rrKSONextCommand=""
                else:
                    exec (kso_tcp.rrKSONextCommand)
                    kso_tcp.rrKSONextCommand=""
        logMessage("rrKSO closed")
    except Exception as e:
        logMessageError(str(e))


def render_KSO(arg):
    rrKSOStartServer(arg)
    
    
def render_default(arg):
    renderFrames (arg,arg.FrStart,arg.FrEnd,arg.FrStep,arg.FrOffset,arg.Renderer,arg.Layer)


def render_overwrite(arg):
    cmdline=arg.OverwriteRenderCmd
    cmdline=cmdline.replace("aFrStart",str(arg.FrStart))
    cmdline=cmdline.replace("aFrEnd",str(arg.FrEnd))
    cmdline=cmdline.replace("aFrStep",str(arg.FrStep))
    if (argValid(arg.FDir)):
        cmdline=cmdline.replace("aFDir",str(arg.FDir))
    if (argValid(arg.FName)):
        cmdline=cmdline.replace("aFName",'"'+str(arg.FName)+'"')
    if (argValid(arg.ArchiveExportName)):
        cmdline=cmdline.replace("aArchiveExportName",'"'+str(arg.ArchiveExportName)+'"')
    if (argValid(arg.FrOffset)):
        cmdline=cmdline.replace("aFrOffset",str(arg.FrOffset))
    if (argValid(arg.Renderer)):
        cmdline=cmdline.replace("aRenderer",str(arg.Renderer))
    if (argValid(arg.Layer)):
        cmdline=cmdline.replace("aLayer",str(arg.Layer))
    if (argValid(arg.Camera)):
        cmdline=cmdline.replace("aCamera",str(arg.Camera))
    logMessage("Executing custom mel line "+cmdline)
    ret=maya.mel.eval(cmdline)
    print ret
    


def setRenderSettings_MayaSoftware(arg):
    try:
        logSetAttr('defaultRenderGlobals.skipExistingFrames',0)
        if (argValid(arg.FOverrideFormat)): 
            maya.mel.eval('setMayaSoftwareImageFormat("'+arg.FOverrideFormat+'")')
        if (argValid(arg.Threads)):
            logSetAttr('defaultRenderGlobals.numCpusToUse',int(arg.Threads))
        if (argValid(arg.AA1)): 
            logSetAttr('defaultRenderQuality.edgeAntiAliasing',int(arg.AA1))
        if (argValid(arg.AA2)): 
            logSetAttr('defaultRenderQuality.shadingSamples',int(arg.AA2))
        if (argValid(arg.AA3)): 
            logSetAttr('defaultRenderQuality.maxShadingSamples',int(arg.AA3))
        if (argValid(arg.AA4)): 
            logSetAttr('defaultRenderQuality.redThreshold',float(arg.AA4))
            logSetAttr('defaultRenderQuality.greenThreshold',float(arg.AA4))
            logSetAttr('defaultRenderQuality.blueThreshold',float(arg.AA4))
            logSetAttr('defaultRenderQuality.coverageThreshold',float(arg.AA4))
        if (argValid(arg.RegionX1)):
            if (not argValid(arg.RegionX2)):    
                arg.RegionX2=19999
            if (not argValid(arg.RegionY1)):    
                arg.RegionY1=0
            if (not argValid(arg.RegionY2)):    
                arg.RegionY2=19999
            maya.mel.eval('setMayaSoftwareRegion('+str(arg.RegionX1)+','+str(arg.RegionX2)+','+str(arg.RegionY1)+','+str(arg.RegionY2)+')')
        if (argValid(arg.RenderMotionBlur)): 
            logSetAttr('defaultRenderGlobals.motionBlur',arg.RenderMotionBlur)
    except Exception as e:
        logMessageError(str(e))        


def setRenderSettings_MRay(arg):
    try:
        logSetAttr('defaultRenderGlobals.skipExistingFrames',0)
        if (argValid(arg.FOverrideFormat)): 
            maya.mel.eval('setMentalRayImageFormat("'+arg.FOverrideFormat+'")')
        if (argValid(arg.Verbose)):
            maya.mel.eval('global int $g_mrBatchRenderCmdOption_VerbosityOn = true; global int $g_mrBatchRenderCmdOption_Verbosity = '+str(arg.Verbose))
        if (argValid(arg.Threads)):
            maya.mel.eval('global int $g_mrBatchRenderCmdOption_NumThreadOn = true; global int $g_mrBatchRenderCmdOption_NumThread = '+str(arg.Threads))
        else:
            maya.mel.eval('global int $g_mrBatchRenderCmdOption_NumThreadAutoOn = true; global int $g_mrBatchRenderCmdOption_NumThreadAuto = true')
        if (argValid(arg.RegionX1)):
            if (not argValid(arg.RegionX2)):    
                arg.RegionX2=19999
            if (not argValid(arg.RegionY1)):    
                arg.RegionY1=0
            if (not argValid(arg.RegionY2)):    
                arg.RegionY2=19999
            maya.mel.eval('setMentalRayRenderRegion('+str(arg.RegionX1)+','+str(arg.RegionX2)+','+str(arg.RegionY1)+','+str(arg.RegionY2)+')')
        if (argValid(arg.RenderDisplace)): 
            logSetAttr('miDefaultOptions.displacementShaders',arg.RenderDisplace)        
        if (argValid(arg.RenderMotionBlur)):
            if (arg.RenderMotionBlur):
                logSetAttr('miDefaultOptions.motionBlur',2)
            else:
                logSetAttr('miDefaultOptions.motionBlur',0)        
        if (argValid(arg.AA1)): 
            logSetAttr('miDefaultOptions.minSamples',int(arg.AA1))
        if (argValid(arg.AA2)): 
            logSetAttr('miDefaultOptions.maxSamples',int(arg.AA2))
        if (argValid(arg.AA3)): 
            logSetAttr('miDefaultOptions.contrastR',float(arg.AA3))
            logSetAttr('miDefaultOptions.contrastR',float(arg.AA3))
            logSetAttr('miDefaultOptions.contrastR',float(arg.AA3))
            logSetAttr('miDefaultOptions.contrastR',float(arg.AA3))
    except Exception as e:
        logMessageError(str(e))

        
def setRenderSettings_VRay(arg):
    try:
        logSetAttr('defaultRenderGlobals.skipExistingFrames',0)
        logSetAttr('vraySettings.animation',True)
        logSetAttrType('vraySettings.fileNamePrefix',arg.FName,"string")
        maya.mel.eval('vrayRegisterRenderer(); vrayCreateVRaySettingsNode();')
        if (argValid(arg.Threads)):
            logSetAttr('vraySettings.sys_max_threads',int(arg.Threads))
        if (argValid(arg.RegionX1)):
            if (not argValid(arg.RegionX2)):    
                arg.RegionX2=19999
            if (not argValid(arg.RegionY1)):    
                arg.RegionY1=0
            if (not argValid(arg.RegionY2)):    
                arg.RegionY2=19999
            maya.mel.eval('vraySetBatchDoRegion('+str(arg.RegionX1)+','+str(arg.RegionX2)+','+str(arg.RegionY1)+','+str(arg.RegionY2)+')')
        if (argValid(arg.ResX)): 
            logSetAttr('vraySettings.width',int(arg.ResX))
        if (argValid(arg.ResY)): 
            logSetAttr('vraySettings.height',int(arg.ResY))
        if (argValid(arg.FPadding)):
            logSetAttr('vraySettings.fileNamePadding',int(arg.FPadding))
        if (argValid(arg.Camera)):
            logSetAttrType('vraySettings.batchCamera',arg.Camera,"string")
        if (argValid(arg.FOverrideFormat)):
            logSetAttrType('vraySettings.imageFormatStr',arg.FOverrideFormat,"string")
    except Exception as e:
        logMessageError(str(e))        
    
def setRenderSettings_Arnold(arg):
    try:
        logSetAttr('defaultRenderGlobals.skipExistingFrames',0)
        logSetAttr('defaultArnoldRenderOptions.renderType',0)
        if (not argValid(arg.FSingleOutput)):
            arg.FName=arg.FName.replace("<Layer>","<RenderLayer>");
            arg.FName=arg.FName.replace("<layer>","<RenderLayer>");
            logSetAttrType('defaultRenderGlobals.imageFilePrefix',arg.FName,"string")
        if (argValid(arg.Threads)):
            logSetAttr('defaultArnoldRenderOptions.threads_autodetect',False)
            logSetAttr('defaultArnoldRenderOptions.threads',int(arg.Threads))
        if (argValid(arg.RenderMotionBlur)): 
            logSetAttr('defaultArnoldRenderOptions.motion_blur_enable',arg.RenderMotionBlur)
        if (argValid(arg.RenderDemo)):
            if (arg.RenderDemo):
                logSetAttr('defaultArnoldRenderOptions.abortOnLicenseFail',False)
                logSetAttr('defaultArnoldRenderOptions.skipLicenseCheck',True)
            else:
                logSetAttr('defaultArnoldRenderOptions.abortOnLicenseFail',True)
                logSetAttr('defaultArnoldRenderOptions.skipLicenseCheck',False)
        if (argValid(arg.RenderDisplace)): 
            logSetAttr('defaultArnoldRenderOptions.ignoreDisplacement',(not arg.RenderDisplace))        
        if (argValid(arg.RenderMotionBlur)):
            logSetAttr('defaultArnoldRenderOptions.ignoreMotionBlur',(not arg.RenderMotionBlur))
        if (argValid(arg.FOverrideFormat)):
            import pymel.core as pm
            dAD = pm.PyNode('defaultArnoldDriver')
            dAD.ai_translator.set(arg.FOverrideFormat)
        if (argValid(arg.FExtOverride)):
            import pymel.core as pm
            dAD = pm.PyNode('defaultArnoldDriver')
            arg.FExtOverride=arg.FExtOverride.lower()
            if (arg.FExtOverride==".exr"):
                dAD.ai_translator.set("exr")
            elif (arg.FExtOverride==".jpeg"):
                dAD.ai_translator.set("jpeg")
            elif (arg.FExtOverride==".jpg"):
                dAD.ai_translator.set("jpeg")
            elif (arg.FExtOverride==".maya"):
                dAD.ai_translator.set("maya")
            elif (arg.FExtOverride==".png"):
                dAD.ai_translator.set("png")
            elif (arg.FExtOverride==".tif"):
                dAD.ai_translator.set("tif")
        if (argValid(arg.RegionX1)):
            if (not argValid(arg.RegionX2)):    
                arg.RegionX2=19999
            if (not argValid(arg.RegionY1)):    
                arg.RegionY1=0
            if (not argValid(arg.RegionY2)):    
                arg.RegionY2=19999
            logSetAttr('defaultArnoldRenderOptions.regionMinX',int(arg.RegionX1))
            logSetAttr('defaultArnoldRenderOptions.regionMaxX',int(arg.RegionX2))
            logSetAttr('defaultArnoldRenderOptions.regionMinY',int(arg.RegionY1))
            logSetAttr('defaultArnoldRenderOptions.regionMaxY',int(arg.RegionY2))
        try:
            if (argValid(arg.Verbose)):
                logSetAttr('defaultArnoldRenderOptions.log_verbosity',int(arg.Verbose))
                logSetAttr('defaultArnoldRenderOptions.log_console_verbosity',int(arg.Verbose))
        except Exception as e:
            logMessageError(str(e))
    except Exception as e:
        logMessageError(str(e))   



def setRenderSettings_Redshift(arg):
    try:
        maya.mel.eval('redshiftRegisterRenderer(); redshiftGetRedshiftOptionsNode(true);')
        logSetAttrType('redshiftOptions.imageFilePrefix',arg.FName,"string")
        logSetAttr('redshiftOptions.skipExistingFrames',0)
        availableCuda= maya.mel.eval('rsPreference -q "AllCudaDevices";')
        logMessage("Available Cuda devices: "+availableCuda)
        if (argValid(arg.CudaDevices)):
            arg.CudaDevices.replace(".",",")
            arg.CudaDevices="{"+arg.CudaDevices+"}"
            logSetAttr("CudaDevices",str(arg.CudaDevices))
            flushLog()
            maya.mel.eval('redshiftSelectCudaDevices('+arg.CudaDevices+');')            
    except Exception as e:
        logMessageError(str(e))      



def rrStart(argAll):
    try:    
        flushLog()
        logMessage("")
        
        timeStart=datetime.datetime.now()
        arg=argParser()
        arg.readArguments(argAll)

     
        if (argValid(arg.PyModPath)): 
            import sys
            logMessage("Append python search path with '" +arg.PyModPath+"'" )
            sys.path.append(arg.PyModPath)
        global kso_tcp
        import kso_tcp            

        try:
            logMessage("Set Workspace to '" +arg.Database+"'" )
            cmds.workspace(arg.Database, openWorkspace=True )
        except Exception as e:
            logMessageGen("WRN",str(e))

        logMessage("Set image dir to '" +arg.FDir+"'" )
        cmds.workspace(fileRule = ['images', arg.FDir])
        cmds.workspace(fileRule = ['depth', arg.FDir])


        try:
            maya.mel.eval('loadPlugin AbcImport;')
        except:
            pass

        mayaVersion = cmds.about(apiVersion=True)
        logMessage("Maya version: "+str(mayaVersion/100)+"."+str(mayaVersion % 100).zfill(2))
        mayaVersion=int(mayaVersion/100)
        

        if (mayaVersion>=2014):
            try:
                maya.mel.eval('loadPlugin xgenMR;')
                maya.mel.eval('loadPlugin xgenToolkit;')
            except:
                pass

        if (arg.Renderer == "arnold"):
            maya.mel.eval('loadPlugin -quiet mtoa;;')        
        if (arg.Renderer == "vray"):
            maya.mel.eval('loadPlugin vrayformaya;;')   
            maya.mel.eval('vrayRegisterRenderer();;')  
        if (arg.Renderer == "redshift"):
            maya.mel.eval('loadPlugin redshift4maya;;')   
        if (arg.Renderer == "mentalRay"):
            maya.mel.eval('loadPlugin Mayatomr;;')
            maya.mel.eval('miLoadMayatomr;;')
            maya.mel.eval('miCreateDefaultNodes();;')
             
            
            
        logMessage("Open Scene file '" +arg.SName+"'" )
        cmds.file( arg.SName, f=True, o=True )


        if (argValid(arg.Layer)): 
            logMessage("Set Layer to '" +arg.Layer+"'" )
            if (arg.Layer == "masterLayer"):
                arg.Layer= "defaultRenderLayer"
            RenderLayer=cmds.listConnections( "renderLayerManager", t="renderLayer")
            if (not arg.Layer.upper() in (name.upper() for name in RenderLayer)):
                logMessageError("Requested layer does not exist!" )
                return
            maya.mel.eval('setMayaSoftwareLayers("'+arg.Layer+'","" );')
                

        if (not argValid(arg.Renderer)): 
            arg.Renderer=cmds.getAttr('defaultRenderGlobals.currentRenderer')
        logMessage("Renderer is '" + arg.Renderer+"'")


        if (not argValid(arg.FPadding)):
            arg.FPadding=4


        if (not argValid(arg.FSingleOutput)):
            logSetAttrType('defaultRenderGlobals.imageFilePrefix',arg.FName,"string")
            maya.mel.eval('removeRenderLayerAdjustmentAndUnlock defaultRenderGlobals.animation;')
            logSetAttr('defaultRenderGlobals.animation',True)
            maya.mel.eval('removeRenderLayerAdjustmentAndUnlock defaultRenderGlobals.startFrame;')
            maya.mel.eval('removeRenderLayerAdjustmentAndUnlock defaultRenderGlobals.endFrame;')
            maya.mel.eval('removeRenderLayerAdjustmentAndUnlock defaultRenderGlobals.byFrameStep;')
            maya.mel.eval('removeRenderLayerAdjustmentAndUnlock defaultRenderGlobals.modifyExtension;')
            maya.mel.eval('removeRenderLayerAdjustmentAndUnlock defaultRenderGlobals.startExtension;')
            logSetAttr('defaultRenderGlobals.modifyExtension',1)
            if (argValid(arg.FPadding)):
                logSetAttr('defaultRenderGlobals.extensionPadding',int(arg.FPadding))
            if (not argValid(arg.FrOffset)):
                arg.FrOffset=0

        
        if (argValid(arg.Camera)): 
            logMessage("Set camera to '" +arg.Camera+"'" )
            maya.mel.eval('makeCameraRenderable("'+arg.Camera+'")')

        if (argValid(arg.Threads)):
            logMessage("Set threads to '" +arg.Threads+"'" )
            cmds.threadCount( n=arg.Threads )

        if (argValid(arg.ResX)): 
            logMessage("Set width to '" +arg.ResX+"'" )
            logSetAttr('defaultResolution.width',int(arg.ResX))
        if (argValid(arg.ResY)): 
            logMessage("Set height to '" +arg.ResY+"'" )
            logSetAttr('defaultResolution.height',int(arg.ResY))


        if (arg.Renderer == "mayaSoftware"):
            setRenderSettings_MayaSoftware(arg)
        elif (arg.Renderer == "mentalRay"):
            setRenderSettings_MRay(arg)
        elif (arg.Renderer == "vray"):
            setRenderSettings_VRay(arg)
        elif (arg.Renderer == "arnold"):
            setRenderSettings_Arnold(arg)
        elif (arg.Renderer == "redshift"):
            setRenderSettings_Redshift(arg)
      


        maya.mel.eval('setImageSizePercent(-1.)')
        logSetAttr('defaultRenderGlobals.renderAll',1)
            

        arg.FrStart=int(arg.FrStart)
        arg.FrEnd=int(arg.FrEnd)
        arg.FrStep=int(arg.FrStep)
        global globalArg
        globalArg=arg #copy for kso render
        timeEnd=datetime.datetime.now()
        timeEnd=timeEnd - timeStart;
        logMessage("Scene load time: "+str(timeEnd)+"  h:m:s.ms")
        logMessage("Scene init done, starting to render... ")
        flushLog()

        if (argValid(arg.OverwriteRenderCmd)):
            render_overwrite(arg)
        elif (argValid(arg.KSOMode) and arg.KSOMode): 
            render_KSO(arg)
        else:
            render_default(arg)
            
        logMessage("Render done")
    except Exception as e:
        logMessageError(str(e))
    flushLog()
    logMessage("                                      .   ")
    logMessage("                                     ...  ")
    logMessage("                                    ..... ")
    logMessage("                                   .......")
    flushLog()
    time.sleep(2) #some delay as some log messages seem to be cut off

print("RR kso_maya.py script  v 7.0.24 loaded\n")
flushLog()

