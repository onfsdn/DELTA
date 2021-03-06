# DELTA: A Penetration Testing Framework for Software-Defined Networks

## What is DELTA?
DELTA is a penetration testing framework that regenerates known attack scenarios for diverse test cases. This framework also provides the capability of discovering unknown security problems in SDN by employing a fuzzing technique.

+ Agent-Manger is the control tower. It takes full control over all the agents deployed to the target SDN network.
+ Application-Agent is a legitimate SDN application that conducts attack procedures and is controller-dependent. The known malicious functions are implemented as application-agent functions.
+ Channel-Agent is deployed between the controller and the OpenFlow-enabled switch. The agent sniffs and modifies the unencrypted control messages. It is controller-independent.
+ Host-Agent behaves as if it was a legitimate host participating in the target SDN network. The agent demonstrates an attack in which a host attempts to compromise the control plane.

![Delta architecture](http://143.248.53.145/research/delta/arch.png)

## Prerequisites
In order to build and run DELTA the following are required:
+ At least 3 virtual machines (based on Ubuntu 14.04 LTS 64 bit)
+ Target Controller ([OpenDaylight_Helium-S3](https://github.com/opendaylight/controller/releases/tag/release%2Fhelium-sr3), [ONOS 1.1.0](https://github.com/opennetworkinglab/onos/tree/onos-1.1) or [Floodlight-0.91](https://github.com/floodlight/floodlight/tree/v0.91)) (for agent-manager in VM-1)
+ [Cbench](https://floodlight.atlassian.net/wiki/display/floodlightcontroller/Cbench) (in VM-1)
+ JPcap library([JPcap 64bit.jar](http://sdnsec.kr/research/delta/jpcap.jar), [libjpcap.so](http://sdnsec.kr/research/delta/libjpcap.so)) (for channel-agent in VM-2)
+ [Mininet 2.1+](http://mininet.org/download/) (for host-agent in VM-3)
+ Ant build system
+ JDK 1.7+

## Installing DELTA
Delta installation depends on JAVA and the ant build system. The ant command is used to install the Agent-Manager and sub-agents.

+ STEP 1. Installing Agent-Manager.

```
$ cd agent-manager
$ ant
```

+ STEP 2. Installing Channel-Agent.

```
$ cd channel-agent
$ ant
```

+ STEP 3. Installing Host-Agent.

```
$ cd host-agent
$ ant
```

+ STEP 4. Installing Application-Agent. It depends on the controller type and version.
<br><br> 1) In the case of Floodlight-0.91: 
```
(before installing application-agent of floodlight-0.91, floodlight-0.91 controller should be installed)

$ ln -s (Delta absolute path)/app-agent/floodlight/0.91/nss (floodlight absolute path)/src/main/java/nss

(Then, Modify floodlight module configuration files)

$ vi (floodlight path)/src/main/resources/floodlightdefault.properties

floodlight.modules=\
nss.delta.appagent.AppAgent,\   # <-- add
net.floodlightcontroller.jython.JythonDebugInterface,\
...

$ vi (floodlight path)/src/main/resources/META-INF/services/net.floodlightcontroller.core.module.IFloodlightModule

nss.delta.appagent.AppAgent     # <-- add
net.floodlightcontroller.core.module.ApplicationLoader
net.floodlightcontroller.core.internal.FloodlightProvider
...

$ cd (floodlight path)
$ sudo ant
```
<br> 2) In the case of ONOS: ...

<br> 3) In the case of OpenDaylight: ...

## Configuring your own experiments
+ The Agent-Manager automatically reads your configuration file and sets up the environment based on the configuration file settings. Setting.cfg contains sample configurations. You can specify your own config file by passing its path:
```
FLOODLIGHT_ROOT=/home/sdn/floodlight/floodlight-0.91/target/floodlight.jar
FLOODLIGHT_VER=0.91
ODL_ROOT=/home/sdn/odl-helium-sr3/opendaylight/distribution/opendaylight/target/distribution.opendaylight-osgipackage/opendaylight/run.shODL_VER=helium-sr3
ODL_APPAGENT=/home/sdn/odl-helium-sr3/opendaylight/appagent/target/appagent-1.4.5-Helium-SR3.jar
ONOS_ROOT=/home/sdn/onos/onos-1.1.0/
ONOS_VER=1.1.0
ONOS_KARAF_ROOT=/home/sdn/Application/apache-karaf-3.0.4/bin/karaf
CBENCH_ROOT=/home/sdn/oflops/cbench/
TARGET_CONTROLLER=Floodlight
OF_PORT=6633
OF_VER=1.0
MITM_NIC=eth0
CONTROLLER_IP=192.168.100.195
SWITCH_IP=192.168.100.185
```

+ The Channel-Agent automatically reads your configuration file and connects the Agent-Manager.
```
AM_IP=192.168.101.X
AM_PORT=3366
```
+ The Host-Agent automatically reads your configuration file and connects the Agent-Manager.
```
AM_IP=192.168.101.X
AM_PORT=3366
```

## Running DELTA
+ STEP 0. Virtual Machine Setting

> VM 1. Agent-Manager and one of the target controllers are installed.
```
(at least two network interfaces are required)
eth0 192.168.100.X/24 # for controller-switch connection
eth1 192.168.101.X/24 # for Delta agents connection
```

> VM 2. Mininet and Host-Agent are installed.
```
(at least two network interfaces are required)
eth0 192.168.100.X/24 # for controller-switch connection
eth1 192.168.101.X/24 # for Delta agents connection
```


+ STEP 1. Running Agent Manager in VM1
```
$ cd [Delta]/agent-manager
$ sudo java -jar ./target/am.jar ./setting.cfg

 DELTA: A Penetration Testing Framework for Software-Defined Networks

 [pP]	- Show all known attacks
 [cC]	- Show configuration info
 [kK]	- Replaying known attack(s)
 [uU]	- Finding an unknown attack
 [qQ]	- Quit Scanner


Command>_
```

+ STEP 2. Running Channel-Agent
```
$ cd [Delta]/channel-agent
$ sudo java -jar ./target/channel-agent.jar setting.cfg
```

+ STEP 3. Running Host-Agent in VM2
```
$ git clone https://github.com/OpenNetworkingFoundation/DELTA.git
$ cd Delta/host-agent
$ ant

$ sudo python ./topo-setup.py (eth0 ip address in VM1) 6633

mininet> xterm h1

$ (console in h1) cd [Delta]/host-agent
$ (console in h1) java -jar ./target/ha.jar setting.cfg
```

+ STEP 4. Reproducing known attacks in VM1
```
 DELTA: A Penetration Testing Framework for Software-Defined Networks

 [pP]	- Show all known attacks
 [cC]	- Show configuration info
 [kK]	- Replaying known attack(s)
 [uU]	- Finding an unknown attack
 [qQ]	- Quit Scanner


Command> k
Select the attack code (replay all, enter the 'A')> A-2-M-1

 10% ===== |

02:10:46.886 - [A-2-M-1] - Control Message Drop attack start
02:10:46.887 - [A-2-M-1] - Controller setting..
```


## Questions?
Send questions or feedback to: lss365@kaist.ac.kr or chyoon87@kaist.ac.kr

in delta-101
