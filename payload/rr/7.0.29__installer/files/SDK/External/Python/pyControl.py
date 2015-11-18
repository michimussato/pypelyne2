
def findRR_Root():
    # findRR_Root adds the RR path as search path for the module
    # This function will only work if RR was installed on the machine
    # If you are using it from an external machine, you have to add the path to the rrPy module yourself
    # sys.path.append(MyModulePath)
    import os
    import platform
    import sys
    import struct
    if (not os.environ.has_key('RR_ROOT')):
        return
    modPath=os.environ['RR_ROOT']
    is64bit=(struct.calcsize("P") == 8)
    if (sys.platform.lower() == "win32") :
        if (is64bit):
            modPath=modPath + '/bin/win64'
        else:
            modPath=modPath + '/bin/win'
        modPath=modPath.replace("\\","/")
    elif (sys.platform.lower() == "darwin"):
        if (is64bit):
            modPath=modPath + '/bin/mac64/lib/python/27'
        else:
            modPath=modPath + '/bin/mac/lib/python/27'
    else:
        modPath=modPath + '/bin/lx64/lib'
    #modPath=modPath.replace("_debug","_release")
    sys.path.append(modPath)
    print("added module path "+modPath)
    

findRR_Root()
import libpyRR2 as rrLib


### --------------------------------------------------------------------- INIT
print("Set up server and login info.")
#A login is required if you have enabled 'Auth required for all connections' in rrConfig tab rrLogin
#Or if you connect via an router (router has to be setup in rrConfig as well)
#Note:  tcp does not keep an open connection to the rrServer.
#Every command re-connects to the server
tcp = rrLib._rrTCP("")
rrServer=tcp.getRRServer() #This function does only work in your company. It uses the RR_ROOT environment installed by rrWorkstationInstaller
if (len(rrServer)==0):
    print (tcp.errorMessage())
if not tcp.setServer(rrServer, 7773):
    print ("Error setServer: "+ tcp.errorMessage())
    sys.exit()
  
tcp.setLogin("TestUser", "Password")



### --------------------------------------------------------------------- CLIENTS
print("\nCheck clients")
if not tcp.clientGetList():
  print("Error getting clients: " + tcp.errorMessage())
else:
  clients = tcp.clients
  nbClients = clients.count()
  print("Number of client found: " + str(nbClients))
  for i in xrange(0, nbClients):
    cl = clients.at(i)
    print("\tCpuUsage %6.2f name: %s" %(cl.CPU_Usage,cl.name) )




### --------------------------------------------------------------------- JOBS
### IMPORTANT: tcp caches all jobs, if you destroy it, the rrServer has to send all jobs again
### A list request will always be executed, so you have a list of all jobs at the rrServer
### But to reduce traffic, you should set a filter for the jobs you need before you request more data
### There are three levels of job information:
### MinInfo: The list, all jobs with ID, user, software, project
### Basic:   Scene information
### Send:    All job data you can have
    
print("\nCheck jobs")
jobUserName="renderfarm"               #retrieve only job details of user "renderfarm" to resuce network traffic, rrServer workload and this Pythons memory.
tcp.jobSetFilter(jobUserName,"","","",rrLib._filterIDs.isAll); 


#if not tcp.jobGetInfoBasic(): //use this command if you do not need the full information about a job

if not tcp.jobGetInfoSend():
  print("Error getting jobs: " + tcp.errorMessage())
else:
  jobs = tcp.jobs
  print("Number of jobs: " + str(jobs.getMaxJobs()))
  nbJobs = jobs.getMaxJobsFiltered()
  print("Number of jobs - filtered by user "+str(jobUserName)+": " + str(nbJobs))
  for i in xrange(0, nbJobs):
    jID = jobs.getJobMinInfo_filterQueue(i).ID
    username= jobs.getJobMinInfo_filterQueue(i).userName
    jobDataType = jobs.getJobDataType(jID) #which kind of data we have for the job
    job = jobs.getJobBasic(jID)
    print("   " + job.IDstr()+"\tuser: "+username     +"\tscene: "+job.sceneName   +"\tscene: "+job.renderer.name     +"\timage dim: "+str(job.imageWidth)+"x"+str(job.imageHeight)  )

##  if (nbJobs>0):
##      print("\nChange Sequence in/out of first job")
##      import random
##      random.seed()
##      modjobValues=rrJob.getClass_SettingsOnly()
##      modjobValues.seqStart=random.randint(2,50)
##      modjobValues.seqEnd=random.randint(80,120)
##      modjobFlags=rrJob.getClass_SettingsOnly()
##      modjobFlags.seqStart=1;
##      modjobFlags.seqEnd=1;
##      modjobList =[]
##      jID = jobs.getJobMinInfo_filterQueue(i).ID
##      modjobList.append(jID)
##      print("    Changing job "+jobs.getJobMinInfo_filterQueue(i).IDstr()+"  min="+str(modjobValues.seqStart)+"  max="+str(modjobValues.seqEnd))
##      tcp.jobModify(modjobList  ,modjobValues, modjobFlags);
      
  
  

    


### --------------------------------------------------------------------- USERS
print("\nCheck users")
if not tcp.userGet("X"):    #---- need a non-zero string and returns all the users!!
  print("Error getting user: " + tcp.errorMessage())
else:
  users = tcp.users
  nbUsers = users.count()
  print("Number of user found: " + str(nbUsers))
  for i in xrange(0, nbUsers):
      print("\tname: " + users.at(i).name)
print("\n\nConnection Stats\  "+tcp.connectionStats())



print("\n\n--- DONE ---\n\n")
