# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import re, os
from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from .const import *
from .utils import *


class Effects():
    themeName=None

    def __init__(self, type, setting):
        self.type=type
        self.setting=setting
        self.onThemeChange()
        addHook("Fanfare.settingsChanged", self.onThemeChange)

    def onThemeChange(self):
        self.themeName=self.setting.config['theme']
        self.ADIR=self.setting.getPathOf(self.type, abs=True)
        self.RDIR=self.setting.getPathOf(self.type, abs=False)
        JSONPAIRS=self.setting.theme['pairs_fname']

        re_image=self.setting.getMediaRegex('image')
        re_media=self.setting.getMediaRegex(self.type)
        self.arr_images=[i for i in os.listdir(self.ADIR) if re_image.search(i)]
        self.arr_sounds=[i for i in os.listdir(self.ADIR) if re_media.search(i)]
        self.dict_pairs=readJson(os.path.join(self.ADIR,JSONPAIRS))

        # index, filename, fullpath
        self.image=(-1,'','')
        self.sound=(-1,'','')


    def set(self):
        self.setImage()
        key=None if not self.image else self.image[1]
        self.setAudio(key)

    def setImage(self):
        idx=-1 if not self.image else self.image[0]
        self.image=getMedia(idx,self.RDIR,self.arr_images)

    def setAudio(self, k):
        if k and self.dict_pairs and k in self.dict_pairs:
            p=os.path.join(self.ADIR,self.dict_pairs[k])
            self.sound=(-1,self.dict_pairs[k],p)
        else:
            idx=-1 if not self.sound else self.sound[0]
            self.sound=getMedia(idx,self.ADIR,self.arr_sounds)


    def get(self):
        return (self.getImage(), self.getAudio())

    def getIndexes(self):
        i=s=-1
        if self.image: i=self.image[0] #path
        if self.sound: s=self.sound[0] #path
        return (i,s)

    def getImage(self):
        if self.image: return self.image[2] #path

    def getAudio(self):
        if self.sound: return self.sound[2] #path

