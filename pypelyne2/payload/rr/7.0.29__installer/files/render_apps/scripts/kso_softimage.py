# Render script for Softimage
#  v 7.0.24
#  Copyright (c)  Holger Schoenberger - Binary Alchemy

import datetime
import time
import sys



xsi = Application
    
def logMessageGen(lvl, msg):
    if (len(lvl)==0):
        xsi.LogMessage(datetime.datetime.now().strftime("' %H:%M.%S") + " rrSI      : " + str(msg))
    else:
        xsi.LogMessage(datetime.datetime.now().strftime("' %H:%M.%S") + " rrSI - " + str(lvl) + ": " + str(msg))

def logMessage(msg):
    logMessageGen("",msg)
    
def logMessageDebug( msg):
    if (False):
        logMessageGen("DGB", msg)

def logMessageError(msg):
    logMessageGen("ERR", str(msg)+"\n\n")

def flushLog():
    sys.stdout.flush()        
    sys.stderr.flush()    
    

def argValid(argValue):
    return ((argValue!= None) and (len(str(argValue))>0))
    
    

def applyRendererOptions_Arnold(arg):
    if ((arg.RenderDemo!= None) and (len(str(arg.RenderDemo))>0)):
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.skip_license_check",True)
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.abort_on_license_fail",False)
    else:
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.skip_license_check",False)
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.abort_on_license_fail",True)
    if ((arg.ArnoldAc!= None) and (len(str(arg.ArnoldAc))>0)):
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.AA_samples",arg.ArnoldAc)
    if ((arg.Verbose!= None) and (len(str(arg.Verbose))>0)):
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.log_level",arg.Verbose)
    if ((arg.RenderThreads!= None) and (len(str(arg.RenderThreads))>0)):
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.autodetect_threads",False)
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.threads",arg.RenderThreads)
    if ((arg.RenderDisplace!= None) and (len(str(arg.RenderDisplace))>0)):
        xsi.SetValue(str(arg.Pass)+".Arnold_Render_Options.ignore_displacement",arg.RenderDisplace)


def applyRendererOptions_Vray(arg):
    if ((arg.Verbose!= None) and (len(str(arg.Verbose))>0)):
        xsi.SetValue(str(arg.Pass)+".VRay_Options.sys_level",arg.Verbose)
    filName=arg.FName
    dirName=""
    PD="/"
    if (arg.FName.find("\\")>=0):
        PD="\\"
    pos= arg.FName.rfind(PD);
    if (pos>0):
        filName= arg.FName[pos+1:]
        dirName= arg.FName[0:pos]
    pos= filName.rfind(".");
    if (pos>0):
        filName= filName[0:pos]
    pos= filName.rfind(".#");
    if (pos>0):
        filName= filName[0:pos]
    filName=filName.replace(".[Frame ]", ".")
    logMessage("Set vray out dirname " +dirName)
    logMessage("Set vray out filename " +filName)
    xsi.SetValue(str(arg.Pass)+".VRay_Options.out_save_in",dirName)
    xsi.SetValue(str(arg.Pass)+".VRay_Options.out_img_file_name",filName)
    xsi.SetValue(str(arg.Pass)+".VRay_Options.gsw_dont_rend_finimg",False)
    
    


def applyRendererOptions_MRay(arg):
    if ((arg.RenderDisplace!= None) and (len(str(arg.RenderDisplace))>0)):
        xsi.SetValue(str(arg.Pass)+".mentalray.EnableDisplacementShaders",arg.RenderDisplace)
    if ((arg.Verbose!= None) and (len(str(arg.Verbose))>0)):
        xsi.SetValue(str(arg.Pass)+".mentalray.VerbosityLevel",arg.Verbose)
    if ((arg.MrayAAsmin!= None) and (len(str(arg.MrayAAsmin))>0)):
        xsi.SetValue(str(arg.Pass)+".mentalray.SamplesMin",arg.MrayAAsmin)
    if ((arg.MrayAAsmax!= None) and (len(str(arg.MrayAAsmax))>0)):
        xsi.SetValue(str(arg.Pass)+".mentalray.SamplesMax",arg.MrayAAsmax)


