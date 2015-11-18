#python
# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Render script for Houdini
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Version v 7.0.20
# Copyright (c) Holger Schoenberger - Binary Alchemy
# 
######################################################################

import datetime
import time
import sys


   
def logMessageGen(lvl, msg):
    if (len(lvl)==0):
        print(datetime.datetime.now().strftime("' %H:%M.%S") + " rrHoudini      : " + str(msg))
    else:
        print(datetime.datetime.now().strftime("' %H:%M.%S") + " rrHoudini - " + str(lvl) + ": " + str(msg))

def logMessage(msg):
    logMessageGen("",msg)
    
def logMessageDebug( msg):
    if (False):
        logMessageGen("DGB", msg)

def logMessageSET(msg):
    logMessageGen("SET",msg)

def flushLog():
    sys.stdout.flush()        
    sys.stderr.flush()    

def logMessageError(msg):
    logMessageGen("ERR", str(msg)+"\n\n")
    flushLog();
    raise NameError("\nError reported, aborting render script\n")

def argValid(argValue):
    return ((argValue!= None) and (len(str(argValue))>0))


class argParser:
    def getParam(self,argFindName):
        argFindName=argFindName.lower()
        for a in range(0,  len(sys.argv)):
            if ((sys.argv[a].lower()==argFindName) and (a+1<len(sys.argv))):
                argValue=sys.argv[a+1]
                if (argValue.lower()=="true"):
                    argValue=True
                elif (argValue.lower()=="false"):
                    argValue=False
                logMessage("Flag  "+argFindName.ljust(15)+": '"+str(argValue)+"'");
                return argValue
        return ""
    
    def readArguments(self):
        self.renderer= self.getParam("-renderer")
        self.rendererExportMode=self.getParam("-exportmode")
        self.sceneFile=self.getParam("-scene")
        self.FrStart=self.getParam("-FrStart")
        self.FrEnd=self.getParam("-FrEnd")
        self.FrStep=self.getParam("-FrStep")
        self.layer=self.getParam("-layer")
        self.FName=self.getParam("-FName")
        self.FRefName=self.getParam("-FRefName")
        self.FExt=self.getParam("-FExt")
        self.FPadding=self.getParam("-FPadding")
        self.camera=self.getParam("-camera")
        self.threads=self.getParam("-threads")
        self.verbose=self.getParam("-verbose")
        self.tile=self.getParam("-tile")
        self.totalTiles=self.getParam("-totalTiles")
        self.width=self.getParam("-width")
        self.height=self.getParam("-height")
        self.KSOMode=self.getParam("-KSOMode")
        self.KSOPort=self.getParam("-KSOPort")
        self.PyModPath=self.getParam("-PyModPath")


def formatExceptionInfo(maxTBlevel=5):
         import traceback
         cla, exc, trbk = sys.exc_info()
         excName = cla.__name__
         try:
             excArgs = exc.__dict__["args"]
         except KeyError:
             excArgs = "<no args>"
         excTb = traceback.format_tb(trbk, maxTBlevel)
         return (excName, excArgs, excTb)




def renderFrames(FrStart,FrEnd,FrStep):
    global arg
    FrStart=int(FrStart)
    FrEnd=int(FrEnd)
    FrStep=int(FrStep)
    try:
        imgRes = ()
        if (argValid(arg.width) and argValid(arg.height)):
            imgRes = (int(arg.width),int(arg.height))
        for fr in xrange(FrStart,FrEnd+1,FrStep):
            logMessage( "Rendering Frame #" + str(fr) +" ...")
            kso_tcp.writeRenderPlaceholder_nr(arg.FRefName, fr, arg.FPadding, arg.FExt)
            flushLog()
            beforeFrame=datetime.datetime.now()
            arg.rop.render( (fr,fr,FrStep),imgRes)
            nrofFrames=1
            afterFrame=datetime.datetime.now()
            afterFrame=afterFrame-beforeFrame;
            afterFrame=afterFrame/nrofFrames
            logMessage("Frame Time : "+str(afterFrame)+"  h:m:s.ms.  Frame Rendered #" + str(fr) )
            logMessage(" ")
            flushLog()
        
    except Exception as e:
        logMessageError(str(e))

    



