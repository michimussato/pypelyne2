import  rrGlobal



def addPreviewCmd():
    print "Adding preview images to shotgun"
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-sgid")
    parser.add_argument("-p1")
    parser.add_argument("-p2")
    parser.add_argument("-p3")
    parser.add_argument("-p4")
    parser.add_argument("-p5")
    parser.add_argument("-status")
    args = parser.parse_args()
    shreID=args.sgid
    if ((len(shreID)<=1) or (shreID=="none")):
        print("Job has no Shotgun ID.")
        return
    
    import royalRifle
    global rRifle
    rRifle=royalRifle.RoyalRifle()

    pathList = []
    pathList.append(args.p1)
    pathList.append(args.p2)
    pathList.append(args.p3)
    pathList.append(args.p4)
    pathList.append(args.p5)
    rRifle.addPreviewImages(int(shreID), pathList)
    rRifle.setRenderEntityState(int(args.sgid),args.status)
  

addPreviewCmd()