def applyRendererOptions_Redshift(arg):
    if ((arg.RsCudaDevices!= None) and (len(str(arg.RsCudaDevices))>0)):
        deviceIDs= list(set(arg.RsCudaDevices.split("."))) #set removed dublicate entries
        devString="["
        for i in range(0,len(deviceIDs)):
            devstr= deviceIDs[i]
            devstr= devstr.strip()
            if (len(devstr)>0):
                devString= devString+devstr+","
        devString=devString[:-1]+"]"
        logMessage("Set SelectCudaDevices to "+devString)
        Application.Redshift_SelectCudaDevices(eval(devString)) 



kso_global__Pass = ""

def ksoRenderFrame(FrStart,FrEnd,FrStep ):
    logMessage("Changing scene frame to frame #"+str(FrStart)+" ...")
    xsi.SetValue("PlayControl.Current", FrStart, "")
    xsi.SceneRefresh()
    logMessage("Starting to render frame #"+str(FrStart)+" ...")
    global kso_global__Pass
    beforeFrame=datetime.datetime.now()
    flushLog()
    xsi.renderpass (kso_global__Pass ,"",  FrStart,FrEnd,FrStep)
    flushLog()
    nrofFrames=((FrEnd-FrStart)/FrStep+1)
    afterFrame=datetime.datetime.now()
    afterFrame=afterFrame-beforeFrame;
    afterFrame=afterFrame/nrofFrames
    logMessage("Average time per frame: "+str(afterFrame)+"  h:m:s.ms")
    logMessage("rrKSO Frame(s) done #"+str(FrEnd)+" ")
    logMessage("                                                            ")
    logMessage("                                                            ")
    logMessage("                                                            ")
    flushLog()
    



def rrKSOStartServer(arg):
    logMessage("rrKSO startup...")
    if ((arg.KSOPort== None) or (len(str(arg.KSOPort))<=0)):
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
        logMessage("                                                            ")
        logMessage("rrKSONextCommand '"+ kso_tcp.rrKSONextCommand+"'")   
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
    global kso_global__Pass
    kso_global__Pass= arg.Pass
    rrKSOStartServer(arg)
    
    
def render_default(arg):
    xsi.renderpass (arg.Pass ,"",  arg.FrStart,arg.FrEnd,arg.FrStep)



