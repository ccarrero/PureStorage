HostAttributes = {}
HostAttributes["personality"] = 'esxi'

HostGroupName = 'CLUSTERCC5'

#Define here the host names that belong to the host group
HostNames = {}
HostNames["hostlist"] = ['CChost5a','CChost5b']

#Now insert the wwwn for each host
WWN = {"CChost5a" : {"wwnlist" : ["91:42:33:44:55:66:77:85", "92:43:44:55:66:77:88:95"]},
       "CChost5b" : {"wwnlist" : ["9A:42:33:44:55:66:77:85", "9B:43:44:55:66:77:88:95"]}
      }


Pod = 'jspod'

LUNS_to_provision=['30G','45G']


