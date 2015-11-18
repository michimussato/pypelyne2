
import nuke
import os
import sys
import platform
import random
import string

from xml.etree.ElementTree import ElementTree, Element, SubElement


#####################################################################################
# This function has to be changed if an app should show info and error dialog box   #
#####################################################################################

def writeInfo(msg):
    print(msg)

def writeError(msg):
    print(msg)


def ireplace(text, old, new ):
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old):]
        idx = index_l + len(old)
    return text



def getAllWriteNodes():
    allNo=nuke.allNodes()
    writeNo=[]
    for gz in allNo:
        if isGizmo(gz):
            with gz:
                gList = nuke.allNodes('Write') + nuke.allNodes('DeepWrite')
                for gnode in gList:
                    if (gnode['disable'].value()):
                        continue
                    pathScripted=gnode['file'].value()
                    if ((pathScripted== None) or (len(pathScripted)<3)):
                        continue                    
                    writeNo.append(gz)
                    break
    writeNo=writeNo+ nuke.allNodes('Write') + nuke.allNodes('DeepWrite')
    return writeNo

def convertWriteToLocal(writeNode, orgDir, orgDirWinDrive, locDir):
    pathScripted=writeNode['file'].value()
    if ((pathScripted== None) or (len(pathScripted)<3)):
        return
    pathResolved=nuke.filename(writeNode)
    pathResolved_new=ireplace(pathResolved, orgDir, locDir)
    pathResolved_new=ireplace(pathResolved, orgDirWinDrive, locDir)
    writeNode['file'].setValue(pathResolved_new)
    writeInfo(writeNode['name'].value()+":   "+pathScripted+" => "+pathResolved+" => "+pathResolved_new)
    writeDir=os.path.dirname(pathResolved_new)
    if not os.path.exists(writeDir):
        writeInfo("     creating directory: "+writeDir)
        os.makedirs(writeDir)


def isGizmo(node):
    gizmo = isinstance(node, nuke.Gizmo)
    return gizmo


def makeLocalRenderOut(orgFilename, locFilename, orgDir, orgDirWinDrive, locDir):
    writeInfo("")
    orgDir=orgDir.replace("\\","/")
    locDir=locDir.replace("\\","/")
    orgDirWinDrive=orgDirWinDrive.replace("\\","/")

    writeInfo("Replacing: "+orgDir+" => "+locDir)
    writeInfo("Replacing: "+orgDirWinDrive+" => "+locDir)
    writeInfo("")
    
    nuke.scriptOpen(orgFilename)    

    #replace all scripted paths in all read nodes
    #change render path to local render out
    n = getAllWriteNodes()
    for writeNode in n:
        if (writeNode['disable'].value()):
            continue
##        if isGizmo(writeNode):
##            with writeNode:
##                gList = nuke.allNodes('Write') + nuke.allNodes('DeepWrite')
##                for gnode in gList:
##                    if (gnode['disable'].value()):
##                        continue
##                    convertWriteToLocal(gnode, orgDir, orgDirWinDrive, locDir)
##        else:
        convertWriteToLocal(writeNode, orgDir, orgDirWinDrive, locDir)
        

    #replace all scripted paths in all read nodes
    n = nuke.allNodes('Read') + nuke.allNodes('DeepRead')
    for readNode in n:
        if (readNode['disable'].value()):
            continue
        pathScripted=readNode['file'].value()
        if ((pathScripted== None) or (len(pathScripted)<3)):
            continue
        pathResolved=nuke.filename(readNode)
        readNode['file'].setValue(pathResolved)
        writeInfo(readNode['name'].value()+":   "+pathScripted+" => "+pathResolved) 

      
    nuke.scriptSaveAs(locFilename,1)
    writeInfo("")
    writeInfo("Done")
    writeInfo("")
    



makeLocalRenderOut(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