def render_overwrite(arg):
    cmdline=arg.OverwriteRenderCmd
    cmdline=cmdline.replace("aFrStart",str(arg.FrStart))
    cmdline=cmdline.replace("aFrEnd",str(arg.FrEnd))
    cmdline=cmdline.replace("aFrStep",str(arg.FrStep))
    cmdline=cmdline.replace("'","\"")
    if (argValid(arg.FDir)):
        cmdline=cmdline.replace("aFDir",str(arg.FDir))
    if (argValid(arg.FName)):
        cmdline=cmdline.replace("aFName",str(arg.FName))
    if (argValid(arg.ArchiveExportName)):
        cmdline=cmdline.replace("aArchiveExportName",str(arg.ArchiveExportName))
    if (argValid(arg.FrOffset)):
        cmdline=cmdline.replace("aFrOffset",str(arg.FrOffset))
    if (argValid(arg.Renderer)):
        cmdline=cmdline.replace("aRenderer",str(arg.Renderer))
    if (argValid(arg.Layer)):
        cmdline=cmdline.replace("aLayer",str(arg.Layer))
    if (argValid(arg.Camera)):
        cmdline=cmdline.replace("aCamera",str(arg.Camera))
    maya.mel.eval(cmdline)
    


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
        #argAll is almost a JSON string, but it is not to keep the commandline cleaner and less error prone
        allArgList= argAll.split(",")   
        self.SName=getParam(allArgList,"SName")
        self.KSOMode=getParam(allArgList,"KSOMode")
        self.KSOPort=getParam(allArgList,"KSOPort")
        self.Database=getParam(allArgList,"Db")
        self.Pass=getParam(allArgList,"Pass")
        self.SkipFrame=getParam(allArgList,"SkipFrame")
        self.FName=getParam(allArgList,"FName")
        self.FExt=getParam(allArgList,"FExt")
        self.FPadding=getParam(allArgList,"FPadding")
        self.FType=getParam(allArgList,"FType")
        self.FNameChannelAdd=getParam(allArgList,"FNameChannelAdd")
        self.FrStart=getParam(allArgList,"FrStart")
        self.FrEnd=getParam(allArgList,"FrEnd")
        self.FrStep=getParam(allArgList,"FrStep")
        self.FrOffset=getParam(allArgList,"FrOffset")
        self.Camera=getParam(allArgList,"Camera")
        self.Verbose=getParam(allArgList,"Verbose")
        self.MrayAAsmin=getParam(allArgList,"MrayAAsmin")
        self.MrayAAsmax=getParam(allArgList,"MrayAAsmax")
        self.ArnoldAc=getParam(allArgList,"ArnoldAc")
        self.ResX=getParam(allArgList,"ResX")
        self.ResY=getParam(allArgList,"ResY")
        self.RegionX1=getParam(allArgList,"RegionX1")
        self.RegionX2=getParam(allArgList,"RegionX2")
        self.RegionY1=getParam(allArgList,"RegionY1")
        self.RegionY2=getParam(allArgList,"RegionY2")
        self.RenderThreads=getParam(allArgList,"RenderThreads")
        self.RenderDemo=getParam(allArgList,"RenderDemo")
        self.RenderDisplace=getParam(allArgList,"RenderDisplace")
        self.PyModPath=getParam(allArgList,"PyModPath")     
        self.ArchiveExportEnabled=getParam(allArgList,"ArchiveExport")
        self.ArchiveExportName=getParam(allArgList,"ArchiveExportName")
        self.OverwriteRenderCmd= getParam(allArgList,"OverwriteRenderCmd")
        self.RsCudaDevices= getParam(allArgList,"RsCudaDevices")
        

