# Royal Render Plugin script for Fusion 5+
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 6.02.12
# Copyright (c) Holger Schoenberger - Binary Alchemy
# rrInstall_Copy: \plugins\
# rrInstall_Change_File: \plugins\menu.tcl, before "# OTHER MENU *****", "menu \"RRender/Submit Comp\" rrSubmit_Nuke_4\n"

proc rrSubmit_Nuke_4 {} {
	global env
	global WIN32

	set RRDir ""
	catch {
		set RRDir $env(RR_ROOT)
	}
	if {$RRDir==""} {
		catch {
			if {$WIN32} {
				set RRDir "%RRLocationWin%"
			} else {
				set RRDir "%RRLocationLx%"
			}
			if {[string range $RRDir 0 0]=="%"} {
			set RRDir ""
			}
		}
	}

	if {$RRDir==""} {
		message "RR_ROOT not set. Please reinstall plugin"
		return
	}

	script_save [knob root.name]
	set CompName [knob root.name] 

	if {$CompName==""} {
		message "Comp was never saved"
		return
	}

	if {$WIN32} {
		exec  "$RRDir\\win__rrSubmitter.bat" "$CompName"
	} else {
		exec  "$RRDir/lx__rrSubmitter.sh" "$CompName"
	}

}

