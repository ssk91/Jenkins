import os
import subprocess
import re
import sys
import time
import paramiko
sys.path.insert(0, '/nobackup/anantram/python3.6/usr/local/lib/python3.6/site-packages/paramiko')
import distro

#print 'Number of arguments:', len (sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

print("####################################################VOB TAG AND MOUNT REMOTELY##########################################################")


count = len(sys.argv)-1
#print(count)
if(count<2):
    print("Inadequate arguments please provide vob tag and user host as input")
    sys.exit()

vob_tag = sys.argv[1]
user_host = sys.argv[2]

y=0
with open ('file.txt', 'rt') as myfile:
    for myline in myfile:
        if re.match('(.+) ' + vob_tag + ' (.+)', myline):
            y=1
            output = myline
            print("Vob tag found in the file: "+output)
if(y==0):
    print("Vob tag: "+vob_tag+" not found in the file !!")
    sys.exit()

keys = paramiko.RSAKey.from_private_key_file("/users/santhsu2/.ssh/id_rsa")
connection = paramiko.SSHClient()
connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
connection.connect( hostname =user_host , username = "santhsu2", pkey = keys, timeout=5 )

stdin , stdout, stderr = connection.exec_command('/usr/atria/bin/cleartool hostinfo -l | grep Registry | grep host')
print("Loggng to user host: "+user_host)

#time.sleep(0.1) # some enviroment maybe need this.
hostinfo = stdout.read().decode("utf-8").split(" ")
Registry_Server = hostinfo[4]
registry=Registry_Server.replace("\n","")
print("Registry Server: "+Registry_Server)
print(stderr.read().decode("utf-8"))
connection.close()

connection.connect( hostname =registry , username = "santhsu2", pkey = keys, timeout=5 )
print("Logging to registry server: "+Registry_Server)
print(stdout.read().decode("utf-8"))
print(stderr.read().decode("utf-8"))

mylines = []

with open ('file.txt', 'rt') as myfile:
    for myline in myfile:
        if re.match('(.+) ' + vob_tag + ' (.+)', myline):

            output = myline
            split = output.split()
            gpath = split[2]
            host = split[5]
            hpath = gpath
            
            #print("Vob tag: "+vob_tag)
            #print("Vob server: "+host)
            #print("Global path: "+gpath)
            #print("Host path: "+hpath)
            #print(stdout.read().decode("utf-8"))
            stdin , stdout, stderr = connection.exec_command("/usr/atria/bin/cleartool register -vob -host " +host+" -hpath " +hpath+" "+gpath)
            print(stdout.read().decode("utf-8"))
            print(stderr.read().decode("utf-8"))
            #print(stdout.read().decode("utf-8"))
            #print("\n")
            stdin , stdout, stderr = connection.exec_command("/usr/atria/bin/cleartool mktag -vob -tag " +vob_tag+ " -tcomment '/vob tag restored' -pub -password 'legendary' -host " +host+" "+"-gpath " +gpath+" "+hpath)
            print(stdout.read().decode("utf-8"))
            print(stderr.read().decode("utf-8"))
            #print("\n")
            stdin , stdout, stderr = connection.exec_command('/usr/atria/bin/cleartool mount -a')
            print(stdout.read().decode("utf-8"))
            print(stderr.read().decode("utf-8"))

connection.close()

connection.connect( hostname =user_host , username = "santhsu2", pkey = keys, timeout=5 )
stdin , stdout, stderr = connection.exec_command('/usr/atria/bin/cleartool mount -a')
print(stdout.read().decode("utf-8"))
print(stderr.read().decode("utf-8"))
connection.close()









