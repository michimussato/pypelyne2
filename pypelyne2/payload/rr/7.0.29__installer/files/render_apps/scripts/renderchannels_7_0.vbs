' Render script for Softimage
'  v 6.01.52
'  Copyright (c) 2009-2010 Holger Schoenberger - Binary Alchemy
'
'
' additional optional parameter:
'
' -volume  true/false                     :enable/disable volume rendering
' -displace true/false                    :enable/disable displacement
' -lambert true                           :creates a lambert material in the background partition (similar to fast Open GL renderings)
' -motionSteps value
'
'
'f




Option explicit

SUB Render_channels (scname,db,wg,pass,skip,fname,fext, frstart,frend,frstep,froffset,ftype,ftype_bit,camera,verbose,AAsmin,AAsmax,AAc,resX,resY,x1,x2,y1,y2,volume,displace,lambert,MdlLvl,SetOffMdl,pad, renderthreads, motionSteps,fnameChannelAdd)
Dim fso, f, filename, PD ,dirname, slen, spos , tempstrg,oldpad,list,OldMdlLvl,chfname,chdname,fbuffer, renderer, fileSystem, ImagesList, Image, imgFileName, fnamechar1, fnamechar2, oPass


if not (IsNull(wg) or (len(wg)=0)) then
  tempstrg=GetValue ("preferences.data_management.workgroup_appl_path")
  if (wg=tempstrg) then 
    logmessage "RR - Workgroup already " & tempstrg
  else
    logmessage "RR - Set workgroup to " & wg
    SetValue "preferences.data_management.workgroup_appl_path", wg
  end if
  end if

if not (IsNull(db) or (len(db)=0)) then
  logmessage "RR - Set project to " & db
  Application.ActiveProject = db 
  end if
logmessage "RR - Active Project: " & Application.ActiveProject2.Path

logmessage "RR - Loading scene"
OpenScene scname, False 

if not (IsNull(db) or (len(db)=0)) then
  logmessage "RR - Set project to " & db
  Application.ActiveProject = db 
  end if
logmessage "RR - Active Project: " & Application.ActiveProject2.Path


if (IsNull(pass)) or (len(pass)=0) then
  pass=GetCurrentPass()
  logmessage "RR - no pass set, using default '" & pass &"'"
  else
  pass="Passes." & pass
  SetCurrentPass pass
  end if

