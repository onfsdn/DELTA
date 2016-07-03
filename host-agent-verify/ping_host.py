'''Script to verify ping to a host'''
import subprocess
import sys

def ping(hostIP, flag):
    """Procedure to ping another host """
    try:
        if flag == 'beforeattack':
            subprocess.Popen(["ping", "-c", "2", hostIP], stdout=subprocess.PIPE).communicate()
        print "starting subprocess ping"
        pingResponse = subprocess.Popen(["ping", "-c", "20", hostIP], stdout=subprocess.PIPE).communicate()[0]
        print pingResponse
    except Exception as e:
        print "Exception occurred: ", e

def main():
    '''Main function'''
    if len(sys.argv) > 2:
        hostIP = sys.argv[1]
        flag = sys.argv[2]
    else:
        print "Host ip not specified. Usage: ping_host.py <host ip> <beforeattack/afterattack>"
        sys.exit()
    ping(hostIP, flag)

if __name__ == '__main__':
    main()

