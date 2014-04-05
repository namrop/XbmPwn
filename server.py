#client example
import socket
from default import vlc_connect, youtube_connect

class Server:

  def __init__(self, address, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((address, port))
    self.socket.listen(1)
    self.connected = 0
    while(True):
      self.accept()
      self.handshake()
      self.loop()

  def accept(self):
    self.conn, self.conn_addr = self.socket.accept()

  def handshake(self):
    data = self.conn.recv(512)
    self.port = data.split()[1]
    self.conn.send("ACK %d" % self.port)
    self.connected = 1

  def loop(self):
    while(self.connected):
      data = self.conn.recv(512)
      if data[0] == "q": self.connected = 0
      elif data[0] == "s": self.stream()
      elif data[0] == "e": self.end_stream()
    self.port = 0
    self.conn.close()
    self.conn_addr = None
    self.conn = None

  def stream(self):
    vlc_connect((self.conn_addr, self.port))
