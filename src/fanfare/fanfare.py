# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap, addHook, runHook
from anki.sound import playFromText
import random, os
from .const import *
from .feedback import *
from .loots import *
from .settings import Settings

# CONSTANTS FOR STATE:
OVERVIEW=1
REVIEW=2
RELOAD=3 #reset from intermission
INTERMISSION=4
RESET=9


class Fanfare():
    state=OVERVIEW
    shown=False #fx locks
    locked=True #key locks
    wasHard=False
    duration=0
    lastDid=0

    def __init__(self):
        addHook('beforeStateChange', self.onBeforeStateChange)
        addHook('profileLoaded', self.onProfileLoaded)
        addHook('showQuestion', self.onShowQuestion)
        addHook('showAnswer', self.onShowAnswer)
        addHook('reset', self.onReset)
        self.limit=random.randint(3,7)

    def onProfileLoaded(self):
        if PY3:
            self.initConfigurations()
        else:
            mw.progress.timer(STARTUP_DELAY,self.initConfigurations,False)

    def initConfigurations(self):
        self.settings=Settings()
        self.fb=Feedback(self.settings)
        self.recess=Intermission('break', self.settings)
        self.reward=Reward('reward', self.settings)

    def onShowAnswer(self):
        self.shown=False

    def onShowQuestion(self):
        self.locked=False

    def onReset(self):
        if self.state==INTERMISSION:
            self.state=RELOAD
        else:
            self.state=RESET


    def onBeforeStateChange(self, newS, oldS, *args):
        if oldS=='resetRequired': #edit note
            self.state==RESET
            self.duration=0
            return
        if newS!='review': return

        if self.state==RELOAD: #reset from intermission
            self.shown=True
            self.locked=True
            self.duration=self.fb.reloadDeck()

        elif oldS=='overview': #on start deck
            self.shown=True
            self.locked=True
            if haveReviews(): #display fx
                self.state=OVERVIEW
                self.duration=self.fb.startDeck() 
            else:
                self.state=RESET
                self.duration=0

        #Makes sure limit breaker is lowered when jumping to a different deck
        did=mw.col.decks.selected()
        if did != self.lastDid:
            self.lastDid=did
            self.limit=max(4,self.limit//1.2)


    def autoplayOnQ(self, r, card, _old):
        "adds delay between overlapping sound tracks"
        bool=_old(r,card)
        if bool and r.state=='question' and self.duration and \
        not self.settings.config['use_mplayer_for_audio']:
            delay=self.settings.config['card_autoplay_delay']
            dmax=self.settings.theme['duration_max']
            dur=max(0,min(dmax,self.fb.audio_duration-self.duration))
            mw.progress.timer(dur+delay,lambda:playFromText(card.q()),False)
            return False
        return bool


    def affirm(self,r,ease,_old):
        if self.shown: return #prevent double taps
        if r.mw.state != "review" or r.state != "answer":
            return
        if r.mw.col.sched.answerButtons(r.card) < ease:
            return

        self.shown=True
        self.locked=True
        self.limit+=1 if r.card.queue==1 else 4-ease
        self.wasHard=ease<=2
        lapsed=ease<=self.settings.config['failed_ease']
        self.duration=self.fb.activate(lapsed)
        _old(r,ease)


    def delayNextCard(self, r, _old):
        if self.state<=RELOAD:
            mw.bottomWeb.hide()
            if self.state==REVIEW and self.checkLimitBreaker():
                self.state=INTERMISSION
                if self.duration:
                    mdur=self.settings.theme['duration_min']
                    self.duration=max(mdur,self.duration//1.4)
            else:
                self.state=REVIEW
            mw.progress.timer(self.duration,lambda:self._nextCard(r,_old),False)
        else:
            self.state=REVIEW
            _old(r)


    def _nextCard(self, r, nxCard):
        self.fb.stop()
        if self.state!=INTERMISSION:
            self.recess.clear()
            nxCard(r)
            mw.bottomWeb.show()
        else:
            self.recess.stop()


    def checkLimitBreaker(self):
        limit_breaker=self.settings.config['limit_breaker']
        if limit_breaker and self.wasHard and \
        self.limit>=limit_breaker and haveReviews():
            self.limit=random.randint(0,9)
            self.recess.start(self.fb.audio_duration)
            return True


    def rewards(self, sch, _old):
        delay=gap=0
        if self.state != OVERVIEW and self.duration:
            gap=self.settings.theme['delay_loots']
            dur=max(0,self.fb.audio_duration-self.duration)
            delay=dur+gap
        self.reward.start(delay)
        did=mw.col.decks.selected()
        img=self.reward.getLoots(did)
        msg="""<img src="%s" style="max-width:100%%" /><br>"""%img
        return msg+_old(sch)



    #Prevents keypress during FX
    def linkHandler(self, r, url, _old):
        if not self.locked: return _old(r,url)
    def keyHandler(self, r, evt, _old): #v2.0
        if not self.locked: return _old(r,evt)
    def onEnterKey(self, r, _old): #v2.1
        if not self.locked: return _old(r)

