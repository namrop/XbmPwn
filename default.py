# import the XBMC libraries so we can use the controls and functions of XBMC
import xbmc, xbmcgui
import xbmcaddon
import xbmcvfs
import lib.common

from lib.utils import log
from lib.settings import get

setting = get()

log('##super test swinging it\'s dick')
print "hello world"
xbmc.executebuiltin('XBMC.PlayMedia(plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=eDegcHZFOQI)')
