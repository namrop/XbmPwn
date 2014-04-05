import Tkinter as tk
from tkFileDialog import askopenfilename
import socket
import os
import subprocess

vlc_path="vlc"

class xpwn(tk.Frame):
  def __init__(self, parent):
    tk.Frame.__init__(self, parent)
    self.parent = parent
    self.initialize()
    #TODO set dst_ip correctly
    self.dst_ip = "127.0.0.1:8080"

    #TODO connect

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
    self.ip = self.ip_entr.get()
    print self.ip
  def streamFile(self):
    filename = askopenfilename()
    if filename==None:
      return
    print "File: " + str(filename)
    cmd = vlc_path + " -vvv '" + filename + "' --sout=\"#standard{access=http,mux=ogg,dst=" + \
        str(self.dst_ip) + "}\""
    print "Command: " + str(cmd)
    os.system(cmd)
    #self.status_var.set("Status: streaming " + filename.split("/")[-1])
  def streamDesk(self):
    cmd = vlc_path + " screen:// " + ":screen-fps=30 " + ":screen-caching=100 " + \
    "--sout=\"#standard{access=http,mux=ogg,dst=" + str(self.dst_ip) + \
    "}:transcode{vcodec=mpv4,acodec=ogg}\""
    print "Command: " + str(cmd)
    print "List: " + str(cmd.split())
    subprocess.call(cmd.split())
    subprocess.Popen(cmd.split())
  def streamWeb(self):
    pass
  def exit(self):
    exit(0)

if __name__ == "__main__":
  top = tk.Tk()
  top.wm_title("X_Pwn")
  app = xpwn(top)
  top.mainloop()
