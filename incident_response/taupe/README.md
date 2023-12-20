# conqueror

Author: unspecialfx

flag: `nite{bonARParte}`

## Description

No wonder we were so easily hacked. Our investiagation revealed that one of our employees has been communicating with the hacker. However, without any proof, there is no way to take action. Find the secret message.

## Flag details

Character format: `nite{bonARParte}`

base64: `bml0ZXtib25BUlBhcnRlfQ==`

## Packets

### 1. Send ARP Broadcast (from printserver)

`sudo arpsend -U -i 10.0.3.8 ens0p3`

### 2. HTTPS curl request (from recorder)

`curl -X GET https://github.com`

`curl -X GET https://google.com`

### 3. Send nmap (from recorder)

`nmap 10.0.3.1`

### 4. Send ARP Broadcast (from printserver)

`sudo arpsend -U -i 10.0.3.8 ens0p3`

### 5. Get FTP files (from printserver to recorder)

```
bash
ftp 10.0.3.12

```

### 6. Send ARP Packet (from recorder)

```
python
from scapy.all import ARP, Ether, srp, sendp

arp_request1 = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, hwsrc="62:6d:6c:30:5a:58", psrc="10.0.3.25", hwdst="ff:ff:ff:ff:ff:ff", pdst="10.0.3.45")
arp_request2 = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, hwsrc="74:69:62:32:35:42", psrc="10.0.3.26", hwdst="ff:ff:ff:ff:ff:ff", pdst="10.0.3.45")
arp_request3 = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, hwsrc="55:6c:42:68:63:6e", psrc="10.0.3.27", hwdst="ff:ff:ff:ff:ff:ff", pdst="10.0.3.45")
arp_request4 = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, hwsrc="52:6c:66:51:3d:3d", psrc="10.0.3.28", hwdst="ff:ff:ff:ff:ff:ff", pdst="10.0.3.45")

sendp(arp_request1, iface="enp0s3")
sendp(arp_request2, iface="enp0s3")
sendp(arp_request3, iface="enp0s3")
sendp(arp_request4, iface="enp0s3")

```

### 7. Get FTP files (from printserver to recorder)

### 8. Send DNS requests (from recorder)

`nslookup`
