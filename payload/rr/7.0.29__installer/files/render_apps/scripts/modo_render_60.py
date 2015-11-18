#python
# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Render script for Modo
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Version v 7.0.20
# Copyright (c) Holger Schoenberger - Binary Alchemy
# 
######################################################################

import datetime
import time
import os
import sys
import random
import lx
import lxu


from lxu import select
scene_service = lx.service.Scene()
current_scene = lxu.select.SceneSelection().current()



   
def logMessageGen(lvl, msg):
    if (len(lvl)==0):
        print(datetime.datetime.now().strftime("' %H:%M.%S") + " rrModo      : " + str(msg))
    else:
        print(datetime.datetime.now().strftime("' %H:%M.%S") + " rrModo - " + str(lvl) + ": " + str(msg))

def logMessage(msg):
    logMessageGen("",msg)
    
def logMessageDebug( msg):
    if (False):
        logMessageGen("DGB", msg)

def flushLog():
    sys.stdout.flush()        
    sys.stderr.flush()    

def logMessageError(msg):
    logMessageGen("ERR", str(msg)+"\n\n")
    flushLog();
    lx.eval("app.quit")
    raise NameError("\nError reported, aborting render script\n")


class argParser:
    def readArguments(self):
        logMessage("readArguments()")
        self.FrStart=str(lx.args()[0])
        self.FrEnd=str(lx.args()[1])
        self.FrStep=str(lx.args()[2])
        self.imgNameAdd=""
        self.layer=""
        self.imgName=""
        self.imgExt=""
        self.padding="FFFF"
        self.passgroup=""
        self.cameraname=""
        self.isLayeredExr =False
        self.regX1=-1
        self.regX2=-1
        self.regY1=-1
        self.regY2=-1
        self.KSOMode=False
        self.KSOPort=6667
        self.PyModPath=""
        self.width=-1
        self.height=-1
        self.verboseLevel=0
        self.imgNameNoVar=""
        for a in range(0,  len(lx.args())):
            if (lx.args()[a].lower()=="-layeredexr"):
                self.isLayeredExr = True
            if ((lx.args()[a].lower()=="-layer") and (a+1<len(lx.args()))):
                self.layer=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-passgroup") and (a+1<len(lx.args()))):
                self.passgroup=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-imgname") and (a+1<len(lx.args()))):
                self.imgName=lx.args()[a+1]
            if ((lx.args()[a].lower()==("-imgNameNoVar").lower()) and (a+1<len(lx.args()))):
                self.imgNameNoVar=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-imgext") and (a+1<len(lx.args()))):
                self.imgExt=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-camera") and (a+1<len(lx.args()))):
                self.cameraname=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-imgnameadd") and (a+1<len(lx.args()))):
                self.imgNameAdd=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-padding") and (a+1<len(lx.args()))):
                self.padding=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-verbose") and (a+1<len(lx.args()))):
                self.verboseLevel=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-region") and (a+4<len(lx.args()))):
                self.regX1=lx.args()[a+1]
                self.regX2=lx.args()[a+2]
                self.regY1=lx.args()[a+3]
                self.regY2=lx.args()[a+4]
            if ((lx.args()[a].lower()=="-width") and (a+1<len(lx.args()))):
                self.width=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-height") and (a+1<len(lx.args()))):
                self.height=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-padding") and (a+1<len(lx.args()))):
                self.padding=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-ksomode")):
                self.KSOMode=True
            if ((lx.args()[a].lower()=="-ksoport") and (a+1<len(lx.args()))):
                self.KSOPort=lx.args()[a+1]
            if ((lx.args()[a].lower()=="-pymodpath") and (a+1<len(lx.args()))):
                self.PyModPath=lx.args()[a+1]


global globalArg




