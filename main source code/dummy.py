# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
import socket
import sys
from struct import *
from netifaces import interfaces, ifaddresses, AF_INET

from data import dummyList

if len(sys.argv) < 2:
    print('not enough argument')
    sys.exit(-1)

try:
    robot_id = int(sys.argv[1])
    dumBot = dummyList[robot_id]
    addrs= []
    for ifaceName in interfaces():
        a = ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}])
        if 'broadcast' in a[0]:
            addrs.append(a[0]['addr'])
    if len(addrs):
        addr = addrs[0]
        SERVER_IP = addr
    SERVER_PORT = dumBot['port']
    dumBot['addr'] = SERVER_IP
    print(dumBot)
except ValueError:
    print('argument mismatch, int required')
    sys.exit(-1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT, 1)
# sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)
sock.bind((SERVER_IP, SERVER_PORT))
        
# sock.bind((SERVER_IP, SERVER_PORT))
sock.settimeout(0.1)

while True:
    try:
        data, addr = sock.recvfrom(1024)
        check = data.decode('utf-8')
        if check[0:3] == 'abc':
            (id, mode, route_id, path_id) = unpack_from('<4b', data, offset=3)
            if id == robot_id and mode == 0:
                print('request masuk')
                print('{}:{}-{}'.format(id, route_id, path_id))
                if route_id == 30:
                    buff = bytearray(18)
                    header = 'abc'
                    write_mode = 1
                    pack_into('<3s',buff, 0, header.encode('utf-8'))
                    pack_into('<4b', buff, 3, robot_id, write_mode, 30, 0)
                    pack_into('<h', buff, 7, 200)
                    sock.sendto(buff, (addr[0], addr[1]))
                    print("sent {}".format(buff))
                elif route_id < 10:
                    if path_id > 20:
                        print('path out of range')
                        continue
                    
                    if str(route_id) not in dumBot['routes']:
                        # print('empty route')
                        dumBot['routes'][str(route_id)] = []
                    routes_ = dumBot['routes']
                    route_ = routes_[str(route_id)]
                    while len(route_) <= path_id:
                        route_.append({
                            'type':0,
                            'speed':0,
                            'turn':0,
                            'timeout':0,
                            'sensor':0,
                        })
                    path_ = route_[path_id]

                    buff = bytearray(18)
                    header = 'abc'
                    write_mode = 1
                    pack_into('<3s',buff, 0, header.encode('utf-8'))
                    pack_into('<4b', buff, 3, robot_id, write_mode, route_id, path_id)
                    pack_into('<5h', buff, 7, path_['type'], path_['speed'],
                        path_['turn'], path_['timeout'], path_['sensor'])
                    sock.sendto(buff, (addr[0], addr[1]))
                    print("sent {}".format(buff))
            elif id == robot_id and mode == 1:
                print('write data')
                if route_id < 10 and path_id < 20:
                    if str(route_id) not in dumBot['routes']:
                        # print('empty route')
                        dumBot['routes'][str(route_id)] = []
                    routes_ = dumBot['routes']
                    route_ = routes_[str(route_id)]
                    while len(route_) <= path_id:
                        route_.append({
                            'type':0,
                            'speed':0,
                            'turn':0,
                            'timeout':0,
                            'sensor':0,
                        })
                    path_ = route_[path_id]
                    
                    (type, speed, turn, timeout, sensor) = unpack_from('<5h', data, offset=7)
                    path_['type'] = type
                    path_['speed'] = speed
                    path_['turn'] = turn
                    path_['timeout'] = timeout
                    path_['sensor'] = sensor
                    
                    buff = bytearray(18)
                    header = 'abc'
                    write_mode = 1
                    pack_into('<3s',buff, 0, header.encode('utf-8'))
                    pack_into('<4b', buff, 3, robot_id, write_mode, route_id, path_id)
                    pack_into('<5h', buff, 7, path_['type'], path_['speed'],
                        path_['turn'], path_['timeout'], path_['sensor'])
                    sock.sendto(buff, (addr[0], addr[1]))
                    print("set {}".format(buff))
                else:
                    print('outofrange')
            else:
                print('wrong robot id')
        else:
            print(check)
    except socket.timeout:
        pass
