# WiFi Hacking 101 --- Detailed Study Notes

**Platform:** TryHackMe\
**Study date:** 10 November 2026\
**Scope:** Task 1 --- The Basics: An Intro to WPA; Task 2 --- You're
Being Watched: Capturing Packets to Attack; practical notes supplied for
Task 2\
**Focus:** Wireless security, ethical testing, and SOC awareness

> Based on the lesson text and practical notes supplied. The practical
> section records the reported troubleshooting and workflow. No
> additional lab result or recovered password is assumed.

------------------------------------------------------------------------

## Task 1 --- The Basics: An Introduction to WPA

### 1. Key wireless terms

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  **SSID**                            The wireless network name displayed
                                      when looking for a Wi-Fi network.

  **ESSID**                           An extended service set identifier.
                                      It may represent a network name
                                      shared across multiple access
                                      points, such as in an office.
                                      Aircrack-ng material often uses
                                      ESSID to refer to the network being
                                      tested.

  **BSSID**                           The MAC address identifying a
                                      particular wireless access
                                      point/radio.

  **WPA2-PSK**                        WPA2 Personal authentication using
                                      a pre-shared password shared by
                                      users of the network.

  **WPA2-EAP**                        Enterprise-style authentication
                                      using credentials and an
                                      authentication server, commonly
                                      RADIUS.

  **RADIUS**                          A centralized authentication
                                      service used by network access
                                      technologies, including enterprise
                                      Wi-Fi.
  -----------------------------------------------------------------------

**Remember:** SSID/ESSID identifies the network name; BSSID identifies a
particular access point.

### 2. WPA Personal and WPA Enterprise

-   **WPA2-Personal (PSK):** A user joins by supplying a shared Wi-Fi
    password.
-   **WPA2-Enterprise (EAP):** A user authenticates with individual
    credentials, with authentication handled through infrastructure such
    as a RADIUS server.

A username-and-password prompt may indicate an enterprise network, while
a shared network password is typical of personal Wi-Fi. This is a rule
of thumb, not a guarantee; verify the actual configuration.

### 3. The WPA four-way handshake

The four-way handshake is central to WPA/WPA2 key establishment. It
allows the client (station) and access point to demonstrate possession
of the necessary key material and derive session keys without
transmitting the Wi-Fi password in plaintext.

The practical notes describe the four messages at a high level:

1.  The access point sends an **ANonce** (authenticator nonce).
2.  The client responds with an **SNonce** (supplicant nonce) and a
    **MIC** (message integrity code).
3.  The access point sends key-installation information.
4.  The client acknowledges key installation.

Important points: - The handshake does **not** reveal the Wi-Fi password
in plaintext. - A captured handshake can provide information used to
test password guesses offline. - The handshake is part of authentication
and key establishment, not a file containing the password.

### 4. How the network name relates to key derivation

The lesson explains that WPA key derivation uses both the network
password and the ESSID. The ESSID acts as a salt, so the same password
used on networks with different ESSIDs produces different derived key
material.

This makes precomputation specific to the network name. An attacker
testing a password list generally needs to perform the relevant
calculations for the target network rather than rely on one universal
precomputed result.

### 5. WEP compared with WPA

The lesson notes that **WEP (Wired Equivalent Privacy)** was an older
wireless security standard and is considered insecure. Its weaknesses
allowed attackers to recover keys through statistical analysis after
collecting sufficient wireless traffic.

WPA/WPA2 use a different authentication and key-establishment approach.
The lesson focuses on attacks against WPA/WPA2 that use captured
handshake information and password candidates.

------------------------------------------------------------------------

## Task 2 --- You're Being Watched: Capturing Packets to Attack

### 1. Aircrack-ng suite

Aircrack-ng is a collection of wireless security auditing tools. The
lesson lists these components:

`aircrack-ng`, `airdecap-ng`, `airmon-ng`, `aireplay-ng`, `airodump-ng`,
`airtun-ng`, `packetforge-ng`, `airbase-ng`, `airdecloak-ng`,
`airolib-ng`, `airserv-ng`, `buddy-ng`, `ivstools`, `easside-ng`,
`tkiptun-ng`, and `wesside-ng`.