def render_frame(FrStart,FrEnd,FrStep):
    FrStart=int(FrStart)
    FrEnd=int(FrEnd)
    FrStep=int(FrStep)
    rend = current_scene.AnyItemOfType(scene_service.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
    chan = current_scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
    cout = lx.object.ChannelWrite(chan)
    idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_STEP)
    cout.Integer(rend, idx, FrStep)
    global globalArg
    try:
        for frameNr in xrange(FrStart,FrEnd+1,FrStep):
            idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_FIRST)
            cout.Integer(rend, idx, frameNr)
            idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_LAST)
            cout.Integer(rend, idx, frameNr)
            logMessage("Starting to render frame #"+str(frameNr)+"...")
            flushLog()
            if ((arg.imgNameNoVar)!=""):
                kso_tcp.writeRenderPlaceholder_nr(arg.imgNameNoVar, frameNr, len(arg.padding) , arg.imgExt)
            beforeFrame=datetime.datetime.now()
            if (globalArg.isLayeredExr):
                if (globalArg.passgroup!=""):
                    logMessage("Starting LayeredEXR and PassGroup Render ...")
                    lx.eval( "render.animation {*} openexrlayers group:" +globalArg.passgroup);
                else:
                    logMessage("Starting LayeredEXR Render ...")
                    lx.eval( "render.animation {*} openexrlayers " );
            else:
                if (globalArg.passgroup!=""):
                    logMessage("Starting PassGroup Render ...")
                    lx.eval( "render.animation {*} group:" +globalArg.passgroup);
                else:
                    logMessage("Starting Render ...")
                    lx.eval( "render.animation {*}" );
            nrofFrames=((FrEnd-FrStart)/FrStep+1)
            afterFrame=datetime.datetime.now()
            afterFrame=afterFrame-beforeFrame;
            logMessage("Frame time: "+str(afterFrame)+"  h:m:s.ms")
            flushLog()
    except:
        logMessageError ("Script crashed during render")
        lx.eval("app.quit")
        return False
    return True



def ksoRenderFrame(FrStart,FrEnd,FrStep ):
    render_frame(FrStart,FrEnd,FrStep)
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
    logMessage("default render...")
    render_frame(arg.FrStart,arg.FrEnd,arg.FrStep)




#Get all pass groups with all passes and per-pass renderlayer  overrides:
class rrPassGroup:
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.name = ""
        self.passes = []
        self.layer = []
        self.layerEnabled = []

def getPassInfo(rrPassGroupList):
    scService = lx.Service( "sceneservice" )
    allItems= scService.query("item.N")
    for obj in range(allItems):
        scService.select("item.id",str(obj))
        if (str(scService.query('item.type'))== "group"):
            gTags=scService.query("render.tags")
            if (gTags!=None and gTags=="render"):
                newPassGr= rrPassGroup()
                newPassGr.name=scService.query('item.name')
                #print ("getPassInfo - Pass Group "+newPassGr.name)
                passInternal=scService.query("pass.itemMembers")
                if (passInternal==None):
                    continue
                if (type(passInternal)==str):
                    passInternal=(passInternal,)
                #print ("getPassInfo - Pass Group "+newPassGr.name+"   "+str(type(passInternal)))
                for pas in passInternal:
                    name=lx.eval("item.name ? item:{%s}" % pas)
                    newPassGr.passes.append(name)
                    #print ("getPassInfo -     -pass "+name)
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
                                    #print(" getPassInfo -  Pass Group '"+newPassGr.name+"' - Pass '"+name+"' found override: "+chn+"  "+str(chnValue))
                rrPassGroupList.append(newPassGr)
                


##############################################################################
    #MAIN "FUNCTION":
##############################################################################
try:
    arg=argParser()
    arg.readArguments()

    if ((arg.PyModPath!= None) and (len(arg.PyModPath)>0)):
        import sys
        sys.path.append(arg.PyModPath)
        logMessage("Added "+arg.PyModPath+"to module search path")
    global kso_tcp
    import kso_tcp            


    sceneIsEmpty= True

    sceneLoaded= lx.eval( "query sceneservice scene.file ? current" )
    logMessage("Scene '"+str(sceneLoaded)+"' loaded")
    if (sceneLoaded!=None):
        sceneIsEmpty= False
        
