# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from __future__ import unicode_literals
import random, os, sys
from aqt import mw
from codecs import open
from anki.utils import tmpdir, json
import collections

from .const import *


def haveReviews():
    counts = list(mw.col.sched.counts())
    return sum(counts)!=0


def getMedia(last, dir, arr):
    i=getRandomIndex(last,arr)
    if i>-1: #have media
        m=arr[i]
        p=os.path.join(dir,m)
        return (i,m,p)
    return None

def getRandomIndex(lstIdx, arr):
    if not arr: return -1 #empty array
    LEN=idx=len(arr)-1
    if LEN>0:
        idx=random.randint(0, LEN)
        while lstIdx==idx:
            idx=random.randint(0, LEN)
    return idx

def readJson(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data=f.read()
        return json.loads(data)




from anki import version
PY3=version.startswith("2.1.")

#From: https://stackoverflow.com/questions/3232943/
def nestedUpdate(d, u):
    if PY3:
        itm=u.items()
    else:
        itm=u.iteritems()
    for k, v in itm:
        if isinstance(v, collections.Mapping):
            d[k] = nestedUpdate(d.get(k, {}), v)
        else:
            d[k] = v
    return d
