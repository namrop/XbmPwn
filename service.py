# modules
import os
import time
import xbmc
import xbmcaddon
import xbmcvfs
import lib.common
from discover import find_ip_linux

#import libraries
from lib.settings import get
from lib.utils import log
import server


def autostart():
  print "autostart working"
  s = server.Server(find_ip_linux(), 8081)
  s.start()

if (__name__ == "__main__"):
  try:
    autostart()
  except:
    print "XPWN: Autostart failed, retarting"
    print "just kidding"
    #xbmc.executebuiltin("XBMC.RestartApp()")
