# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Fanfare
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


#=== CONFIGS ===============================

# For Anki2.0, used to allow the backported addonManager21 to load first
STARTUP_DELAY = 300 #in ms

#=== END_CONFIGS ===========================
############################################

import os, re
from aqt import mw
from anki import version
PY3 = version.startswith("2.1.")

#All for calculating the addon ID and prevent conflicts w/ other similar pathnames on A21
MOD_ABS,_ = os.path.split(__file__)
MOD_DIR = os.path.basename(MOD_ABS)
ADDON_FOLDER=mw.pm.addonFolder()
ADDON_TAG = os.path.dirname(__file__)
