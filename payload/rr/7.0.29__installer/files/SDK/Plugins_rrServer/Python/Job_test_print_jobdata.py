# Royal Render plugin
# Information: RR reads the first comment block to get the settings for this plugin.
# Can can write as many lines as you like.
#
# These lines are just information lines for users and have no effect.  They are *not* required
# rrPluginName:		Hello World
# rrPluginAuthor:	Holger Schoenberger
# rrPluginVersion:	1.0
# rrPluginType:		Job Plugin
# rrRRversion:		7.0.15
#
#
# These settings are important for server job plugins and have to be set.
# They tell the rrServer when the plugin should be executed. 
# A 1 activates the plugin. Everything else or nothing disables it.
#
# rrJobExec FirstCheck:		   1
# rrJobExec ScriptPreRender:	   1
# rrJobExec PreviewRender:	   1
# rrJobExec ScriptAfterPreview:	   
# rrJobExec WaitForApprovalMain:   
# rrJobExec MainRender:		   
# rrJobExec ScriptPostRender:	   1
# rrJobExec WaitForApprovalDone:   0
# rrJobExec ScriptFinished:	   0
# rrJobExec Finished:		   0
#
#
#

# The first line without an # will stop the information parser.
# Therefore these lines are not read any more.



job= rr.getJob()

rrGlobal.writeLog(rrGlobal.logLvL.info,  "Example Python script:\n I am job " +job.sceneName,  "Hello Job Script")




