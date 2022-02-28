import time
import sys
from cryptography.fernet import Fernet
if len(sys.argv) < 2:
  print("Usage: <Program> <Amount of keys> > keys")
  exit()
for i in range(int(sys.argv[1])):
    print(Fernet.generate_key().decode())
