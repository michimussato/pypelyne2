// Royal Render Plugin script for After Effects
// Author:  Royal Render, Holger Schoenberger, Binary Alchemy
// Last change: v 6.00.30
// Copyright (c) 2009-2010 Holger Schoenberger - Binary Alchemy
// #win: rrInstall_Copy: \include\startup\ui\
// #linux: rrInstall_Copy: \include\startup\ui\
// #mac: rrInstall_Copy: ../PlugIns/startup/ui/


extern "C" {
int system(const char*);
}


void CallSystemMenu()
{	
const char* command = stringf("%RRLocationWin%\\win__rrSubmitter.bat %s &", NRiMainWin1.scriptName);
system(command);
const char* command2 = stringf("%RRLocationLx%/lx__rrSubmitter.sh %s &", NRiMainWin1.scriptName);
system(command2);
const char* command3 = stringf("%RRLocationMac%/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter %s &", NRiMainWin1.scriptName);
system(command3);
}

nuiPushMenu("RoyalRender");
nuiMenuItem("Submit Composite", CallSystemMenu());
nuiPopMenu();