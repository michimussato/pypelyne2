// Royal Render Plugin script for Softimage XSI
// Author: Royal Render, Holger Schoenberger, Binary Alchemy
// Last change: v 6.02.31
// Copyright (c) Holger Schoenberger - Binary Alchemy
// #win:  rrInstall_Copy: ..\Plugins\
// #linux:  rrInstall_Copy: Application\Plugins\



function getRR_root( )
{
    rr_root="";
    rr_root=XSIUtils.Environment.Item("RR_ROOT");
    
    if (rr_root=="") {
        //if the environment variable is not set on this machine
        //then we use the hardcoded path (hardcoded by the plugin installer)
        if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
            rr_root="%RRLocationWin%";
        } else {
            rr_root="%RRLocationLx%";
        }
        if (rr_root.charAt(0)=="%") { //if %RRLocation% was not replaced, so clear the variable
            rr_root="";
        }
    }
    if (rr_root=="") {
        Application.LogMessage("Royal Render path not found! Please re-install the plugin or define a system environment variable RR_root.", siError);
    }
    return rr_root;
}

function XSILoadPlugin( in_reg )
{
    in_reg.Author = "Holger Schoenberger";
    in_reg.Name = "RRSubmitPlugin";
    in_reg.Email = "";
    in_reg.URL = "";
    in_reg.Major = 6;
    in_reg.Minor = 0;

    in_reg.RegisterCommand("RRSubmit","RRSubmit");
    in_reg.RegisterCommand("RRSubmitCamera","RRSubmitCamera");
    in_reg.RegisterCommand("RRSubmitLocal","RRSubmitLocal");
    in_reg.RegisterCommand("RRSubmitFx","RRSubmitFx");
    in_reg.RegisterCommand("RRViewControl","RRViewControl");
    in_reg.RegisterMenu(siMenuTbRenderRenderID,"RRSubmit_Menu",true,false);
    //RegistrationInsertionPoint - do not remove this line

//    Application.LogMessage("RR has been loaded.");
    //RRSubmit_Execute(  )    
    getRR_root();
    return true;
}

function XSIUnloadPlugin( in_reg )
{
    return true;
}

function RRSubmit_Init( in_ctxt )
{
    var oCmd;
    oCmd = in_ctxt.Source;
    oCmd.Description = "Submit scene to Royal Render";
    oCmd.ReturnValue = false;

    return true;
}


function RRSubmit_Menu_Init( in_ctxt )
{
    var oMenu;
    oMenu = in_ctxt.Source;
    oMenu.Name="Royal Render..";
    oMenu.AddCommandItem ("Submit Scene...","RRSubmit");
    oMenu.AddCommandItem ("Submit Scene - Select Camera ...","RRSubmitCamera");
    oMenu.AddCommandItem ("Submit Scene - Local Textures","RRSubmitLocal");
    oMenu.AddCommandItem ("Submit FxTree...","RRSubmitFx");
    oMenu.AddSeparatorItem();
    oMenu.AddCommandItem ("View Control...","RRViewControl");
    return true;
}

function PD( ) //return PathDelim
{
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
    return "\\";
    } else {
    return "/";
    }
}

function RRViewControl_Execute(  )
{
    if (getRR_root()=="") return false;
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
        XSIUtils.LaunchProcess(getRR_root()+"\\bin\\win\\rrControl.exe");
    } else {
        XSIUtils.LaunchProcess(getRR_root()+PD()+"lx__rrControl.sh");    
    }
       return true;
}