The lesson focuses particularly on `airmon-ng`, `airodump-ng`, and
`aircrack-ng`; the practical notes also discuss `aireplay-ng`.

  -----------------------------------------------------------------------
  Tool                                Role described in the
                                      lesson/practical notes
  ----------------------------------- -----------------------------------
  `airmon-ng`                         Helps enable monitor mode on a
                                      compatible wireless adapter.

  `airodump-ng`                       Discovers wireless networks and
                                      captures wireless packets.

  `aircrack-ng`                       Tests password candidates against
                                      captured WPA handshake data.

  `aireplay-ng`                       Supports packet injection,
                                      including deauthentication testing.
  -----------------------------------------------------------------------

The suite is available on Kali Linux or can be installed using a package
manager or the [official Aircrack-ng
website](https://www.aircrack-ng.org/).

### 2. Wireless adapter requirements

The lesson emphasizes that packet capture for this exercise requires a
wireless network interface capable of **monitor mode**. Not every
wireless adapter supports it.

The practical notes explain that packet injection can be useful in a
controlled lab. The lesson describes deauthentication as a way to cause
a client to disconnect and reconnect, potentially producing another
handshake capture. Otherwise, a tester may need to wait for a normal
client connection.

Only perform packet injection or deauthentication tests on equipment and
networks you own or are explicitly authorized to assess. These actions
can disrupt connectivity.

### 3. Managed mode and monitor mode

-   **Managed mode:** The wireless adapter behaves as a normal client
    and connects to an access point.
-   **Monitor mode:** A compatible adapter can observe wireless frames
    in range, including frames not specifically addressed to that
    adapter.

The practical notes show this example for enabling monitor mode:

``` bash
sudo airmon-ng start wlan0
```

The interface may be renamed, for example:

``` text
wlan0mon
```

The exact interface name depends on the adapter, driver, and system.

### 4. Interfering network processes

Network-management processes can interfere with monitor mode by
controlling the wireless adapter, changing its channel, or switching it
back to managed mode.

The practical notes record:

``` bash
sudo airmon-ng check kill
```

It identifies and stops processes that may interfere. Stopping
network-management services can disconnect the machine from Wi-Fi or
interrupt networking. Use it only in a controlled lab and understand how
to restore normal networking afterward.

### 5. Discovering wireless networks

The practical notes use:

``` bash
sudo airodump-ng wlan0mon
```

This displays wireless networks visible to the adapter.

  -----------------------------------------------------------------------
  Field                               Meaning
  ----------------------------------- -----------------------------------
  **BSSID**                           MAC address of the access point.

  **ESSID**                           Wireless network name.

  **PWR**                             Signal-strength indicator reported
                                      by the tool.

  **CH**                              Wireless channel.

  **Encryption**                      Security/encryption information
                                      reported for the network.
  -----------------------------------------------------------------------

The practical notes identify two options: - `-bssid` --- selects a
particular access point by its BSSID. - `-w` --- specifies the output
capture-file prefix.

### 6. BSSID versus ESSID in practice

The practical notes recorded this BSSID:

``` text
02:1A:11:EF:D9:BD
```

It is an example access-point MAC address from the supplied notes.

-   **BSSID:** identifies a particular access point.
-   **ESSID:** identifies the wireless network name.

A network name can be shared by multiple access points, so identifying a
particular BSSID helps distinguish one access point from another.

### 7. Wordlists and dictionary attacks

A **wordlist** is a collection of candidate passwords. The lesson
suggests using a controlled hotspot with a deliberately weak test
password selected from `rockyou.txt`.

The common Kali path is:

``` text
/usr/share/wordlists/rockyou.txt
```

The practical notes explain:

``` bash
head /usr/share/wordlists/rockyou.txt -n 10000 | shuf -n 5 -
```

-   `head -n 10000` --- outputs the first 10,000 lines.
-   `shuf` --- randomizes the input lines.
-   `-n 5` --- selects five lines.
-   The final `-` tells `shuf` to read input from standard input.

This produces five randomly selected candidates from the first 10,000
entries. It is a small demonstration subset, not a comprehensive
password audit.

### 8. Offline dictionary attack concept

The practical notes give this general command structure:

``` bash
aircrack-ng -w <wordlist> -b <BSSID> <capture-file>
```

  Argument       Purpose
  -------------- ---------------------------------------------------
  `-w`           Specifies the wordlist.
  `-b`           Specifies the target access point BSSID.
  Capture file   Supplies captured wireless handshake/packet data.

An **offline dictionary attack** tests password candidates against
captured authentication data without repeatedly attempting to log in to
the access point. If a candidate matches, the tool can report that the
key was found.

The command is included to explain the syntax from the supplied notes.
Use it only with capture files and networks that are yours or that you
have explicit permission to test.

------------------------------------------------------------------------

## Practical Notes --- Troubleshooting the Wireless Interface

### 1. The initial monitor-mode error

The practical notes record that:

``` bash
sudo airmon-ng start wlan0
```

returned:

``` text
Requested device "wlan0" does not exist.
```

This indicated that the expected wireless interface was not present
under that name.

### 2. Commands used to investigate

``` bash
ip -br link
lsusb
lspci | grep -i network
```

Recorded findings: - `eth0` was available as a virtual Ethernet
interface. - No wireless adapter was detected. - No physical wireless
PCI device was visible.

### 3. Why the VirtualBox setup mattered

Kali was running inside VirtualBox. The virtual Ethernet interface
provided by the virtual machine did not expose the wireless hardware
functions needed for monitor mode.

The practical lesson was that wireless monitor-mode capture requires a
compatible wireless adapter to be made available to the environment. In
a VirtualBox lab, this commonly means a supported USB Wi-Fi adapter
passed through to the virtual machine.

**Important distinction:** A virtual Ethernet interface is not the same
thing as a wireless adapter. Seeing `eth0` does not mean the VM can
perform wireless monitor-mode capture.

### 4. Continuing with a provided capture

Although the local VM did not detect a wireless adapter, the practical
notes say the password-testing stage could continue using a capture file
and the TryHackMe AttackBox environment.

This demonstrates that wireless packet acquisition and offline analysis
are separate stages: a tester does not need to capture packets on the
same machine that later analyzes the capture.

------------------------------------------------------------------------

## Practical Notes --- Working with the Provided Capture File

### 1. Initial file error

The notes record an attempt to run:

``` bash
aircrack-ng -w /usr/share/wordlists/rockyou.txt NinjaJc01-01.cap
```

The terminal returned:

``` text
Failed to open 'NinjaJC01-01.cap'
No such file or directory
```

The issue was the filename and working directory.

### 2. Locating the file

The notes show navigating to Downloads:

``` bash
cd ~/Downloads
ls
```

The actual filename was:

``` text
NinjaJc01-01.cap
```

Linux filenames are case-sensitive. Therefore, `NinjaJC01-01.cap` and
`NinjaJc01-01.cap` are different names.

The practical notes state that the command was corrected using the
actual filename/path and that the cracking process identified WPA
handshake data and tested candidates from the RockYou wordlist.

**Source limitation:** The supplied notes do not include the final
recovered password or complete terminal output. This README therefore
does not state a password or invent a `KEY FOUND!` result.

### 3. General troubleshooting lessons

-   Check the current directory with `pwd`.
-   List files with `ls`.
-   Copy the exact filename, including capitalization.
-   Confirm the capture file exists before running analysis.
-   Separate adapter/interface problems from capture-file path problems;
    they are different issues.

------------------------------------------------------------------------

## SOC Analyst Perspective

Understanding wireless attack techniques also helps a defensive analyst
recognize suspicious activity.

The supplied practical notes identify these behaviors as worth
investigating: - Repeated wireless deauthentication frames. - Unexpected
client disconnections. - Unusual authentication activity. - Rogue
wireless access points. - Suspicious wireless reconnaissance.

These observations are investigative leads, not automatic proof of an
attack. A SOC analyst should correlate them with access-point/controller
logs, endpoint reports, known maintenance activity, and affected users
or locations.

### Defensive questions to ask

1.  Are multiple clients disconnecting from the same access point?
2.  Did the disconnections begin suddenly or follow a known maintenance
    event?
3.  Is an unfamiliar access point advertising a network name similar to
    the organization's?
4.  Are there repeated authentication failures or unusual connection
    patterns?
5.  Can wireless infrastructure logs confirm the observed activity?

------------------------------------------------------------------------

## Important Concepts --- Quick Revision

  -----------------------------------------------------------------------
  Concept                             What I learned
  ----------------------------------- -----------------------------------
  SSID                                The displayed wireless network
                                      name.

  ESSID                               Network identifier that may apply
                                      across multiple access points.

  BSSID                               MAC address identifying a
                                      particular access point.

  WPA2-PSK                            Personal Wi-Fi authentication using
                                      a shared pre-shared key.

  WPA2-EAP                            Enterprise authentication using an
                                      authentication infrastructure such
                                      as RADIUS.

  RADIUS                              Centralized authentication service.

  Four-way handshake                  WPA/WPA2 key-establishment exchange
                                      between client and access point.

  ANonce / SNonce                     Nonces exchanged during the
                                      handshake.

  MIC                                 Message integrity code used in
                                      handshake messages.

  Monitor mode                        Wireless interface mode for
                                      observing wireless frames.

  Packet capture                      Recording wireless packets/frames
                                      for later analysis.

  Wordlist                            Collection of candidate passwords.

  Dictionary attack                   Testing candidate passwords against
                                      captured authentication data.

  Offline cracking                    Testing candidates against captured
                                      data without repeatedly logging in
                                      to the access point.

  Packet injection                    Transmitting crafted wireless
                                      frames.

  Deauthentication                    A frame/action that can disconnect
                                      a wireless client.
  -----------------------------------------------------------------------

## Self-Test Questions

1.  What is the difference between SSID/ESSID and BSSID?
2.  What is the difference between WPA2-PSK and WPA2-EAP?
3.  What role does a RADIUS server play?
4.  What is the purpose of the WPA four-way handshake?
5.  Does a captured handshake reveal the Wi-Fi password in plaintext?
6.  Why does the ESSID matter in WPA key derivation?
7.  Why is WEP considered insecure?
8.  What is the difference between managed mode and monitor mode?
9.  Which Aircrack-ng tool is used to enable monitor mode?
10. Which tool is used to discover networks and capture packets?
11. What does the `-b` option specify in the practical command
    structure?
12. What does the `-w` option specify?
13. Why might `wlan0` be missing inside a virtual machine?
14. Why are exact filename capitalization and working directory
    important in Linux?
15. What is an offline dictionary attack?
16. Name three wireless behaviors a SOC analyst may investigate.

## My Key Takeaways

-   I learned the difference between SSID/ESSID and BSSID and why an
    access point's BSSID is useful when identifying a specific target.
-   I understood the difference between personal WPA2-PSK authentication
    and enterprise WPA2-EAP authentication.
-   I learned that the WPA four-way handshake does not expose the
    password directly, but captured handshake information can support
    offline password testing.
-   I became familiar with the Aircrack-ng tools used in the lesson:
    `airmon-ng`, `airodump-ng`, `aircrack-ng`, and `aireplay-ng`.
-   I understood why a compatible wireless adapter and monitor-mode
    support are necessary for wireless packet capture.
-   I troubleshot a missing `wlan0` interface and learned that a
    VirtualBox virtual Ethernet adapter does not provide wireless
    monitor-mode functionality.
-   I learned to troubleshoot missing capture files by checking the
    working directory and exact case-sensitive filename.
-   I connected wireless attack concepts to defensive monitoring,
    including deauthentication activity, suspicious authentication, and
    rogue access points.

## Practice Checklist

-   [ ] Explain SSID, ESSID, and BSSID in my own words.
-   [ ] Compare WPA2-PSK and WPA2-EAP.
-   [ ] Explain the four-way handshake at a high level.
-   [ ] Explain why a handshake capture does not contain the password in
    plaintext.
-   [ ] Identify the roles of the main Aircrack-ng tools.
-   [ ] Explain monitor mode and its hardware requirements.
-   [ ] Explain why a VirtualBox virtual Ethernet adapter is
    insufficient for monitor-mode capture.
-   [ ] Troubleshoot a missing interface and a missing capture file.
-   [ ] Describe the difference between online login attempts and
    offline password testing.
-   [ ] Identify wireless behaviors that may warrant SOC investigation.

## Safety and Authorization

Wireless testing can affect other users' connectivity and privacy.
Perform packet capture, injection, deauthentication, and password
testing only on networks and devices you own or have explicit permission
to assess. Use an isolated lab or the authorized TryHackMe environment.

## Source and Scope

Based on the user's supplied TryHackMe **WiFi Hacking 101** material and
practical notes, including Task 1 concepts and Task 2 tool
usage/troubleshooting. The supplied material includes a heading for Task
3 but no separate Task 3 lesson content; no additional Task 3 material
has been inferred. The final recovered password and complete cracking
output were not supplied and are intentionally not invented.

