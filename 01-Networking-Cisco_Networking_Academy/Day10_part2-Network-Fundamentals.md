# Day 10 - Network Troubleshooting Commands


# 1. Network Troubleshooting Flow

When a network issue occurs, I learned to troubleshoot in this order:

```
Check IP Configuration
        ↓
Check Connectivity (Ping)
        ↓
Check Active Connections
        ↓
Trace the Route
        ↓
Verify DNS Resolution
```

---

# 2. ipconfig

Displays the current IP configuration of the device.

```cmd
ipconfig
```

Example:

```cmd
C:\> ipconfig

IPv4 Address : 192.168.1.10
Subnet Mask  : 255.255.255.0
Default Gateway : 192.168.1.1
```

Used to verify:

- IP Address
- Subnet Mask
- Default Gateway

---

# 3. ipconfig /all

Displays detailed network information.

```cmd
ipconfig /all
```

Shows:

- MAC Address
- DHCP Status
- DNS Server
- Lease Information
- Gateway

Useful when troubleshooting incorrect network configurations.

---

# 4. ipconfig /release

Releases the current DHCP-assigned IP address.

```cmd
ipconfig /release
```

Used before requesting a new IP address.

---

# 5. ipconfig /renew

Requests a new IP address from the DHCP server.

```cmd
ipconfig /renew
```

Useful when the current IP configuration is invalid or outdated.

---

# 6. ping

Tests whether another device is reachable over the network.

```cmd
ping 192.168.1.1
```

or

```cmd
ping google.com
```

Successful output:

```
Reply from 192.168.1.1
```

If it fails, common messages include:

- Request timed out
- Destination host unreachable
- General failure

---

# 7. How Ping Works

```
Computer A
      │
Echo Request
      │
Computer B
      │
Echo Reply
      │
Computer A
```

If the reply returns, the connection is working.

---

# 8. Ping Troubleshooting

If pinging an IP works but pinging a domain fails:

```
Ping 8.8.8.8 ✅
Ping google.com ❌
```

The issue is most likely DNS.

If pinging the default gateway fails:

```
ping 192.168.1.1
```

The problem is usually on the local network.

If both gateway and internet fail, check:

- Cable/Wi-Fi connection
- Router
- DHCP configuration
- Firewall

---

# 9. netstat

Shows active network connections.

```cmd
netstat
```

Useful for checking:

- Established connections
- Listening ports
- Active sessions

---

# 10. tracert

Shows every router (hop) a packet passes through to reach the destination.

```cmd
tracert google.com
```

Example:

```
PC
 ↓
Router
 ↓
ISP
 ↓
Internet
 ↓
Google
```

Helpful for locating where a connection fails.

---

# 11. nslookup

Queries a DNS server to resolve a domain name into its IP address.

```cmd
nslookup google.com
```

Example:

```
Name: google.com
Address: 142.250.xxx.xxx
```

Useful for troubleshooting DNS issues.

---

# Commands Practiced

```cmd
ipconfig
ipconfig /all
ipconfig /release
ipconfig /renew
ping 192.168.1.1
ping google.com
netstat
tracert google.com
nslookup google.com
```

---

