import Tkinter as tk
import tkSimpleDialog
from tkFileDialog import askopenfilename
import socket
import os
import subprocess
from threading import Thread
import client

vlc_path=u"vlc"
#correct_cmd = "vlc screen:// :screen-fps=30 :screen-caching=100 --sout '#transcode{vcodec=mp4v, acodec=ogg}:standard{access=http,mux=ogg,dst=127.0.0.1:8080}'"


class xpwn(tk.Frame):
  def __init__(self, parent):
    tk.Frame.__init__(self, parent)

    
    self.parent = parent
    #TODO scan for or prompt for this
    self.dst_ip = "10.1.42.71:8081"
    #TODO automatically get this
    self.myip = "10.0.2.15:8081"
    self.vlcport = 8080
    self.initialize()

  def initialize(self):
    self.connected =0
    self.state = 0
    #TODO connect
    try:
      self.client = client.Client(self.dst_ip.split(":")[0],\
          int(self.dst_ip.split(":")[1]))
      self.connected = 1
    except socket.error:
      print "connection failed"

    if self.connected == 1:
      self.client.handshake(self.vlcport)
    self.grid()

    px = 5
    py = 4

    self.title = tk.Label(self, text='X_Pwn', font=40)
    self.title.grid(column=0, row=0, columnspan=5, stick="EW", padx=px, pady=py)
    
    self.ip_txt = tk.Label(self, text="R-Pi IP: ", font=20)
    self.ip_txt.grid(column=0, row=2, stick="EW", padx=px, pady=py)

    self.ip_str_var = tk.StringVar()
    self.ip_str_var.set(self.dst_ip)
    self.ip_entr = tk.Entry(self, textvariable=self.ip_str_var, font=20)
    self.ip_entr.grid(column=1, row=2, stick="EW", padx=px, pady=py)
   
    self.ip_but = tk.Button(self, text="Set IP", command=self.setIP, font=20)
    self.ip_but.grid(column=2, row=2, stick="EW", padx=px, pady=py)

    self.stream_file = tk.Button(self, text="Stream File", command=self.streamFile, font=20)
    self.stream_file.grid(column=1, row=3, columnspan=3, stick="EW", padx=px, pady=py)

    self.stream_desk = tk.Button(self, text="Stream Desktop", command=self.streamDesk, font=20)
    self.stream_desk.grid(column=1, row=4, columnspan=3, stick="EW", padx=px, pady=py)

    self.stream_web = tk.Button(self, text="Stream Web", command=self.streamWeb, font=20)
    self.stream_web.grid(column=1, row=5, columnspan=3, stick="EW", padx=px, pady=py)

    self.exit = tk.Button(self, text="Exit", command=self.exit, font=20)
    self.exit.grid(column=1, row=6, columnspan=3, stick="EW", padx=px, pady=py)

    self.status_var = tk.StringVar()
    if self.connected == 1:
      self.status_var.set("Status: Connected, Idle")
    elif self.connected == 0:
      self.status_var.set("Status: Not Connected")
    self.status = tk.Label(self, textvariable=self.status_var, font=12)
    self.status.grid(column=0, row=7, columnspan=3, stick="EW", padx=px, pady=py)

    self.cancel_but = tk.Button(self, text="Cancel")
    self.cancel_but.grid(column=3, row=7, padx=px, pady=py)


    self.pack()
  
  def setIP(self):
    if self.state == 1:
      print "Couldn't disconnect: stream in progress"
      return
    self.dst_ip = self.ip_entr.get()
    print self.dst_ip
    if self.connected == 0:
      try:
        self.client = client.Client(self.dst_ip.split(":")[0], \
            int(self.dst_ip.split(":")[1]))
        self.connected = 1
      except socket.error:
        print "connection failed"
    elif self.connected == 1:
      self.client.quit()
      try:
        self.client = client.Client(self.dst_ip.split(":")[0], \
            int(self.dst_ip.split(":")[1]))
        self.connected = 1
      except socket.error:
        print "connection failed"
        self.connected = 0
    if self.connected == 0:
      self.status_var.set("Disconnected")
    else:
      self.status_var.set("Connected, Idle")
  
  def streamFile(self):
    if self.state==1:
      return
    filename = askopenfilename()
    if filename==None or filename=="":
      return
    print filename
    self.state = 1
    print "File: " + str(filename)
    cmd = vlc_path + " -vvv '" + filename + "' --sout=\"#standard{access=http,mux=ogg,dst=" + \
        str(self.myip) + "}\""
    print "Command: " + str(cmd)
    thread = Thread(target=self.threadExx, args=(cmd, ))
    thread.start()
    client.stream()
    self.status_var.set("Streaming File...")
  def streamDesk(self):
    if self.state==1:
      return
    self.state = 1
    cmd = vlc_path + u" screen:// " + u":screen-fps=30 " + u":screen-caching=100 " + \
        u"--sout '#transcode{vcodec=mpv4, acodec=ogg}:standard{access=http,mux=ogg,dst=" + self.myip + \
    u"}'"
    print cmd
    thread = Thread(target=self.threadEx, args=(cmd, ))
    thread.start()
    client.stream()
    self.status_var.set("Streaming Desktop...")
  def threadEx(self, cmd):
    os.system(cmd)
    self.status_var.set("Status: Idle")
    self.state = 0
    client.stop()
  def streamWeb(self):
    if self.state == 1:
      return
    self.state == 1
    url = tkSimpleDialog.askstring("Stream Website", "Url:")
    if(url == ""):
      self.state = 0
      return
    client.youtube_stream(url.split("=")[-1])
  def exit(self):
    exit(0)

if __name__ == "__main__":
  top = tk.Tk()
  top.wm_title("X_Pwn")
  app = xpwn(top)
  top.mainloop()
