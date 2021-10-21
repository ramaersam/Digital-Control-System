from datetime import datetime
import socket
import threading
from netifaces import interfaces, ifaddresses, AF_INET

DT_FORMAT = '%d/%m/%y-%H:%M'

class ServerThread(threading.Thread):
    def __init__(self, parent, addr=socket.gethostname(), port=4210):
        threading.Thread.__init__(self)
        self.parent = parent
        # self.root = parent
        self.status = False
        # while self.root.parent() != None:
        #     self.root = self.root.parent()
        if addr == socket.gethostname():
            addrs= []
            for ifaceName in interfaces():
                a = ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}])
                if 'broadcast' in a[0]:
                    addrs.append(a[0]['addr'])
            if len(addrs):
                addr = addrs[0]
        # print(socket.gethostbyname(socket.gethostname()))
        # print(type(addr))
        self.SERVER_IP = addr
        self.SERVER_PORT = port
        self.rawdata = ''
        self.parent.closeEvent = self.closeEvent
    
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try :
            self.sock.bind((self.SERVER_IP, self.SERVER_PORT))
            # self.parent.logText.appendPlainText(
            #     '({}) Aplikasi Terkoneksi ke jaringan pada soket {}:{}'
            #     .format(datetime.now().strftime(DT_FORMAT),
            #     self.SERVER_IP, self.SERVER_PORT))
        except OSError:
            print('failed to bind socket')
            # self.parent.logText.appendPlainText('({}) Gagal membuat soket'
            #     .format(datetime.now().strftime(DT_FORMAT)))
        self.status = True
        self.sock.settimeout(0.1)
            

        while self.parent.status:
            try:
                data, addr = self.sock.recvfrom(1024)
                print('received ', data)
                print('dikirim oleh ', addr)
                self.process(data)
                    
            except socket.timeout:
                # print('timeout')
                pass

        self.sock.close()
        print('thread exited.({}:{})'.format(self.SERVER_IP, self.SERVER_PORT))

    def process(self, data):
        # print(self.rawdata)
        self.bin = data
        print(data)
        # if self.parent == self.root:
        self.parent.cbUDP()
        # else:
        #     self.rawdata = data.decode('utf-8')
        # self.parent.update()

    def closeEvent(self, event):
        self.parent.closeFunction()
        self.parent.status = False
        event.accept()

    def parent(self):
        return self.parent