import sys


print "Deleting this job from the RR queue"

modPath=rrGlobal.rrModPyrrPath()

sys.path.append(modPath)
print("added module path "+modPath)
import libpyRR2 as rr


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-jid")
parser.add_argument("-authstr")
args = parser.parse_args()


print("Set up server and login info")
tcp = rr._rrTCP("")
tcp.setServer(rrGlobal.rrServer(), 7773)
tcp.setLogin(args.authstr, "")


print("Sending Job Command")
jobsApply=[]
jobsApply.append(int(args.jid))
tcp.jobSendCommand(jobsApply,rrJob._LogMessage.lDelete,0)

print "done"
