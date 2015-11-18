	-- Creates menu for Royal Render 
	-- Author:  Royal Render, Holger Schoenberger, Binary Alchemy
	-- Last change: v 6.01.70
	-- Copyright (c) Holger Schoenberger - Binary Alchemy
	-- rrInstall_Copy: \Scripts\Startup\
(
	print "--------------------"
	rrMenu = menuman.findmenu "RRender"
	if rrMenu == undefined do
		rrMenu = menuman.createmenu "RRender"
		
	if rrMenu != undefined do
	(
		numItems = rrMenu.numitems()
		if numItems == 0 then
		(
			local rrAction1 = menuman.createActionItem "rrSubmit" "RoyalRender"
			rrMenu.additem rrAction1 -1
			local rrAction2 = menuman.createActionItem "rrSubmitRPManager" "RoyalRender"
			rrMenu.additem rrAction2 -1
		)
		else
		(
			local nameList = #()
			for i in 1 to numItems do (
				name=(rrMenu.getitem i).gettitle()
				append nameList name
				)
			if finditem nameList "Submit scene" == 0 do
			(
				local rrAction1 = menuman.createActionItem "rrSubmit" "RoyalRender"
				rrMenu.additem rrAction1 -1
			)
			if finditem nameList "Submit Scene, read RP-Manager passes" == 0 do
			(
				local rrAction2 = menuman.createActionItem "rrSubmitRPManager" "RoyalRender"
				rrMenu.additem rrAction2 -1
			)
		)
		local mainMenu = menuman.getmainmenubar()
		local items = mainmenu.numitems()
		menuList = for i in 1 to items collect (mainMenu.getitem i).gettitle()
		if finditem menuList "RRender" == 0 do
		(
			local subMenuItem = menuMan.createSubMenuItem "RRender" rrMenu 
			mainmenu.additem subMenuItem (items - 1)
			menuMan.updateMenuBar()
		)
	)
)

rollout deleteInstallScript ""
(
	timer timr active:true interval:1000
	
	on timr tick do
	(
		deletefile (scriptspath + "startup\\rrSubmit_3dsMax_8.0+_MenuInstaller.ms")
		if (getfiles (scriptspath + "startup\\rrSubmit_3dsMax_8.0+_MenuInstaller.ms")).count == 0 do
			destroydialog deleteInstallScript
	)
)

createdialog deleteInstallScript pos:[-50,-50]