function RRgetSceneInfo( )
{
    var sceneInfo = new Object();
    sceneInfo.filename= Application.ActiveProject.ActiveScene.Parameters("FileName").value;
    sceneInfo.database= Application.ActiveProject2.Path;
    sceneInfo.version=  Application.Version();
    var p= sceneInfo.version.indexOf(".");
    p= sceneInfo.version.indexOf(".",p+1);
    p= sceneInfo.version.indexOf(".",p+1);
    if (p>0) {
        var buldString=sceneInfo.version;
        sceneInfo.version= sceneInfo.version.substr(0,p);
        buldString=buldString.substr(p+1,buldString.length);
        p= buldString.indexOf(".");
        if (p>0) {
            buldString= buldString.substr(0,p);
        }
        p= sceneInfo.version.indexOf(".");
        main= sceneInfo.version.substr(0,p);
        if ((main=="8") && parseInt(buldString)>=248) {
            sceneInfo.version=sceneInfo.version.replace('.0', '.1' );
        }
    }
    p= sceneInfo.version.indexOf(".");
    if ((p==1) && (sceneInfo.version.charAt(0)=='8')) {
         sceneInfo.version= "2010"+ sceneInfo.version.substr(1,sceneInfo.version.length-1);
    } else if ((p==1) && (sceneInfo.version.charAt(0)=='9')) {
    sceneInfo.version= "2011"+ sceneInfo.version.substr(1,sceneInfo.version.length-1);
    } else if ((p==2) && (sceneInfo.version.charAt(0)=='1') && (sceneInfo.version.charAt(1)=='0')) {
    sceneInfo.version= "2012"+ sceneInfo.version.substr(2,sceneInfo.version.length-2);
    } else if ((p==2) && (sceneInfo.version.charAt(0)=='1') && (sceneInfo.version.charAt(1)=='1')) {
    sceneInfo.version= "2013"+ sceneInfo.version.substr(2,sceneInfo.version.length-2);
    } else if ((p==2) && (sceneInfo.version.charAt(0)=='1') && (sceneInfo.version.charAt(1)=='2')) {
      var subversion = sceneInfo.version.substr(2,sceneInfo.version.length-2);
      sceneInfo.version= "2014"+ subversion;
      if ((subversion.charAt(1)=='1') && (subversion.charAt(3)=='9') && (subversion.charAt(4)=='9')) {
         sceneInfo.version= "2014.2";
	}
    } else if ((p==2) && (sceneInfo.version.charAt(0)=='1') && (sceneInfo.version.charAt(1)=='3')) {
    sceneInfo.version= "2015"+ sceneInfo.version.substr(2,sceneInfo.version.length-2);
    } else if ((p==2) && (sceneInfo.version.charAt(0)=='1') && (sceneInfo.version.charAt(1)=='4')) {
    sceneInfo.version= "2016"+ sceneInfo.version.substr(2,sceneInfo.version.length-2);
    } else if ((p==2) && (sceneInfo.version.charAt(0)=='1') && (sceneInfo.version.charAt(1)=='5')) {
    sceneInfo.version= "2017"+ sceneInfo.version.substr(2,sceneInfo.version.length-2);
    } else if ((p==2) && (sceneInfo.version.charAt(0)=='1') && (sceneInfo.version.charAt(1)=='6')) {
    sceneInfo.version= "2018"+ sceneInfo.version.substr(2,sceneInfo.version.length-2);
    } else if ((p==2) && (sceneInfo.version.charAt(0)=='1') && (sceneInfo.version.charAt(1)=='7')) {
    sceneInfo.version= "2019"+ sceneInfo.version.substr(2,sceneInfo.version.length-2);
    }

    var cpu = XSIUtils.Environment.Item("XSI_CPU");
    if (cpu.indexOf("64") != -1) 
        sceneInfo.appBit="64";
      else
        sceneInfo.appBit="32";


    sceneInfo.seqStart=1;  
    sceneInfo.seqEnd=100;  
    sceneInfo.seqStep=1;  
    sceneInfo.frameSet="";  

    switch (GetValue("Passes.RenderOptions.FrameRangeSource")) {
        case 2:
            sceneInfo.seqStart=Getvalue("PlayControl.In");
            sceneInfo.seqEnd=Getvalue("PlayControl.Out");
            sceneInfo.seqStep=1;
            break;
        case 1:
            sceneInfo.frameSet=Getvalue("Passes.RenderOptions.FrameSet");
            sceneInfo.seqStart=Getvalue("PlayControl.In");
            sceneInfo.seqEnd=Getvalue("PlayControl.Out");
            sceneInfo.seqStep=1;
            break;
        default:
            sceneInfo.seqStart=Getvalue("Passes.RenderOptions.FrameStart");
            sceneInfo.seqEnd=Getvalue("Passes.RenderOptions.FrameEnd");
            sceneInfo.seqStep=Getvalue("Passes.RenderOptions.FrameStep");
    }
    sceneInfo.outputDir=Getvalue("Passes.RenderOptions.OutputDir");
    sceneInfo.outputDir=XSIUtils.ResolveTokenString (sceneInfo.outputDir.replace(/\[Pass\]/gi, "<Layer>").replace(/\[Camera\]/gi, "<Camera>").replace(/\[Project Path\]/gi, "<Database>").replace(/\[Scene\]/gi, "<SceneFile>"),0,false);
    sceneInfo.outputDir = sceneInfo.outputDir.replace(/\[/gi, "<").replace(/\]/gi, ">");
    if ((sceneInfo.outputDir.charAt(sceneInfo.outputDir.length-1)!="\\") && (sceneInfo.outputDir.charAt(sceneInfo.outputDir.length-1)!="/") ) {
        sceneInfo.outputDir=sceneInfo.outputDir+PD();
    }
    sceneInfo.imageWidth=Getvalue("Passes.RenderOptions.ImageWidth");
    sceneInfo.imageHeight=Getvalue("Passes.RenderOptions.ImageHeight");
    sceneInfo.renderer=Getvalue("Passes.RenderOptions.Renderer");
    sceneInfo.framePadding=Getvalue("Passes.RenderOptions.FramePadding");
    sceneInfo.fields=((GetValue("Passes.RenderOptions.FieldEnable")) && (!GetValue("Passes.RenderOptions.FieldInterleave")));
    return sceneInfo;
}



