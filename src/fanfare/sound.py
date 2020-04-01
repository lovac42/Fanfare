# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import anki
import wave, contextlib
import threading, time

from .const import *
from .lib.playsound import PlaysoundException

try:
    from aqt.sound import _player
    import aqt.sound as s
except ImportError:
    import anki.sound as s


class FxWavPlayer(threading.Thread):
    def run(self):
        try: #For missing modules on non-window platforms
            from .lib.playsound import playsound
            playsound(self.getName())
        except ImportError:
            s.play(self.getName())
            print("error using soundFX API, default to mplayer")
        except PlaysoundException:
            s.play(self.getName())
            print("Invalid 8.3 wav filename, default to mplayer")

    def play(self, mplayer=False):
        if mplayer:
            s.play(self.getName())
        else:
            self.start()

    def getDuration(self):
        w=wave.open(self.getName(),'r')
        with contextlib.closing(w) as f:
            frames=f.getnframes()
            rate=f.getframerate()
            return int(frames/float(rate)*1000)
