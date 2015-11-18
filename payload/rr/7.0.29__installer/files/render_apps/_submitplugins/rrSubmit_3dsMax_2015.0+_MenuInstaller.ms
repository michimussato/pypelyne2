	-- Creates menu for Royal Render 
	-- Author:  Royal Render, Holger Schoenberger, Binary Alchemy
	-- Last change: v 7.0.11
	-- Copyright (c) Holger Schoenberger - Binary Alchemy
	-- rrInstall_Copy: \Scripts\Startup\
(
	print "Royal Render: Checking for RRender menu..."
	changesMade=false
	rrMenu = menuman.findmenu "RRender"
	if rrMenu == undefined do (
		print "Royal Render: Creating RRender menu"
		rrMenu = menuman.createmenu "RRender"
		changesMade=true
		)
		
	if rrMenu != undefined do
	(
		
		numItems = rrMenu.numitems()
		if numItems == 0 then
		(
			print "Royal Render: Empty menu, creating new items"
			local rrAction1 = menuman.createActionItem "rrSubmit_new" "RoyalRender"
			rrMenu.additem rrAction1 -1
			local rrAction2 = menuman.createActionItem "rrSubmit_new_subfolder" "RoyalRender"
			rrMenu.additem rrAction2 -1
			local rrAction3 = menuman.createActionItem "rrSubmit" "RoyalRender"
			rrMenu.additem rrAction3 -1
			local rrAction4 = menuman.createActionItem "rrSubmitRPManager" "RoyalRender"
			rrMenu.additem rrAction4 -1
			changesMade=true
		) else (
			foundMenu1=false
			foundMenu2=false
			foundMenu3=false
			foundMenu4=false
			local nameList = #()
			for i = rrMenu.numitems() to 1 by -1 do (
				name=(rrMenu.getitem i).gettitle()
				if (name=="Submit scene                                    (New. VRay and scanline)") then (
					if (foundMenu1) do (
						print "Royal Render: deleting dublicate submit 1"
						rrMenu.removeItemByPosition  i
						changesMade=true
					)
					foundMenu1=true
				) else if (name=="Submit scene, element subfolders   (New. VRay and scanline)") then (
					if (foundMenu2) do (
						print "Royal Render: deleting dublicate submit 2"
						rrMenu.removeItemByPosition  i
						changesMade=true
					)
					foundMenu2=true
				) else if (name=="Submit scene    (Old; all renderer)") then (
					if (foundMenu3) do (
						print "Royal Render: deleting dublicate submit 3"
						rrMenu.removeItemByPosition  i
						changesMade=true
					)
					foundMenu3=true
				) else if (name=="Submit RPM Scene   (read RP-Manager passes)") then (
					if (foundMenu4) do (
						print "Royal Render: deleting dublicate submit 4"
						rrMenu.removeItemByPosition  i
						changesMade=true
					)
					foundMenu4=true
				) else (
					print "Royal Render: deleting old submit "+name
					rrMenu.removeItemByPosition  i
					changesMade=true
				)

			)

			if (not foundMenu1) then (
				local rrAction1 = menuman.createActionItem "rrSubmit_new" "RoyalRender"
				rrMenu.additem rrAction1 -1
				changesMade=true
			)
			if (not foundMenu2) then (
				local rrAction2 = menuman.createActionItem "rrSubmit_new_subfolder" "RoyalRender"
				rrMenu.additem rrAction2 -1
				changesMade=true	
			)
			if (not foundMenu3) then (
				local rrAction3 = menuman.createActionItem "rrSubmit" "RoyalRender"
				rrMenu.additem rrAction3 -1
				changesMade=true	
			)
			if (not foundMenu4) then (
				local rrAction4 = menuman.createActionItem "rrSubmitRPManager" "RoyalRender"
				rrMenu.additem rrAction4 -1
				changesMade=true	
			)
		)
		local mainMenu = menuman.getmainmenubar()
		local items = mainmenu.numitems()
		menuList = for i in 1 to items collect (mainMenu.getitem i).gettitle()
		if finditem menuList "RRender" == 0 do
		(
			local subMenuItem = menuMan.createSubMenuItem "RRender" rrMenu 
			mainmenu.additem subMenuItem (items - 1)
			changesMade=true
		)
	if changesMade do
		(
		menuMan.updateMenuBar()
		)
	)
)

rollout deleteInstallScript ""
(
	timer timr active:true interval:1000
	
	on timr tick do
	(
		deletefile (scriptspath + "startup\\rrSubmit_3dsMax_2013.0+_MenuInstaller.ms")
		deletefile (scriptspath + "startup\\rrSubmit_3dsMax_2015.0+_MenuInstaller.ms")
		if (getfiles (scriptspath + "startup\\rrSubmit_3dsMax_2015.0+_MenuInstaller.ms")).count == 0 do
			destroydialog deleteInstallScript
	)
)

createdialog deleteInstallScript pos:[-50,-50]
