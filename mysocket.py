import socket
import sys
from thread import *
import threading
import time
import os
currentbrightness=100
gotthread=False
defaultlist=[25,50,100]
def fifty():
    os.system('''sudo pilight-send -p raw --code="1140 380 380 1140 1140 380 380 1140 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 380 1140 380 1140 1140 380 380 1140 380 1140 380 1140 380 12920"''')
    time.sleep(0.2)
def tf():
    os.system('''sudo pilight-send -p raw --code="1140 380 380 1140 1140 380 380 1140 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 380 1140 380 1140 1140 380 380 1140 380 1140 1140 380 380 12920"''')
    time.sleep(0.2)
def plus():
    os.system('''sudo pilight-send -p raw --code="1140 380 380 1140 1140 380 380 1140 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 380 1140 380 1140 380 1140 1140 380 380 1140 1140 380 380 12920"''')
    time.sleep(0.2)
def minus():
    os.system('''sudo pilight-send -p raw --code="1119 373 373 1119 1119 373 373 1119 373 1119 373 1119 1119 373 1119 373 1119 373 1119 373 373 1119 373 1119 1119 373 1119 373 1119 373 1119 373 373 1119 373 1119 373 1119 373 1119 373 1119 1119 373 1119 373 373 1492 373 12682"''')
    time.sleep(0.2)
def max_bright():
    os.system('''sudo pilight-send -p raw --code="1140 380 380 1140 1140 380 380 1140 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 380 1140 380 1140 380 1140 1140 380 1140 380 1140 380 380 12920"''')
    time.sleep(0.2)

def change_to_percent(percent):
    percent=int(percent)
    global currentbrightness
    global gotthread
    if abs(currentbrightness-percent)>25:
        set_to_brightness=min(defaultlist, key=lambda x:abs(x-percent))
        if set_to_brightness==25:
            tf()
            currentbrightness=25
        if set_to_brightness==50:
            fifty()
            currentbrightness=50
        if set_to_brightness==100:
            max_bright()
            currentbrightness=100
        print "setto",set_to_brightness
    while currentbrightness>(percent+7):
        minus()
        currentbrightness-=5
        print currentbrightness, percent
    while currentbrightness<(percent-7):
        plus()
        currentbrightness+=5
        print currentbrightness, percent
    print "done"
    gotthread=False


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    global gotthread
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data:
            break
     	print data

        if "onoff" in data:
            os.system('''sudo pilight-send -p raw --code="1140 380 380 1140 1140 380 380 1140 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 1140 380 1140 380 1140 380 1140 380 380 1140 380 1140 380 1140 380 1140 380 1140 380 1140 380 1140 1140 380 380 12920"''')
        if "percent" in data:
            if gotthread:
                if not thread.isAlive():
                    thread = threading.Thread(target=change_to_percent, args=(data.split(",")[1].split("\n")[0],))
                    thread.start()
                    gotthread=True
                else:
                    print "already changing"
            else:
                thread = threading.Thread(target=change_to_percent, args=(data.split(",")[1].split("\n")[0],))
                thread.start()
                gotthread=True
        conn.sendall(reply)

    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
