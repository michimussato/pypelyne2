# Example script to simulate something with RR.
#  v 7.0.11
#  Copyright (c)  Holger Schoenberger - Binary Alchemy

import datetime
import time
import sys
xsi = Application
    
def logMessage(lvl, msg):
    if (len(lvl)==0):
        xsi.LogMessage(datetime.datetime.now().strftime("' %H:%M.%S") + " rrSI      : " + str(msg))
    else:
        xsi.LogMessage(datetime.datetime.now().strftime("' %H:%M.%S") + " rrSI - " + str(lvl) + ": " + str(msg))
    
def logMessageDebug( msg):
    if (False):
        logMessage("DGB", msg)

def flushLog():
    sys.stdout.flush()        
    sys.stderr.flush()    
    

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
            logMessage("","Flag  "+argFindName.ljust(15)+": '"+str(argValue)+"'");
            return argValue
    return ""


class argParser:
    def readArguments(self,argAll):
        #argAll is almost a JSON string, but it is not to keep the commandline cleaner and less error prone
        allArgList= argAll.split(",")   
        self.PyModPath=getParam(allArgList,"PyModPath")
        self.KSOMode=getParam(allArgList,"KSOMode")
        self.KSOPort=getParam(allArgList,"KSOPort")
        self.SName=getParam(allArgList,"SName")
        self.Database=getParam(allArgList,"Db")
        self.Pass=getParam(allArgList,"Pass")
        self.Pass=getParam(allArgList,"emObject")
        self.FName=getParam(allArgList,"FName")
        self.FExt=getParam(allArgList,"FExt")
        self.FPadding=getParam(allArgList,"FPadding")
        self.FrStart=getParam(allArgList,"FrStart")
        self.FrEnd=getParam(allArgList,"FrEnd")
        self.FrStep=getParam(allArgList,"FrStep")
        self.Verbose=getParam(allArgList,"Verbose")
        self.RenderThreads=getParam(allArgList,"RenderThreads")



def render_emRPC_frame(emObj, FrStart,FrEnd,FrStep):
    # Cache to force emRPC4 to render.
    filePath = os.environ["TEMP"]  # "TEMP" is set by RR to RR_localdata and deleted before/after each job
    fileName = "[object]_[version]_[frame #5]"
    versionString = "temp"

    writeAnimation = xsi.Dictionary.GetObject("WriteAnimation")
    writeAnimation.Parameters("FilePath").PutValue2(None, filePath)
    writeAnimation.Parameters("FileName").PutValue2(None, fileName)
    writeAnimation.Parameters("VersionString").PutValue2(None, versionString)
    writeAnimation.Parameters("FileType").PutValue2(None, 0)

    cachePath = os.path.join(filePath, fileName + ".icecache")
    cachePath = cachePath.replace("[version]", versionString).replace("[frame #4]", "####")
    logMessage("","Starting to render frame #"+str(FrStart)+"-"+str(FrEnd)+","+str(FrStep)+" ...")
    xsi.CacheObjectsIntoFile(emObj, 5, FrStart, FrEnd, FrStep, False, False, "", versionString, cachePath, False)
    return True




kso_global__emObj = ""



def ksoRenderFrame(FrStart,FrEnd,FrStep ):
    logMessage("","Changing scene frame to frame #"+str(FrStart)+" ...")
    xsi.SetValue("PlayControl.Current", FrStart, "")
    xsi.SceneRefresh()
    logMessage("","Starting to render frame #"+str(FrStart)+" ...")
    
    beforeFrame=datetime.datetime.now()
    flushLog()
    global kso_global__emObj
    render_emRPC_frame(kso_global__emObj,FrStart,FrEnd,FrStep)
    flushLog()
    nrofFrames=((FrEnd-FrStart)/FrStep+1)
    afterFrame=datetime.datetime.now()
    afterFrame=afterFrame-beforeFrame;
    afterFrame=afterFrame/nrofFrames
    logMessage("","Average time per frame: "+str(afterFrame)+"  h:m:s.ms")
    logMessage("","rrKSO Frame(s) done #"+str(FrEnd)+" ")
    xsi.LogMessage("                                                            ")
    xsi.LogMessage("                                                            ")
    xsi.LogMessage("                                                            ")
    flushLog()

    

def rrKSOStartServer(arg):
    import kso_tcp
    kso_tcp.log_command="Application.LogMessage(' \\\'"
    logMessage("","rrKSO startup...")
    if ((arg.KSOPort== None) or (len(str(arg.KSOPort))<=0)):
        arg.KSOPort=7774
    HOST, PORT = "localhost", 7774
    server = kso_tcp.rrKSOServer((HOST, PORT), kso_tcp.rrKSOTCPHandler)
    flushLog()
    logMessage("","rrKSO server started")
    flushLog()
    kso_tcp.rrKSONextCommand=""
    while server.continueLoop:
        try:
            logMessageDebug("rrKSO waiting for new command...")
            server.handle_request()
            time.sleep(1) # handle_request() seem to return before handle() completed execution
        except Exception, e:
            logMessage("ERR", e)
            server.continueLoop= False;
            import traceback
            logMessage("ERR",traceback.format_exc())
        logMessage("","                                                            ")
        logMessage("","                                                            ")
        logMessage("","                                                            ")
        logMessage("","rrKSONextCommand '"+ kso_tcp.rrKSONextCommand+"'")   
        flushLog()
        if (len(kso_tcp.rrKSONextCommand)>0):
            if ((kso_tcp.rrKSONextCommand=="ksoQuit()") or (kso_tcp.rrKSONextCommand=="ksoQuit()\n")):
                server.continueLoop=False
                kso_tcp.rrKSONextCommand=""
            else:
                exec (kso_tcp.rrKSONextCommand)
                kso_tcp.rrKSONextCommand=""
    logMessage("","rrKSO closed")





