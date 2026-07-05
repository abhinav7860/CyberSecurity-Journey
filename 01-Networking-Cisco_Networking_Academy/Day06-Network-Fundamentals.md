# Day 6 - Introduction to IPv6

# 1. Why do we need IPv6?

Think of an IP address like a **house address**.

Every device connected to the internet needs its own address.

Earlier, IPv4 gave addresses to computers, laptops and phones.

Now we have billions of devices like:

- Smartphones
- Smart TVs
- Smartwatches
- Cars
- Cameras
- IoT devices

There are simply **too many devices**.

IPv4 started running out of addresses.

So IPv6 was created.

### Easy Example

Imagine your school has only **100 lockers**.

But next year **500 students** join.

Now there aren't enough lockers for everyone.

Instead of making students share lockers, the school builds **millions of new lockers**.

That's exactly why IPv6 was created.

---

# 2. IPv4 vs IPv6

### IPv4

- 32-bit address
- Around **4.3 billion** addresses
- Getting exhausted

Example

```
192.168.1.10
```

### IPv6

- 128-bit address
- Around **340 undecillion** addresses 🤯
- Enough for the future

Example

```
2001:0db8:0000:1111:0000:0000:0000:0200
```

I don't need to memorize this address now.

I only need to understand the format.

---

# 3. Why not just keep using IPv4?

We tried.

One solution was **NAT**.

NAT allows many devices inside a home to share one public IP.

It helped for many years.

But as more and more devices came online, NAT alone wasn't enough.

IPv6 became the long-term solution.

---

# 4. IPv4 and IPv6 Together

The whole internet cannot change in one day.

So IPv4 and IPv6 work together for now.

There are three ways this happens.

### Dual Stack

A device runs both IPv4 and IPv6.

Think of a person who speaks both English and Malayalam.

He can talk to both groups.

---

### Tunneling

Imagine sending a small gift inside a bigger box.

The IPv6 packet is placed inside an IPv4 packet until it reaches the destination.

---

### NAT64 (Translation)

Think of Google Translate.

One person speaks English.

Another speaks Malayalam.

The translator helps them understand each other.

NAT64 does the same thing between IPv4 and IPv6.

---

# 5. Hexadecimal Numbers

IPv6 doesn't use only numbers like IPv4.

It uses **Hexadecimal**.

Hexadecimal has **16 values**.

```
0 1 2 3 4 5 6 7 8 9 A B C D E F
```

After 9 comes A instead of 10.

---

# 6. IPv6 Address Format

IPv6 is **128 bits** long.

It is divided into **8 parts**.

Each part is called a **Hextet**.

Example

```
2001:0db8:0000:1111:0000:0000:0000:0200
```

Each section has **4 hexadecimal digits**.

Unlike IPv4, IPv6 uses **colons (:)** instead of dots (.).

---

# 7. Rule 1 - Remove Leading Zeros

If a hextet starts with zeros, we can remove them.

Example

```
000A
```

becomes

```
A
```

Another example

```
0025
```

becomes

```
25
```

This makes IPv6 addresses easier to read.

---

# 8. Rule 2 - Double Colon (::)

If there are many groups containing only zeros, they can be replaced with **::**

Example

Instead of writing

```
2001:0db8:0000:0000:0000:0000:0000:0001
```

we can write

```
2001:db8::1
```

This makes the address much shorter.

**Note:** We can use **::** only **once** in an IPv6 address.

---

