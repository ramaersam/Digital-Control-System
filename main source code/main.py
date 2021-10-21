from datetime import datetime
from struct import unpack
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap
from router import Router
import sys

from PyQt5.QtWidgets import QApplication, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QProgressBar, QRadioButton
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from serverThread import ServerThread
from caller import Caller
from style import style
from data import robotList

DT_FORMAT = '%d/%m/%y-%H:%M'

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # init base App
        self.initData()
        self.initUI()

        # init server
        self.status = True
        self.server = ServerThread(self, port=3343)
        self.server.start()

        # init submodule
        self.initSubModule()

    # read setting from data file
    def initData(self):
        self.robotList = robotList

    # initialize base UI
    def initUI(self):
        self.setWindowTitle('AGV Control Panel')
        self.setGeometry(200, 100, 500, 300)

    # main layout
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
    # title
        self.titleLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.titleLayout)
        self.logo = QLabel()
        self.pixmap = QPixmap('img/logo.png')
        self.logo.resize(100, 100)
        self.logo.setPixmap((self.pixmap.scaled(self.logo.size())))
        self.titleLayout.addWidget(self.logo, 0, Qt.AlignCenter)
    # status Group
        self.statusWidget = QWidget()
        self.statusWidget.setObjectName('statusWidget')
        self.radioLayout = QFormLayout()
        self.statusWidget.setLayout(self.radioLayout)
        self.titleLayout.addWidget(self.statusWidget, alignment=Qt.AlignRight)
    # Robot ID
        self.cbRobotIDList = QComboBox()
        self.cbRobotIDList.addItems([str(x) for x in range(3)])
        self.cbRobotIDList.currentIndexChanged.connect(self.onIDChange)
        self.radioLayout.addRow('Robot ID', self.cbRobotIDList)
     # LineEdit IP:Port
        self.lnRobotIP = QLineEdit()
        self.radioLayout.addRow('IP Addr', self.lnRobotIP)
        self.lnRobotPort = QLineEdit()
        self.radioLayout.addRow('Port', self.lnRobotPort)
    # base layouts
        self.baseLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.baseLayout)
        self.panelLayout = QVBoxLayout()
        self.panelTabs = QTabWidget()
        self.viewLayout = QWidget()
        self.baseLayout.addLayout(self.panelLayout)
        self.baseLayout.addWidget(self.viewLayout)
        self.panelLayout.addWidget(self.panelTabs)
    # Progress Bar
        self.progress = QProgressBar()
        self.progress.setMaximum(13)
        self.progress.setMinimum(0)
        self.panelLayout.addWidget(self.progress)
    # log text
        self.logText = QPlainTextEdit(self)
        self.panelLayout.addWidget(self.logText)
        self.logText.setReadOnly(True)
        self.logText.appendPlainText('({}) Aplikasi Berjalan'
            .format(datetime.now().strftime(DT_FORMAT)))

    def initSubModule(self):
        # caller
        self.caller = Caller(self)
        self.panelTabs.addTab(self.caller, 'AGV Caller')
        # router
        self.router = Router(self)
        self.panelTabs.addTab(self.router, 'Route Setting')

    def onIDChange(self):
        id = self.cbRobotIDList.currentIndex()
        self.logText.appendPlainText(
            '({}) robot ID {} dipilih'.format(
            datetime.now().strftime(DT_FORMAT), id))
        self.lnRobotIP.setText(self.robotList[id]['addr'])
        self.lnRobotPort.setText(str(self.robotList[id]['port']))
        try:
            self.router.onPathChange()
        except AttributeError:
            print('server not initialized')

    # action on UDP callback
    def cbUDP(self):
        temp = self.server.bin
        (header, rid, f, route_id, path_id, tp, v, tr, to, sn, ck) = unpack('<3s4b5hb',temp)
        print(unpack('<3s4b5hb',temp))
        
        # requested path return
        if header.decode('utf-8') == 'abc' and f == 1 and route_id < 10 and path_id < 20:
            curBot = self.robotList[rid]
            if str(route_id) not in curBot['routes']:
                curBot['routes'][str(route_id)] = []
            curRoute = curBot['routes'][str(route_id)]
            while len(curRoute) <= path_id:
                curRoute.append({
                    'type':0,
                    'speed':0,
                    'turn':0,
                    'timeout':0,
                    'sensor':0,
                })
            curPath = curRoute[path_id]
            curPath['type'] = tp
            curPath['speed'] = v
            curPath['turn'] = tr
            curPath['timeout'] = to
            curPath['sensor'] = sn
            self.router.onPathChange()
            # self.logText.appendPlainText('({}): Rute {} Path {} telah di update.'
            #     .format(datetime.now().strftime(DT_FORMAT), route_id, path_id))
        
        

    def closeFunction(self):
        print('close')


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()