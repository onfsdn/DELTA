#!/usr/bin/python
import sys
import os
from mininet.cli import CLI 
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, Controller, RemoteController

#class myTopo(Topo):
#  def __init__(self):
#    Topo.__init__(self)

def DeltaNetwork():
#Make topology
	net = Mininet(topo=None, controller=None, build=False)

#	c1 = net.addController(name='c1', controller=RemoteController, ip=sys.argv[1], port=int(sys.argv[2]))

#Add Switch
	s0 = net.addSwitch('s0')
	s1 = net.addSwitch('s1')

#Add hosts
	h1 = net.addHost('h1', ip='10.0.0.1')
	h2 = net.addHost('h2', ip='10.0.0.2')
        h3 = net.addHost('h3', ip='10.0.0.3')

#Link
	net.addLink(s1, h1)
	net.addLink(s1, h2)
        net.addLink(s1, h3)

	net.addLink(s1, h1, intfName2='eth1') # changed s0 to s1
	
#net.addLink(s1, h1, intfName2='eth0')
#net.addLink(s1, h2, intfName2='eth0')

#	net.build()
	net.start()

#Add hardware interfaces
	s1.attach('eth1') # changed s0 to s1
#	s1.attach('eth0')

#Set ip
	h1.cmd("ifconfig eth1 10.0.2.20 netmask 255.255.255.0")
        h2.cmd("ifconfig eth1 10.0.2.21 netmask 255.255.255.0")
        h3.cmd("ifconfig eth1 10.0.2.22 netmask 255.255.255.0")
	
#connect a controller
        os.system("sudo ovs-vsctl set-controller s1 tcp:"+sys.argv[1]+":"+sys.argv[2])
        os.system("ovs-vsctl set bridge s1 protocols=OpenFlow13")

#h1.cmd("ifconfig eth0 10.0.0.1 netmask 255.255.255.0")
#h2.cmd("ifconfig eth0 10.0.0.2 netmask 255.255.255.0")

	CLI(net)
	net.stop()

if __name__=='__main__':
	DeltaNetwork()
