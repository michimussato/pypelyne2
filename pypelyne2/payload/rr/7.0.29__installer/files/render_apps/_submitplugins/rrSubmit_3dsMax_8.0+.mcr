	-- Royal Render Plugin script for Max 
	-- Author:  Royal Render, Holger Schoenberger, Binary Alchemy
	-- Last change: v 6.02.31
	-- Copyright (c) Holger Schoenberger - Binary Alchemy
	-- rrInstall_Copy: \ui\macroscripts\


			
macroScript rrSubmit
category:"RoyalRender"
buttontext:"Submit scene"
tooltip:"Submit scene to Server"
--fn rrSubmit =
(
	struct rrSceneInfo
		(
			MaxVersion,
			SceneFile,
			projectpath,
			Renderer,
			RequiredLicenses,
			imageWidth,
			imageHeight,
			HiddenCommand,
			seqFileOffset,
			seqStart,
			seqEnd,
			seqStep,
			seqFrameset,
			imageFileName,
			imageExt,
			channelFileNames,
                        channelExt,
			Cameras,
			Layer,
			cmdOptions
		)
		
	global rrSI= rrSceneInfo()
	

	fn splitFileName &file &ext = 
		(
		for c = file.count to 1 by -1 do 
			if (file[c]==".") then (
				ext= substring file c (file.count - c+1)
				file= substring file 1 (c-1)
				return OK
			)
		)
	

	fn getRRPath =
		(
		cmdLine= "cmd.exe /c echo %RR_ROOT% > " + sysInfo.tempdir + "env.txt"
		DOSCommand cmdLine
		in_text = openfile (sysInfo.tempdir + "env.txt")
		if (not eof in_text) do
			(
			str = readLine in_text
			)
		close in_text
		deleteFile (sysInfo.tempdir + "env.txt")
		str = trimRight str
		if ((str.count>0) and (str[1]=="%")) then str = ""
		if (str.count==0) then str = "%RRLocationWin%"
		if ((str.count>0) and (str[1]=="%")) then str = ""
		str 
		)
		
	fn getTempFileName=
		(
		rnd= random 1 10000
		rnd= rnd as string
		str=sysInfo.tempdir + "rrSubmitMAX_" + rnd + ".xml"  
		str 
		)
		
	fn getSceneInfo=
		(
		rrSI.projectpath = pathConfig.getCurrentProjectFolder()
		rrSI.SceneFile = maxFilePath + maxFileName 	
		ver= maxVersion()
		ver= ver[1]
		rrSI.HiddenCommand = (ver>=10000)
		ver2 = ver - (( ver / 1000)*1000)
		ver = ver/1000
		if (ver>10) do ver=ver-12+2010
		rrSI.MaxVersion= ver as string + "." + ver2 as string

		rrSI.Layer = #()
		maxLayer= sceneStateMgr.getCount()
		for l = 1 to maxLayer do (
			append rrSI.Layer (sceneStateMgr.GetSceneState(l))
		)		
		
		camobjs = cameras as array
		rrSI.Cameras =#()
		for c in 1 to camobjs.count do 	(
			if ((classof camobjs[c] == TargetCamera) or  (classof camobjs[c] == FreeCamera)  or  (classof camobjs[c] == VRayPhysicalCamera) or  (classof camobjs[c] == VRayDomeCamera)) then
				append rrSI.Cameras camobjs[c].name
		)
		rrSI.Renderer= classof renderers.production as string
		posi = findString rrSI.Renderer "V_Ray"
		if (posi != undefined) do rrSI.Renderer= "VRay"
		posi = findString rrSI.Renderer "Brazil"
		if (posi != undefined) do rrSI.Renderer= "Brazil"
		rrSI.RequiredLicenses = rrSI.Renderer

		rrSI.seqFrameset=""

		if (rendTimeType==1) then (
			rrSI.seqStart=animationRange.start.frame  as integer
			rrSI.seqEnd=animationRange.start.frame  as integer
		) else if (rendTimeType==2) then (
			rrSI.seqStart=animationRange.start.frame as integer
			rrSI.seqEnd=animationRange.end.frame  as integer
		) else if (rendTimeType==3) then (
			rrSI.seqStart=rendStart.frame  as integer
			rrSI.seqEnd=rendEnd.frame  as integer
		) else (
			rrSI.seqFrameset= rendPickupFrames
			rrSI.seqStart=animationRange.start.frame
			rrSI.seqEnd=animationRange.end.frame
		)
		 
		
		rrSI.seqStep=rendNThFrame
		rrSI.seqFileOffset=rendFileNumberBase
		
		rrSI.imageWidth=renderWidth
		rrSI.imageHeight=renderHeight
		rrSI.imageFileName= rendOutputFilename
		rrSI.imageExt= ""
		if (rrSI.Renderer== "VRay") then (
			if (renderers.production.adv_irradmap_mode==6) then (
				rrSI.imageFileName=renderers.production.adv_irradmap_autoSaveFileName
			)
		)
		splitFileName &rrSI.imageFileName &rrSI.imageExt
		rrSI.channelFileNames = #()
		rrSI.channelExt = #()
		theManager = maxOps.GetRenderElementMgr(0)
		for n = 0 to (theManager.numrenderelements()- 1) do
		(
			imgName = theManager.GetRenderElementFileName n
			if (rrSI.imageFileName=="") then (
				rrSI.imageFileName=imgName
			) else (
				imageExt=""
				splitFileName &imgName &imageExt
				append rrSI.channelFileNames imgName
				append rrSI.channelExt imageExt
			)
		)
		rrSI.cmdOptions=""
		if (IDisplayGamma.colorCorrectionMode== #gamma) then (
			tmpStrg1=fileInGamma as string
			tmpStrg2=fileOutGamma as string
			tmpStrg1 = substituteString tmpStrg1 "." "<dec>"
			tmpStrg2 = substituteString tmpStrg2 "." "<dec>"
			rrSI.cmdOptions=" \"COGammaCorrect=0~0\"  \"AdditionalCommandlineParam=0~0~ -gammaCorrection:1 -gammaValueIn:" + tmpStrg1 + " -gammaValueOut:" + tmpStrg2 +"\" "
			if (fileOutGamma==1.0)  then (
				rrSI.cmdOptions= rrSI.cmdOptions + " \"PreviewGamma2.2=1~1\"  "
			)
		)		
	)

	fn WriteNodeToFile out_text nam val =
		(	
		val = val as string
		val = substituteString val "&" "&amp;"
		val = substituteString val "<" "&lt;"
		val = substituteString val ">" "&gt;"
		val = substituteString val "\"" "&quot;"
		val = substituteString val "'" "&apos;"
		format "\t<%>%</%>\n" nam val nam to:out_text
		)	
		
		
	fn WriteLayerToFile out_text lay cam active =
		(	
		format "<Job>\n"  to:out_text 
		WriteNodeToFile out_text "SceneOS" "win"
		WriteNodeToFile out_text "Software" "3dsMax" 
		WriteNodeToFile out_text "Layer" lay 
		WriteNodeToFile out_text "Camera" cam 
		WriteNodeToFile out_text "IsActive" active
		WriteNodeToFile out_text "Version" rrSI.MaxVersion
		WriteNodeToFile out_text "SceneName" rrSI.SceneFile
		WriteNodeToFile out_text "SceneDatabaseDir" rrSI.projectpath
		WriteNodeToFile out_text "Renderer" rrSI.Renderer
		WriteNodeToFile out_text "RequiredLicenses" rrSI.RequiredLicenses
		WriteNodeToFile out_text "SeqStart" rrSI.seqStart
		WriteNodeToFile out_text "SeqEnd" rrSI.seqEnd
		WriteNodeToFile out_text "SeqStep" rrSI.seqStep
		WriteNodeToFile out_text "SeqFileOffset" rrSI.seqFileOffset
		WriteNodeToFile out_text "SeqFrameSet" rrSI.seqFrameset
		WriteNodeToFile out_text "ImageWidth" rrSI.imageWidth
		WriteNodeToFile out_text "ImageHeight" rrSI.imageHeight
		WriteNodeToFile out_text "ImageFilename" rrSI.imageFileName
		WriteNodeToFile out_text "ImageExtension" rrSI.imageExt
		WriteNodeToFile out_text "ImageFramePadding" 4
		for c = 1 to rrSI.channelFileNames.count do (
			WriteNodeToFile out_text "ChannelFilename" rrSI.channelFileNames[c]
			WriteNodeToFile out_text "ChannelExtension" rrSI.channelExt[c]
		)

		format "</Job>\n"  to:out_text 
		)	
		
-----------------------------------------------------------------------
-- Function body start
-----------------------------------------------------------------------

	print "Royal Render v 6.02.31"
	-- Get all data
	if (maxFileName.count==0) then
		(
		messageBox "Scene was never saved." title:"Royal Render" 
		return "Scene was never saved."
		)
	if SceneExplorerManager.GetExplorerCount() != 0 then ( -- close all SceneExplorers
		SceneExplorerManager.ClearAllExplorers()
	)

	if getSaveRequired() then (
		ret=yesNoCancelBox "The Scene has been modified.\nDo you want to save your changes?" title:"Royal Render"
		if (ret==#yes) then (
			saveMaxFile(maxFilePath + maxFileName) 
		)
		if (ret==#cancel) then (
			return "Canceled"
		)
	)

	if getSaveRequired() then (
		ret=yesNoCancelBox "The Scene has been modified.\nDo you want to save your changes?" title:"Royal Render"
		if (ret==#yes) then (
			saveMaxFile(maxFilePath + maxFileName) 
		)
		if (ret==#cancel) then (
			return "Canceled"
		)
	)
	getSceneInfo()
    if (rrSI.imageFileName=="") then
		(
		messageBox "You have not defined a render output for your scene." title:"Royal Render" 
		return "No render output defined."
		)
	if (getRenderType()!=#view) then (
		if (not (queryBox "You have enabled Region in your render settings.\nContinue submission?" title:"Royal Render") ) then (
			return "region"
		)
	)

	-- Write XML file
	XMLfileName=getTempFileName()
	out_text = createFile XMLfileName
	format "<rrJob_submitFile syntax_version=\"6.0\">\n"  to:out_text 
	format "<DeleteXML>1</DeleteXML>\n"  to:out_text 
	WriteNodeToFile out_text "SubmitterParameter" rrSI.cmdOptions

	if (rrSI.Layer.count>0) then  (
		for c = 1 to rrSI.Cameras.count do
			(
				WriteLayerToFile out_text "" rrSI.Cameras[c] 0
			)
		lp=-1
		for p=rrSI.imageFileName.count  to 1 by -1 do
			if (rrSI.imageFileName[p] == "\\") then (
				lp=p
				exit
				)
		if (lp >-1) then (
			rrSI.imageFileName= replace rrSI.imageFileName lp 1 "\\<Layer>\\"
			)
		for l = 1 to rrSI.Layer.count do
			for c = 1 to rrSI.Cameras.count do
				(
					WriteLayerToFile out_text rrSI.Layer[l] rrSI.Cameras[c] 0
				)
	) else (
		WriteLayerToFile out_text "" "" 1
		for c = 1 to rrSI.Cameras.count do
			(
			WriteLayerToFile out_text "" rrSI.Cameras[c] 0
			)
		)
	format "</rrJob_submitFile>\n"  to:out_text 
	close out_text
	
	
	-- start submitter
	RR_ROOT=GetRRPath()
	if (RR_ROOT.count==0) then
		(
		messageBox "No RR_Root variable defined. Please reinstall." title:"Royal Render" 
		return "No RR_Root variable defined. Please reinstall."
		)	
	cmdLine="\"" + RR_ROOT + "\\win__rrSubmitter.bat\"  '" + XMLfileName+"'"
	DOSCommand cmdLine
)