def rrStart(argAll):
    flushLog()
    logMessage("")
    timeStart=datetime.datetime.now()
    arg=argParser()
    arg.readArguments(argAll)
    
    wgstrg=xsi.GetValue("preferences.data_management.workgroup_appl_path")
    logMessage( "Active Shader Workgroup: " + str(wgstrg))

    

    if ((arg.PyModPath!= None) and (len(arg.PyModPath)>0)):
        import sys
        sys.path.append(arg.PyModPath)

    global kso_tcp
    import kso_tcp            

        
    if ((arg.Database!= None) and (len(arg.Database)>0)):
        logMessage("Set project to '" + arg.Database+"'...")
        xsi.ActiveProject = arg.Database 
    logMessage( "Active Project: " + str(xsi.ActiveProject2.Path))

    logMessage( "Loading Scene '" + str(arg.SName)+"'...")
    xsi.OpenScene(arg.SName, False, "")
    if ((arg.Database!= None) and (len(arg.Database)>0)):
        logMessage("Set project to '" + arg.Database+"'...")
        xsi.ActiveProject = arg.Database 
    logMessage( "Active Project: " + str(xsi.ActiveProject2.Path))


    if ((arg.Pass!= None) and (len(arg.Pass)>0)):
        logMessage("Set pass to '" + str(arg.Pass) +"'")
        arg.Pass= "Passes." + str(arg.Pass)
        xsi.SetCurrentPass(str(arg.Pass))
    else:
        arg.Pass= xsi.GetCurrentPass()
        logMessage("Using current pass '" + arg.Pass +"'")
        
    renderer=xsi.GetValue(str(arg.Pass)+".renderer")
    if (len(renderer)==0):
        renderer = xsi.GetValue("Passes.RenderOptions.Renderer")    
    logMessage("renderer used: '" + renderer +"'")
    
    if ((arg.Camera!= None) and (len(arg.Camera)>0)):
        logMessage("Set renderer to " +arg.Camera)
        xsi.SetValue(str(arg.Pass)+".Camera",arg.Camera)
        
    if ((arg.SkipFrame!= None) and (len(str(arg.SkipFrame))>0)):
        logMessage("Set FrameSkipRendered to " +str(arg.SkipFrame))
        xsi.SetValue(str(arg.Pass)+".FrameSkipRendered",arg.SkipFrame)

    if ((arg.ResX!= None) and (len(str(arg.ResX))>0)):
        logMessage("Set width to " +str(arg.ResX))
        if (xsi.GetValue(str(arg.Pass)+".ImageFormatOverride")):
            xsi.SetValue(str(arg.Pass)+".ImageWidth",arg.ResX)
        else:
            xsi.SetValue("Passes.RenderOptions.ImageWidth",arg.ResX)

    if ((arg.ResY!= None) and (len(str(arg.ResY))>0)):
        logMessage("Set height to " +str(arg.ResY))
        if (xsi.GetValue(str(arg.Pass)+".ImageFormatOverride")):
            xsi.SetValue(str(arg.Pass)+".ImageLockAspectRatio",False)
            xsi.SetValue(str(arg.Pass)+".ImageHeight",arg.ResY)
        else:
            xsi.SetValue("Passes.RenderOptions.ImageLockAspectRatio",False)
            xsi.SetValue("Passes.RenderOptions.ImageHeight",arg.ResY)

    if ((arg.RegionX1!= None) and (len(str(arg.RegionX1))>0)):
        xsi.SetValue(str(arg.Pass)+".CropWindowEnabled",True)
        xsi.SetValue(str(arg.Pass)+".SelectionTracking",False)
        xsi.SetValue(str(arg.Pass)+".CropWindowOffsetY",0)
        xsi.SetValue(str(arg.Pass)+".CropWindowHeight",9999)
        arg.RegionX1=int(arg.RegionX1)
        arg.RegionX2=int(arg.RegionX2)
        xsi.SetValue(str(arg.Pass)+".CropWindowOffsetX",arg.RegionX1)
        xsi.SetValue(str(arg.Pass)+".CropWindowWidth",(arg.RegionX2-arg.RegionX1+1))
        if ((arg.RegionY1!= None) and (len(str(arg.RegionY1))>0)):
            arg.RegionY1=int(arg.RegionY1)
            arg.RegionY2=int(arg.RegionY2)
            xsi.SetValue(str(arg.Pass)+".CropWindowOffsetY",arg.RegionY1)
            xsi.SetValue(str(arg.Pass)+".CropWindowHeight",(arg.RegionY2-arg.RegionY1+1))
            logMessage("Set region to X:" +str(arg.RegionX1)+"-" +str(arg.RegionX2)+"  Y:" +str(arg.RegionY1)+"-" +str(arg.RegionY2))
        else:
            logMessage("Set region to X:" +str(arg.RegionX1)+"-" +str(arg.RegionX2))
        
    if ((arg.FPadding!= None) and (len(str(arg.FPadding))>0)):
        if (arg.FPadding<=4):
            logMessage("Set frame padding to " +str(arg.FPadding))
            xsi.SetValue("Passes.RenderOptions.FramePadding",arg.FPadding)
    
    arg.FNameCopy=arg.FName

    if ((arg.FName!= None) and (len(str(arg.FName))>0)):
        xsi.SetValue(str(arg.Pass)+".Main.Enabled", True)
        arg.FName=arg.FName.replace("<Layer>", "[Pass]")
        arg.FName=arg.FName.replace("<Channel>", "[Framebuffer]")
        arg.FName=arg.FName.replace("<Camera>", "[Camera]")
        arg.FName=arg.FName.replace("<Camera_no.>", "[Camera]")
        orgFileName=xsi.GetValue(str(arg.Pass)+".Main.Filename")      
        if ((arg.FPadding!= None) and (len(str(arg.FPadding))>0)):
            if (arg.FPadding>4):
                for o in range(1, int(arg.FPadding)):
                    arg.FName= arg.FName+"#"
            else:
                arg.FName= arg.FName+"[Frame]"
        else:
            arg.FName= arg.FName + "[Frame "
            if ((arg.FrOffset!= None) and (len(str(arg.FrOffset))>0) and (int(arg.FrOffset)!=0)):
                if (int(arg.FrOffset<0)):
                    arg.FName= arg.FName + str(arg.FrOffset)
                else:
                    arg.FName= arg.FName + "+" +str(arg.FrOffset)
            arg.FName= arg.FName + "]"
        if ((arg.FExt!= None) and (len(arg.FExt)>0)):
            arg.FName= arg.FName + arg.FExt
        logMessage("Set Filename to " +arg.FName)
        xsi.SetValue(str(arg.Pass)+".Main.Filename",arg.FName)      
        if ((renderer=="Arnold Render" or renderer=="Redshift") and (orgFileName.lower().find("framebuffer")<=0)):
            oPass= xsi.GetValue(str(arg.Pass))
            for fbuffer in oPass.Framebuffers:
                if (orgFileName==xsi.GetValue(fbuffer.FileName)):
                    logMessage("Set Channel Filename to " +arg.FName)
                    fbuffer.FileName=arg.FName


    if ((arg.FNameChannelAdd!= None) and (len(str(arg.FNameChannelAdd))>0)):
        oPass= xsi.GetValue(str(arg.Pass))
        for fbuffer in oPass.Framebuffers:
            if (fbuffer.name!="Main"):
                chFname= xsi.GetValue(fbuffer.Filename)
                if (chFname!=arg.FName):
                    chDname=""
                    spos=chFname.lower().find("[Frame")  
                    if (spos>0):
                        chDname =  chFname[spos:]
                        chFname =  chFname[0:spos-1]
                        chDname="."+chdname
                    else:
                        spos=chFname.lower().find("#")
                        if (spos>0):
                            chDname = chFname[spos:]
                            chFname = chFname[0:spos-1]
                            chDname="."+chDname
                    if ((chFname[-1] != ".") and (chFname[-1] != "_")):
                        chFname=chFname +"."
                    chFname= chFname + arg.FNameChannelAdd + chDname
                    xsi.SetValue(fbuffer.Filename, chFname)
                    logMessage("Set framebuffer output to " +arg.FName)
    if (renderer=="Arnold Render"):
        applyRendererOptions_Arnold(arg)
    elif (renderer=="VRay"):
        applyRendererOptions_Vray(arg)
    elif (renderer=="Redshift"):
        applyRendererOptions_Redshift(arg)
    else:
        applyRendererOptions_MRay(arg)

       
    

    arg.FrStart=int(arg.FrStart)
    arg.FrEnd=int(arg.FrEnd)
    arg.FrStep=int(arg.FrStep)
    logMessage("Changing current frame to " +str(arg.FrStart))
    xsi.SetValue("PlayControl.Current", arg.FrStart, "")
    xsi.SceneRefresh()


    timeEnd=datetime.datetime.now()
    timeEnd=timeEnd - timeStart;
    logMessage("Scene load time: "+str(timeEnd)+"  h:m:s.ms")
    logMessage("Scene init done, starting to render... ")
    flushLog()

    if (argValid(arg.OverwriteRenderCmd)):
        render_overwrite(arg)
    elif (argValid(arg.KSOMode)): 
        render_KSO(arg)
    else:
        render_default(arg)
        
    logMessage("Render done")
    logMessage("                                        ")
    logMessage("                                        ")
    logMessage("                                        ")
    logMessage("                                        ")
    flushLog()
    return 0


