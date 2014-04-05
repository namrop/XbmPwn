# modules
import os
import time
import xbmc
import xbmcaddon
import xbmcvfs
import lib.common

#import libraries
from lib.settings import get
from lib.utils import log
import server


def autostart():
  print "autostart working"
  s = server.Server("localhost", 5051)
  s.start()

if (__name__ == "__main__"):

  autostart()
