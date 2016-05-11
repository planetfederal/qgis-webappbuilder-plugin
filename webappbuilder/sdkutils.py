# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os

def isSdkInstalled():
    sdkPath = os.path.join(os.path.dirname(__file__), "websdk", "node_modules")
    return os.path.exists(sdkPath)