def render_KSO(arg):
    # Get objects to cache.
    if ((arg.emObject== None) or (len(arg.emObject)==0)):
        logMessage("","No emObject specified")
        return False

    emObj=[]
    if ((arg.emObject.lower()=="emcache_group") or (arg.emObject.lower()=="cache_group") ):
        emObj = xsi.Dictionary.GetObject(arg.emObject, False)
        if (not emObj):
            logMessage("ERR", "Couldn't find '"+arg.emObject+"'.")
            return False
        logMessage("","Caching  '" + emObj.GetAsText() +"'")        
    else:
        emObj=xsi.Dictionary.GetObject(arg.emObject, False)
        if (not emObj):
            logMessage("ERR", "Couldn't find '" + str(arg.emObject) +"'.")
            return False
        logMessage("","Caching  '" + str(emObj) +"'")
    logMessage("","Importing kso...")
    global kso_global__emObj
    kso_global__emObj= emObj
    rrKSOStartServer(arg)
    return True





def render_default(arg):
    # Get objects to cache.
    if ((arg.emObject== None) or (len(arg.emObject)==0)):
        logMessage("","No emObject specified")
        return False

    emObj=[]
    if ((arg.emObject.lower()=="emcache_group") or (arg.emObject.lower()=="cache_group") ):
        emObj = xsi.Dictionary.GetObject(arg.emObject, False)
        if (not emObj):
            logMessage("ERR", "Couldn't find '"+arg.emObject+"'.")
            return False
        logMessage("","Caching  '" + emObj.GetAsText() +"'")        
    else:
        emObj=xsi.Dictionary.GetObject(arg.emObject, False)
        if (not emObj):
            logMessage("ERR", "Couldn't find '" + str(arg.emObject) +"'.")
            return False
        logMessage("","Caching  '" + str(emObj) +"'")
    render_emRPC_frame(emObj,arg.FrStart,arg.FrEnd,arg.FrStep)
    return True




def rrStart(argAll):
    flushLog()
    logMessage("","")
    timeStart=datetime.datetime.now()
    arg=argParser()
    arg.readArguments(argAll)
    
    wgstrg=xsi.GetValue("preferences.data_management.workgroup_appl_path")
    logMessage("", "Active Shader Workgroup: " + str(wgstrg))
    

    if ((arg.PyModPath!= None) and (len(arg.PyModPath)>0)):
        import sys
        sys.path.append(arg.PyModPath)
        
    if ((arg.Database!= None) and (len(arg.Database)>0)):
        logMessage("","Set project to '" + arg.Database+"'...")
        xsi.ActiveProject = arg.Database 
    logMessage("", "Active Project: " + str(xsi.ActiveProject2.Path))

    logMessage("", "Loading Scene '" + str(arg.SName)+"'...")
    xsi.OpenScene(arg.SName, False, "")
    if ((arg.Database!= None) and (len(arg.Database)>0)):
        logMessage("","Set project to '" + arg.Database+"'...")
        xsi.ActiveProject = arg.Database 
    logMessage("", "Active Project: " + str(xsi.ActiveProject2.Path))

    if ((arg.Pass!= None) and (len(arg.Pass)>0)):
        logMessage("","Set pass to '" + str(arg.Pass) +"'")
        arg.Pass= "Passes." + str(arg.Pass)
        xsi.SetCurrentPass(str(arg.Pass))
    else:
        arg.Pass= xsi.GetCurrentPass()
        logMessage("","Using current pass '" + str(arg.Pass) +"'")


    arg.FrStart=int(arg.FrStart)
    arg.FrEnd=int(arg.FrEnd)
    arg.FrStep=int(arg.FrStep)
    logMessage("","Changing current frame to " +str(arg.FrStart))
    xsi.SetValue("PlayControl.Current", arg.FrStart, "")
    xsi.SceneRefresh()
    timeEnd=datetime.datetime.now()
    timeEnd=timeEnd - timeStart;
    logMessage("","Scene load time: "+str(timeEnd)+"  h:m:s.ms")
    logMessage("","Scene init done, starting to render... ")
    flushLog()

    rtn = True
    if ((arg.KSOMode!= None) and (len(str(arg.KSOMode))>0)):
        rtn=render_KSO(arg)
    else:
        rtn=render_default(arg)


    if not rtn:
        logMessage("ERR", "Render failed.")
        exit = 1
    else:
        logMessage("", "Render done.")
        exit = 0
    flushLog()
    return exit

