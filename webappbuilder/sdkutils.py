import os
import execjs

def isSdkInstalled():
    sdkPath = os.path.join(os.path.dirname(__file__), "websdk")
    if not os.path.exists(sdkPath):
        return False
    try:
        node = execjs.get("Node")
        return node.is_available()
    except execjs.RuntimeUnavailable:
        return False

