import sys
import os
import site

site.addsitedir(os.path.abspath(os.path.dirname(__file__) + '/ext-libs'))

def classFactory(iface):

    from webappbuilder import WebAppBuilderPlugin
    return WebAppBuilderPlugin(iface)
