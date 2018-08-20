#!/usr/bin/python

import purestorage

import urllib3
# We're using a version that warns us about insecure requests, and we don't want to see that noise.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

################################################################################
################## MODIFY THIS WITH YOUR OWN DEFINITIONS #######################
################################################################################

from Cluster_UK import *
from definitions_UK import *

################################################################################

# Verify Array name is correct with the IP address
################################################################################

try:
    array1 = purestorage.FlashArray(IP1, api_token=token1)

except: 
    print ("Issue connecting with Array: % " % IP)
    raise

    
info1 = array1.get() 
if (info1["array_name"] != ArrayName1):
    print "There is some mis-configuration because array name1 does not match"
    raise
    
try:
    array2 = purestorage.FlashArray(IP2, api_token=token2)

except: 
    print ("Issue connecting with Array: % " % IP)
    raise
    
    
info2 = array2.get() 
if (info2["array_name"] != ArrayName2):
    print "There is some mis-configuration because array name2 does not match"
    raise

    
# If we have a list of hosts to connect the volume, lets make sure they exists
################################################################################

for host in HostNames["hostlist"]:
    print ("Checking that host %s is already defined within each array" % (host))
    
    try:
        h_info = array1.get_host(host)
    except:
        print ("Host: %s does not exists on Array %s. Create it first and execute again" % (host, ArrayName1))
        exit()
     
    try:
        h_info = array2.get_host(host)
    except:
        print ("Host: %s does not exists on Array %s. Create it first and execute again" % (host, ArrayName2))
        exit()
        
    
#Lets make sure we have enough capacity in the Array
################################################################################

array_info1 = array1.get(space="true")
for info in array_info1:
    capacity = info["capacity"]/1024/1024/1024
    total = (info["total"]/1024/1024/1024)
    utilization = float(100*total/capacity)
    print ("Array: %s" % (ArrayName1))
    print ("Total Capacity: %d GiB, Total Used: %d GiB" % (capacity, total))
    print ("Percentage capacity used: %d percent" % (utilization))

    
if utilization > threshold:
        print ("Space utilization is %d, make sure you have enough space before creating volumes" % utilization)
        print ("Volume not created")
        exit()
          

array_info2 = array2.get(space="true")
for info in array_info2:
    capacity = info["capacity"]/1024/1024/1024
    total = (info["total"]/1024/1024/1024)
    utilization = float(100*total/capacity)
    print ("Array: %s" % (ArrayName2))
    print ("Total Capacity: %d GiB, Total Used: %d GiB" % (capacity, total))
    print ("Percentage capacity used: %d percent" % (utilization))

if utilization > threshold:
        print ("Space utilization is %d, make sure you have enough space before creating volumes" % utilization)
        print ("Volume not created")
        exit()
          

# Create the volumes from the given list
################################################################################

LUNS_created = []

TempName = Pod + "::" + "Temporal"

for LUN in LUNS_to_provision:
    try:
        newvol = array1.create_volume(TempName, LUN)
    except:
        print "Error while creating the volume"
        raise    
    
    serial = newvol["serial"]
    newname = Pod + "::" + HostGroupName + "-" + serial[-4:]
    
    rename = array1.rename_volume(TempName, newname)
    
    print ("Created new volume: {} of size {}").format(newname, LUN)

    LUNS_created.append(newname)        
            
    
# Connect the Volume to the Hosts
################################################################################


for volume in LUNS_created:

    try:
        array1.connect_hgroup(HostGroupName, volume)
        array2.connect_hgroup(HostGroupName, volume)
        print ("Volume: %s, conected to Host Group: %s from both arrays" % (volume, HostGroupName))
    except:
        print ("There was some issue connecting Host Group: %s, with volume %s. Please check" % (HostGroupName, volume))
        raise
