#!/bin/csh -f

#Set this path to the installation (mounted) directory of RRender
#e.g.  setenv RR_ROOT_INSTALLER "/mnt/rrender"
setenv RR_ROOT_INSTALLER ""

source "$RR_ROOT_INSTALLER/lx__global.sh"
"$RR_ROOT_INSTALLER/bin/lx64/rrWorkstation_installer" $argv:q $RRCMD