function SplitFileName(obj)
{
    var ps=obj.imageFilename.lastIndexOf("[Frame");
    newExt="";
    if (ps>0) {
        var pe=obj.imageFilename.indexOf("]",ps); 
        if ((ps>=0) && (pe>=0)) {
            var s1=obj.imageFilename.substring(ps+6,pe);
            s1=s1.replace(/^\s*/, "").replace(/\s*$/, ""); //trim string  (remove spaces)
            newExt= obj.imageFilename.substr(pe+1);
            obj.imageFilename= obj.imageFilename.substr(0,ps);
            ps=s1.indexOf("#");
            if ((ps>=0) && (ps+1<s1.length)) {
                pe=ps+2;
                s2=s1.substr(ps+1);
                if (s2.indexOf(" ")>0) s2=s2.substr(0,s2.indexOf(" "));
                obj.framePadding=s2;
            }
            ps=s1.indexOf("+");
            if ((ps>=0) && (ps+1<s1.length)) {
                pe=ps+2;
                s2=s1.substr(ps+1);
                if (s2.indexOf(" ")>0) s2=s2.substr(0,s2.indexOf(" "));
                obj.seqFileOffset=s2;
            }
            ps=s1.indexOf("-");
            if ((ps>=0) && (ps+1<s1.length)) {
                pe=ps+2;
                s2=s1.substr(ps+1);
                if (s2.indexOf(" ")>0) s2=s2.substr(0,s2.indexOf(" "));
                obj.seqFileOffset="-"+s2;
            }
        }
    }
    
    ps=obj.imageFilename.indexOf("#");
    if (ps>0) {
        var pe=obj.imageFilename.lastIndexOf("#");
        obj.framePadding=pe-ps+1;
        newExt= obj.imageFilename.substr(pe+1);
        obj.imageFilename= obj.imageFilename.substr(0,ps);
    }

    if ((newExt!=obj.imageExtension) && (newExt!=".")) {
        ps= newExt.indexOf(obj.imageExtension);
        if (ps<=0) {
            obj.imageExtension=newExt + obj.imageExtension;
        } 
    }
    if ((obj.imageFilename.charAt(obj.imageFilename.length-1)!='.') && (obj.imageFilename.charAt(obj.imageFilename.length-1)!='_')) {
        obj.imageFilename = obj.imageFilename+ ".";
    }
}


function removeModelName(ObjName)
{
    var ps=ObjName.lastIndexOf(".");
    if (ps>0) {
    ObjName=ObjName.substring(ps+1,9999);
    }
    return ObjName;
}

