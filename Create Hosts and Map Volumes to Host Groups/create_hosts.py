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


# Verify Array name is correct with the IP address. Just double checking.
################################################################################

try:
    array1 = purestorage.FlashArray(IP1, api_token=token1)

except: 
    print ("Issue connecting with Array: % " % IP)
    raise

    
info1 = array1.get() 
if (info1["array_name"] != ArrayName1):
    print "There is some mis-configuration because array name does not match"
    raise
    
try:
    array2 = purestorage.FlashArray(IP2, api_token=token2)

except: 
    print ("Issue connecting with Array: % " % IP)
    raise
    
    
info2 = array2.get() 
if (info2["array_name"] != ArrayName2):
    print "There is some mis-configuration because array name does not match"
    raise

    
# Create the hosts in each of the arrays
################################################################################

if HostNames is not None:   # we have a list of hosts to be connected
    for host in HostNames["hostlist"]:
        wwnlist_host = WWN[host]
                
        try:
            h_info = array1.create_host(host, **wwnlist_host)
            print ("Adding Host: %s to Array: %s" % (host, ArrayName1))
            h_info = array1.set_host(host, **HostAttributes) 
            print ("Setting Attributre: %s on Host: %s and Array: %s" % (HostAttributes["personality"], host, ArrayName1))            
                                     
        except:
            print ("Issue adding host %s at array %s" % (host, ArrayName1))
            raise
     
        try:
            h_info = array2.create_host(host, **wwnlist_host)
            print ("Adding Host: %s to Array: %s" % (host, ArrayName2))
            h_info = array2.set_host(host, **HostAttributes) 
            print ("Setting Attributre: %s on Host: %s and Array: %s" % (HostAttributes["personality"], host, ArrayName2))            

        except:
            print ("Issue adding host %s at array %s" % (host, ArrayName2))
            raise

            
# Create the host group in each array
################################################################################

try:
    hgroup = array1.create_hgroup(HostGroupName, **HostNames)
    print ("Host Group: %s created in Array: %s" % (HostGroupName, ArrayName1))
except:
    print ("Issue creating Host Group %s in Array %s" % (HostGroupName, ArrayName1))
    raise
 
try:
    hgroup = array2.create_hgroup(HostGroupName, **HostNames)
    print ("Host Group: %s created in Array: %s" % (HostGroupName, ArrayName2))
except:
    print ("Issue creating Host Group %s in Array %s" % (HostGroupName, ArrayName2))
    raise

