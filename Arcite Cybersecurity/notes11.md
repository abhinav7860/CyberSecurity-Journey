# DNSDumpster, crt.sh & Shodan

## Basic Reconnaissance Notes

**Topic:** DNSDumpster, crt.sh and Shodan.io  
**Date Added:** 26 August 2026  
**Status:** Studied - Basic Level

---

## Why I Studied These

These are useful reconnaissance tools/services that can help collect information about a target before deeper security testing.

I mainly studied what each one does and how it can help during the information-gathering stage.

```text
DNSDumpster -> DNS and subdomain information
crt.sh      -> Certificate and subdomain information
Shodan      -> Internet-facing services and devices
```

---

# 1. DNSDumpster

## What is DNSDumpster?

DNSDumpster is a reconnaissance tool used to gather DNS-related information about a domain.

It can help find things like:

- Subdomains
- DNS records
- IP addresses
- Mail servers
- Name servers
- Related infrastructure

The main idea I understood is that DNS information can reveal parts of an organisation's infrastructure that aren't obvious from the main website.

## Basic Use

I can enter a domain into DNSDumpster and it will show information related to that domain.

For example:

```text
example.com
```

The results can contain:

```text
example.com
www.example.com
mail.example.com
api.example.com
```

This can give me a better picture of the target's external infrastructure.

## What I Learned

DNSDumpster is mainly useful during reconnaissance.

Instead of directly attacking anything, I can first collect publicly available DNS information and understand what systems and subdomains exist.

---

# 2. crt.sh

## What is crt.sh?

crt.sh is a website that allows me to search Certificate Transparency logs.

When websites use HTTPS certificates, information about those certificates can appear in Certificate Transparency logs.

Searching a domain on crt.sh can reveal domain names and subdomains that have appeared in certificates.

## Basic Search

I can search for a domain such as:

```text
example.com
```

The results may contain:

```text
example.com
www.example.com
api.example.com
dev.example.com
mail.example.com
```

This can sometimes reveal subdomains that I wouldn't find just by looking at the main website.

## Wildcard Search

A common search format is:

```text
%.example.com
```

This can help find certificates containing subdomains of the target domain.

## What I Learned

The main thing I understood about crt.sh is that SSL/TLS certificates can reveal useful information about an organisation's domains.

It is another passive reconnaissance source and can be useful together with DNS enumeration.

```text
DNSDumpster -> DNS information
crt.sh      -> Certificate information
```

---

# 3. Shodan.io

## What is Shodan?

Shodan is often described as a search engine for internet-connected devices and services.

Instead of searching normal web pages like Google, Shodan indexes information about publicly accessible systems and the services they expose.

It can show things such as:

- IP addresses
- Open ports
- Running services
- Server information
- Network devices
- IoT devices

## Basic Search

A simple search could be:

```text
apache
```

Shodan also supports filters to narrow results.

Some basic filters I studied are:

```text
country:IN
port:80
port:22
org:"Example Organisation"
hostname:example.com
```

The exact results depend on what Shodan has discovered publicly.

## Why Shodan is Useful

Shodan can help a security tester understand what an organisation is exposing to the internet.

For example:

```text
IP address
    ↓
Open port
    ↓
Service
    ↓
Service version
```

This information can then be used during an authorised security assessment to identify systems that need further investigation.

---

# Comparing the Three

I understood their main differences like this:

| Tool | Main Purpose |
|---|---|
| DNSDumpster | DNS and infrastructure reconnaissance |
| crt.sh | Certificate and subdomain discovery |
| Shodan | Internet-facing device/service discovery |

They can also complement each other:

```text
Target Domain
     |
     +---- DNSDumpster
     |       ↓
     |   DNS / subdomains
     |
     +---- crt.sh
     |       ↓
     |   Certificates / subdomains
     |
     +---- Shodan
             ↓
       Public services / devices
```

---

# Basic Recon Workflow

My basic understanding of using these tools together is:

```text
1. Start with the target domain
        ↓
2. Use DNSDumpster
        ↓
3. Collect DNS and subdomain information
        ↓
4. Check crt.sh
        ↓
5. Look for additional domain/subdomain information
        ↓
6. Check Shodan
        ↓
7. Look at publicly exposed services
        ↓
8. Organise the information
        ↓
9. Continue with authorised testing
```

The important part is that these tools help me gather information before deeper testing.

---

# What I Learned

The biggest thing I understood is that reconnaissance doesn't always mean immediately scanning a target.

A lot of useful information is already publicly available.

```text
DNSDumpster -> Helps understand DNS infrastructure
crt.sh      -> Helps discover domains through certificates
Shodan      -> Helps see publicly exposed services/devices
```

Using different sources together can give a much better picture of a target's external attack surface.

---

# My Takeaway

For now, I only studied the basics of these three tools.

I don't need to know every advanced filter or feature yet.

What matters to me at this stage is knowing:

- What DNSDumpster is used for
- How crt.sh can help find subdomains through certificates
- What Shodan searches for
- How these tools fit into reconnaissance
- Why publicly available information can be useful during a security assessment

These are mainly reconnaissance tools, so the information collected from them can be used as a starting point for further authorised testing.

---

## Important Note

I should only use these tools for:

- My own systems
- TryHackMe/CTF labs
- Training environments
- Security assessments where I have permission

Finding information about a public system does not automatically give me permission to test or attack it.

---

