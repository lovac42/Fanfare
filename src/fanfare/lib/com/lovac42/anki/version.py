# -*- coding: utf-8 -*-
# Copyright (c) 2020 Lovac42
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from anki import version

VERSION = version.split('_')[0]
m,n,p = VERSION.split('.')

MAJOR_VERSION = int(m)
MINOR_VERSION = int(n)
PATCH_VERSION = int(p)
POINT_VERSION = PATCH_VERSION

