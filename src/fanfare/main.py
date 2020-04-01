# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from anki.hooks import wrap
import os, anki
import anki.sched
from .const import *
from .fanfare import *

from .lib.com.lovac42.anki.version import ANKI21, CCBC


fan=Fanfare()


##################################################
# Monkey Patches - adds delay for animation smoothness
#################################################


#Need to block this from calling nextCard()
#giving a brief pause for transition effects.
Reviewer._answerCard = wrap(Reviewer._answerCard, fan.affirm, "around")
Reviewer.nextCard = wrap(Reviewer.nextCard, fan.delayNextCard, "around")
Reviewer.autoplay = wrap(Reviewer.autoplay, fan.autoplayOnQ, "around")


#Rewards
anki.sched.Scheduler.finishedMsg = wrap(anki.sched.Scheduler.finishedMsg, fan.rewards, 'around')
if ANKI21 or CCBC:
    import anki.schedv2
    anki.schedv2.Scheduler.finishedMsg = wrap(anki.schedv2.Scheduler.finishedMsg, fan.rewards, 'around')

if ANKI21:
    #Disables keys during fx
    Reviewer.onEnterKey = wrap(Reviewer.onEnterKey, fan.onEnterKey, "around")
else:
    Reviewer._keyHandler = wrap(Reviewer._keyHandler, fan.keyHandler, "around")
    Reviewer._linkHandler = wrap(Reviewer._linkHandler, fan.linkHandler, "around")


################################################################
# Monkey Patches - bypass file:/// access on Anki 2.1's webview
################################################################

# Replace /user/collection.media folder with actual addon path
def _redirectWebExports(self, path, _old):
    targetPath=os.path.join(os.getcwd(),ADDON_TAG)
    if path.startswith(targetPath):
        targetLength=len(targetPath)+1
        return os.path.join(ADDON_FOLDER,path[targetLength:])
    return _old(self,path)

if ANKI21:
    from aqt.mediasrv import RequestHandler
    RequestHandler._redirectWebExports = wrap(RequestHandler._redirectWebExports, _redirectWebExports, 'around')
