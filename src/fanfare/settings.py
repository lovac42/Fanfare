# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.2


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook, runHook
from codecs import open
from anki.utils import json
import os
from .utils import *


DEFAULT_THEME_SETTINGS={
    "version":1,
    "delay_loots":500,
    "duration_min":300,
    "duration_max":1200,
    "duration_meh":300,
    "neutral_img":'neutral.png',
    "pairs_fname":"pairs.json",
    "imgfx":{
        "y_offset":-100,
        "x_offset":0
    },
    "dir":{
        "start":"start",
        "lapse":"lapse",
        "pass":"pass",
        "break":"break",
        "reload":"reload",
        "reward":"reward"
    },
    "ext":{
        "image":"\.(?:jpe?g|gif|png|tiff)$",
        "audiofx":"[^_]\.(?:wav)$",
        "media":"\.(?:mp[34]|mkv|mpe?g|Flac|Ape|Ogg|Aac|Wma|Aiff|au|wav)$"
    }
}


class Settings:
    theme=DEFAULT_THEME_SETTINGS
    config=None

    def __init__(self):
        self.setConfigs()
        self.setConfigCB()

    def setConfigCB(self):
        try: #Must be loaded after profile loads, after addonmanger21 loads.
            mw.addonManager.setConfigUpdatedAction(__name__, self.setConfigs) 
        except AttributeError: pass

    def setConfigs(self, config=None):
        if not config:
            try:
                config=mw.addonManager.getConfig(__name__)
            except AttributeError:
                path = os.path.join(MOD_ABS, 'config.json')
                config=readJson(path)
        if config:
            self.config=config
            self.setTheme(config['theme'])
            self.setupFolders()
            runHook("Fanfare.settingsChanged")

    def setTheme(self, t):
        s=os.path.join(MOD_ABS,'user_files',t,'settings.json')
        tdata=readJson(s)
        if tdata:
            self.theme.update(tdata)

    def setupFolders(self):
        self.theme_dir=self.config['theme']
        self.resrc_dir=self.getResourceFolder(False)
        self.abs_path=self.getResourceFolder(True)
        self.neutral_img=os.path.join(self.resrc_dir,self.theme['neutral_img'])

    def getResourceFolder(self, abs=False):
        if ANKI21 and not abs:
            return os.path.join(ADDON_TAG,MOD_DIR,'user_files',self.theme_dir)
        return os.path.join(MOD_ABS,'user_files',self.theme_dir)

    def getPathOf(self, key, abs=False):
        if abs:
            return os.path.join(self.abs_path,self.theme['dir'][key])
        return os.path.join(self.resrc_dir,self.theme['dir'][key])

    def getImageOffset(self, key):
        if key=='x':
            return self.theme['imgfx']['x_offset']
        return self.theme['imgfx']['y_offset']

    def isShowImage(self):
        return self.config["show_visual_fx"]

    def isPlayAudio(self):
        return self.config["play_audio_fx"]

    def useMPlayer(self):
        return self.config["use_mplayer_for_audio"]

    def getMediaRegex(self, type):
        if type=='image':
            t='image'
        elif type=='pass' or type=='lapse':
            t='audiofx'
        else:
            t='media'
        return re.compile(self.theme['ext'][t], re.I)
