# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from anki.sound import clearAudioQueue
from anki.utils import isWin
import random, os, anki
from .const import *
from .utils import *
from .sound import FxWavPlayer


class AudFeedback():

    def __init__(self, settings):
        self.settings=settings

    def play(self, path):
        if not self.settings.isPlayAudio(): return 0
        mp=self.settings.useMPlayer()
        fx=FxWavPlayer(name=path)
        fx.play(mp)
        return fx.getDuration()
