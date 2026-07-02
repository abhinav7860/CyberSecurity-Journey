# Day 4 - Network Communication

Today I learned how devices communicate inside a network, how switches work, and how data is sent from one device to another using encapsulation.

---

## 1. Access Layer

The **Access Layer** is where end devices like computers, laptops, and printers connect to the network.

Earlier, Ethernet hubs were used to connect devices, but they had a major problem.

### Ethernet Hub

- Can send only one message at a time.
- If two devices send data together, a collision occurs.
- Too many collisions slow down the network.
- Hubs are now mostly replaced by switches.

---

## 2. Ethernet Switch

An **Ethernet Switch** works at **Layer 2 (Data Link Layer)** of the OSI Model.

The switch reads the **MAC Address** of the destination device and forwards the data only to that specific device.

This makes communication much faster and avoids collisions.

### MAC Address Table

A switch maintains a **MAC Address Table**.

It stores:
- Device MAC Address
- Port number where the device is connected

Whenever a new device sends data, the switch automatically learns its MAC address and updates the table.

---

## 3. Encapsulation

When data is sent through a network, it follows a specific format.

This process is called **Encapsulation**.

A good example is sending a letter.

- The letter is placed inside an envelope.
- The envelope contains the sender's and receiver's address.

Similarly, in networking:
- Data is placed inside a **Frame**.
- The frame contains the source and destination addresses.

Without proper formatting, the data cannot reach the correct destination.

---

## 4. De-encapsulation

When the receiver gets the frame, it removes the outer information and reads the actual data.

This process is called **De-encapsulation**.

Just like opening an envelope and reading the letter inside.

---

## 5. Frame

Before data is transmitted over a network, it is packed into a **Frame**.

A frame contains:
- Source Address
- Destination Address
- Actual Data
- Control Information

The frame helps the data reach the correct device.

---

## 6. Internet Protocol (IP)

Internet Protocol (IP) works like the address written on an envelope.

It helps identify:
- Source device
- Destination device

Without an IP address, data cannot be delivered to the correct destination.

---