function RRgetPassesInfo(sceneInfo)
{
    var passes = new Object();
    passes.p= new Array();
    passes.max=0;
    var oPasses = ActiveProject.ActiveScene.Passes;
    for (var i =0;  i < oPasses.Count; i++ ) {
        passes.max++;
        passes.p[passes.max-1]= new Object();
        passes.p[passes.max-1].name=oPasses(i).Name;
        passes.p[passes.max-1].selected=false;
        if (oPasses(i).Name==getCurrentPass().name) passes.p[passes.max-1].selected=true;
        var SelList = GetValue("SelectionList")
        for (var p =0;  p < SelList.Count; p++ ) {
            if (oPasses(i).Name==SelList(i)) passes.p[passes.max-1].selected=true;
        }        
        passes.p[passes.max-1].frameSet=""; 
        switch (Getvalue(oPasses(i).FrameRangeSource)) {
            case 3:
                passes.p[passes.max-1].seqStart=sceneInfo.seqStart
                passes.p[passes.max-1].seqEnd=sceneInfo.seqEnd;
                passes.p[passes.max-1].seqStep=sceneInfo.seqStep;
                passes.p[passes.max-1].frameSet=sceneInfo.frameSet;
                break;
            case 2:
                passes.p[passes.max-1].seqStart=Getvalue("PlayControl.In");
                passes.p[passes.max-1].seqEnd=Getvalue("PlayControl.Out");
                passes.p[passes.max-1].seqStep=1;
                break;
            case 1:
                passes.p[passes.max-1].frameSet=Getvalue(oPasses(i).FrameSet); 
                passes.p[passes.max-1].seqStart=Getvalue("PlayControl.In");
                passes.p[passes.max-1].seqEnd=Getvalue("PlayControl.Out");
                passes.p[passes.max-1].seqStep=1;
                break;
            default:
                passes.p[passes.max-1].seqStart=Getvalue(oPasses(i).FrameStart);
                passes.p[passes.max-1].seqEnd=Getvalue(oPasses(i).FrameEnd);
                passes.p[passes.max-1].seqStep=Getvalue(oPasses(i).FrameStep);
        }
        passes.p[passes.max-1].renderer= oPasses(i).Renderer;  
        if (passes.p[passes.max-1].renderer=="") passes.p[passes.max-1].renderer=sceneInfo.renderer;
        if (passes.p[passes.max-1].renderer=="Hardware Renderer")  {
            Application.LogMessage("Batch rendering with OGL Hardware renderer not supported by XSIBatch.", siWarning);
            passes.max--;
            continue;
        }
        passes.p[passes.max-1].RequiredLicenses= passes.p[passes.max-1].renderer;
        
        if (passes.p[passes.max-1].renderer=="VRay")  {
            passes.p[passes.max-1].imageFilename = Getvalue("Passes." +  oPasses(i).Name + ".VRay_Options.out_img_file_name");
            passes.p[passes.max-1].imageFilename= passes.p[passes.max-1].imageFilename.replace(/\[Channel\]/gi, "Main" ).replace(/\[Framebuffer\]/gi, "Main" );
            passes.p[passes.max-1].imageExtension=".unknown";
            switch (Getvalue("Passes." + oPasses(i).Name + ".VRay_Options.out_file_ext")) { 
                case 0:
                    passes.p[passes.max-1].imageExtension=".png";
                    break;
                case 1:
                    passes.p[passes.max-1].imageExtension=".bmp";
                    break;
                case 2:
                    passes.p[passes.max-1].imageExtension=".tga";
                    break;
                case 3:
                    passes.p[passes.max-1].imageExtension=".jpg";
                    break;
                case 4:
                    passes.p[passes.max-1].imageExtension=".exr";
                    break;
                case 5:
                    passes.p[passes.max-1].imageExtension=".exr";
                    break;
                case 6:
                    passes.p[passes.max-1].imageExtension=".hdr";
                    break;
                case 7:
                    passes.p[passes.max-1].imageExtension=".sgi";
                    break;
                case 8:
                    passes.p[passes.max-1].imageExtension=".pic";
                    break;
                case 9:
                    passes.p[passes.max-1].imageExtension=".png";
                    break;
            }
            passes.p[passes.max-1].overrideImageFormat= "";
        } else {
            var oChannels = oPasses(i).Framebuffers;
            passes.p[passes.max-1].channel= new Array();
            //passes.p[passes.max-1].channelExtension= new Array();
            passes.p[passes.max-1].channelsMax=-1;
            var bitDepth=0;
            for (var c =0;  c < oChannels.Count; c++ ) {
                if (Getvalue(oChannels(c).Enabled)) {
					chFileName=Getvalue(oChannels(c).Filename);
					chFileName=chFileName.replace(/\[Channel\]/gi, oChannels(c).Name ).replace(/\[Framebuffer\]/gi, oChannels(c).Name );
					chExt="." + Getvalue(oChannels(c).Format);
                    passes.p[passes.max-1].channelsMax++;
                    if (passes.p[passes.max-1].channelsMax==0) { //use the first channel as our main channel (as we do not know if "Main" is active)
                        passes.p[passes.max-1].imageFilename = chFileName;
                        passes.p[passes.max-1].imageExtension ="."+Getvalue(oChannels(c).Format); 
                        bitDepth=Getvalue(oChannels(c).BitDepth);
                    } else {
                        if (oChannels(c).Name=="Main") {  
						    //we want the main channel as our image directory (if existing)
                            //the first one was not main, as we get it now. So copy the other channel where is belongs
							if (chFileName!= passes.p[passes.max-1].imageFilename || chExt!=passes.p[passes.max-1].imageExtension) {
	                            passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1]= new Object();
    	                        passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1].imageFilename  =passes.p[passes.max-1].imageFilename;
        	                    passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1].imageExtension =passes.p[passes.max-1].imageExtension;
							} else {
								passes.p[passes.max-1].channelsMax--;
							}
                            
                            passes.p[passes.max-1].imageFilename = chFileName;
                            passes.p[passes.max-1].imageExtension= chExt;
                            bitDepth=Getvalue(oChannels(c).BitDepth);
                        } else {
							if (chFileName!= passes.p[passes.max-1].imageFilename  || chExt!=passes.p[passes.max-1].imageExtension ) {
	                            passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1]= new Object();
	                            passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1].imageFilename = chFileName;
	                            passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1].imageExtension= chExt;
							} else {
								passes.p[passes.max-1].channelsMax--;
							}
                            
                        }
                    }
                }
            }
            if (passes.p[passes.max-1].channelsMax<0) {
                passes.max--;
                continue;
            }
            //We override the extension at render time in case someone changes the extension in the pass settings
            //If the render extension is wrong, RRender does not find the rendered images.
            passes.p[passes.max-1].overrideImageFormat= passes.p[passes.max-1].imageExtension;
            switch (passes.p[passes.max-1].overrideImageFormat) { 
                case ".exr": switch (bitDepth) {
                             case 20: passes.p[passes.max-1].overrideImageFormat="Fexr"; break;
                             case 21: passes.p[passes.max-1].overrideImageFormat="exr"; break;
                             }
                              break;
                case ".tif": switch (bitDepth) {
                             case 3: passes.p[passes.max-1].overrideImageFormat="tif8"; break;
                             case 4: passes.p[passes.max-1].overrideImageFormat="tif16"; break;
                             case 21: passes.p[passes.max-1].overrideImageFormat="tiff"; break;
                             }
                              break;
                case ".map": switch (bitDepth) {
                             case 3: passes.p[passes.max-1].overrideImageFormat="map8"; break;
                             case 4: passes.p[passes.max-1].overrideImageFormat="map16"; break;
                             case 21: passes.p[passes.max-1].overrideImageFormat="mapf"; break;
                             }
                              break;
                case ".sgi": switch (bitDepth) {
                             case 3: passes.p[passes.max-1].overrideImageFormat="sgi8"; break;
                             case 4: passes.p[passes.max-1].overrideImageFormat="sgi16"; break;
                             }
                              break;
                case ".ct": switch (bitDepth) {
                             case 3: passes.p[passes.max-1].overrideImageFormat="ct8"; break;
                             case 4: passes.p[passes.max-1].overrideImageFormat="ct16"; break;
                             case 21: passes.p[passes.max-1].overrideImageFormat="ctf"; break;
                             }
                              break;
                case ".st": switch (bitDepth) {
                             case 3: passes.p[passes.max-1].overrideImageFormat="st8"; break;
                             case 4: passes.p[passes.max-1].overrideImageFormat="st16"; break;
                             case 21: passes.p[passes.max-1].overrideImageFormat="stf"; break;
                             }
                              break;
            }
        }
       
        passes.p[passes.max-1].framePadding=sceneInfo.framePadding;
        passes.p[passes.max-1].seqFileOffset=0;
        
        SplitFileName(passes.p[passes.max-1]);
        for (var c =0;  c < passes.p[passes.max-1].channelsMax; c++ ) {            
            SplitFileName(passes.p[passes.max-1].channel[c]);
        }
        
        passes.p[passes.max-1].imageFilename = XSIUtils.ResolveTokenString (passes.p[passes.max-1].imageFilename.replace(/\[Pass\]/gi, "<Layer>").replace(/\[Camera\]/gi, "<Camera_no.>").replace(/\[Project Path\]/gi, "<Database>").replace(/\[Scene\]/gi, "<SceneFile>"),0,false);
        passes.p[passes.max-1].imageFilename = passes.p[passes.max-1].imageFilename.replace(/\[/gi, "<").replace(/\]/gi, ">");

        for (var c =0;  c < passes.p[passes.max-1].channelsMax; c++ ) {            
            passes.p[passes.max-1].channel[c].imageFilename = XSIUtils.ResolveTokenString (passes.p[passes.max-1].channel[c].imageFilename.replace(/\[Pass\]/gi, "<Layer>").replace(/\[Camera\]/gi, "<Camera_no.>").replace(/\[Project Path\]/gi, "<Database>").replace(/\[Scene\]/gi, "<SceneFile>"),0,false);
            passes.p[passes.max-1].channel[c].imageFilename = passes.p[passes.max-1].channel[c].imageFilename.replace(/\[/gi, "<").replace(/\]/gi, ">");
        }

        if ( (passes.p[passes.max-1].imageFilename.charAt(0)!=PD()) && (passes.p[passes.max-1].imageFilename.charAt(1)!=":")) {
            if (passes.p[passes.max-1].renderer=="VRay") {
              passes.p[passes.max-1].imageFilename= Getvalue("Passes." +  oPasses(i).Name + ".VRay_Options.out_save_in") + PD() + passes.p[passes.max-1].imageFilename;
              passes.p[passes.max-1].imageFilename = XSIUtils.ResolveTokenString (passes.p[passes.max-1].imageFilename.replace(/\[Pass\]/gi, "<Layer>").replace(/\[Camera\]/gi, "<Camera>").replace(/\[Project Path\]/gi, "<Database>").replace(/\[Scene\]/gi, "<SceneFile>"),0,false);
              passes.p[passes.max-1].imageFilename = passes.p[passes.max-1].imageFilename.replace(/\[/gi, "<").replace(/\]/gi, ">");
            } else 
              passes.p[passes.max-1].imageFilename= sceneInfo.outputDir+passes.p[passes.max-1].imageFilename;
        }
        for (var c =0;  c < passes.p[passes.max-1].channelsMax; c++ ) {            
            if ((passes.p[passes.max-1].channel[c].imageFilename.charAt(0)!=PD()) && (passes.p[passes.max-1].channel[c].imageFilename.charAt(1)!=":")) {
                passes.p[passes.max-1].channel[c].imageFilename= sceneInfo.outputDir+passes.p[passes.max-1].channel[c].imageFilename;
            }
        }

        
        if (Getvalue(oPasses(i).FieldOverride)) {
            passes.p[passes.max-1].fields=((GetValue(oPasses(i).FieldEnable)) && (!GetValue(oPasses(i).FieldInterleave)));
        } else {
            passes.p[passes.max-1].fields=sceneInfo.fields;
        }
        
        if (Getvalue(oPasses(i).ImageFormatOverride)) {
            passes.p[passes.max-1].imageWidth= Getvalue(oPasses(i).ImageWidth);
            passes.p[passes.max-1].imageHeight= Getvalue(oPasses(i).ImageHeight);
        } else {
            passes.p[passes.max-1].imageWidth=sceneInfo.imageWidth;
            passes.p[passes.max-1].imageHeight=sceneInfo.imageHeight;
        }
        
        passes.p[passes.max-1].camera="";  
        //We do not want to override the camera at render time
        //if it is not used in the render name
        if (passes.p[passes.max-1].imageFilename.indexOf("<Camera")>=0) {
            camName= Getvalue(oPasses(i).Camera);
            var oCam = Dictionary.GetObject( camName );
            if (Application.ClassName(oCam)=="Group") {
                rtn = oCam.Members;
                if (rtn.Count>0) {
                    camName=rtn(rtn.Count-1).Name;
                }
                for (var c =0;  c<rtn.Count-1; c++ ) {
                    passes.p[passes.max-1].channelsMax++;
                    passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1]= new Object();
                    passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1].imageFilename  =passes.p[passes.max-1].imageFilename;
                    passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1].imageExtension =passes.p[passes.max-1].imageExtension;
                    passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1].imageFilename=passes.p[passes.max-1].channel[passes.p[passes.max-1].channelsMax-1].imageFilename.replace(/<Camera_no.>/gi, removeModelName(rtn(c).Name));
                }
                
            }        
            passes.p[passes.max-1].camera=camName+" MultiCam";  
        }
