# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import json

from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from anki.hooks import wrap
import os, anki
import anki.sched
from .const import *
from .fanfare import *

from .lib.com.lovac42.anki.version import PATCH_VERSION

from aqt.gui_hooks import webview_did_receive_js_message, overview_did_refresh
from aqt.overview import Overview

fan=Fanfare()

def linkHandler(handled, message, context):
    if message == 'refresh':
        mw.requireReset()
        mw.web.page().runJavaScript("""
document.getElementById("intermission").style.display = 'none';
document.getElementById("qa").style.display = 'block';
""")
        return (True, None)
    elif message == 'replay':
        fan.recess.replay()
        return (True, None)
    else:
        return handled

webview_did_receive_js_message.append(linkHandler)

#Rewards
def showRewards(overview: Overview):
    def on_congrats(in_congrats):
        if in_congrats:
            overview.web.eval("""
            var rewardsHTML = %s;
            document.body.insertAdjacentHTML('beforeend', rewardsHTML);
            """ % json.dumps(fan.getRewards()))
    overview.web.evalWithCallback("""
    (() => {
        var rewardElement = document.getElementById("fanfare-reward");
        if(rewardElement) {
            rewardElement.remove();
        }
        return %s
    })();
    """ % ('false' if sum(mw.col.sched.counts()) else 'true'), on_congrats)

overview_did_refresh.append(showRewards)

##################################################
# Monkey Patches - adds delay for animation smoothness
#################################################


#Need to block this from calling nextCard()
#giving a brief pause for transition effects.
Reviewer._answerCard = wrap(Reviewer._answerCard, fan.affirm, "around")
Reviewer.nextCard = wrap(Reviewer.nextCard, fan.delayNextCard, "around")
Reviewer.autoplay = wrap(Reviewer.autoplay, fan.autoplayOnQ, "around")


#Disables keys during fx
Reviewer.onEnterKey = wrap(Reviewer.onEnterKey, fan.onEnterKey, "around")


################################################################
# Monkey Patches - bypass file:/// access on Anki 2.1's webview
################################################################

# Replace /user/collection.media folder with actual addon path
def _redirectWebExports(path):
    targetPath=os.path.join(os.getcwd(),ADDON_TAG)
    if path.startswith(targetPath):
        targetLength=len(targetPath)+1
        return os.path.join(ADDON_FOLDER,path[targetLength:])
    return None

def _redirectWebExportsOld(self, path, _old):
    redirected = _redirectWebExports(path)
    if redirected:
        return redirected
    return _old(self,path)

def _redirectWebExportsNew(path, _old):
    redirected = _redirectWebExports(path)
    if redirected:
        return redirected
    return _old(path)

mw.addonManager.setWebExports(__name__, r"user_files/.*")
if PATCH_VERSION >= 50:
    from aqt import mediasrv
    mediasrv._extract_addon_request = wrap(mediasrv._extract_addon_request, _redirectWebExportsNew, 'around')
elif PATCH_VERSION >= 28:
    from aqt import mediasrv
    mediasrv._redirectWebExports = wrap(mediasrv._redirectWebExports, _redirectWebExportsNew, 'around')
else:
    from aqt.mediasrv import RequestHandler
    RequestHandler._redirectWebExports = wrap(RequestHandler._redirectWebExports, _redirectWebExportsOld, 'around')
