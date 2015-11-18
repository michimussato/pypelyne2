import  rrGlobal
'''import  rrSG
import  sys
modPath=rrGlobal.rrModPyrrPath()
sys.path.append(modPath)
print("added module path "+modPath)
import libpyRR2 as rr'''

def updateStatsCmd():
    print "Update render stats in shotgun"
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-sgid")
    parser.add_argument("-avMemUsage")
    parser.add_argument("-avRenderTime")
    parser.add_argument("-status")
    args = parser.parse_args()
    if ((len(args.sgid)<=1) or (args.sgid=="none")):
        print("Job has no Shotgun ID.")
        return

setRenderEntityState
    
    import royalRifle
    global rRifle
    rRifle=royalRifle.RoyalRifle()
    renderEntity={}

    #renderEntity_old= rRifle._findRenderEntity(int(args.sgid))
    #print "\t\t renderEntity1 : %s" % renderEntity_old
    renderEntity['sg_average_render_time']=args.avRenderTime
    memFloat=float(args.avMemUsage)
    renderEntity['sg_average_memory_usage']=memFloat
    rRifle._updateRenderEntity(int(args.sgid),renderEntity)
    rRifle.setRenderEntityState(int(args.sgid),args.status)
updateStatsCmd()
