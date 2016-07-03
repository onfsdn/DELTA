'''This program will connect to the DELTA Agent Manager
and execute the layer 2 attack requested by the user
'''
import socket
import time
import sys
import struct
import attack_test
import util

AGENTMANAGERIP = util.getConfig("agent_manager_ip")
AGENTMANAGERPORT = util.getConfig("agent_manager_port")
BUFFERLEN = 1024

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientSocket.connect((AGENTMANAGERIP, int(AGENTMANAGERPORT)))            # Connect to DELTA Agent Manager
    size = len('L2HostAgent')
    clientSocket.send(struct.pack("!H", size))
    clientSocket.send('L2HostAgent')                                         # Send the Agent name
except Exception as e:
    print 'Unable to connect to server', e
    sys.exit()

while 1:
    try:
        data = clientSocket.recv(BUFFERLEN)
        print "Agent Manager sent :"+data
        data = data.strip()
        time.sleep(5)
        ret = "failed"                                                       # Initializing the return status to fail
        # Start Layer 2 attack based on info passed from Agent Manager
        if '7.0.1' in data:
            ret = attack_test.simpleARPFlood()
        elif '7.0.2' in data:
            ret = attack_test.ARPFloodUnknownDest()
        elif '7.1.1' in data:
            ret = attack_test.ARPFloodRandomSourceMACUnknownDest()
        elif '7.1.2' in data:
            ret = attack_test.ARPFloodRandomSourceMACKnownDest()
        elif '7.2.1' in data:
            ret = attack_test.ARPFloodKnownSourceMACUnknownDest()
        elif '7.2.2' in data:
            ret = attack_test.ARPFloodKnownSourceMACKnownDest()
        elif '7.3.1' in data:
            ret = attack_test.ARPFloodRandomSourceMACUnknownDest()
        size = len(ret)
        clientSocket.send(struct.pack("!H", size))
        clientSocket.send(ret)
    except Exception as e:
        print "Connection closed", e

