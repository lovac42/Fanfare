# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


import anki
import wave, contextlib
import threading, time
from anki.sound import clearAudioQueue
from .lib.playsound import *
from .const import *


class FxWavPlayer(threading.Thread):
    def run(self):
        playsound(self.getName())

    def play(self, mplayer=False):
        if mplayer:
            anki.sound.play(self.getName())
        else:
            self.start()

    def getDuration(self):
        w=wave.open(self.getName(),'r')
        with contextlib.closing(w) as f:
            frames=f.getnframes()
            rate=f.getframerate()
            return int(frames/float(rate)*1000)