//      if (passes.p[passes.max-1].renderer=="Arnold Render") {
//          if (UseArnold41()) {
//              passes.p[passes.max-1].renderer=="Arnold Render 41"
//          }
//      }  
    }
    return passes;
}


function getTempFileName()
{
    var fileName;
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
        fileName=XSIUtils.Environment.Item("TEMP");
    } else {
        fileName="/tmp";
    }
    fileName+= PD()+ "rrSubmitXSI_"+Math.round(Math.random()*10000)+".xml";
    return  fileName;
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
    return str.replace(/\&/gi, "&amp;").replace(/\</gi, "&lt;").replace(/\>/gi, "&gt;").replace(/\'/gi, "&apos;").replace(/\\"/gi, "&quot;").replace(String.fromCharCode(228), "&#228;").replace(String.fromCharCode(246), "&#246;").replace(String.fromCharCode(252), "&#252;").replace(String.fromCharCode(223), "&#223;");
}

function writeNode(fil,name,value)
{
    fil.WriteLine("\t<"+AddSpacesEnd(name+">",25) + ReplaceIllegal(AddSpacesEnd(value,20)) + "   </"+name+">");
}


function exportPassToXML(nr,passes,sceneInfo,fil,CameraName,LocalTextureFile)
{

    fil.WriteLine("<Job>");
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
    writeNode(fil,"SceneOS", "win");
    } else {
    writeNode(fil,"SceneOS", "lx");
    }

    writeNode(fil,"Software", "Softimage");
    writeNode(fil,"Version", sceneInfo.version);
    writeNode(fil,"SendAppBit", sceneInfo.appBit);
    writeNode(fil,"Renderer", passes.p[nr].renderer);
    writeNode(fil,"RequiredLicenses", passes.p[nr].RequiredLicenses);
    writeNode(fil,"SceneName", sceneInfo.filename);
    writeNode(fil,"SceneDatabaseDir", sceneInfo.database);
    writeNode(fil,"Layer", passes.p[nr].name);
    writeNode(fil,"Camera",CameraName);
    writeNode(fil,"IsActive",passes.p[nr].selected);
    writeNode(fil,"SeqStart",passes.p[nr].seqStart);
    writeNode(fil,"SeqEnd",passes.p[nr].seqEnd);
    writeNode(fil,"SeqStep",passes.p[nr].seqStep);
    writeNode(fil,"SeqFileOffset",passes.p[nr].seqFileOffset);
    writeNode(fil,"SeqFrameSet",passes.p[nr].frameSet);
    writeNode(fil,"ImageWidth",passes.p[nr].imageWidth);
    writeNode(fil,"ImageHeight",passes.p[nr].imageHeight);
    writeNode(fil,"ImageFilename",passes.p[nr].imageFilename);
    writeNode(fil,"ImageFramePadding",passes.p[nr].framePadding);    
    if ((passes.p[nr].imageFilename.charAt(passes.p[nr].imageFilename.length-1)=='_')) {
        writeNode(fil,"ImagePreNumberLetter","_");    
    } else writeNode(fil,"ImagePreNumberLetter",".");    

    writeNode(fil,"OverrideImageFormat",passes.p[nr].overrideImageFormat);
    if (passes.p[nr].fields) {
        writeNode(fil,"ImageExtension",".2"+passes.p[nr].imageExtension);
    } else {
        writeNode(fil,"ImageExtension",passes.p[nr].imageExtension);
    }
    for (var c =0;  c < passes.p[nr].channelsMax; c++ ) {
        writeNode(fil,"ChannelFilename",passes.p[nr].channel[c].imageFilename);
        writeNode(fil,"ChannelExtension",passes.p[nr].channel[c].imageExtension);
    }
    writeNode(fil,"LocalTexturesFile",LocalTextureFile);    
    fil.WriteLine("</Job>");
}




