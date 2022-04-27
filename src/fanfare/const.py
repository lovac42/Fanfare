# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import os
from aqt import mw

#All for calculating the addon ID and prevent conflicts w/ other similar pathnames on A21
MOD_ABS,_ = os.path.split(__file__)
MOD_DIR = os.path.basename(MOD_ABS)
ADDON_FOLDER=mw.pm.addonFolder()
ADDON_TAG = os.path.dirname(__file__)
