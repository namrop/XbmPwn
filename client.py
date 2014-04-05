#client example
import socket
class Client:

  def __init__(self, dest, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((dest, port))

  def handshake(self, port):
    self.socket.send("X_pwn %d" % port)
    self.stream_port = port
    data = self.socket.recv(512)
    data.split()
    print data
    #assert int(data[1]) == port

  def stream(self):
    self.socket.send("s")

  def end_stream(self):
    self.socket.send("e")

  def quit(self):
    self.socket.send("q")
    self.socket.close()
