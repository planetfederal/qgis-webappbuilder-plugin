import os
from PyQt4 import uic
from sdkutils import isSdkInstalled

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'ui_appcreateddialog.ui'))

class AppCreatedDialog(BASE, WIDGET):

    def __init__(self, folder):
        super(AppCreatedDialog, self).__init__()
        self.setupUi(self)

        folder = os.path.join(folder, "webapp")
        node = ''
        if isSdkInstalled():
            node = '<a href="node">Run Node to create web-app</a>'

        html = '''
        <p>The web app has been created at %s</p>

        <p>You will find the following files:</p>

        <ul>
        <li><b>index.html:</b> Web application using a babelify transform prebuilt version of SDK components. It should not be used in production. </li>
        <li><b>index_debug.html:</b>Same as above but with prebuilt SDK files not minified. To be used for debugging</li>
        <li><b>index_node.html/app.jsx:</b>Files to be used for creating a production-ready web by using Node and the Boundless WebSDK. %s</li>
        ''' % (folder, node)

        self.webView.setHtml(html)