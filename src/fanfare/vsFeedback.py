# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from anki.utils import json
from anki.hooks import addHook
import os
from .const import *
from .utils import *


class VsFeedback():
    def __init__(self, settings):
        addHook("showQuestion", self._onShowQuestion)
        self.settings=settings
        self.label=QLabel(mw.web)
        self.label.hide()

    def _onShowQuestion(self):
        mw.web.eval("$('#qa').css('visibility','')")

    def hideOverview(self):
        mw.web.eval('document.body.innerHTML="";')

    def show(self, img):
        if not self.settings.isShowImage(): return
        if self.settings.theme['imgfx'].get('hide_bg',True):
            mw.web.eval("$('#qa').css('visibility','hidden')")
        lbl=self.label
        pos=self.getPos(lbl,img)
        lbl.move(pos)
        lbl.show() #https://bugreports.qt.io/browse/QTBUG-67533?attachmentOrder=desc

    def close(self):
        self.label.hide()

    def getPos(self, lbl, img):
        x_offset=self.settings.getImageOffset('x')
        y_offset=self.settings.getImageOffset('y')
        pmap=QPixmap(img)
        lbl.setPixmap(pmap)
        lbl.resize(pmap.width(),pmap.height())
        f=mw.web.frameGeometry().center()
        pos=QPoint( x_offset + f.x()-lbl.width()//2,
                    y_offset + f.y()-lbl.height()//2 )
        return pos




##https://bugreports.qt.io/browse/QTBUG-67533?attachmentOrder=desc
#This is a temp work around. Putting pics inside the reviewer,
#but it sometimes gets squished due to malformed html/css template.
class VsFeedback21(VsFeedback):
    def show(self, img):
        if self.settings.theme['imgfx'].get('hide_bg',True):
            mw.web.eval("$('#qa').css('visibility','hidden')")
        abs_img=img.replace(ADDON_TAG,ADDON_FOLDER)
        lbl=self.label #shows in overview, but not in review
        pos=self.getPos(lbl,abs_img)

        html="""<img id="visualFeedback21_img" src="%s" 
style="width: %d; height: %d; position:fixed; left:%dpx; top: %dpx;" />
"""%(img, lbl.width(),lbl.height(), pos.x(),pos.y())

        mw.web.page().runJavaScript("""
try{ //reviewer
  var img=%s
  document.getElementById("qa").outerHTML+=img
}catch(err){ //overview
  document.body.outerHTML+=img
}"""%json.dumps(html) )

    def close(self):
        mw.web.page().runJavaScript("""
try{
  document.getElementById("visualFeedback21_img").outerHTML=""
}catch(err){}
""")

