import sys
import threading
import seeed_mlx90640
import time
import os
from serial import Serial
from PyQt5.QtWidgets import (
        QApplication,
        QGraphicsView,
        QGraphicsScene,
        QGraphicsPixmapItem,
        QGraphicsTextItem,
        QGraphicsEllipseItem,
        QGraphicsLineItem,
        QGraphicsBlurEffect
    )
from PyQt5.QtGui import QPainter, QBrush, QColor, QFont, QPixmap
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QPointF, Qt


def mapValue(value, curMin, curMax, desMin, desMax):
    curDistance = value - curMax
    if curDistance == 0:
        return desMax
    curRange = curMax - curMin
    direction = 1 if curDistance > 0 else -1
    ratio = curRange / curDistance
    desRange = desMax - desMin
    value = desMax + (desRange / ratio)
    return value


def constrain(value, down, up):
    value = up if value > up else value
    value = down if value < down else value
    return value        


def isDigital(value):
    try:
        if value == "nan":
            return False
        else:
            float(value)
        return True
    except ValueError:
        return False


hetaData = []
lock = threading.Lock()
minHue = 180
maxHue = 360


class DataReader(QThread):
    drawRequire = pyqtSignal()

    I2C = 0,
    SERIAL = 1
    MODE = I2C

    def __init__(self, port):
        super(DataReader, self).__init__()
        self.frameCount = 0
        # i2c mode
        if port is None:
            self.dataHandle = seeed_mlx90640.grove_mxl90640()
            self.dataHandle.refresh_rate = seeed_mlx90640.RefreshRate.REFRESH_8_HZ
            self.readData = self.i2cRead
        else:
            self.MODE = DataReader.SERIAL
            self.port = port
            self.dataHandle = Serial(self.port, 2000000, timeout=5)
            self.readData = self.serialRead

    def i2cRead(self):
        hetData = [0]*768
        self.dataHandle.getFrame(hetData)
        return hetData

    def serialRead(self):
        hetData = self.dataHandle.read_until(terminator=b'\r\n')
        hetData = str(hetData, encoding="utf8").split(",")
        hetData = hetData[:-1]
        return hetData

    def run(self):
        global hetaData
        # throw first frame
        self.readData()
        while True:
            process_time = time.time()
            
            maxHet = 0
            minHet = 500
            tempData = []
            nanCount = 0
            
            hetaData = self.readData()
            #print("data")
            #print(*hetData)
            #saving data when object gets under 5 degree

            self.drawRequire.emit()
            self.frameCount = self.frameCount + 1
            
            #print("data->" + str(self.frameCount))
            
            #print("time : {}".format(time.time()-process_time))
        self.com.close()
        
def run():
    global minHue
    global maxHue
    if len(sys.argv) >= 2 and sys.argv[1] == "-h":
        print("Usage: %s [PortName] [minHue] [maxHue] [NarrowRatio] [UseBlur]" % sys.argv[0])
        exit(0)

    if len(sys.argv) >= 4:
        minHue = int(sys.argv[2])
        maxHue = int(sys.argv[3])
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    else:
        port = None
    app = QApplication(sys.argv)
    #window = painter()
    dataThread = DataReader(port)
    #dataThread.drawRequire.connect(window.draw)
    dataThread.start()
    #window.show()
    app.exec_()
    

#run()
