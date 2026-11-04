# TRAFFIC INVESTIGATION REPORT

**Analyst:** Abhinav Sabu  
**Analysis Date:** 4 November 2026  
**Engagement:** Network Traffic Capture Investigation  
**Tool:** Wireshark  
**Methodology:** Orient → Question → Filter → Follow → Compare → Document

> **Documentation note:** This is an illustrative completed investigation based on a DNS-focused, ordinary web-traffic scenario. Capture-specific values and observations below are working assumptions, not verified measurements from an uploaded PCAP. They should not be represented as actual packet evidence until checked against the capture.

---

## 1. CAPTURE SUMMARY

**Source:** Public Wireshark sample capture – DNS and ordinary network communication (DNS-focused sample scenario).

**Total packets:** Not recorded; requires verification in the original PCAP.

**Time span:** Not recorded; requires verification using the first and last packet timestamps.

**Headline:**

The investigated traffic scenario represents ordinary network communication involving DNS queries, DNS responses and subsequent network connections. No confirmed indicators of malicious activity were identified in the illustrative investigation. The available observations do not establish the presence of a port scan, DNS tunnelling, beaconing or plaintext credential exposure.

---

## 2. ORIENTATION

### Top protocols (from Protocol Hierarchy)

The initial protocol assessment focused on identifying DNS, TCP, TLS and other supporting network protocols.

The working observations were:

- **DNS:** Used for domain-name resolution before connections to network services.
- **TCP:** Provided the transport layer for communication between hosts.
- **TLS:** Represented encrypted application communication.
- **UDP:** Supported DNS communication.
- **ARP:** Supported local network address resolution, where present.

The traffic profile was treated as consistent with ordinary web communication rather than an obvious attack pattern.

Exact packet counts and protocol percentages were not recorded.

### Busiest conversation (from Conversations, sorted by bytes)

The TCP and IPv4 Conversations tabs were selected to understand which hosts exchanged the most data.

The investigation focused on identifying the highest-volume communication and understanding whether the traffic represented ordinary client-server communication.

No verified source and destination IP addresses or byte totals were retained in the investigation notes.

### Notable endpoints (from Endpoints)

The endpoint assessment focused on identifying hosts communicating with multiple destinations and checking whether any destination appeared unusual.

No verified evidence of an endpoint exhibiting scanning behaviour or communicating with an unusually large number of destinations was recorded.

**Initial assessment:** No specific endpoint was established as malicious based on the available working observations.

---

## 3. INVESTIGATION

### Question chased

**What domains are being resolved through DNS, and does the DNS activity show any characteristics associated with suspicious communication or possible DNS-based data exfiltration?**

I selected DNS as the investigation thread because domain resolution provides useful context about subsequent network connections and can help identify unusual communication patterns.

### Filters used

The following Wireshark display filters were selected for the investigation:

**1. Identify DNS traffic**
```wireshark
dns
```

**2. Identify DNS queries**
```wireshark
dns.flags.response == 0
```

**3. Identify DNS responses**
```wireshark
dns.flags.response == 1
```

**4. Examine traffic associated with a particular host**
```wireshark
ip.addr == <target-ip>
```

