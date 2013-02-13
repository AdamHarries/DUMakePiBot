from socket import *
import socket as sock
import sys
import select
import nxt, thread, time

b = nxt.find_one_brick()
mx = nxt.Motor(b, nxt.PORT_B)
my = nxt.Motor(b, nxt.PORT_C)
motors = [mx, my]
address = ('0.0.0.0', 6005)
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(address)

def turnmotor(m, power, degrees):
    m.turn(power, degrees,False)
def stopmotor(m):
    m.brake()
def runmotor(m):
    m.run(70,False)
def runinstruction(i):
    motorid, speed, degrees = i
    thread.start_new_thread(
        turnmotor,
        (motors[motorid], speed, degrees))

#main loop
while(true):
    print "Listening"
    recv_data, addr = server_socket.recvfrom(2048)
    if recv_data == "left" :
        print "left"
        runinstruction([0,30,80])
        runinstruction([1,-30,80])
    elif recv_data == "LEFT" :
        print "LEFT"
        runinstruction([0,50,180])
        runinstruction([1,-50,180])
    elif recv_data == "right" :
        print "right"
        runinstruction([0,-30,80])
        runinstruction([1,30,80])
    elif recv_data == "RIGHT" :
        print "RIGHT"
        runinstruction([0,-50,180])
        runinstruction([1,50,180])
    elif recv_data == "forward" :
        print "forward"
        ms=nxt.SynchronizedMotors(mx,my,0)
        ms.run(70)
    elif recv_data == "Uturn" :
        print "Uturn"
        runinstruction([0,-70,350])
        runinstruction([1,70,350])
    elif recv_data == "Stop" :
        print "Stop"
        stopmotor(mx)
        stopmotor(my)
    elif recv_data == "back" :
        print "back"
        runinstruction([0,-70,380])
        runinstruction([1,-70,580])
