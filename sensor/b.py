import sys
import threading
import time
import os
from serial import Serial
import seeed_python_ircamera

global minHue
global maxHue

hetaData = []
lock = threading.Lock()
minHue = 180
maxHue = 360


#app = QApplication(sys.argv)
#window = painter()
dataThread = DataReader(None)
#dataThread.drawRequire.connect(window.draw)
dataThread.start()
#window.show()
#app.exec_()

