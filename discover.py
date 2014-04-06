import os
import socket

def find_ip_linux():
  import netifaces  
  for iface in netifaces.interfaces():
    if iface == 'lo': continue
    addrs = netifaces.ifaddresses(iface)
    if 2 in addrs: 
      ip = addrs[2][0]['addr']
      print ip
      return ip

find_ip_linux()

def discover_servers():

  UDP_IP = "<broadcast>"
  UDP_PORT = 5005
  MESSAGE = "XbmPwn client"

  print "UDP target IP:", UDP_IP
  print "UDP target port:", UDP_PORT
  print "message:", MESSAGE

  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  sock.bind(('', UDP_PORT))
  sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

  
