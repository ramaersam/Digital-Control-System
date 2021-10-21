from struct import pack_into, unpack
import sys
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit, QProgressBar
from PyQt5.QtWidgets import QPushButton, QRadioButton, QVBoxLayout

from serverThread import ServerThread
from style import style
from data import robotList

DT_FORMAT = '%d/%m/%y-%H:%M'

class Router(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        if self.parent == None:
            self.robotList = robotList
        else : self.robotList = parent.robotList
        self.initUI()
        if self.parent == None:
            self.status = True
            self.server = ServerThread(self, port=3343)
            self.server.start()
        else : self.server = parent.server

    def initUI(self):
        self.setWindowTitle('AGV Router')
        self.setGeometry(100, 100, 400, 400)

        self.baseLayout = QVBoxLayout()
        self.setLayout(self.baseLayout)
    # title 
        if self.parent == None:
            self.titleLayout = QHBoxLayout()
            self.baseLayout.addLayout(self.titleLayout)
            self.logo = QLabel()
            self.pixmap = QPixmap('img/logo.png')
            self.logo.resize(100, 100)
            self.logo.setPixmap((self.pixmap.scaled(self.logo.size())))
            self.titleLayout.addWidget(self.logo, 0, Qt.AlignCenter)
        # status Radio Button
            self.radioWidget = QWidget()
            self.radioLayout = QFormLayout()
            self.radioWidget.setLayout(self.radioLayout)
            self.titleLayout.addWidget(self.radioWidget, alignment=Qt.AlignRight)
            self.radioStandby = QRadioButton('standby')
            self.radioRunning = QRadioButton('running')
            self.radioStandby.setChecked(True)
            self.radioStandby.setEnabled(False)
            self.radioRunning.setEnabled(False)
            self.radioLayout.addRow(self.radioStandby)
            self.radioLayout.addRow(self.radioRunning)
        else: self.titleLayout = self.parent.titleLayout
    # Form
        self.formLayout = QFormLayout()
        self.baseLayout.addLayout(self.formLayout)
    # Robot ID
        if self.parent == None:
            self.cbRobotIDList = QComboBox()
            self.cbRobotIDList.addItems([str(x) for x in range(3)])
            self.cbRobotIDList.currentIndexChanged.connect(self.onIDChange)
            self.formLayout.addRow('Robot ID', self.cbRobotIDList)
    # LineEdit IP:Port
            self.lnRobotIP = QLineEdit()
            self.formLayout.addRow('IP Addr', self.lnRobotIP)
            self.lnRobotPort = QLineEdit()
            self.formLayout.addRow('Port', self.lnRobotPort)
        else:
            self.cbRobotIDList = self.parent.cbRobotIDList
            self.lnRobotIP = self.parent.lnRobotIP
            self.lnRobotPort = self.parent.lnRobotPort
    # From
        self.cbStart = QComboBox()
        self.cbStart.addItems([str(x) for x in range(8)])
        self.cbStart.currentIndexChanged.connect(self.onStartChange)
        self.formLayout.addRow('Route', self.cbStart)
    # To
        self.cbDestination = QComboBox()
        self.cbDestination.addItems([str(x) for x in range(1, 8)])
        # self.cbDestination.removeItem(0)
        self.cbDestination.currentIndexChanged.connect(self.onDestChange)
        # self.formLayout.addRow('Target Pos', self.cbDestination)
    # path id
        self.cbPath = QComboBox()
        self.cbPath.addItems([str(x) for x in range(20)])
        self.cbPath.currentIndexChanged.connect(self.onPathChange)
        self.formLayout.addRow('Path number', self.cbPath)
    # path settings
        self.lineType = QLineEdit()
        self.lineSpeed = QLineEdit()
        self.lineTurn = QLineEdit()
        self.lineTimeout = QLineEdit()
        self.lineSensor = QLineEdit()
        self.formLayout.addRow('Type', self.lineType)
        self.formLayout.addRow('Speed', self.lineSpeed)
        self.formLayout.addRow('Turn Speed', self.lineTurn)
        self.formLayout.addRow('Timeout', self.lineTimeout)
        self.formLayout.addRow('Sensor', self.lineSensor)
        self.btnSave = QPushButton('Save Path Setting', self)
        self.btnSave.clicked.connect(self.onSave)
        self.formLayout.addRow(self.btnSave)
        self.btnGetData = QPushButton('Get Robot Setting', self)
        self.btnGetData.clicked.connect(self.onGetData)
        self.formLayout.addRow(self.btnGetData)
    # Progress Bar
        if self.parent == None:
            self.progress = QProgressBar()
            self.progress.setMaximum(13)
            self.progress.setMinimum(0)
            self.formLayout.addRow(self.progress)
        else: self.progress = self.parent.progress
    # log
        if self.parent == None:
            self.logText = QPlainTextEdit(self)
            self.formLayout.addRow(self.logText)
            self.logText.setReadOnly(True)
            self.logText.appendPlainText('({}) Aplikasi Berjalan'
                .format(datetime.now().strftime(DT_FORMAT)))
        else: self.logText = self.parent.logText
    # initials
        self.cbRobotIDList.setCurrentIndex(1)
        self.onPathChange()

    def onIDChange(self):
        id = self.cbRobotIDList.currentIndex()
        self.logText.appendPlainText(
            '({}) robot ID {} dipilih'.format(
            datetime.now().strftime(DT_FORMAT), id))
        self.lnRobotIP.setText(self.robotList[id]['addr'])
        self.lnRobotPort.setText(str(self.robotList[id]['port']))
        self.onPathChange()
    
    def onStartChange(self):
        start = int(self.cbStart.currentText())
        # self.logText.appendPlainText(
        #     '({}) start pos {}'.format(
        #     datetime.now().strftime(DT_FORMAT), start))
        self.cbDestination.clear()
        for i in range(8):
            if i != start:
                self.cbDestination.addItem(str(i))
        self.onPathChange()
        
    def onDestChange(self):
        tar = int(self.cbDestination.currentText())
        # self.logText.appendPlainText(
        #     '({}) target pos {}'.format(
        #     datetime.now().strftime(DT_FORMAT), tar))
        self.onPathChange()

    def onGetData(self):
        id = int(self.cbRobotIDList.currentText())
        start = int(self.cbStart.currentText())
        end = int(self.cbDestination.currentText())
        route = start # (start << 3) + end
        path = int(self.cbPath.currentText())
        self.logText.appendPlainText(
            '({}) request setting robot-{} rute {}-{}:{}'.format(
            datetime.now().strftime(DT_FORMAT), id, start, end, path))
        self.RequestFromRobot(self.robotList[id], route, path)
    
    def onSave(self):
    # get current path
        id = int(self.cbRobotIDList.currentText())
        start = int(self.cbStart.currentText())
        end = int(self.cbDestination.currentText())
        route = str(start) # str((start << 3) + end)
        path = int(self.cbPath.currentText())
        curBot = self.robotList[id]
        cuRoute = curBot['routes'][route]
        curPath = cuRoute[path]
    #save on list and robot
        curPath['type'] = int(self.lineType.text())
        curPath['speed'] = int(self.lineSpeed.text())
        curPath['turn'] = int(self.lineTurn.text())
        curPath['timeout'] = int(self.lineTimeout.text())
        curPath['sensor'] = int(self.lineSensor.text())
        self.sendToRobot(curBot, int(route), path, curPath)

    def RequestFromRobot(self, robot, route, path):
        buff = bytearray(18)
        header = 'abc'
        write_mode = 0
        pack_into('<3s',buff, 0, header.encode('utf-8'))
        pack_into('<4b', buff, 3, robot['id'], write_mode, route, path)
        checksum = 0
        for i in range(3,17):
            checksum += buff[i]
        print(checksum)
        pack_into('<B', buff, 17, checksum)
        print('______________________')
        print('requested {}:{}'.format(route, path))
        target_ = self.lnRobotIP.text()
        port_ = int(self.lnRobotPort.text())
        print('to ({})[{}:{}]'.format(robot['id'], target_, port_))
        print(unpack('<3s4b5hb', buff))
        self.server.sock.sendto(buff, (target_, port_))
        # self.server.sock.sendto(buff, (robot['addr'], robot['port']))

    def sendToRobot(self, robot, route, path, data):
        buff = bytearray(18)
        header = 'abc'
        write_mode = 1
        pack_into('<3s',buff, 0, header.encode('utf-8'))
        pack_into('<4b', buff, 3, robot['id'], write_mode, route, path)
        pack_into('<5h', buff, 7, data['type'], data['speed'], data['turn'],
            data['timeout'], data['sensor'])
        checksum = 0
        for i in range(3,17):
            checksum += buff[i]
        print(checksum)
        pack_into('<B', buff, 17, checksum)
        print(unpack('<3s4b5hb', buff))
        print('sent {}:{}'.format(route, path))
        target_ = self.lnRobotIP.text()
        port_ = int(self.lnRobotPort.text())
        print('to ({})[{}:{}]'.format(robot['id'], target_, port_))
        print('______________________')
        self.server.sock.sendto(buff, (target_, port_))
        self.server.sock.sendto(buff, (robot['addr'], robot['port']))

    def onPathChange(self):
        id = int(self.cbRobotIDList.currentText())
        start = int(self.cbStart.currentText())
        end = int(self.cbDestination.currentText())
        route = str(start) # str((start << 3) + end)
        # print('{}+{}={}'.format(start,end, route))
        path = int(self.cbPath.currentText())
        if id > len(self.robotList):
            self.logText.appendPlainText(
            '({}) invalid robot ID'.format(
            datetime.now().strftime(DT_FORMAT)))
            return
        curBot = self.robotList[id]
        if route not in curBot['routes']:
            curBot['routes'][route] = []
        cuRoute = curBot['routes'][route]
        while path >= len(cuRoute):
            cuRoute.append({
                'type':0,
                'speed':0,
                'turn':0,
                'timeout':0,
                'sensor':0,
                'status':0
            })
        curPath = cuRoute[path]
        self.lineType.setText(str(curPath['type']))
        self.lineSpeed.setText(str(curPath['speed']))
        self.lineTurn.setText(str(curPath['turn']))
        self.lineTimeout.setText(str(curPath['timeout']))
        self.lineSensor.setText(str(curPath['sensor']))
        print(curBot)
    
    def cbUDP(self):
        temp = self.server.bin
        (h, id, f, route, path, tp, v, tr, to, sn, ck) = unpack('<3s4b5hb',temp)
        print(unpack('<3s4b5hb',temp))
        if f == 1 and route < 63 and path < 20:
            curBot = self.robotList[id]
            if str(route) not in curBot['routes']:
                curBot['routes'][str(route)] = []
            cuRoute = curBot['routes'][str(route)]
            while path >= len(cuRoute):
                cuRoute.append({
                    'type':0,
                    'speed':0,
                    'turn':0,
                    'timeout':0,
                    'sensor':0,
                    'status':0
                })
            curPath = cuRoute[path]
            if h.decode('utf-8') == 'abc' and f == 1 and route < 10:
                curPath['type'] = tp
                curPath['speed'] = v
                curPath['turn'] = tr
                curPath['timeout'] = to
                curPath['sensor'] = sn
                curPath['status'] = 0

    def closeFunction(self):
        print('close')


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    win = Router()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