function RRSubmit_Execute(  )
{
    Application.LogMessage("rrSubmit v 6.02.31.");
    if (getRR_root()=="") return false;
    
    var sceneInfo = RRgetSceneInfo();
    var p= sceneInfo.filename.indexOf("Untitled.scn");
    if (p>0) {
        Application.LogMessage("Scene was never saved", siError);
        return false;
    }

    var passes = RRgetPassesInfo(sceneInfo);
    
    var fso = new ActiveXObject("Scripting.FileSystemObject");
    var XMLFileName=getTempFileName();
    var fil = fso.CreateTextFile(XMLFileName, true);
    fil.WriteLine("<rrJob_submitFile syntax_version=\"6.0\">");
    fil.WriteLine("<DeleteXML>1</DeleteXML>");
    for (var p =0;  p < passes.max; p++ ) {
        exportPassToXML(p,passes,sceneInfo,fil,passes.p[p].camera,"");
    }
    fil.WriteLine("</rrJob_submitFile>");
    fil.Close();
   
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
        XSIUtils.LaunchProcess("\""+getRR_root()+"\\bin\\win\\rrSubmitter.exe\" \""+XMLFileName+"\"",false,getRR_root())
    } else {
        XSIUtils.LaunchProcess("\""+getRR_root()+"/lx__rrSubmitter.sh\" \""+XMLFileName+"\"",false,getRR_root())
    }

   
    return true;
}


