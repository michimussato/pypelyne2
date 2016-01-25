try (
	logFilename= sysInfo.tempdir+ "rrMaxRender.log"
	out_text = openFile logFilename mode:"a+"
	format "     /n"  to:out_text 
	format "     /n"  to:out_text 
	format "                  ###########################################################################################/n"  to:out_text 
        format "                  ######################         RENDER IS STARTING FROM NOW           ######################/n"  to:out_text 
	format "                  ###################### IGNORE OLDER MESSAGES ABOUT SCENE AND FRAMES  ######################/n"  to:out_text 
	close out_text	
        python.ExecuteFile "*rrScriptFolder*\kso_3dsmax.py"
	sleep 2
) catch (
	errMessage=getCurrentException()
	print errMessage
	logFilename= sysInfo.tempdir+ "rrMaxRender.log"
	out_text = openFile logFilename mode:"a+"
	format "     \n"  to:out_text 
	format " Error executing render script!\n"  to:out_text 
	format errMessage to:out_text 
	format "     \n"  to:out_text 
	format "     \n"  to:out_text 
	format "     \n"  to:out_text 
	close out_text	
	sleep 2
)
