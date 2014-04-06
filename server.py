#client examplue
# import the XBMC libraries so we can use the controls and functions of XBMC
import socket
import xbmc, xbmcgui
import xbmcaddon
import xbmcvfs
import lib.common

from lib.utils import log
from lib.settings import get


class Server:

  def __init__(self, address, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((address, port))
    self.socket.listen(1)
    self.socket.settimeout(0)
    self.connected = 0
    self.conn = None
 
  def start(self):
    print "XPWN start"
    while(True):
      try:
        self.accept()
        print "XPWN: sockname: " + str(self.socket.getsockname())
        self.handshake()
        self.loop()
      except  socket.error: pass
      self.port = 0
      if self.conn:
        self.conn.close()
      self.conn_addr = None
      self.conn = None

  def accept(self):
    #print "XPWN accept"
    self.conn, self.conn_addr = self.socket.accept()

  def handshake(self):
    print "XPWN handshake"
    try:
      data = self.conn.recv(512)
      print "XPWN: " + str(data)
      self.port = int(data.split()[1])
      self.conn.send("XPWN: ACK ")#%d" % self.port)
      self.connected = 1
    except  socket.error, TypeError:
      print "XPWN: handshake error, closing connection"
      self.conn.close()

  def loop(self):
    print "XPWN loop"
    self.conn.settimeout(200)
    while(self.connected):
      try:
        #TODO: might cause an infinite loop
        data = self.conn.recv(512)
      except  socket.error: continue
      if len(data) == 0:
        print "XPWN DATA len 0 and error not caught"
        return
      print "XPWN Data: " + data
      switch = data[0]
      if switch == "q": self.connected = 0
      elif switch == "s": self.stream()
      elif switch == "e": self.stop()
      elif switch == "p": self.play() 
      elif switch == "y": self.youtube_connect(data[1:]) 

  def stream(self):
    print "XPWN stream"
    self.vlc_connect(self.conn_addr, self.port)

  def vlc_connect(self, address, port):
    print "XPWN vlc_connect"
    command = 'XBMC.PlayMedia(udp://' + str(address[0]) + ':' + str(port) + ')'
    print command
    xbmc.executebuiltin(command)

  def youtube_connect(self, vid):
    print "XPWN youtube_connect"
    command = 'XBMC.PlayMedia(plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + vid + ')'
    xbmc.executebuiltin(command)

  def stop(self):
    print "XPWN stop"
    command = "XBMC.PlayerControl(self, Stop)"
    xbmc.executebuiltin(command)

  def play(self):
    print "XPWN play"
    command = "XBMC.PlayerControl(self, Play)"
    xbmc.executebuiltin(command)
    
