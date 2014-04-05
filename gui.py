import Tkinter as tk
import tkSimpleDialog
from tkFileDialog import askopenfilename
import socket
import os
import subprocess
from threading import Thread
import client
import platform
this_os = platform.system()
if( "Linux" in this_os):
  vlc_path="/usr/bin/vlc"
elif( "Windows" in this_os):
  vlc_path = "vlc.exe"
  vlc_extra_path=u"C:\Program Files (x86)\VideoLAN\VLC"
  print vlc_extra_path
else:
  print "UNKNOWN OS"
  exit(0)

#correct_cmd = "vlc screen:// :screen-fps=30 :screen-caching=100 --sout '#transcode{vcodec=mp4v, acodec=ogg}:standard{access=http,mux=ogg,dst=127.0.0.1:8080}'"


class xpwn(tk.Frame):
  def __init__(self, parent):
    #TODO set debug to 0
    self.debug = 1
    tk.Frame.__init__(self, parent)

    print socket.gethostbyname(socket.gethostname())
    print [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
    
    self.parent = parent
    #TODO scan for or prompt for this
    self.dst_ip = "192.168.1.10:8080"
    #TODO automatically get this
    self.myip = "127.0.0.1:8080"
    self.vlcport = 8080
    self.initialize()

  def initialize(self):
    self.connected =0
    self.state = 0
    #TODO connect
#    try:
#      self.client = client.Client(self.dst_ip.split(":")[0],\
#          int(self.dst_ip.split(":")[1]))
#      self.connected = 1
#    except socket.error:
#      print "connection failed"

    if self.connected == 1:
      self.client.handshake(self.vlcport)
      print self.client.socket.getsockname()[0]

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
 
  ####################
  # set the ip of the server; resets connection
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
      check = self.client.handshake(self.vlcport)
      if check == 1:
        self.status_var.set("Connect handshake failed")
        self.connected = 0
      else:
        self.status_var.set("Connected, Idle")
        print self.client.socket.getsockname()[0]

  ###########################
  # sends message to server to stream video from the internet
  def streamWeb(self):
    if self.debug==0:
      if self.state==1:
        print "can't stream!  stream already in progress"
        return
      if self.connected == 0:
        print "can't stream!  connection not established"
        return
    self.state == 1
    url = tkSimpleDialog.askstring("Stream Website", "Url:")
    if(url == ""):
      print "Oops emty url"
      self.state = 0
      return
    video_id = url.split("=")[1].split("&")[0]
    print "Sending url " + url + ", Youtube video " + video_id
    self.client.youtube_stream(url.split("=")[-1])
    #TODO: figure out state, video finishing
 
  ###################################
  # stream video from local file
  def streamFile(self):
    if self.debug==0:
      if self.state==1:
        print "can't stream!  stream already in progress"
        return
      if self.connected == 0:
        print "can't stream!  connection not established"
        return
    filename = askopenfilename()
    if filename==None or filename=="":
      "No filename..."
      return
    print "File selected: " + str(filename)
    self.state = 1
    
    # Popen
    self.exPopenFile(filename)
    return

    #TODO clean
    # os.system
    cmd = vlc_path + " -vvv \"" + filename + "\" --sout=\"#standard{access=http,mux=ogg,dst=" + \
        str(self.myip) + "}\""
    self.exOsSys(cmd,"File")
  
  ####################################
  # stream desktop image
  def streamDesk(self):
    if self.debug==0:
      if self.state==1:
        print "can't stream!  stream already in progress"
        return
      if self.connected == 0:
        print "can't stream!  connection not established"
        return
    self.state = 1
    cmd = vlc_path
    cmd += u" screen:// " 
    cmd += u":screen-fps=30 " 
    cmd += u":screen-caching=100 "
    cmd += u"--sout=\"#transcode{vcodec=mpv4, acodec=ogg}:standard{access=http,mux=ogg,dst="
    cmd += self.myip
    cmd += u"}\""
    # Popen for windows, os.system for linux??
    if("Windows" in this_os):
      self.exPopenDesk()
      return
    else:
      self.exPopenDesk()
      #self.exOsSys(cmd,"Desktop")
    return

  ######################################
  # uses Popen for desktop streaming
  def exPopenDesk(self):
    print "EXECUTING SUBPROCESS.POPEN (desk)"
    array = []
    array.append(vlc_path)
    array.append("screen://")
    array.append(":screen-fps=30")
    array.append(":screen-caching=100")
    array.append("--sout=\"#transcode{vcodec=mp4v, acodec=ogg}:standard{access=http,mux=ogg,dst=127.0.0.1:8080}\"")
    print array
    if("Windows" in this_os):
      os.chdir(vlc_extra_path)
      p = subprocess.Popen(array)
    else:
      p = subprocess.Popen(array)
    print p

  ############################################
  # uses Popen for file streaming
  def exPopenFile(self, fname):
    print "EXECUTING SUBPROCESS.POPEN (file)"
    array = []
    array.append(vlc_path)
    array.append("-vvv")
    array.append(fname)
    array.append("--sout=\"#standard{access=http,mux=ogg,dst=127.0.0.1:8080}\"")
    print array
    if("Windows" in this_os):
      os.chdir(vlc_extra_path)
      p = subprocess.Popen(array, executable=vlc_extra_path)
    else:
      p = subprocess.Popen(array)
    print p

  #########################################
  # uses os.system to execute cmd
  def exOsSys(self, cmd, service):
    print "EXECUTING OS.SYS"
    print cmd
    thread = Thread(target=self.threadEx, args=(cmd, ))
    thread.start()
    if self.debug==0:
      self.client.stream()
    self.status_var.set("Streaming " + service + " (os)")
  #### thread helper for os.system execution
  def threadEx(self, cmd):
    os.system(cmd)
    self.status_var.set("Status: Idle")
    self.state = 0
    print "os.system returned; stending stop to client"
    if self.debug==0:
      self.client.stop()

  ##########
  # exit app
  def exit(self):
    if self.connected == 1:
      self.client.quit()
    exit(0)

if __name__ == "__main__":
  top = tk.Tk()
  top.wm_title("X_Pwn")
  app = xpwn(top)
  top.mainloop()
