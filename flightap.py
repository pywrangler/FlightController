import subprocess
import sys

stopAP = subprocess.Popen([ "systemctl stop create_ap"], stdout=subprocess.PIPE, shell=True)
print "Attemting to terminate AP",stopAP.stdout.read()
if (stopAP.stderr):
    print "Cannot terminate AP error",stopAP.stderr.read()

if(raw_input("Continue y/n")=="n"):
    sys.exit()

proc = subprocess.Popen([ "sudo create_ap -n wlxc4e9840ce06f controlServ darksector"], stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
print "AP status :", proc.stdout.read()
if (proc.stderr):
    print "AP error",proc.stderr.read()

print "Wireless AP maybe created"
if(raw_input("Exit y/n")=="n"):
    sys.exit()

