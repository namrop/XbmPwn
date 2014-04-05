import Tkinter as tk
from tkFileDialog import askopenfilename
import socket
import os
import subprocess
from threading import Thread

vlc_path=u"vlc"
correct_cmd = "vlc screen:// :screen-fps=30 :screen-caching=100 --sout '#transcode{vcodec=mp4v, acodec=ogg}:standard{access=http,mux=ogg,dst=127.0.0.1:8080}'"


class xpwn(tk.Frame):
  def __init__(self, parent):
    tk.Frame.__init__(self, parent)
    self.parent = parent
    self.initialize()
    #TODO set dst_ip correctly
    self.dst_ip = u"127.0.0.1:8080"

    #TODO connect
    self.state = 0

  def initialize(self):
    self.grid()

    px = 5
    py = 4

    self.title = tk.Label(self, text='X_Pwn', font=40)
    self.title.grid(column=0, row=0, columnspan=3, stick="EW", padx=px, pady=py)
    
    self.ip_txt = tk.Label(self, text="R-Pi IP: ", font=20)
    self.ip_txt.grid(column=0, row=2, stick="EW", padx=px, pady=py)

    self.ip_str_var = tk.StringVar()
    self.ip_str_var.set("192.168.1.1")
    self.ip_entr = tk.Entry(self, textvariable=self.ip_str_var, font=20)
    self.ip_entr.grid(column=1, row=2, stick="EW", padx=px, pady=py)
   
    self.ip_but = tk.Button(self, text="Set IP", command=self.setIP, font=20)
    self.ip_but.grid(column=2, row=2, stick="EW", padx=px, pady=py)

    self.stream_file = tk.Button(self, text="Stream File", command=self.streamFile, font=20)
    self.stream_file.grid(column=0, row=3, columnspan=3, stick="EW", padx=px, pady=py)

    self.stream_desk = tk.Button(self, text="Stream Desktop", command=self.streamDesk, font=20)
    self.stream_desk.grid(column=0, row=4, columnspan=3, stick="EW", padx=px, pady=py)

    self.stream_web = tk.Button(self, text="Stream Web", command=self.streamWeb, font=20)
    self.stream_web.grid(column=0, row=5, columnspan=3, stick="EW", padx=px, pady=py)

    self.exit = tk.Button(self, text="Exit", command=self.exit, font=20)
    self.exit.grid(column=0, row=6, columnspan=3, stick="EW", padx=px, pady=py)

    self.status_var = tk.StringVar()
    self.status_var.set("Status: Connected, Idle")
    self.status = tk.Label(self, textvariable=self.status_var, font=12)
    self.status.grid(column=0, row=7, columnspan=3, stick="EW", padx=px, pady=py)


    self.pack()
  
  def setIP(self):
    if self.state==1:
      return
    self.ip = self.ip_entr.get()
    #TODO connect
    print self.ip
  def streamFile(self):
    if self.state==1:
      return
    filename = askopenfilename()
    if filename==None:
      return
    self.state = 1
    print "File: " + str(filename)
    cmd = vlc_path + " -vvv '" + filename + "' --sout=\"#standard{access=http,mux=ogg,dst=" + \
        str(self.dst_ip) + "}\""
    print "Command: " + str(cmd)
    thread = Thread(target=self.threadExx, args=(cmd, ))
    thread.start()
    self.status_var.set("Streaming File...")
  def streamDesk(self):
    if self.state==1:
      return
    self.state = 1
    cmd = vlc_path + u" screen:// " + u":screen-fps=30 " + u":screen-caching=100 " + \
        u"--sout '#transcode{vcodec=mpv4, acodec=ogg}:standard{access=http,mux=ogg,dst=" + self.dst_ip + \
    u"}'"
    print cmd
    print correct_cmd
    thread = Thread(target=self.threadEx, args=(cmd, ))
    thread.start()
    self.status_var.set("Streaming Desktop...")
  def threadEx(self, cmd):
    os.system(cmd)
    self.status_var.set("Status: Idle")
    self.state = 0
  def streamWeb(self):
    if self.state == 1:
      return
    self.state == 1
    url = tk.tkSimpleDialog.askstring("Stream Website", "Url:")
    if(url == ""):
      self.state = 0
      return
    #TODO send url over socket
  def exit(self):
    exit(0)

if __name__ == "__main__":
  top = tk.Tk()
  top.wm_title("X_Pwn")
  app = xpwn(top)
  top.mainloop()