##    totalItems=0
##    item_type = scene_service.ItemTypeLookup(lx.symbol.sITYPE_LIGHT)
##    totalItems = totalItems + current_scene.ItemCount(item_type)-1  #-1 as the default scene has one
##    item_type = scene_service.ItemTypeLookup(lx.symbol.sITYPE_CAMERA)
##    totalItems = totalItems + current_scene.ItemCount(item_type)-1  #-1 as the default scene has one
##    item_type = scene_service.ItemTypeLookup(lx.symbol.sITYPE_MESH)
##    totalItems = totalItems + current_scene.ItemCount(item_type)-1  #-1 as the default scene has one
##    if (totalItems>0):
##        sceneIsEmpty=False
##    if sceneIsEmpty:
##        meshName=current_scene.ItemByIndex(scene_service.ItemTypeLookup(lx.symbol.sITYPE_MESH), 0).UniqueName()
##        if (meshName!="Mesh"):
##            sceneIsEmpty=False
##    if sceneIsEmpty:
##        logMessage("\n\nWARNING: The scene seems might have been unable to be loaded. This could be caused by a missing texture.\n")
##        sceneIsEmpty=False
##        lx.eval("query layerservice layer.id ? Mesh")
##        num_verts = lx.eval("query layerservice vert.n ?")
##        print ("number of vertices in the scene: "+str(num_verts))
        
    
    if (sceneIsEmpty):
        logMessageError ("Unable to load the scene file. This can be caused by a texture not found.")
        
    
    ### set the memory cache settings
    memory= 20
    logMessage("Set render.cacheSize to "+str(memory)+" GB" )
    memory=memory*1024*1024*1024 #convert GB into Bytes
    lx.eval( "pref.value render.cacheSize "+str(memory) )
    memory= 6
    logMessage ("Set render.frameCacheSize to "+str(memory)+" GB" )
    memory=memory*1024*1024*1024 #convert GB into Bytes
    lx.eval( "pref.value render.frameCacheSize "+str(memory) )

    if (arg.verboseLevel>0):
        lx.eval("log.toConsole true")
    if (arg.verboseLevel>1):
        lx.eval("log.toConsoleRolling true")


    if ((int(arg.width)>0) and (int(arg.height)>0)):
        logMessage("Set image resolution to "+str(arg.width)+"x"+str(arg.height))
        rend = current_scene.AnyItemOfType(scene_service.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
        chan = current_scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
        idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_RESX)
        cout = lx.object.ChannelWrite(chan)
        cout.Integer(rend, idx, int(arg.width))
        cout.Integer(rend, idx + 1, int(arg.height))


    if (arg.layer!=""):
        arg.imgName= arg.imgName.replace("<Layer>",arg.layer)
    else:
        arg.imgName= arg.imgName.replace("<Layer>","<output>")
        
    firstvar=arg.imgName.find("<")
    lastfolder=arg.imgName.rfind("/")
    if (lastfolder<=0):
        lastfolder=arg.imgName.find("\\")
    if (firstvar>=0 and lastfolder>=0 and lastfolder>firstvar):
        firstvar=lastfolder
        
    outPattern="";
    if (firstvar>=0):
        outPattern= arg.imgName[firstvar:]
        arg.imgName=arg.imgName[:firstvar]
        outPattern= outPattern.replace("<StereoLR>","[<LR>]")
        outPattern= outPattern.replace("<StereoRL>","[<LR>]")
        outPattern= outPattern.replace("<Channel>","<pass>")
        outPattern= outPattern.replace("<Camera>",arg.cameraname)
    outPattern= outPattern+ "<" + arg.padding + ">"

    if ((arg.layer!="") or (arg.passgroup!="")):
        logMessage("Set Output Pattern to \"" +outPattern+"\"")
        rend = current_scene.AnyItemOfType(scene_service.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
        chan = current_scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
        idx = rend.ChannelLookup(lx.symbol.sICHAN_POLYRENDER_OUTPAT)
        cout = lx.object.ChannelWrite(chan)
        cout.String(rend, idx, outPattern)
    
    logMessage("ImgName: \"" +arg.imgName+"\"")
    logMessage("ImgNameAdd: \"" +arg.imgNameAdd+"\"")

    if (arg.regX1!= -1):
        logMessage("Set region: " +str(arg.regX1)+" "+str(arg.regX2)+" "+str(arg.regY1)+" "+str(arg.regY2)+" ")
        lx.eval( "item.channel polyRender$region true" )
        lx.eval( "item.channel polyRender$regX0 %s" % arg.regX1 )
        lx.eval( "item.channel polyRender$regX1 %s" % arg.regX2 )
        lx.eval( "item.channel polyRender$regY0 %s" % arg.regY1 )
        lx.eval( "item.channel polyRender$regY1 %s" % arg.regY2 )    


    #get pass groups and enable/disable for each output layer
    if (arg.passgroup!=""):
        rrPassGroupList=[];
        getPassInfo(rrPassGroupList)
        logMessage("Found "+str(len(rrPassGroupList))+" pass groups")
        logMessage("PassGroup \"" +arg.passgroup+"\" set to render via commandline ")
        for pg in range(0, len(rrPassGroupList)):
            #logMessage("compare \"" +rrPassGroupList[pg].name+"\"  \"" +arg.passgroup+"\"")
            if (rrPassGroupList[pg].name==arg.passgroup):
                logMessage("    PassGroup: "+str(len(rrPassGroupList[pg].layer))+" layer overrides found")
                logMessage("    PassGroup: Applying layer overrides...")
                nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
                for L in range(0, nbOutputs):
                    layerName= lx.eval( "query sceneservice renderOutput.name ? "+str(L) );
                    objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
                    lx.eval( "select.item "+objID)
                    isEnabledOrg= lx.eval( "item.channel textureLayer$enable ?" );
                    isEnabled= isEnabledOrg;
                    overrideFound=False
                    for p in range(1,len(rrPassGroupList[pg].layer)):
                        if (layerName!=rrPassGroupList[pg].layer[p]):
                            continue
                        if (not overrideFound):
                            logMessage("    PassGroup:  Layer %15s  - first   override: %s" % (layerName, str(rrPassGroupList[pg].layerEnabled[p])))
                            isEnabled=rrPassGroupList[pg].layerEnabled[p]
                            overrideFound=True
                        elif rrPassGroupList[pg].layerEnabled[p]:
                            logMessage("    PassGroup:  Layer %15s  - another override: %s" % (layerName, str(rrPassGroupList[pg].layerEnabled[p])))
                            isEnabled=rrPassGroupList[pg].layerEnabled[p]
                    if (isEnabledOrg!=isEnabled):
                        if (isEnabled):
                            logMessage("         enable layer "+layerName)
                            lx.eval( "item.channel textureLayer$enable true" )
                        else:
                            logMessage("         disable layer "+layerName)
                            lx.eval( "item.channel textureLayer$enable false" )
        scService = lx.Service( "sceneservice" )
        nbItems= scService.query("item.N")
        for obj in range(nbItems):
            scService.select("item.id",str(obj))
            nbOutputs= scService.query("item")
            if (str(scService.query('item.type'))== "group"):
                name=scService.query('item.name')
                if (name==arg.passgroup):
                    arg.passgroup=scService.query('item.id')
                    logMessage("PassGroup to render: (internal modo name) \"" +arg.passgroup+"\"")


    if (arg.cameraname!=""):
        logMessage("Camera override: \"" +arg.cameraname+"\"")
        lx.eval( "render.camera \""+arg.cameraname+"\"" )


    #if we render one layer, enable it and set output 
    if (arg.layer!=""):
        logMessage("Layer to render: \"" +arg.layer+"\"")
        logMessage("List layers...")
        nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
        foundLayer=False
        for L in range(0, nbOutputs):
            #get layer by name
            layerName= lx.eval( "query sceneservice renderOutput.name ? "+str(L) );
            logMessage("    '" +layerName+"'")
            objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
            lx.eval( "select.item "+objID)
            isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
            if (layerName==arg.layer):
                foundLayer=True
                if (not isEnabled):
                    #set enabled
                    logMessage("        enable layer")
                    lx.eval( "item.channel textureLayer$enable true" )
                if (arg.imgName!=""):
                    logMessage("        set renderOutput to \"" +arg.imgName+"\"")
                    lx.eval( "item.channel renderOutput$filename \"%s\"" % arg.imgName )
            else:
                if (isEnabled):
                    if (layerName!="Alpha Output"):
                        #set disabled
                        logMessage("        disable layer")
                        lx.eval( "item.channel textureLayer$enable false" )
        if (not foundLayer):
            #if the layer is not set by name, test if it is set by type:
            logMessage("List layers by type name...")
            for L in range(0, nbOutputs):
                objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
                lx.eval( "select.item "+objID)
                isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
                layerName= lx.eval( "item.channel renderOutput$effect ?" );
                if (layerName==arg.layer):
                    logMessage("     '" +layerName+"'")
                    foundLayer=True
                    if (not isEnabled):
                        #set enabled
                        logMessage("        enable layer")
                        lx.eval( "item.channel textureLayer$enable true" )
                    if (arg.imgName!=""):
                        logMessage("        set renderOutput to \"" +arg.imgName+"\"")
                        lx.eval( "item.channel renderOutput$filename \"%s\"" % arg.imgName )
    elif ((arg.imgName.find("<output>")>=0) or (outPattern.find("<output>")>=0)):
        logMessage("List Layers...")
        nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
        foundLayer=False
        for L in range(0, nbOutputs):
            #get layer by name
            layerName= lx.eval( "query sceneservice renderOutput.name ? "+str(L) );
            logMessage("    '" +layerName+"'")
            objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
            lx.eval( "select.item "+objID)
            isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
            imgLocalName= arg.imgName
            imgLocalName= imgLocalName.replace("<output>",layerName)
            if (isEnabled):
                logMessage("        set renderOutput to \"" +imgLocalName+"\"")
                lx.eval( "item.channel renderOutput$filename \"%s\"" % imgLocalName )

    global globalArg
    globalArg=arg #copy for kso render
    

    logMessage("Scene init done, starting to render... ")
    flushLog()

    if (arg.KSOMode):
        render_KSO(arg)
    else:
        render_default(arg)


    logMessage(" ");
    logMessage("Done")
    logMessage(" ");
    logMessage(" ");
    lx.eval("app.quit")
except:
    import traceback
    msg = traceback.format_exc()
    logMessage ("Error: script crashed during render\n"+msg)
    lx.eval("app.quit")
    
lx.eval("app.quit")

