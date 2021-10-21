import sys
from datetime import datetime
from struct import pack_into, unpack
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QRadioButton
from PyQt5.QtWidgets import QLabel, QPlainTextEdit, QProgressBar
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFormLayout
from PyQt5.QtWidgets import QPushButton, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap

from serverThread import ServerThread
from style import style

DT_FORMAT = '%d/%m/%y-%H:%M'

class Caller(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        if self.parent == None:
            self.robotList = [{
                    'addr':'192.168.0.47',
                    'port':4210
                },{
                    'addr':'192.168.43.17',
                    'port':4210
                },{
                    'addr':'192.168.1.17',
                    'port':4210
                }
            ]
        else : self.robotList = parent.robotList
        self.initUI()
        if self.parent == None:
            self.status = True
            self.server = ServerThread(self, port=3343)
            self.server.start()
        else :
            self.server = parent.server

    # initialize UI
    def initUI(self):
        self.setWindowTitle('AGV Caller App')
        self.setGeometry(100, 100, 400, 300)

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
    # Target
        self.cbDestination = QComboBox()
        self.cbDestination.addItems([str(x) for x in range(10)])
        self.cbDestination.currentIndexChanged.connect(self.onTargetChange)
        self.formLayout.addRow('Target Pos', self.cbDestination)
    # Call Button
        self.btnCall = QPushButton('Call', self)
        self.btnCall.clicked.connect(self.onCall)
        self.formLayout.addRow(self.btnCall)
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
    # initial ID
        self.cbRobotIDList.setCurrentIndex(1)

    # callback call button action
    def onCall(self):
        # get target robot data
        id = self.cbRobotIDList.currentIndex()
        target_ = self.lnRobotIP.text()
        port_ = int(self.lnRobotPort.text())
        to = int(self.cbDestination.currentText())

        # ready buffer data
        buff = bytearray(18)
        header = 'abc'
        write_mode = 0

        pack_into('<3s',buff, 0, header.encode('utf-8'))
        pack_into('<4b', buff, 3, id, write_mode, 40, to)
        checksum = 0
        for i in range(3,17):
            # self.progress.setValue(self.progress.value()+1)
            checksum += buff[i]
        pack_into('<b', buff, 17, checksum)
        
        # debugging
        print('request call to {}'.format(to))
        print(unpack('<3s4b5hb',buff))
        print('______________________')

        self.server.sock.sendto(buff, (target_, port_))
        self.logText.appendPlainText(
            '({}) Robot {} dipanggil ke rute {}'.format(
            datetime.now().strftime(DT_FORMAT), id, to))

    # callback UDP data
    def cbUDP(self):
        self.progress.reset()
        id = self.cbRobotIDList.currentIndex()
        to = int(self.cbDestination.currentText())
        self.logText.appendPlainText(
            '({}) Robot {} menuju ke rute {}'.format(
            datetime.now().strftime(DT_FORMAT), id, to))

    def onIDChange(self):
        id = self.cbRobotIDList.currentIndex()
        self.logText.appendPlainText(
            '({}) robot ID {} dipilih'.format(
            datetime.now().strftime(DT_FORMAT), id))
        self.lnRobotIP.setText(self.robotList[id]['addr'])
        self.lnRobotPort.setText(str(self.robotList[id]['port']))
    
    def onTargetChange(self):
        id = self.cbDestination.currentIndex()
        self.logText.appendPlainText(
            '({}) tujuan pemanggilan ke rute {}'.format(
            datetime.now().strftime(DT_FORMAT), id))

    def parent(self):
        return self.parent

    def closeFunction(self):
        print('close')


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    win = Caller(None)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()