function RRSubmitLocal_Execute(  )
{
    Application.LogMessage("rrSubmit v 6.02.31.");
    if (getRR_root()=="") return false;
    
    var sceneInfo = RRgetSceneInfo();
    var p= sceneInfo.filename.indexOf("Untitled.scn");
    if (p>0) {
        Application.LogMessage("Scene was never saved", siError);
        return false;
    }

    var passes = RRgetPassesInfo(sceneInfo);
    var fso = new ActiveXObject("Scripting.FileSystemObject");

    var LocalTexfilename= Application.ActiveProject.ActiveScene.Parameters("FileName").value;
    if (LocalTexfilename.indexOf(".scn")>=0)
        LocalTexfilename=LocalTexfilename.replace(/.scn/gi, ".localtex");
        else LocalTexfilename= LocalTexfilename+".localtex";

    var filL = fso.CreateTextFile(LocalTexfilename, true);
    filL.WriteLine("<RR_LocalTextures syntax_version=\"6.0\">");
    writeNode(filL,"DatabaseDir", sceneInfo.database);
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
    writeNode(filL,"SceneOS", "win");
    } else {
    writeNode(filL,"SceneOS", "lx");
    }
    writeNode(filL,"Software", "Softimage");
    var oExt = ActiveProject.ActiveScene.ExternalFiles;
    for (var i =0;  i < oExt.Count; i++ ) {
        if ((oExt(i).FileType=="Pictures" || oExt(i).FileType=="Models") &&  (oExt(i).Path.indexOf("noIcon.pic")<0) )  {
            filL.WriteLine("<File>");
            writeNode(filL,"Original", oExt(i).Path);
            filL.WriteLine("</File>");
        }
    }
    filL.WriteLine("</RR_LocalTextures>");
    filL.Close();

    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
        XSIUtils.LaunchProcess("\""+getRR_root()+"\\bin\\win\\rrSubmitterconsole.exe\" \""+LocalTexfilename+"\"",false,getRR_root())
    } else {
        XSIUtils.LaunchProcess("\""+getRR_root()+"/lx__rrSubmitter.sh\" \""+LocalTexfilename+"\"",false,getRR_root())
    }


    var XMLFileName=getTempFileName();
    var fil = fso.CreateTextFile(XMLFileName, true);
    fil.WriteLine("<rrJob_submitFile syntax_version=\"6.0\">");
    fil.WriteLine("<DeleteXML>1</DeleteXML>");
    for (var p =0;  p < passes.max; p++ ) {
        exportPassToXML(p,passes,sceneInfo,fil,passes.p[p].camera,LocalTexfilename);
    }
    fil.WriteLine("</rrJob_submitFile>");
    fil.Close();
   
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
        XSIUtils.LaunchProcess("\""+getRR_root()+"\\bin\\win\\rrSubmitter.exe\" \""+XMLFileName+"\"",false,getRR_root())
    } else {
        XSIUtils.LaunchProcess("\""+getRR_root()+"/lx__rrSubmitter.sh\" \""+XMLFileName+"\"",false,getRR_root())
    }

   
    return true;
}



