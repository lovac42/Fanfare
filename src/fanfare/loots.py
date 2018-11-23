# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from anki.sound import clearAudioQueue, play
from anki.utils import json
import random, os, re
from .const import *
from .utils import *
from .effect import Effects


class Loots(Effects):
    timer=None

    def __init__(self, type, setting):
        Effects.__init__(self, type, setting)

    def onThemeChange(self):
        Effects.onThemeChange(self)
        if self.timer: self.timer.stop()
        self.seen=[]
        self.heard=[]

    def stop(self):
        clearAudioQueue()

    def start(self, delay=0):
        if self.timer: self.timer.stop()
        self.timer=mw.progress.timer(delay+200,self.replay,False)

    def replay(self):
        au=self.getAudio()
        if au:
            self.clear()
            play(au)

    def clear(self):
        if self.timer: self.timer.stop()
        clearAudioQueue()

    def setUniqueMedia(self):
        self.set()
        i,a=self.getIndexes()

        ILEN=len(self.arr_images)
        SLEN=len(self.arr_sounds)
        if len(self.seen) > ILEN//1.5:
            self.seen=[]
        if len(self.heard) > SLEN//1.5:
            self.heard=[]

        while ILEN and i in self.seen:
            self.set()
            i,a=self.getIndexes()
        while SLEN and a in self.heard:
            self.set()
            i,a=self.getIndexes()

        self.seen.append(i)
        self.heard.append(a)
        return (i,a)



class Reward(Loots):
    def onThemeChange(self):
        Loots.onThemeChange(self)
        self.decksPic={}
        self.decksMov={}

    def getAudio(self):
        return self.audio

    def getLoots(self, did):
        i=a=-1 #indexes
        if did in self.decksPic:
            i=self.decksPic[did]
        if did in self.decksMov:
            a=self.decksMov[did]
        if i<0 or a<0:
            i,a=self.setUniqueMedia()

        self.decksPic[did]=i
        img=os.path.join(self.RDIR,self.arr_images[i])

        self.decksMov[did]=a
        self.audio= os.path.join(self.ADIR,self.arr_sounds[a])
        return img



class Intermission(Loots):
    def _linkHandler(self, url):
        if url=='refresh':
            mw.delayedMaybeReset()
        elif url=='replay':
            self.replay()

    def stop(self):
        mw.web.eval("$('#intermission').css('display','')")

    def start(self, delay=0):
        mw.requireReset(True)
        if ANKI21:
            mw.web.resetHandlers()
            mw.web.onBridgeCmd = lambda url: self._linkHandler(url)
            cmd='pycmd'
        else:
            mw.web.setLinkHandler(lambda url: self._linkHandler(url))
            cmd='py.link'

        self.setUniqueMedia()
        img,au=self.get()
        Loots.start(self, delay)
        msg='<br><i>( Click Image To Replay )</i>' if au else ''

        html="""<div id="intermission" style="display:none;">
<center><table><tr><td><h1>Intermission 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h1></td>
<td valign="bottom"><button id="resume" class="but " 
onclick="%s('refresh');return false;" autofocus>
Resume Now</button></td></tr></table><br><br>
<img src="%s" style="max-width:100%%" 
onclick="%s('replay');return false;" />
%s</center></div>"""%(cmd,img,cmd,msg)

        mw.web.stdHtml(html, css='' if ANKI21 else mw.sharedCSS)
        # mw.bottomWeb.hide()
        mw.web.setFocus()
