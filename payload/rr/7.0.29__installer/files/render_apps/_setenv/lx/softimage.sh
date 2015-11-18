
setenv XSI_LOG_LOAD_TIME 1
setenv XSI_USERHOME "${rrLocalPrefs}${rrExeVersion}"
setenv XSI_USERROOT "${rrLocalPrefs}"



switch ( {$rrExeVersionMajor} )
  case 6:    
    setenv WorkgroupPath "${rrPluginsNoOS}workgroup_6"
    breaksw
  case 7:    
    setenv WorkgroupPath "${rrPluginsNoOS}workgroup_7"
    breaksw
  case 2010:    
    setenv WorkgroupPath "${rrPluginsNoOS}workgroup_2010"
    breaksw
  case 2011:    
    setenv WorkgroupPath "${rrPluginsNoOS}workgroup_2011"
    breaksw
  case 2012:    
    setenv WorkgroupPath "${rrPluginsNoOS}workgroup_2012"
    breaksw
  case 2013:    
    setenv WorkgroupPath "${rrPluginsNoOS}workgroup_2013"
    breaksw
  case 2014:    
    setenv WorkgroupPath "${rrPluginsNoOS}workgroup_2014"
    breaksw
  default:
    setenv WorkgroupPath "${rrPluginsNoOS}workgroup_${rrJobVersionMajor}"
    breaksw
endsw


#do not forget the empty line at the end:
