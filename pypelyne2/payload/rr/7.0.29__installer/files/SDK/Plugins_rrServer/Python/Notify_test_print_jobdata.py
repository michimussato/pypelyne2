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
#
#
# These settings are optional for notification plugins.
# They are shown as dropdown in rrSubmitter and you can access them via job.NotifyFinishParam
#
# rrParamDisplayName:	MyLanguageID
# rrParam:		Hello
# rrParam:		Hallo
# rrParam:		Hola
# rrParam:		Allo
# rrParam:		Ciao
#
#
#
#

# The first line without an # will stop the information parser.
# Therefore these lines are not read any more.



job= rr.getJob()

rrGlobal.writeLog(rrGlobal.logLvL.info,  "Example Python script:\n I am job " +job.sceneName,  "Hello Job Script")
rrGlobal.writeLog(rrGlobal.logLvL.info,  "Notify parameter ID: "+str(job.notifyFinishParam),  "Hello Job Script")




