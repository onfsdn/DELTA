'''Program to formulate test scenarios'''
import util
import time
import threading
import Queue as queue

UNKNOWNHOSTIP = str(util.getConfig("unknown_host_ip"))
HOSTIP1 = util.getConfig("host_ip1")
HOSTIP2 = util.getConfig("host_ip2")
HOSTIP3 = util.getConfig("host_ip3")
USERNAME = util.getConfig("host_username")
PASSWORD = util.getConfig("host_password")
SCRIPTPATH = util.getConfig("script_path")
SELF = 'self'

def simpleARPFlood():
    '''Procedure to execute simple ARP flood'''
    print "attack started"
    statBefore = util.verifyPing(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP3, 'beforeattack')
    q1 = queue.Queue()
    time.sleep(1)
    # Using threads to execute test and verify the test case simultaneously
    t1 = threading.Thread(target=util.ARPGenerator, args=(HOSTIP3, SELF))
    t2 = threading.Thread(target=util.verifyPing, args=(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP3, 'afterattack', q1))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    time.sleep(2)
    t1.start()
    result1 = q1.get()
    t1, t2, q1 = None, None, None
    print "ping result before : ", statBefore
    print "ping result after  : ", result1
    print "attack ended"
    if result1 == "drop":
        return "failed"
    else:
        return "passed"

def ARPFloodUnknownDest():
    '''Procedure to execute Flooding ARP: Unknown Destination '''
    print "attack started"
    statBefore = util.verifyPing(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP3, 'beforeattack')
    #util.ARPGenerator(UNKNOWNHOSTIP)
    q1 = queue.Queue()
    time.sleep(1)
    # Using threads to execute test and verify the test case simultaneously
    t1 = threading.Thread(target=util.ARPGenerator, args=(UNKNOWNHOSTIP, SELF))
    t2 = threading.Thread(target=util.verifyPing, args=(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP3, 'afterattack', q1))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    time.sleep(2)
    t1.start()
    result1 = q1.get()
    t1, t2, q1 = None, None, None
    print "ping result before : ", statBefore
    print "ping result after  : ", result1
    print "attack ended"
    if result1 == "drop":
        return "failed"
    else:
        return "passed"



def ARPFloodRandomSourceMACUnknownDest():
    '''Procedure to execute Flooding ARP: RANDOM SMAC to unknown Destination'''
    print "attack started"
    statBefore = util.verifyPing(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP1, 'beforeattack')
    q1 = queue.Queue()
    time.sleep(1)
    # Using threads to execute test and verify the test case simultaneously
    t1 = threading.Thread(target=util.ARPGenerator, args=(UNKNOWNHOSTIP, "random"))
    t2 = threading.Thread(target=util.verifyPing, args=(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP1, 'afterattack', q1))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    time.sleep(2)
    t1.start()
    result1 = q1.get()
    t1, t2, q1 = None, None, None
    print "ping result before : ", statBefore
    print "ping result after  : ", result1
    print "attack ended"
    if result1 == "drop":
        return "failed"
    else:
        return "passed"

def ARPFloodRandomSourceMACKnownDest():
    '''Procedure to execute Flooding ARP: RANDOM SMAC to known Destination '''
    print "attack started"
    statBefore = util.verifyPing(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP1, 'beforeattack')
    q1 = queue.Queue()
    time.sleep(1)
    # Using threads to execute test and verify the test case simultaneously
    t1 = threading.Thread(target=util.ARPGenerator, args=(HOSTIP3, "random"))
    t2 = threading.Thread(target=util.verifyPing, args=(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP1, 'afterattack', q1))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    time.sleep(2)
    t1.start()
    result1 = q1.get()
    t1, t2, q1 = None, None, None
    print "ping result before : ", statBefore
    print "ping result after  : ", result1
    print "attack ended"
    if result1 == "drop":
        return "failed"
    else:
        return "passed"


def ARPFloodKnownSourceMACUnknownDest():
    '''Procedure to execute ARP Poisoning in Switch: Unknown Destination'''
    print "attack started"
    host3Mac = util.getMacFromIp(HOSTIP3)
    statBefore = util.verifyPing(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP3, 'beforeattack')
    q1 = queue.Queue()
    time.sleep(1)
    # Using threads to execute test and verify the test case simultaneously
    t1 = threading.Thread(target=util.ARPGenerator, args=(UNKNOWNHOSTIP, host3Mac))
    t2 = threading.Thread(target=util.verifyPing, args=(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP3, 'afterattack', q1))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    time.sleep(2)
    t1.start()
    result1 = q1.get()
    t1, t2, q1 = None, None, None
    print "ping result before : ", statBefore
    print "ping result after  : ", result1
    print "attack ended"
    if result1 == "drop":
        return "failed"
    else:
        return "passed"


def ARPFloodKnownSourceMACKnownDest():
    '''Procedure to execute ARP Poisoning in Switch: Known Destination '''
    print "attack started"
    host3Mac = util.getMacFromIp(HOSTIP3)
    statBefore = util.verifyPing(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP3, 'beforeattack')
    q1 = queue.Queue()
    time.sleep(1)
    # Using threads to execute test and verify the test case simultaneously
    t1 = threading.Thread(targe=util.ARPGenerator, args=(HOSTIP1, host3Mac))
    t2 = threading.Thread(target=util.verifyPing, args=(HOSTIP2, USERNAME, PASSWORD, SCRIPTPATH, HOSTIP3, 'afterattack', q1))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    time.sleep(2)
    t1.start()
    result1 = q1.get()
    t1, t2, q1 = None, None, None
    print "ping result before : ", statBefore
    print "ping result after  : ", result1
    print "attack ended"
    if result1 == "drop":
        return "failed"
    else:
        return "passed"


def HostARPPoisoning():
    pass    






