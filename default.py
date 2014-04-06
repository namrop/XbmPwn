# import the XBMC libraries so we can use the controls and functions of XBMC
import xbmc, xbmcgui
import xbmcaddon
import xbmcvfs
import lib.common

from lib.utils import log
from lib.settings import get

def vlc_connect((address, port)):
  command = 'XBMC.PlayMedia(http://' + str(address[0]) + ':' + str(port) + ')'
  print command
  xbmc.executebuiltin(command)

def youtube_connect(vid):
  command = 'XBMC.PlayMedia(plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + vid + ')'
  xbmc.executebuiltin(command)
