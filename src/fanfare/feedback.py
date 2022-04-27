# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from anki.utils import json
from anki.hooks import addHook
from anki.sound import clearAudioQueue
import random, os
from .const import *
from .utils import *
from .audFeedback import *
from .vsFeedback import *
from .effect import *

class Feedback():
    audio_duration=0
    failCnt=-1
    revCount=0

    def __init__(self, settings):
        self.settings=settings
        self.ch_image=VsFeedback21(settings)
        self.ch_audio=AudFeedback(settings)

        self.lapseFx=Effects('lapse', settings)
        self.passFx=Effects('pass', settings)
        self.startFx=Effects('start', settings) #start from overview
        self.reloadFx=Effects('reload', settings) #exit intermission


    def activate(self, lapsed):
        freq=self.settings.config['fx_repetition_frequency']
        self.revCount+=1

        if lapsed:
            self.failCnt+=1
            if self.revCount%freq!=0: return 0
            if self.failCnt>self.settings.config['multilapse_limit']:
                neuImg=self.settings.neutral_img
                self.ch_image.show(neuImg)
                return self.settings.theme['duration_meh']
            fx=self.lapseFx
        else:
            self.failCnt=0
            if self.revCount%freq!=0: return 0
            fx=self.passFx

        dmin=self.settings.theme['duration_min']
        dmax=self.settings.theme['duration_max']
        dur=self._play(fx,dmin)
        return min(dmax,max(dmin,dur-200))

#--------------------------------
    def reloadDeck(self):
        self.ch_image.hideOverview()
        dmin=self.settings.theme['duration_reload_min']
        dmax=self.settings.theme['duration_reload_max']
        dur=self._play(self.reloadFx,dmin)
        return min(dmax,dur)

    def startDeck(self):
        self.ch_image.hideOverview()
        dmin=self.settings.theme['duration_start_min']
        dmax=self.settings.theme['duration_start_max']
        dur=self._play(self.startFx,dmin)
        return min(dmax,dur)
#--------------------------------

    def _play(self, fx, dur=0):
        clearAudioQueue()
        fx.set()
        img,au=fx.get()
        if img: self.ch_image.show(img)
        if au:
            dur=self.ch_audio.play(au)
        self.audio_duration=dur
        return dur

    def stop(self):
        self.ch_image.close()

