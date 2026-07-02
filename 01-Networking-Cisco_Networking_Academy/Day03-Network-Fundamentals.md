# Day 3 - Home Network

Today I learned about home networks, wired and wireless technologies, and I also created my first home network using Cisco Packet Tracer.

---

## 1. Home Router Ports

A home router mainly has two types of ports.

### Ethernet (LAN) Port
- Used to connect devices inside the home network.
- Usually labeled as **LAN** or **Ethernet**.
- Devices like PCs, laptops, printers, and switches connect here.

### Internet (WAN) Port
- Used to connect the router to the Internet.
- Connects the home network to another network (ISP).

---

## 2. LAN Wireless Frequencies

### Bluetooth
- Uses the **2.4 GHz** frequency band.
- Suitable for short-range communication.
- Uses less power.
- Can connect multiple devices at the same time.

### Wi-Fi (IEEE 802.11)
- Uses **2.4 GHz** and **5 GHz** frequency bands.
- Provides a longer range than Bluetooth.
- Supports higher speeds and better throughput.

---

## 3. Wired Network Technologies

The most commonly used wired network technology is **Ethernet**.

Ethernet allows devices to communicate over a wired LAN.

### Category 5e (Cat5e)

- Most commonly used LAN cable.
- Contains four twisted pairs of wires.
- Twisted wires help reduce electrical interference.

### Coaxial Cable

- Has a single inner wire surrounded by insulation and a protective shield.
- Commonly used for cable TV and broadband connections.

### Fiber-Optic Cable

- Made of glass or plastic fibers.
- Can transmit data over long distances.
- Supports very high speed and high bandwidth.

---

## 4. Wireless Standards

The **IEEE 802.11** standard defines how Wi-Fi networks work.

Wi-Fi mainly operates on:
- 2.4 GHz
- 5 GHz

The **Wi-Fi Alliance** tests and certifies wireless devices from different manufacturers to make sure they work together properly.

---

## 5. Wireless Settings

When configuring a wireless router, some important settings are:

### Network Mode
Determines which Wi-Fi standard is used.

Examples:
- 802.11b
- 802.11g
- 802.11n
- Mixed Mode

### SSID (Service Set Identifier)

- The name of the Wi-Fi network.
- All devices must use the correct SSID to connect.
- SSID is case-sensitive.
- Maximum length is 32 characters.

### Standard Channel

- Determines the wireless channel used for communication.
- Usually set to **Auto**.

### SSID Broadcast

- Controls whether the Wi-Fi name is visible to nearby devices.
- Enabled by default.

---

## Cisco Packet Tracer Practice

Today I also practiced using **Cisco Packet Tracer**.

I created a simple home network and configured the basic wireless settings.

This helped me understand how:
- A router connects to different devices.
- Wired and wireless devices communicate.
- SSID is used to identify a wireless network.
- Basic home network configuration works.

---
## Communication Protocol

Protocols are the rules that govern communication between devices on a
network. They define how data is formatted, transmitted, received, and
processed.

Protocols include: - HTTP - TCP - IP - Ethernet

Protocols define: - Message format - Message size - Timing - Encoding -
Encapsulation - Message patterns

### Message Format

Every message must follow a specific structure or format.

### Message Size

The size of the transmitted data depends on the network and protocol
being used. Large data is divided into smaller pieces before
transmission.

### Timing

Timing controls how fast data is transmitted, when devices can send
data, and how much data can be sent.

### Encoding

Before transmission, data is converted into bits (0s and 1s). These bits
are then transmitted as electrical signals, light pulses, or radio waves
depending on the medium.

### Encapsulation

As data moves through the network layers, each layer adds its own header
containing important information such as source and destination
addresses.

### Message Pattern

Some protocols use a request-response communication pattern, while
others continuously stream data without waiting for acknowledgements.

------------------------------------------------------------------------

# Communication Standards

Communication standards ensure that different networking devices can
communicate using the same set of rules.

A standard: - Defines how networking devices should communicate. -
Allows devices from different manufacturers to work together. - Ensures
compatibility and reliable communication.

Internet standards are documented in RFC (Request for Comments)
documents and are maintained by organizations like the IETF.

------------------------------------------------------------------------

# Network Communication Models

Network communication is divided into layers so that each layer performs
a specific function independently.

Two common models are:

-   OSI Model
-   TCP/IP Model

## TCP/IP Model (4 Layers)

1.  Application
    -   Represents data to the user.
    -   Handles application services.
2.  Transport
    -   Provides end-to-end communication.
    -   Segments and reassembles data.
3.  Internet
    -   Determines the best path through the network.
    -   Handles logical addressing and routing.
4.  Network Access
    -   Includes the hardware and media used for network communication.

------------------------------------------------------------------------

# OSI Model (7 Layers)

The OSI (Open Systems Interconnection) Model is a reference model used
to understand network communication.

## Layer 7 -- Application

Provides network services directly to user applications.

## Layer 6 -- Presentation

Responsible for data formatting, encryption, compression, and
translation.

## Layer 5 -- Session

Establishes, manages, and terminates communication sessions.

## Layer 4 -- Transport

Segments, transfers, and reassembles data between devices.

## Layer 3 -- Network

Provides logical addressing and determines the best route for data.

## Layer 2 -- Data Link

Transfers data frames between devices on the same network.

## Layer 1 -- Physical

Handles the transmission of raw bits over physical media such as cables
or wireless signals.

---