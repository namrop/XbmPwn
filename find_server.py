from scapy.all import *

import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

host_IP = get_ip_address("wlan0")
DPORT = 5050 # change this

print "Scanning {}/24 : Port {}".format(host_IP, DPORT)

ans, unans = sr1(IP(dst="{}/30".format(host_IP))/TCP(dport=[DPORT],flags="S"), verbose=False)
ans.nsummary( lfilter=lambda (s,r): (r.haslayer(TCP) and (r.getlayer(TCP).flags & 2)) )
return ans
