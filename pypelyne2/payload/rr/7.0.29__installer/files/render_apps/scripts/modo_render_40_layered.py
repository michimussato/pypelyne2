#python
# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Render script for Modo
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Version v 6.01.40
# Copyright (c) 2009-2011 Holger Schoenberger - Binary Alchemy
# 
######################################################################

import lx
import os
import sys
import random


lx.eval("log.toConsole true")
if (not len(lx.args())>=3):
    print (" RR - ")
    print (" RR - ")
    print (" RR - Usage: \@modo_render_40.py first last step" )
    print (" RR - Frame arguments required" )
    print (" RR - ")
    print (" RR - ")
    lx.eval("app.quit")
    sys.exit(0)

sceneName = lx.eval('query sceneservice scene.file ? current')
if ((sceneName==None) or (len(sceneName)==0)):
    print ("   ")
    print (" RR - ERROR: Unable to load scene file.")
    print (" RR - The reason could be a missing external file like a texture, reference model" )
    print (" RR - Hint: If you use paths relative to the scene, disable 'local scene copy' at the rrSubmitter"  )
    print ("   ");
    lx.eval("app.quit")
    sys.exit(0)

try:
    print (" RR - set sequence to "+str(lx.args()[0]) +"-"+str(lx.args()[1]) + "," +str(lx.args()[2])  )
    lx.eval( "select.itemType polyRenders" )
    lx.eval( "item.channel first "+str(lx.args()[0]) )
    lx.eval( "item.channel last "+str(lx.args()[1]) )
    lx.eval( "item.channel step " +str(lx.args()[2]))

    imgNameAdd=""
    layer=""
    imgName=""
    regX1=-1
    regX2=-1
    regY1=-1
    regY2=-1
    
    for a in range(0,  len(lx.args())):
        if ((lx.args()[a].lower()=="-layer") and (a+1<len(lx.args()))):
            layer=lx.args()[a+1]
        if ((lx.args()[a].lower()=="-imgname") and (a+1<len(lx.args()))):
            imgName=lx.args()[a+1]
        if ((lx.args()[a].lower()=="-imgnameadd") and (a+1<len(lx.args()))):
            imgNameAdd=lx.args()[a+1]
        if ((lx.args()[a].lower()=="-region") and (a+4<len(lx.args()))):
            regX1=lx.args()[a+1]
            regX2=lx.args()[a+2]
            regY1=lx.args()[a+3]
            regY2=lx.args()[a+4]

    print (" RR - Layer: '" +layer+"'")
    print (" RR - ImgName: '" +imgName+"'")
    print (" RR - ImgNameAdd: '" +imgNameAdd+"'")
    print (" RR - Region: " +str(regX1)+" "+str(regX2)+" "+str(regY1)+" "+str(regY2)+" ")
    if (regX1!= -1):
        lx.eval( "item.channel polyRender$region true" )
        lx.eval( "item.channel polyRender$regX0 %s" % regX1 )
        lx.eval( "item.channel polyRender$regX1 %s" % regX2 )
        lx.eval( "item.channel polyRender$regY0 %s" % regY1 )
        lx.eval( "item.channel polyRender$regY1 %s" % regY2 )    

    print (" RR - List Layers...")

    nbOutputs=lx.eval( "query sceneservice renderOutput.N ?")
    for L in range(0, nbOutputs):
        layerName= lx.eval( "query sceneservice renderOutput.name ? "+str(L) );
        print (" RR - List Layers: '" +layerName+"'")
        objID= lx.eval( "query sceneservice renderOutput.id ? "+str(L))
        lx.eval( "select.item "+objID)
        isEnabled= lx.eval( "item.channel textureLayer$enable ?" );
        if (layer!=""):
            if (layerName==layer):
                if (not isEnabled):
                    #set enabled
                    print (" RR -              enable layer")
                    lx.eval( "item.channel textureLayer$enable true" )
            else:
                if (isEnabled):
                    #set disabled
                    print (" RR -              disable layer")
                    lx.eval( "item.channel textureLayer$enable false" )
                continue
        if (imgName!=""):
            print (" RR - set renderOutput to '" +imgName+"'")
            lx.eval( "item.channel renderOutput$filename \"%s\"" % imgName )
        elif (imgNameAdd!=""):
            ImageFilename= lx.eval( "item.channel renderOutput$filename ? " );
            if ((ImageFilename==None) or (len(ImageFilename)==0)):
                continue
            ImageFilename=ImageFilename+imgNameAdd
            print (" RR - adding renderOutput '%s'" % ImageFilename)
            lx.eval( "item.channel renderOutput$filename \"%s\"" % ImageFilename )

    print (" RR - Starting Render...")

    lx.eval( "render.animation {*} openexrlayers " );

    print (" RR - ")
    print (" RR - Finished")
    print (" RR - ")
    lx.eval("app.quit")
except:
    print (" RR - Error: script crashed")
lx.eval("app.quit")
