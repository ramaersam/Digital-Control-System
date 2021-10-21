# AGV Wireless Controller

Program utama terdapat pada file main.py. Development UI menggunakan PyQt5, dapat menggunakan QtDesigner jika dibutuhkan.

## Sub Modules
- Server thread
- Caller
- Router
- Logger

## Server Thread
- Setting soket berdasarkan IP local jaringan wifi dan port default robot.
- mengirimkan request, dan memerima response dari robot
- aksi callback terkhadap request berdasarkan parent class (submodule/main)
- pada Linux menggunakan modul **netifaces**, dan pada windows **ifaddr**
- server 

## Caller
- request target route pada robot
- bisa dijalankan dan di build sebagai aplikasi standalone 

## Router
- Membaca setting rute/path dari robot
- setting rute/path robot
- bisa dijalankan dan di build sebagai aplikasi standalone 

## Logger
- Menampilkan log pada text box

## dummy
- pengganti robot untuk simulasi pengiriman request
-dijalankan sebagai aplikasi standalone

## Additional Files

### file data.py
- setting default robot pada aplikasi, bisa disesuaikan berdasarkan robot
- disarankan diubah ke file .json dan dibaca oleh program dengan read

### file style.py
- setting view style dengan css stylesheet

### file cli.py
- untuk generate excecutable dengan modul pyinstaller dengan command:
```
pyinstaller cli.py --onefile --noconsole --name main
```
- ganti nama dengan **main.exe** untuk windows
- hasil generate akan berada pada folder **dist**

### file main.spec
- file hasil generate pyinstaller, bisa diabailkan atau digunakan untuk setting ulang build pyinstaller

### logo.png
- logo aplikasi dapat diganti dengan mengganti file logo.png pada folder img
- folder img harus ada di folder yang sama dengan excecutable

------------------------------

# System Requirement
 untuk development, dibutuhkan:
- menggunakan python3 min. 3.6
- PyQt5
- netifaces (linux)
- ifaddr (windows)

package python bisa di-install menggunakan pip/pip3