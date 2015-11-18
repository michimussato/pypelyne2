// Royal Render Plugin script for After Effects
// Author:  Royal Render, Holger Schoenberger, Binary Alchemy
// Last change: v 7.0.24
// Copyright (c) Holger Schoenberger - Binary Alchemy
// rrInstall_Copy:   Scripts\
// rrInstall_Delete: Scripts\rrSubmit_Afx_7.0+.jsx
// rrInstall_Delete: Scripts\rrSubmit_Afx_11.0+.jsx
// rrInstall_Delete: Scripts\rrSubmit_Afx_2014.0+.jsx



function getRR_root( )
{
    rr_root="";
    var isWindows = (system.osName=="") || (system.osName.search(/Microsoft.+/)!=-1);
    if (isWindows) {   
        rr_root = $.getenv("RR_ROOT")  
    }
    
    if (rr_root=="") {
        //if the environment variable is not set on this machine
        //then we use the hardcoded path (hardcoded by the plugin installer)
        if (isWindows) { 
            rr_root="%RRLocationWin%";
        } else {
            rr_root="%RRLocationMac%";
        }    
        if (rr_root.charAt(0)=="%") { //if %RRLocation% was not replaced, clear the variable
            rr_root="";
        }
    }
    if (rr_root=="") {
        alert("Royal Render path not found! Please re-install the plugin or define a system environment variable RR_root.");
    }
    return rr_root;
}

function PD( ) //return PathDelim
{
    var isWindows = (system.osName=="") || (system.osName.search(/Microsoft.+/)!=-1);
    if (isWindows) {  
        return "\\";
    } else {
        return "/";
    }
}


function getTempFileName()
{
    var fileName;
    var isWindows = (system.osName=="") || (system.osName.search(/Microsoft.+/)!=-1);
    if (isWindows) {         
    fileName = $.getenv("TEMP")  
    } else {
        fileName="/tmp";
    }
    fileName+= PD()+ "rrSubmitAFX_"+Math.round(Math.random()*10000)+".xml";
    return  fileName;
}





function RRgetPassesInfo(sceneInfo)
{
    var passes = new Object();
    passes.p= new Array();
    passes.max=0;
    passes.max++;
    passes.p[0]= new Object();
    passes.p[0].name='** All **';
    passes.p[0].selected=false;

    
    for( p = 1; p <= app.project.renderQueue.numItems; p++ )   {
        if( app.project.renderQueue.item(p).status != RQItemStatus.QUEUED )  continue;
        foundComp=false;
        for( i = 0; i < passes.max; i++ )   {
            if (app.project.renderQueue.item( p).comp.name==passes.p[i].name )    foundComp=true;
            }
        if (foundComp) continue;
            
        passes.max++;
        passes.p[passes.max-1]= new Object();
        passes.p[passes.max-1].name=app.project.renderQueue.item( p).comp.name;
        passes.p[passes.max-1].selected=true;
        var frameDuration = app.project.renderQueue.item( p ).comp.frameDuration;
        passes.p[passes.max-1].seqStart = app.project.displayStartFrame+ Math.round( app.project.renderQueue.item( p).comp.displayStartTime / frameDuration ) +Math.round( app.project.renderQueue.item(p ).timeSpanStart / frameDuration );
        passes.p[passes.max-1].seqEnd = passes.p[passes.max-1].seqStart + Math.round( app.project.renderQueue.item( p).timeSpanDuration / frameDuration ) - 1;
        passes.p[passes.max-1].seqStep=1;
        passes.p[passes.max-1].seqFileOffset=0;
        passes.p[passes.max-1].imageFilename=app.project.renderQueue.item( p ).outputModule( 1 ).file.fsName;
    }

    if  (passes.max==1)  {
        passes.max=0;
    } else {
        passes.p[0].seqStart=passes.p[1].seqStart;
        passes.p[0].seqEnd=passes.p[1].seqEnd;
        passes.p[0].seqStep=passes.p[1].seqStep;
        passes.p[0].seqFileOffset= 0;
        passes.p[0].imageFilename=passes.p[1].imageFilename;
        }
        
    return passes;
}


