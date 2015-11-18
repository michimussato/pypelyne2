import  rrGlobal



def addQuicktimeCmd():
    print "Adding preview images to shotgun"
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-sgid")
    parser.add_argument("-movh")
    parser.add_argument("-movl")
    args = parser.parse_args()
    shreID=args.sgid
    if ((len(shreID)<=1) or (shreID=="none")):
        print("Job has no Shotgun ID.")
        return
    
    import royalRifle
    global rRifle
    rRifle=royalRifle.RoyalRifle()

    rRifle.addQuicktime(int(shreID), args.movh, args.movl)
  

addQuicktimeCmd()