Set fileSystem = CreateObject( "Scripting.FileSystemObject" )
Set ImagesList=EnumElements("Sources.Image")
IF TypeName(ImagesList) <> "Nothing" THEN
    FOR EACH Image IN ImagesList
		imgFileName = GetValue ( Image & ".FileName")
		spos= InStr(1,imgFileName ,"noIcon.pic",vbTextCompare)
		IF (spos=0) THEN
			imgFileName=XSIUtils.ResolveTokenString(imgFileName,0,false)
			imgFileName= Replace(imgFileName, "/", "\")
			fnamechar1 = left(imgFileName,1)
			fnamechar2 = right(left(imgFileName,2),1)
	
			IF (fnamechar2 <> ":") AND (fnamechar2 <> "\") AND (fnamechar1 <> "\") THEN
				imgFileName= Application.ActiveProject2.Path & "\" & imgFileName
			END IF
			IF NOT fileSystem.FileExists( imgFileName ) THEN
				logmessage "Info: Image file does not exist: " & imgFileName
'''commented out:				logmessage "Error: Exit render because of missing texture file!"
'''commented out:				exit sub
			END IF
		END IF
	NEXT
END IF 


renderer=Getvalue(pass &".Renderer")
if (renderer="") then
  renderer = Getvalue("Passes.RenderOptions.Renderer")
  end if
logmessage "RR - renderer used: '" & renderer &"'"


if not (IsNull(camera) or (len(camera)=0)) then
  logmessage "RR - Set camera to " & camera
  SetValue pass & ".Camera", camera
  end if
if not (IsNull(skip) or (len(skip)=0)) then
  SetValue pass & ".FrameSkipRendered", skip
  end if
if not (IsNull(ftype) or (len(ftype)=0)) then
  SELECT CASE ftype
  CASE "map8"  SetValue pass & ".Main.Format", "map"
               SetValue pass & ".Main.BitDepth", 3
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "map16" SetValue pass & ".Main.Format", "map"
               SetValue pass & ".Main.BitDepth", 4
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "map32" SetValue pass & ".Main.Format", "map"
               SetValue pass & ".Main.BitDepth", 21
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "mapfp" SetValue pass & ".Main.Format", "map"
               SetValue pass & ".Main.BitDepth", 21
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "exr16" SetValue pass & ".Main.Format", "exr"
               SetValue pass & ".Main.BitDepth", 20
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "exr32" SetValue pass & ".Main.Format", "exr"
               SetValue pass & ".Main.BitDepth", 21
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "exrfp" SetValue pass & ".Main.Format", "exr"
               SetValue pass & ".Main.BitDepth", 21
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "sgi8"  SetValue pass & ".Main.Format", "sgi"
               SetValue pass & ".Main.BitDepth", 3
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "sgi16" SetValue pass & ".Main.Format", "sgi"
               SetValue pass & ".Main.BitDepth", 4
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "tif8"  SetValue pass & ".Main.Format", "tif"
               SetValue pass & ".Main.BitDepth", 3
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "tif16" SetValue pass & ".Main.Format", "tif"
               SetValue pass & ".Main.BitDepth", 4
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "tif32" SetValue pass & ".Main.Format", "tif"
               SetValue pass & ".Main.BitDepth", 21
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "tiffp" SetValue pass & ".Main.Format", "tif"
               SetValue pass & ".Main.BitDepth", 21
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "ct8"   SetValue pass & ".Main.Format", "ct"
               SetValue pass & ".Main.BitDepth", 3
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "ct16"  SetValue pass & ".Main.Format", "ct"
               SetValue pass & ".Main.BitDepth", 4
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "ct32"  SetValue pass & ".Main.Format", "ct"
               SetValue pass & ".Main.BitDepth", 21
               SetValue pass & ".Main.DataType", "RGBA"
  CASE "ctfp"  SetValue pass & ".Main.Format", "ct"
               SetValue pass & ".Main.BitDepth", 21
               SetValue pass & ".Main.DataType", "RGBA"
  Case Else SetValue pass & ".Main.Format", ftype
  END SELECT
  end if
if not (IsNull(ftype_bit) or (len(ftype_bit)=0)) then
  SetValue pass & ".Main.BitDepth", ftype_bit
  end if

if not (IsNull(resX) or (len(resX)=0)) then
  IF GetValue(pass & ".ImageFormatOverride") THEN
	SetValue pass & ".ImageWidth", resX
  ELSE
	SetValue "Passes.RenderOptions.ImageWidth", resX
  END IF

  end if
if not (IsNull(resY) or (len(resY)=0)) then
  IF GetValue(pass & ".ImageFormatOverride") THEN
	SetValue pass & ".ImageLockAspectRatio", false
  	SetValue pass & ".ImageHeight", resY  
  ELSE
	SetValue "Passes.RenderOptions.ImageLockAspectRatio", false
	SetValue "Passes.RenderOptions.ImageHeight", resY  
  END IF
  end if
  


if not (IsNull(pad) or (len(pad)=0)) then
  pad=int(pad)
  IF (pad<4) THEN
      SetValue "Passes.RenderOptions.FramePadding", pad
    ELSE
      SetValue "Passes.RenderOptions.FramePadding", 4
    END IF
  end if

SetValue pass & ".Main.Enabled", true

filename=fname
if not (IsNull(fname) or (len(fname)=0)) then
  fname= fname & "[Frame "
  if not (IsNull(froffset) or (len(froffset)=0) or (froffset="0")) then
	froffset=int(froffset)
	if (froffset<0) then
	    fname= fname & froffset
	else
	    fname= fname & "+" & froffset
        end if 
  end if
  fname= fname & "]"
  if not (IsNull(fext) or (len(fext)=0)) then
      fname= fname & fext
  end if
  SetValue pass & ".Main.Filename", fname
  end if
  

if not (IsNull(fnameChannelAdd) or (len(fnameChannelAdd)=0)) then
  set oPass= GetValue (pass)
  FOR EACH fbuffer IN oPass.Framebuffers
	if (NOT fbuffer.name="Main") THEN
		chfname=GetValue(fbuffer.Filename)
		chdname=""
		spos= InStr(1,chfname ,"[Frame",vbTextCompare)
		IF (spos>0) THEN
			chdname = right(chfname,len(chfname)-spos+1)
			chfname = left(chfname,spos-1)
			chdname="."+chdname
		ELSE
			spos= InStr(1,chfname ,"#",vbTextCompare)
			IF (spos>0) THEN
				chdname = right(chfname,len(chfname)-spos+1)
				chfname = left(chfname,spos-1)
				chdname="."+chdname
			END IF
		END IF
		IF ((right(chfname,1) <> ".") AND  (right(chfname,1) <> "_")) THEN
			chfname=chfname +"."
		END IF
		chfname= chfname+fnameChannelAdd+chdname
		SetValue fbuffer.Filename, chfname
	END IF
  NEXT
END IF


SELECT CASE renderer
   CASE "VRay"
       if not (IsNull(verbose) or (len(verbose)=0)) then
          SetValue pass & ".VRay_Options.sys_level", verbose
          end if

    if InStr(1,filename,"/",vbTextCompare)>0 then
        PD="/"
    else
        PD="\"
    end if          
    spos=InStrRev(filename,PD,-1, vbTextCompare)
    if (spos>0) THEN
        dirname= left(filename,spos)
        slen = len(filename)
        filename= right(filename,slen-spos)
        end if
    spos=InStrRev(filename,".",-1,vbTextCompare)
    filename= left(filename,spos)

   SetValue "VRayPassOptions.SaveIn", dirname
   SetValue "VRayPassOptions.ImgFileName", filename
   
   
   CASE "Arnold Render"

       SetValue pass & ".Arnold_Render_Options.abort_on_license_fail", True


          
        if not (IsNull(AAsmax) or (len(AAsmax)=0)) then
          SetValue pass & ".Arnold_Render_Options.AA_samples", AAsmax
          end if
          
        if not (IsNull(verbose) or (len(verbose)=0)) then
          SetValue pass & ".Arnold_Render_Options.log_level", verbose
          end if
          
        if not (IsNull(renderthreads) or (len(renderthreads)=0)) then
          SetValue pass & ".Arnold_Render_Options.autodetect_threads", False
          On Error Resume Next
          SetValue pass & ".Arnold_Render_Options.threads", renderthreads
          if (Err.Number=6) then
            SetValue "Passes.Arnold_Render_Options.threads", 16
            end if
          On Error GoTo 0
          end if
          
        if not (IsNull(displace) or (len(displace)=0)) then
          SetValue pass & ".Arnold_Render_Options.ignore_displacement", not displace
          end if          

        SetValue pass & ".Arnold_Render_Options.progressive_switch", false


   Case Else

        if not (IsNull(x1) or (len(x1)=0)) then
          SetValue pass & ".CropWindowEnabled", True
          SetValue pass & ".SelectionTracking", False
          SetValue pass & ".CropWindowOffsetY", 0
          SetValue pass & ".CropWindowHeight", 19999

          SetValue pass & ".CropWindowOffsetX", x1
          SetValue pass & ".CropWindowWidth", x2-x1+1
          if not (IsNull(y1) or (len(y1)=0)) then
            SetValue pass & ".CropWindowOffsetY", y1
            SetValue pass & ".CropWindowHeight", y2-y1+1
            end if
          end if


        if not (IsNull(volume) or (len(volume)=0)) then
          SetValue pass & ".mentalray.EnableVolumeShaders", volume
          end if
        if not (IsNull(displace) or (len(displace)=0)) then
          SetValue pass & ".mentalray.EnableDisplacementShaders", displace
          end if
        if not (IsNull(verbose) or (len(verbose)=0)) then
          SetValue pass & ".mentalray.VerbosityLevel", verbose
          end if
        if not (IsNull(AAsmin) or (len(AAsmin)=0)) then
          SetValue pass & ".mentalray.SamplesMin", AAsmin
          end if
        if not (IsNull(AAsmax) or (len(AAsmax)=0)) then
          SetValue pass & ".mentalray.SamplesMax", AAsmax
          end if
        if not (IsNull(AAc) or (len(AAc)=0)) then
          tempstrg= GetValue("Passes.mentalray.SamplesContrastAlpha")
          if InStr(1,tempstrg,",",vbTextCompare)>0 then
           AAc = Replace(AAc , ".", ",") 
           else
           AAc = Replace(AAc , ",", ".") 
           end if
          SetValue pass & ".mentalray.SamplesContrastRed", AAc
          SetValue pass & ".mentalray.SamplesContrastGreen", AAc
          SetValue pass & ".mentalray.SamplesContrastBlue", AAc
          SetValue pass & ".mentalray.SamplesContrastAlpha", AAc
          end if
        if not (IsNull(motionSteps) or (len(motionSteps)=0)) then
          SetValue pass & ".MotionStepsDeform", motionSteps
          SetValue pass & ".MotionStepsTransform", motionSteps
          end if


   END SELECT 




if not (IsNull(lambert) or (len(lambert)=0)) then
  ApplyShader "Lambert",  pass & ".Background_Objects_Partition" , "Lambert_gray" , , siLetLocalMaterialsOverlap
  end if



logmessage "RR - start rendering"

frstart=int(frstart)
frend=int(frend)
frstep=int(frstep)




if (frstart>GetValue ("PlayControl.GlobalIn")) then
SetValue "PlayControl.Current", frstart-1
else
SetValue "PlayControl.Current", frstart
end if

SceneRefresh
renderpass pass , ,  frstart,frend,frstep

logmessage "RR - Rendering done!"
END SUB


