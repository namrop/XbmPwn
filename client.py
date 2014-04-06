#client example
import socket
class Client:

  def __init__(self, dest, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((dest, port))
    print "client init " + dest + " " + str(port)
    self.shook = 0

  def handshake(self, port):
    try:
      self.socket.send("X_pwn %d" % port)
      self.stream_port = port
      data = self.socket.recv(512)
      data.split()
      print data
      print "CLient handshake success"
      self.shook = 1
      return 0
    except socket.error:
      print "Handshake error, exiting"
      self.socket.close()
      #assert int(data[1]) == port
      return 1

  def stream(self):
    if self.shook ==0:
      print "Client called stream before handshake"
      return
    print "Client stream()"
    self.socket.send("s")

  def youtube_stream(self, vid):
    if self.shook ==0:
      print "Client called youtube_stream before handshake"
      return
    print "Client youtube_stream()"
    self.socket.send("y" + vid)

  def stop(self):
    if self.shook ==0:
      print "Client called stop before handshake"
      return
    print "Client stop()"
    self.socket.send("e")

  def play(self):
    if self.shook ==0:
      print "Client called play before handshake"
      return
    print "Client play()"
    self.socket.send("p")

  def quit(self):
    if self.shook ==0:
      print "Client called quit before handshake"
      return
    print "Client quit()"
    try:
      self.socket.send("q")
    except:
      print "COULDN'T SEND QUIT"
    self.socket.close()
    self.shook = 0
