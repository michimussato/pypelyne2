#!/bin/csh -f

if ( ! $?RR_ROOT ) then
#Set this path to the installation (mounted) directory of RRender
#e.g.  setenv RR_ROOT "/mnt/rrender"
   setenv RR_ROOT ""
endif

setenv LD_LIBRARY_PATH ""

source "$RR_ROOT/lx__global.sh"
"$RR_ROOT/bin/lx64/rrStartLocal" "rrSubmitter" $argv:q $RRCMD




