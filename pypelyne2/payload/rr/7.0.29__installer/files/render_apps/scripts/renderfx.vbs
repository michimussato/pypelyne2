
'  v 6.01.40
'  Copyright (c) 2009-2010 Holger Schoenberger - Binary Alchemy


SUB RenderIt (scname,oname,fname,sfr,efr,stfr,db,wg)
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

OpenScene scname, False 

if not (IsNull(db) or (len(db)=0)) then
  logmessage "RR - Set project to " & db
  Application.ActiveProject = db 
  end if
logmessage "RR - Active Project: " & Application.ActiveProject2.Path


sfr=int(sfr)
efr=int(efr)
stfr=int(stfr)
if (sfr=efr) then
    stfr=1
end if

SetValue oname & ".StartFrame", sfr
SetValue oname & ".EndFrame", efr
SetValue oname & ".Step", stfr
SetValue oname & ".FileName", fname
RenderFxOp oname, False
END SUB