macroScript rrSubmitRPManager
category:"RoyalRender"
buttontext:"Submit Scene, read RP-Manager passes"
tooltip:"Submit scene with RP-Manager passes to Server"
--fn rrSubmitRPManager=
(
	struct rrSceneInfo
		(
			MaxVersion,
			SceneFile,
			projectpath,
			Renderer,
			RequiredLicenses,
			imageWidth,
			imageHeight,
			HiddenCommand,
			seqFileOffset,
			seqStart,
			seqEnd,
			seqStep,
			seqFrameset,
			imageFileName,
			imageExtension,
			channelFileNames,
                        channelExt,
			Cameras,
			Layer,
			cmdOptions
		)
	global rrSI= rrSceneInfo()

	fn splitFileName &file &ext = 
		(
		for c = file.count to 1 by -1 do 
			if (file[c]==".") then (
				ext= substring file c (file.count - c+1)
				file= substring file 1 (c-1)
				return OK
			)
		)
	

	fn getRRPath =
		(
		cmdLine= "cmd.exe /c echo %RR_ROOT% > " + sysInfo.tempdir + "env.txt"
		DOSCommand cmdLine
		in_text = openfile (sysInfo.tempdir + "env.txt")
		if (not eof in_text) do
			(
			str = readLine in_text
			)
		close in_text
		deleteFile (sysInfo.tempdir + "env.txt")
		str = trimRight str
		if ((str.count>0) and (str[1]=="%")) then str = ""
		if (str.count==0) then str = "%RRLocationWin%"
		if ((str.count>0) and (str[1]=="%")) then str = ""
		str 
		)
		
	fn getTempFileName=
		(
		rnd= random 1 10000
		rnd= rnd as string
		str=sysInfo.tempdir + "rrSubmitMAX_" + rnd + ".xml"  
		str 
		)		
		
	fn getSceneInfo=
		(
		rrSI.projectpath = pathConfig.getCurrentProjectFolder()
		rrSI.SceneFile = maxFilePath + maxFileName 	
		ver= maxVersion()
		ver= ver[1]
		rrSI.HiddenCommand = (ver>=10000)
		ver2 = ver - (( ver / 1000)*1000)
		ver = ver/1000
		if (ver>10) do ver=ver-12+2010
		rrSI.MaxVersion= ver as string +"." + ver2 as string
		camobjs = cameras as array
		rrSI.Cameras =#()
		for c in 1 to camobjs.count do 	(
			if ((classof camobjs[c] == TargetCamera) or  (classof camobjs[c] == FreeCamera)  or  (classof camobjs[c] == VRayPhysicalCamera) or  (classof camobjs[c] == VRayDomeCamera)) then
				append rrSI.Cameras camobjs[c].name
		)
		rrSI.Renderer= classof renderers.production as string
		posi = findString rrSI.Renderer "V_Ray"
		if (posi != undefined) do rrSI.Renderer= "VRay"
		posi = findString rrSI.Renderer "Brazil"
		if (posi != undefined) do rrSI.Renderer= "Brazil"
 		rrSI.RequiredLicenses = rrSI.Renderer

		rrSI.seqFrameset=""
		
		if (rendTimeType==1) then (
			rrSI.seqStart=animationRange.start.frame  as integer
			rrSI.seqEnd=animationRange.start.frame  as integer
		) else if (rendTimeType==2) then (
			rrSI.seqStart=animationRange.start.frame as integer
			rrSI.seqEnd=animationRange.end.frame  as integer
		) else if (rendTimeType==3) then (
			rrSI.seqStart=rendStart.frame  as integer
			rrSI.seqEnd=rendEnd.frame  as integer
		) else (
			rrSI.seqFrameset= rendPickupFrames
			rrSI.seqStart=animationRange.start.frame
			rrSI.seqEnd=animationRange.end.frame
		)

		rrSI.seqStep=rendNThFrame
		rrSI.seqFileOffset=rendFileNumberBase
		rrSI.imageWidth= #()
		rrSI.imageHeight= #()
		if (not rendSaveFile) then rendSaveFile= true
		rrSI.imageFileName=rendOutputFilename

		rrSI.channelFileNames = #()
		rrSI.channelExt = #()
		rrSI.cmdOptions=""
		if (IDisplayGamma.colorCorrectionMode== #gamma) then (
			tmpStrg1=fileInGamma as string
			tmpStrg2=fileOutGamma as string
			tmpStrg1 = substituteString tmpStrg1 "." "<dec>"
			tmpStrg2 = substituteString tmpStrg2 "." "<dec>"
			rrSI.cmdOptions=" \"COGammaCorrect=0~0\"  \"AdditionalCommandlineParam=0~0~ -gammaCorrection:1 -gammaValueIn:" + tmpStrg1 + " -gammaValueOut:" + tmpStrg2 +"\" "
			if (fileOutGamma==1.0)  then (
				rrSI.cmdOptions= rrSI.cmdOptions + " \"PreviewGamma2.2=1~1\"  "
			)
		)
	)
		
	fn get_RPM_layer = (
		rrSI.Renderer="RPManager"
		rrSI.Cameras =#()
		rrSI.Layer = #()
		rrSI.seqStart= #()
		rrSI.seqEnd= #()
		rrSI.seqStep= #()
		rrSI.seqFrameset= #()
		rrSI.seqFileOffset= 0
		rrSI.imageFileName= #()
		rrSI.imageExtension= #()
		rrSI.imageWidth= #()
		rrSI.imageHeight= #()
		currentPass= RPMdata.GetPassSelection()
		
		
		maxLayer= RPMdata.GetPassCount()
		if (maxLayer!=0) then (
			callbacks.removescripts id:#RR_RPMPassChange
			callbacks.addscript #filepostopen "try(filein \"C:\\\\RR_LocalData\\\\RR_RPMPassChange.ms\" ) catch()" id:#RR_RPMPassChange persistent:true
			for l = 1 to maxLayer do (
				pass= RPMdata.GetPassName(l)
				SRange=RPMdata.GetPassRange(l)
				fOut1Add=""
				fOut2Add=""
				fOut3Add=""
				fUse1=false
				fUse2=false
				fUse3=false
				fCam1=RPMdata.GetPassCamera(l)
				fCam2=RPMdata.getPassSecondCamera(l)
				fCam3=RPMdata.getPassThirdCamera(l)
				seqFrameset=""

				if (classof SRange == Point3) then (
					seqStart= (SRange.x as integer)
					seqEnd= (SRange.y as integer)
					seqStep= (SRange.z as integer)
				)  else (
					seqStart= (SRange as integer)
					seqEnd= (SRange as integer)
					seqStep= 1
					) 
				
				
				CamInfo= RPMdata.getPassCameraExtraInfo l
				if ((CamInfo[1]=="Both") or (CamInfo[1]=="Render Only") ) then (
					fOut1Add=CamInfo[2] as string
					fUse1=true
				)
				CamInfo= RPMdata.getPassSecondCameraExtraInfo l
				if ((CamInfo[1]=="Both") or (CamInfo[1]=="Render Only") ) then (
						fOut2Add=CamInfo[2] as string
						fUse2=true
				)
				CamInfo= RPMdata.getPassThirdCameraExtraInfo l
				if ((CamInfo[1]=="Both") or (CamInfo[1]=="Render Only") ) then (
						fOut3Add=CamInfo[2] as string
						fUse3=true
				)
				useSubDirs=RPMdata.getOutputSetupData index:42

				fOut= RPMdata.GetPassOutputPath(l)
				fOutDir= ""
				fOutName= ""
				fOutExt=""
				fOut=filterString fOut "."  splitEmptyTokens:true
				fOutName=fOut[1]
				for i = 2 to fOut.count-1 do (
					fOutName=fOutName+ "." + fOut[i]
				)
				fOutExt="."+fOut[fOut.count]
				fOut=filterString fOutName "\\" splitEmptyTokens:true
				for i = 1 to fOut.count-1 do (
					fOutDir=fOutDir+ fOut[i]+"\\"
				)
				fOutName=fOut[fOut.count]	
				
					
				if (useSubDirs) then (
					if (fUse1) then (
						append rrSI.imageExtension fOutExt
						append rrSI.Cameras fCam1.name
						append rrSI.Layer pass
						append rrSI.seqStart seqStart
						append rrSI.seqEnd seqEnd
						append rrSI.seqStep seqStep
						append rrSI.seqFrameset seqFrameset
						if (fOut1Add=="") then (
							comb=fOutDir+fOutName+fOutExt
							append rrSI.imageFileName comb
						) else (
							comb=fOutDir+fOut1Add+"\\"+fOutName+fOut1Add
							append rrSI.imageFileName comb
						)
					) 
					if (fUse2) then (
						append rrSI.imageExtension fOutExt
						append rrSI.Cameras fCam2.name
						append rrSI.Layer pass
						append rrSI.seqStart seqStart
						append rrSI.seqEnd seqEnd
						append rrSI.seqStep seqStep
						append rrSI.seqFrameset seqFrameset
						if (fOut2Add=="") then (
							comb=fOutDir+fOutName+fOutExt
							append rrSI.imageFileName comb
						) else (
							comb=fOutDir+fOut2Add+"\\"+fOutName+fOut2Add
							append rrSI.imageFileName comb
						)
					) 
					if (fUse3) then (
						append rrSI.imageExtension fOutExt
						append rrSI.Cameras fCam3.name
						append rrSI.Layer pass
						append rrSI.seqStart seqStart
						append rrSI.seqEnd seqEnd
						append rrSI.seqStep seqStep
						append rrSI.seqFrameset seqFrameset
						if (fOut3Add=="") then (
							comb=fOutDir+fOutName+fOutExt
							append rrSI.imageFileName comb
						) else (
							comb=fOutDir+fOut3Add+"\\"+fOutName+fOut3Add
							append rrSI.imageFileName comb
						)
					) 
				) else (
					if (fUse1) then (
						append rrSI.imageExtension fOutExt
						append rrSI.Cameras fCam1.name
						append rrSI.Layer pass
						append rrSI.seqStart seqStart
						append rrSI.seqEnd seqEnd
						append rrSI.seqStep seqStep
						append rrSI.seqFrameset seqFrameset
						if (fOut1Add=="") then (
							comb=fOutDir+fOutName+fOutExt
							append rrSI.imageFileName comb
						) else (
							comb=fOutDir+fOutName+fOut1Add
							append rrSI.imageFileName comb
						)
					) 
					if (fUse2) then (
						append rrSI.imageExtension fOutExt
						append rrSI.Cameras fCam2.name
						append rrSI.Layer pass
						append rrSI.seqStart seqStart
						append rrSI.seqEnd seqEnd
						append rrSI.seqStep seqStep
						append rrSI.seqFrameset seqFrameset
						if (fOut2Add=="") then (
							comb=fOutDir+fOutName+fOutExt
							append rrSI.imageFileName comb
						) else (
							comb=fOutDir+fOutName+fOut2Add
							append rrSI.imageFileName comb
						)
					) 
					if (fUse3) then (
						append rrSI.imageExtension fOutExt
						append rrSI.Cameras fCam3.name
						append rrSI.Layer pass
						append rrSI.seqStart seqStart
						append rrSI.seqEnd seqEnd
						append rrSI.seqStep seqStep
						append rrSI.seqFrameset seqFrameset
						if (fOut3Add=="") then (
							comb=fOutDir+fOutName+fOutExt
							append rrSI.imageFileName comb
						) else (
							comb=fOutDir+fOutName+fOut3Add
							append rrSI.imageFileName comb
						)
					) 
				)
				
				RPMData.RMRestValues(l)
				
				if (rrSI.Renderer== "VRay") then (
					if (renderers.production.adv_irradmap_mode==6) then (
						rrSI.imageFileName=renderers.production.adv_irradmap_autoSaveFileName
					)
				)

				append rrSI.imageWidth renderWidth
				append rrSI.imageHeight renderHeight
				append rrSI.channelFileNames #()
				append rrSI.channelExt #()
				theManager = maxOps.GetRenderElementMgr(0)
				for n = 0 to (theManager.numrenderelements()- 1) do
				(
					imgName = theManager.GetRenderElementFileName n
					if (imgName=="") then (
						imgName= fOutDir+fOutName+"_" + (theManager.GetRenderElement n).elementName + fOutExt
					) 
					imageExt=""
					splitFileName &imgName &imageExt
					append rrSI.channelFileNames[l] imgName
					append rrSI.channelExt[l] imageExt

				)
			)
		)
		RPMData.RMRestValues(currentPass[1])
	)
	
	fn WriteNodeToFile out_text name val =
		(	
		val = val as string
		val = substituteString val "&" "&amp;"
		val = substituteString val "<" "&lt;"
		val = substituteString val ">" "&gt;"
		val = substituteString val "\"" "&quot;"
		val = substituteString val "'" "&apos;"
		format "\t<%>%</%>\n" name val name to:out_text
		)	
		
		
	fn WriteLayerToFile out_text layerNumber=
		(	
		format "<Job>\n"  to:out_text 
		WriteNodeToFile out_text "SceneOS" "win"
		WriteNodeToFile out_text "Software" "3dsMax" 
		WriteNodeToFile out_text "Layer" rrSI.Layer[layerNumber]
		WriteNodeToFile out_text "Camera" rrSI.Cameras[layerNumber]
		WriteNodeToFile out_text "IsActive" 1
		WriteNodeToFile out_text "Version" rrSI.MaxVersion
		WriteNodeToFile out_text "SceneName" rrSI.SceneFile
		WriteNodeToFile out_text "SceneDatabaseDir" rrSI.projectpath
		WriteNodeToFile out_text "Renderer" "RPManager"
		WriteNodeToFile out_text "RequiredLicenses" rrSI.RequiredLicenses
		WriteNodeToFile out_text "SeqStart" rrSI.seqStart[layerNumber]
		WriteNodeToFile out_text "SeqEnd" rrSI.seqEnd[layerNumber]
		WriteNodeToFile out_text "SeqStep" rrSI.seqStep[layerNumber]
		WriteNodeToFile out_text "SeqFileOffset" rrSI.seqFileOffset
		WriteNodeToFile out_text "SeqFrameSet" rrSI.seqFrameset[layerNumber]
		WriteNodeToFile out_text "ImageWidth" rrSI.imageWidth[layerNumber]
		WriteNodeToFile out_text "ImageHeight" rrSI.imageHeight[layerNumber]
		WriteNodeToFile out_text "ImageFilename" rrSI.imageFileName[layerNumber]
		WriteNodeToFile out_text "ImageExtension" rrSI.imageExtension[layerNumber]
		WriteNodeToFile out_text "ImageFramePadding" 4
		for c = 1 to rrSI.channelFileNames[layerNumber].count do (
			WriteNodeToFile out_text "ChannelFilename" rrSI.channelFileNames[layerNumber][c]
                        WriteNodeToFile out_text "ChannelExtension" rrSI.channelExt[layerNumber][c]
		)
		format "</Job>\n"  to:out_text 
		)	
		
-----------------------------------------------------------------------
-- Function body start
-----------------------------------------------------------------------

	print "Royal Render v 6.02.31"
	-- Get all data
	if (maxFileName.count==0) then
		(
		messageBox "Scene was never saved." title:"Royal Render" 
		return "Scene was never saved."
		)
	if SceneExplorerManager.GetExplorerCount() != 0 then ( -- close all SceneExplorers
		SceneExplorerManager.ClearAllExplorers()
	)

	if getSaveRequired() then (
		ret=yesNoCancelBox "The Scene has been modified.\nDo you want to save your changes?" title:"Royal Render"
		if (ret==#yes) then (
			saveMaxFile(maxFilePath + maxFileName) 
		)
		if (ret==#cancel) then (
			return "Canceled"
		)
	)

	getSceneInfo()
	get_RPM_layer()
	if (rrSI.Layer.count==0) then (
		messageBox "No RP-Manager pass found." title:"Royal Render" 
		return "No RP-Manager pass found."	
	)
	saveMaxFile(maxFilePath + maxFileName) 
	if (getRenderType()!=#view) then (
		if (not (queryBox "You have enabled Region in your render settings.\nContinue submission?" title:"Royal Render") ) then (
			return "region"
		)
	)

	-- Write XML file
	XMLfileName=getTempFileName()
	out_text = createFile XMLfileName
	format "<rrJob_submitFile syntax_version=\"6.0\">\n"  to:out_text 
	format "<DeleteXML>1</DeleteXML>\n"  to:out_text 
	WriteNodeToFile out_text "SubmitterParameter" rrSI.cmdOptions

	for c = 1 to rrSI.Cameras.count do
		(
		WriteLayerToFile out_text c
		)
	format "</rrJob_submitFile>\n"  to:out_text 
	close out_text
	
	
	-- start submitter
	RR_ROOT=GetRRPath()
	if (RR_ROOT.count==0) then
		(
		messageBox "No RR_Root variable defined. Please reinstall." title:"Royal Render" 
		return "No RR_Root variable defined. Please reinstall."
		)	
	cmdLine="\"" + RR_ROOT + "\\win__rrSubmitter.bat\"  '" + XMLfileName+"'"
	DOSCommand cmdLine
)