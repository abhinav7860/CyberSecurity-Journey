### ifconfig

Displays network interface information such as IP address, subnet mask, and MAC address.

**Syntax**

```bash
ifconfig
```

**Practical Example**

```bash
ifconfig eth0
```

Displays only the `eth0` interface.

**Tested Example**

While working in Kali Linux, I used:

```bash
ifconfig
```

to verify that my VM had received the IP address `10.0.2.15` before starting an Nmap scan.

---

### ip addr

Displays detailed information about all network interfaces.

**Syntax**

```bash
ip addr
```

**Practical Example**

```bash
ip addr show eth0
```

**Tested Example**

I used:

```bash
ip addr
```

to confirm that my Kali machine was using the IP address `10.0.2.15` before running `enum4linux` against my Metasploitable VM.

---

### hostname -I

Displays the local IP address.

**Syntax**

```bash
hostname -I
```

**Practical Example**

```bash
hostname -I
```

**Tested Example**

Before scanning my target VM, I checked my own IP using:

```bash
hostname -I
```

to make sure both machines were on the same VirtualBox network.

---

### ping

Checks whether a target host is reachable.

**Syntax**

```bash
ping <ip>
```

**Practical Example**

```bash
ping 8.8.8.8
```

**Tested Example**

I tested connectivity between Kali and Metasploitable using:

```bash
ping 10.0.2.15
```

and received replies, confirming that both machines could communicate.

---

### arp -a

Displays the ARP table containing IP-to-MAC address mappings.

**Syntax**

```bash
arp -a
```

**Practical Example**

```bash
arp -a
```

**Tested Example**

After pinging my target VM, I ran:

```bash
arp -a
```