function RRSubmitCamera_Execute(  )
{
    Application.LogMessage("rrSubmit v 6.02.31.");
    if (getRR_root()=="") return false;
    
    var sceneInfo = RRgetSceneInfo();
    var p= sceneInfo.filename.indexOf("Untitled.scn");
    if (p>0) {
        Application.LogMessage("Scene was never saved", siError);
        return false;
    }

    var passes = RRgetPassesInfo(sceneInfo);
    var camera_list = Application.ActiveProject.ActiveScene.Root.FindChildren( '',siCameraPrimType  );
    var fso = new ActiveXObject("Scripting.FileSystemObject");
    var XMLFileName=getTempFileName();
    var fil = fso.CreateTextFile(XMLFileName, true);
    fil.WriteLine("<rrJob_submitFile syntax_version=\"6.0\">");
    fil.WriteLine("<DeleteXML>1</DeleteXML>");
    for(var c=0; c<camera_list.count; c++)
    {
        for (var p =0;  p < passes.max; p++ ) {
            exportPassToXML(p,passes,sceneInfo,fil,camera_list(c),"");
        }
    }    
    fil.WriteLine("</rrJob_submitFile>");
    fil.Close();
   
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
        XSIUtils.LaunchProcess("\""+getRR_root()+"\\bin\\win\\rrSubmitter.exe\" \""+XMLFileName+"\"",false,getRR_root())
    } else {
        XSIUtils.LaunchProcess("\""+getRR_root()+"/lx__rrSubmitter.sh\" \""+XMLFileName+"\"",false,getRR_root())
    }

   
    return true;
}




function RRgetFxInfo(sceneInfo)
{
    var passes = new Object();
    passes.p= new Array();
    passes.max=0;
    
    XSIFXTrees = FindObjects('','{9ACB71FF-0E3E-41cc-BB6B-D050B9DACD41}');
    for(var i=0;i<XSIFXTrees.count;i++)
    {
        var treeOut = XSIFXTrees(i);
        passes.max++;
        passes.p[passes.max-1]= new Object();
        passes.p[passes.max-1].name= treeOut;
        passes.p[passes.max-1].frameSet="";  
        passes.p[passes.max-1].RequiredLicenses="";  
        passes.p[passes.max-1].selected=false;
        passes.p[passes.max-1].seqStart= GetValue(treeOut.StartFrame);
        passes.p[passes.max-1].seqEnd= GetValue(treeOut.EndFrame);
        passes.p[passes.max-1].seqStep= GetValue(treeOut.Step);
        passes.p[passes.max-1].renderer= "FxTree";  
        passes.p[passes.max-1].overrideImageFormat= "";
        passes.p[passes.max-1].framePadding=sceneInfo.framePadding;
        passes.p[passes.max-1].seqFileOffset=0;
        passes.p[passes.max-1].imageFilename= GetValue(treeOut.FileName);
        passes.p[passes.max-1].imageExtension ="."+GetValue(treeOut.ImageParser);
        ps= passes.p[passes.max-1].imageFilename.indexOf(passes.p[passes.max-1].imageExtension);
        if (ps>0) {
            passes.p[passes.max-1].imageFilename= passes.p[passes.max-1].imageFilename.substr(0,ps);
        }
        if ( (passes.p[passes.max-1].imageFilename.charAt(0)!=PD()) && (passes.p[passes.max-1].imageFilename.charAt(1)!=":")) {
            passes.p[passes.max-1].imageFilename= "<Database>" + passes.p[passes.max-1].imageFilename;
        }
        passes.p[passes.max-1].imageFilename = XSIUtils.ResolveTokenString (passes.p[passes.max-1].imageFilename.replace(/\[Pass\]/gi, "<Layer>").replace(/\[Project Path\]/gi, "<Database>").replace(/\[Scene\]/gi, "<SceneFile>"),0,false);
        passes.p[passes.max-1].imageFilename = passes.p[passes.max-1].imageFilename.replace(/\[/gi, "<").replace(/\]/gi, ">");

        passes.p[passes.max-1].fields= false;
        passes.p[passes.max-1].imageWidth= 100;
        passes.p[passes.max-1].imageHeight= 100;

        passes.p[passes.max-1].camera="";  
    }    
    return passes;
}


function RRSubmitFx_Execute(  )
{
    Application.LogMessage("rrSubmit v 6.02.31.");
    if (getRR_root()=="") return false;
    
    var sceneInfo = RRgetSceneInfo();
    var p= sceneInfo.filename.indexOf("Untitled.scn");
    if (p>0) {
        Application.LogMessage("Scene was never saved", siError);
        return false;
    }

    var passes = RRgetFxInfo(sceneInfo);
    

    var fso = new ActiveXObject("Scripting.FileSystemObject");
    var XMLFileName=getTempFileName();
    var fil = fso.CreateTextFile(XMLFileName, true);
    fil.WriteLine("<rrJob_submitFile syntax_version=\"6.0\">");
    fil.WriteLine("<DeleteXML>1</DeleteXML>");
    for (var p =0;  p < passes.max; p++ ) {
        exportPassToXML(p,passes,sceneInfo,fil,"","");
    }
    fil.WriteLine("</rrJob_submitFile>");
    fil.Close();
    

   
    if ((Application.Platform == "Win32" ) || (Application.Platform == "Win64" )) { 
        XSIUtils.LaunchProcess("\""+getRR_root()+"\\bin\\win\\rrSubmitter.exe\" \""+XMLFileName+"\"",false,getRR_root())
    } else {
        XSIUtils.LaunchProcess("\""+getRR_root()+"/lx__rrSubmitter.sh\" \""+XMLFileName+"\"",false,getRR_root())
    }
    
    return true;
}
