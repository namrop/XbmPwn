#client example
import socket
class Client:

  def __init__(self, dest, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((dest, port))

  def handshake(self, port):
    try:
      self.socket.send("X_pwn %d" % port)
      self.stream_port = port
      data = self.socket.recv(512)
      data.split()
      print data
    except socket.error:
      print "Handshake error, exiting"
      self.socket.close()
      #assert int(data[1]) == port

  def stream(self):
    self.socket.send("s")

  def youtube_stream(self, vid):
    self.socket.send("y" + vid)

  def stop(self):
    self.socket.send("e")

  def play(self):
    self.socket.send("p")

  def quit(self):
    try:
      self.socket.send("q")
    except:
      print "COULDN'T SEND QUIT"
    self.socket.close()