def ksoRenderFrame(FrStart,FrEnd,FrStep ):
    renderFrames(FrStart,FrEnd,FrStep)
    flushLog()
    logMessage("rrKSO Frame(s) done #"+str(FrEnd)+" ")
    logMessage("                                                            ")
    logMessage("                                                            ")
    logMessage("                                                            ")
    flushLog()
    



def rrKSOStartServer():
    global arg
    try:
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
                logMessageError(e)
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
    except Exception as e:
        logMessageError(str(e))


def render_KSO():
    rrKSOStartServer()
        
def render_default():
    global arg
    renderFrames(arg.FrStart,arg.FrEnd,arg.FrStep)




def applyRendererOptions_default():
    global arg
    logMessage("Rendering with default renderer");
    if (argValid(arg.threads) and not arg.rendererExportMode):
        try:
            usemaxthread=arg.rop.parm('vm_usemaxthreads').set(0)
            arg.rop.parm('vm_threadcount').set(int(arg.threads))
        except hou.LoadWarning, e:
            logMessage( "Error: Unable to set thread count")
            logMessage( e)
    outFileName=arg.FName
    if (argValid(arg.totalTiles) and (int(arg.totalTiles)>1)):
        arg.rop.parm('vm_tile_render').set(1)
        arg.rop.parm('vm_tile_count_y').set(1)
       
        logMessageSET("vm_tile_count_x "+str(arg.totalTiles))
        arg.rop.parm('vm_tile_count_x').set(int(arg.totalTiles))
        logMessageSET("vm_tile_index "+str(arg.tile))
        arg.rop.parm('vm_tile_index').set(int(arg.tile))
        if (outFileName.endswith('.')):
            outFileName=outFileName+'.'
    logMessageSET("output name to "+outFileName)
    if (arg.rendererExportMode):
        arg.rop.parm('soho_outputmode').set(1)
        arg.rop.parm('soho_diskfile').set(outFileName +"$F"+str(arg.FPadding) + arg.FExt)
    else:
        arg.rop.parm('soho_outputmode').set(0)
        arg.rop.parm('vm_picture').set(outFileName +"$F"+str(arg.FPadding) + arg.FExt)

        
    
    
def applyRendererOptions_Arnold():
    global arg
    logMessage("Rendering with Arnold");
    if (arg.rendererExportMode):
        arg.rop.parm('ar_ass_export_enable').set(1)

    if (arg.rendererExportMode):
        arg.rop.parm('ar_ass_export_enable').set(1)
        arg.rop.parm('ar_ass_file').set(arg.FName +"$F"+str(arg.FPadding) + arg.FExt)
    else:
        arg.rop.parm('ar_ass_export_enable').set(0)
        arg.rop.parm('ar_picture').set(arg.FName +"$F"+str(arg.FPadding) + arg.FExt)
   
    


try:
    logMessage("init" )
    flushLog()
    timeStart=datetime.datetime.now()
    global arg
    arg=argParser()
    arg.readArguments()
    if (argValid(arg.PyModPath)):
        import sys
        logMessage("Append python search path with '" +arg.PyModPath+"'" )
        sys.path.append(arg.PyModPath)
        global kso_tcp
        import kso_tcp
    if (not argValid(arg.rendererExportMode)):
        arg.rendererExportMode=False
    if (not argValid(arg.FPadding)):
        arg.FPadding=1



    logMessage("loading scene file..." )
    flushLog()
    try:
        hou.hipFile.load( arg.sceneFile, True )
    except hou.LoadWarning, e:
        print( "Error: LoadWarning (probably wrong houdini version)")
        print( e)
    

    arg.rop = hou.node( arg.layer )
    if arg.rop == None:
        logMessageError("Driver node \"" + arg.layer + "\" does not exist" )

    if (arg.renderer=="arnold"):
        applyRendererOptions_Arnold()
    else:
        applyRendererOptions_default()

    timeEnd=datetime.datetime.now()
    timeEnd=timeEnd - timeStart;
    logMessage("Scene load time: "+str(timeEnd)+"  h:m:s.ms")
    logMessage("Scene init done, starting to render... ")
    flushLog()

    if (argValid(arg.KSOMode) and arg.KSOMode):
        render_KSO()
    else:
        render_default()



except hou.OperationFailed, e:
    logMessageError( e)
    print( formatExceptionInfo())
            
except:
    logMessageError( formatExceptionInfo())
