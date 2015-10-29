import os

def isSdkInstalled():
    sdkPath = os.path.join(os.path.dirname(__file__), "websdk", "node_modules")
    return os.path.exists(sdkPath)