function AddSpacesEnd(str,len) //for better human readability of the xml file
{
    str=str+" "; //converts value into string
    while (str.length < len) {
        str+=" ";
    }
    return str;
}

function ReplaceIllegal(str) 
{
    return str.replace(/\&/gi, "&amp;").replace(/\</gi, "&lt;").replace(/\>/gi, "&gt;").replace(/\'/gi, "&apos;").replace(/\\"/gi, "&quot;").replace(/\ä/gi, "&#228;").replace(/\ö/gi, "&#246;").replace(/\ü/gi, "&#252;").replace(/\ß/gi, "&#223;");
}

function writeNode(fil,name,value)
{
    fil.writeln("    <"+AddSpacesEnd(name+">",25) + ReplaceIllegal(AddSpacesEnd(value,20)) + "   </"+name+">");
}


function exportPassToXML(nr,passes,sceneInfo,fil,CameraName)
{

    fil.writeln("<Job>");
    
    var isWindows = (system.osName=="") || (system.osName.search(/Microsoft.+/)!=-1);
    if (isWindows) {     
        writeNode(fil,"SceneOS", "win");
    } else {
        writeNode(fil,"SceneOS", "mac");
    }
    writeNode(fil,"Software", "AFX");
    writeNode(fil,"Version", sceneInfo.version);
    writeNode(fil,"SceneName", sceneInfo.filename);
    writeNode(fil,"Layer", passes.p[nr].name);
    writeNode(fil,"IsActive",passes.p[nr].selected);
    writeNode(fil,"SeqStart",passes.p[nr].seqStart);
    writeNode(fil,"SeqEnd",passes.p[nr].seqEnd);
    writeNode(fil,"SeqStep",passes.p[nr].seqStep);
    writeNode(fil,"SeqFileOffset",passes.p[nr].seqFileOffset);
    writeNode(fil,"ImageFilename",passes.p[nr].imageFilename);
    fil.writeln("</Job>");
}


function RRgetSceneInfo( )
{
    var sceneInfo = new Object();
    
    sceneInfo.filename= app.project.file.fsName;
    sceneInfo.version=  app.version;
    sceneInfo.version=sceneInfo.version.substring( 0, sceneInfo.version.indexOf( 'x' ))
    
    return sceneInfo;
}







function RRSubmit_Execute( options )
{
    if (getRR_root()=="") return false;

    if (!app.project) {
        alert( "No project opened!" );
        return false;
        }
    if( ! app.project.file ) {
        alert( "Project never saved!" );
        return false;
        }
    app.project.save( app.project.file );
        
    var sceneInfo = RRgetSceneInfo();

    var passes = RRgetPassesInfo(sceneInfo);

    if (passes.max==0) {
        alert( "No active item in your render queue!" );
        return false;
        }
    

    var XMLFileName=getTempFileName();
    var fil = new File(XMLFileName);
    fil.open( "w" );
    fil.writeln("<rrJob_submitFile syntax_version=\"6.0\">");
    fil.writeln("<DeleteXML>1</DeleteXML>");
    fil.writeln("<SubmitterParameter> " + options  +" </SubmitterParameter>");
    for (var p =0;  p < passes.max; p++ ) {
        exportPassToXML(p,passes,sceneInfo,fil,passes.p[p].camera);
    }
    fil.writeln("</rrJob_submitFile>");
    fil.close();
   
    var isWindows = (system.osName=="") || (system.osName.search(/Microsoft.+/)!=-1);
    if (isWindows) {     
        system.callSystem("\""+getRR_root()+PD()+"win__rrSubmitter.bat\" \""+XMLFileName+"\"");
    } else {
        system.callSystem("\""+getRR_root()+PD()+"bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter\" \""+XMLFileName+"\"");
    }
    return true;
}


{
    RRSubmit_Execute("");
}