**5. Identify TCP connection attempts**
```wireshark
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

**6. Examine TCP conversations**
```wireshark
tcp
```

The Follow TCP Stream feature was also used as an investigation technique to understand individual TCP conversations rather than examining isolated packets.

### What I found following the thread

The investigation focused on understanding the relationship between DNS queries, DNS responses and subsequent network communication.

In the illustrative scenario, DNS requests represented domain-resolution activity, while responses provided the corresponding resolution information. The investigation considered whether the queries contained unusually long or random-looking domain names, repeated requests, or patterns that could indicate DNS tunnelling.

The subsequent TCP communication was considered in context to understand how the resolved destinations were being accessed. No specific evidence of DNS tunnelling, suspicious domain generation or confirmed data exfiltration was established in this working scenario.

The investigation demonstrated how filtering and examining related network conversations can provide more useful context than analysing individual packets independently.

---

## 4. COMPARISON TO BASELINE

The traffic was assessed against the normal-traffic characteristics and attack patterns studied during the Networks track.

Working assessment:

- [x] Normal traffic – working scenario; not independently verified against the PCAP.
- [ ] Port scan signature observed.
- [ ] Suspicious DNS observed.
- [ ] Beacon pattern observed.
- [ ] Plaintext exposure observed.
- [ ] Other / unexplained.

### Evidence for the assessment

The investigation considered four common network attack indicators.

**1. Port scanning**

The filter:

```wireshark
tcp.flags.reset == 1
```

was identified as a useful way to examine TCP reset responses.

A potential port scan would require correlating connection attempts, destination ports, source addresses and responses. RST packets alone do not establish scanning activity.

No verified evidence of a single source systematically probing multiple destination ports was recorded.

**2. Suspicious DNS**

The filter:

```wireshark
dns
```

was used to examine DNS communication.

The assessment considered unusually long domain names, random-looking subdomains and repeated queries. No confirmed suspicious DNS pattern was established in the working scenario.

**3. Beaconing**

The Wireshark IO Graph was identified as a useful feature for examining traffic volume over time.

Regular, small connections to a single external destination could indicate beacon-like behaviour. However, a regular traffic pattern alone is insufficient to confirm command-and-control communication.

No verified beacon interval or suspicious recurring destination was documented.

**4. Plaintext exposure**

The following filter was considered:

```wireshark
http || ftp || telnet
```

These protocols can expose application data because they do not provide transport encryption by default.

The presence of unencrypted protocols would require further inspection to establish whether sensitive information was actually exposed. No confirmed credential exposure was documented.

---

## 5. VERDICT AND CONFIDENCE

**Verdict:** No confirmed malicious activity identified in the illustrative investigation scenario.

**Confidence:** PROBABLE (provisional).

### Reasoning

The working assessment is consistent with ordinary network communication involving DNS resolution and TCP-based connections. The investigation considered several common attack indicators, including port scanning, suspicious DNS activity, beaconing and plaintext exposure. However, the available investigation notes do not contain packet-level evidence establishing any of these behaviours. Therefore, there is insufficient justification to classify the traffic as malicious. The appropriate preliminary conclusion is that no suspicious activity was confirmed within the scope of the illustrative investigation. Confidence remains provisional because the original capture statistics, packet details and conversation evidence have not been independently verified.

---

## 6. RECOMMENDED NEXT STEPS

If this were a real security engagement, I would recommend:

- [x] Preserve the original PCAP and document its source, capture duration and packet count.
- [x] Retain the filters and investigation methodology to make the analysis reproducible.
- [ ] Examine additional DNS traffic to identify unusual query patterns and potentially suspicious domains.
- [ ] Correlate suspicious external IP addresses and domains with reputable threat-intelligence sources such as AbuseIPDB and VirusTotal.
- [ ] Review additional traffic from the same hosts to identify recurring connections or possible beaconing.
- [ ] Correlate network observations with endpoint and DNS server logs if investigating a suspected security incident.

**Priority:** No containment or blocking action is justified by the illustrative findings alone. Further investigation should be driven by newly identified evidence.

---

## INVESTIGATION REFLECTION

This investigation helped me understand that network traffic analysis is not simply about identifying unusual packets. It requires understanding the overall communication environment, developing a specific investigation question, applying appropriate filters, examining conversations and comparing observations against known network behaviour.

The most useful Wireshark feature in this workflow was **Protocol Hierarchy**, because it provides an initial understanding of the protocols present before narrowing the investigation.

If I had more time, I would investigate DNS communication further and correlate network observations with endpoint logs to identify whether any suspicious activity occurred outside the capture window.

Compared with the Day 26 Network Footprint Report, this investigation focused on a different aspect of network security:

- **Day 26 – Reconnaissance:** Understanding what information and services are exposed by a target.
- **Day 35 – Traffic Investigation:** Understanding how hosts communicate and whether their network behaviour indicates potential security issues.

I found traffic investigation particularly interesting because it required following actual communication and interpreting evidence rather than simply identifying exposed services.

**My main takeaway:** A good security analyst should not force an attack hypothesis onto network traffic. The conclusion must follow the evidence, even when the result is that no malicious activity was identified.

---

**END OF REPORT**  
