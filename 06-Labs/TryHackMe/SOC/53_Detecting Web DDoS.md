# Detecting Web DDoS — SOC L1 Study Notes

**Date:** 30 September 2026  
**Source:** TryHackMe — Detecting Web DDoS  
**Focus:** SOC / Blue Team / Web Attack Detection

---

## 1. Introduction

A **Denial-of-Service (DoS)** attack attempts to make a website or application unavailable to legitimate users.

A **Distributed Denial-of-Service (DDoS)** attack does the same thing, but uses many systems at the same time.

The main security objective being attacked is **Availability** in the CIA triad.

This room focuses mainly on **application-layer (Layer 7)** web attacks.

### Simple idea

Think of a restaurant:

- Normal traffic = customers entering at a manageable rate.
- DoS = one person repeatedly occupying tables and overwhelming staff.
- DDoS = thousands of people arriving together and overwhelming the restaurant.

The important SOC question is not simply "Are there many requests?"

It is:

> Is the traffic pattern abnormal, what resource is being targeted, and is the service actually being affected?

---

# 2. DoS and DDoS

## 2.1 Denial-of-Service (DoS)

A DoS attack attempts to prevent a web service from functioning normally.

A single attacker-controlled system may send:

- Large numbers of requests
- Repeated requests to expensive endpoints
- Specially crafted requests
- Malformed input that causes application processing problems
- Large requests that consume server resources

### Example

Suppose a website has:

`/search`

The endpoint receives a search term, queries a database, and returns results.

If the application is poorly designed, an attacker may repeatedly request an expensive search operation.

The important point is that not every HTTP request costs the server the same amount of resources.

---

## 2.2 Distributed Denial-of-Service (DDoS)

A DDoS attack distributes traffic across many systems.

Attackers may control a **botnet**, a collection of compromised:

- Computers
- Servers
- IoT devices
- Other internet-connected systems

The attacker instructs these systems to send traffic toward the target.

### Why distribution matters

One machine has limited CPU, memory, bandwidth, and request-generation capacity.

Thousands of machines can generate much more traffic.

| DoS | DDoS |
|---|---|
| Usually one attacking source | Multiple distributed sources |
| Often smaller scale | Can reach very large scale |
| Easier to associate with one source | Sources may be widely distributed |
| Can still cause serious disruption | Can create extremely high traffic volume |

---

# 3. Application-Layer / Layer 7 Focus

The room focuses on the **application layer**, specifically web applications.

Layer 7 traffic includes application behavior such as HTTP/HTTPS and web API requests.

A Layer 7 DDoS can look similar to legitimate web traffic because attackers may send normal-looking HTTP requests.

Therefore:

> A Layer 7 DDoS is not necessarily obvious from malformed packets. The behavior and volume of application requests matter.

---

# 4. Attack Motives

Possible motives described in the room include:

## Financial Loss

Disrupt services and reduce sales or revenue.

## Extortion

Demand payment to stop an attack.

## Hacktivism

Use disruption as a form of social or political protest.

## Distraction

Draw defenders' attention while other activity takes place.

## Competition

Disrupt a rival's service.

## Denial of Wallet

Cause increased cloud or service usage costs.

## Reputational Damage

Cause customers to lose confidence after an outage.

---

# 5. Real-World Examples Mentioned

## BBC — 2015

The source describes a DDoS attack against the BBC on New Year's Eve 2015. The website became unavailable and users experienced timeouts and internal errors.

## Microsoft — 2023

The source describes a large Layer 7 DDoS affecting Microsoft services including Azure, OneDrive, and Outlook. Techniques mentioned include HTTP flooding and Slowloris.

---

# 6. Log-Based Detection

Web server logs are an important source of evidence.

Common servers include:

- Apache
- NGINX
- Microsoft IIS

Useful fields can include:

- Client IP
- Timestamp
- HTTP method
- Requested URI
- Status code
- Response size
- User-Agent
- Referrer

The SOC analyst should look for **patterns**, not isolated events.

---

# 7. Important DDoS Indicators

## High Request Rate

Example:

`10.10.10.100 → 1000 GET /login`

A sudden large number of requests may indicate automation.

However, high traffic does not automatically mean an attack because legitimate events can also create traffic spikes.

## Odd User-Agents

Examples:

- `curl/7.6.88`
- `Python-urllib/3.x`

These can indicate automation, but User-Agent strings can be changed and should not be treated as proof.

## Geographic Anomalies

A globally distributed pattern can be consistent with botnet traffic, but legitimate organizations may also have users worldwide.

## Burst Timestamps

Example:

`50 requests in 1 second → /search`

A sudden burst can indicate scripted activity.

## 5xx Server Errors

Examples:

- `500 Internal Server Error`
- `502 Bad Gateway`
- `503 Service Unavailable`

A sudden increase can indicate that the application is struggling.

The strongest signal comes from correlation:

**Traffic spike + resource pressure + increased 5xx errors + user impact**

---

# 8. Logic Abuse

Not every DoS requires enormous traffic.

An attacker can use requests designed to consume excessive resources.

Example:

`GET /products?limit=999999`

If the application processes an extremely large result set, even a relatively small number of requests could consume significant resources.

Important lesson:

> **Request cost matters, not only request count.**

---

# 9. Targeted Resources

Attackers may target endpoints that require significant server-side processing.

### `/login`

May involve authentication, password verification, database queries, and session creation.

### `/search`

May involve database queries, filtering, sorting, and large result sets.

### `/api`

APIs often provide critical dynamic functionality.

### `/register` or `/signup`

May involve database writes and validation.

### `/contact` or `/feedback`

May write database records or trigger email processing.

### `/cart` or `/checkout`

May involve sessions, inventory, pricing, payment processing, and database operations.

Therefore, an attacker may deliberately target expensive endpoints rather than static files.

---

# 10. Example Attack Sequence

A simplified sequence:

1. **Normal traffic** — users access the website normally.
2. **Attack begins** — repeated requests target an endpoint such as `/login.php`.
3. **Resource pressure** — response times increase and infrastructure becomes stressed.
4. **Service degradation** — 5xx responses increase.
5. **User impact** — legitimate users cannot access the service.

Mental model:

**Normal → Traffic spike → Resource pressure → 5xx errors → Availability failure**

---

# 11. SIEM Detection

A SIEM makes DDoS investigation easier by centralizing logs and allowing analysts to aggregate fields.

Useful fields include:

- `clientip`
- `useragent`
- URI/path
- HTTP method
- Status code
- Timestamp

The TryHackMe exercise uses **Splunk** and begins with:

`index="main"`

An analyst can then investigate traffic patterns using extracted fields.

---

# 12. Splunk Investigation Mindset

Ask these questions:

### How many requests occurred?

Determine whether request volume suddenly increased.

### Which endpoint was targeted?

For example:

`/login.php`

### Which IPs generated the traffic?

Look for one dominant source or many distributed sources.

### Which User-Agents were used?

Look for unusual or automated clients.

### Did server errors increase?

Check for 5xx responses.

### When did the attack begin?

Build a timeline.

### What happened to legitimate users?

Determine whether availability was actually affected.

---

# 13. Time-Series Analysis

A timechart can make an attack visible quickly.

Normal traffic may show relatively stable request volume.

A DDoS may appear as a sudden spike:

```text
Requests
  |
  |                 ███████████████
  |                 ███████████████
  |                 ███████████████
  |_________________███████████████___ Time
```

This demonstrates why **baselining** is important.

---

# 14. Application-Level Defense

## Secure Development Practices

Applications should prevent requests from unnecessarily consuming unlimited resources.

Important controls include:

- Input validation
- Request-size limits
- Pagination
- Query limits
- Timeouts
- Efficient database queries
- Authentication controls
- Rate limiting

---

# 15. CAPTCHA and Challenges

Challenges can help distinguish automated traffic from legitimate users.

Examples:

- CAPTCHA
- JavaScript challenges
- Other bot-detection mechanisms

Basic model:

**Suspicious request → Challenge → Verify → Allow or deny**

---

# 16. CDN Protection

A **Content Delivery Network (CDN)** distributes content through edge servers.

Instead of every request reaching the origin:

**User → CDN Edge → Origin**

the CDN can serve cached content directly.

Benefits include:

- Reduced origin load
- Lower latency
- Traffic distribution
- DDoS mitigation
- Better traffic visibility

---

# 17. Caching

If a page such as:

`/products`

is cached at the CDN edge, repeated requests may be served without repeatedly querying the origin.

This reduces origin-server load.

Dynamic endpoints may be harder to cache effectively.

---

# 18. Web Application Firewall (WAF)

A WAF examines web requests and can:

- Allow
- Block
- Challenge

requests based on configured rules and security intelligence.

A WAF can help protect against:

- Malicious request patterns
- Automated abuse
- Known attack indicators
- Excessive request rates

---

# 19. Rate Limiting

Rate limiting restricts how frequently a client can access a resource.

Example:

`/login.php → maximum 5 requests per minute per IP`

When the limit is exceeded, the system may:

- Block
- Temporarily restrict
- Challenge
- Delay requests

Rate limiting is particularly useful for sensitive or expensive endpoints.

---

# 20. Large-Scale Mitigation

Large providers can use globally distributed networks to absorb and filter traffic.

The source describes the use of:

- Distributed infrastructure
- Traffic filtering
- Load balancing
- Global edge networks

Large-scale DDoS protection is therefore a combination of detection, filtering, distribution, and capacity.

---

# 21. Bypassing Security Measures

Attackers may attempt to bypass CDN and WAF controls.

## Random Query Parameters

Instead of:

`/products`

an attacker may request:

`/products?a=abcd`

and then:

`/products?a=efgh`

Depending on CDN configuration, unique URLs can reduce the effectiveness of caching and force more requests toward the origin.

## Changing User-Agents

Attackers may rotate User-Agent strings.

Therefore, User-Agent filtering should not be the only defense.

## Changing Referrers

Attackers may vary or spoof referrer information.

## Geographic Distribution

Distributed traffic from many regions can make simple geographic blocking less effective.

---

# 22. SOC Investigation Workflow

## Step 1 — Confirm the Alert

Determine:

- What triggered it?
- When did it happen?
- Which service is affected?

## Step 2 — Establish a Baseline

Compare current traffic with normal behavior.

## Step 3 — Identify the Target

Look for endpoints such as:

- `/login`
- `/search`
- `/api`
- `/register`
- `/cart`
- `/checkout`

## Step 4 — Analyze Request Volume

Determine:

- Requests per second
- Requests per minute
- Requests per source
- Requests per endpoint

## Step 5 — Analyze Source Distribution

Check:

- Source IPs
- Geographic distribution
- Internal vs external sources
- Network ownership if available

## Step 6 — Analyze User-Agents

Identify automated or unusual clients.

## Step 7 — Check HTTP Status Codes

Look for changes in:

- 2xx
- 4xx
- 5xx

Especially increased 5xx responses.

## Step 8 — Correlate Infrastructure Telemetry

Check:

- CPU
- Memory
- Network utilization
- Database utilization
- Application latency
- Connection counts

## Step 9 — Determine Impact

Ask:

> Are legitimate users actually experiencing degradation?

## Step 10 — Check Defensive Controls

Determine whether:

- CDN protection is active
- WAF rules are triggering
- Rate limits are triggering
- Load balancers are functioning

## Step 11 — Build a Timeline

Example:

`10:00 — Normal`

`10:01 — Traffic spike`

`10:02 — /login targeted`

`10:03 — CPU increases`

`10:04 — 503 responses increase`

`10:05 — Users report service unavailable`

## Step 12 — Document the Incident

Record:

- Start/end time
- Target
- Source IPs
- Request volume
- Targeted endpoints
- Error rates
- User impact
- Mitigation
- Evidence

---

# 23. Important SOC Lessons

## High traffic does not automatically mean DDoS

Traffic can increase because of legitimate events such as product launches, news, or seasonal demand.

## One IP does not automatically mean DoS

The IP could represent a corporate proxy, NAT gateway, testing system, or another legitimate shared source.

## Many IPs do not automatically mean DDoS

A global website naturally has users from many regions.

### What matters?

Look at:

**Rate + timing + endpoint + source distribution + behavior + server health + user impact**

---

# 24. Detection vs Proof

An indicator is not automatically proof.

For example:

`curl` User-Agent

does not mean:

> "This is definitely an attacker."

Instead:

> "This is an indicator that should be investigated in context."

A stronger investigation combines multiple signals:

**High request rate**
+
**Repeated expensive endpoint**
+
**Automated User-Agent**
+
**Sudden traffic spike**
+
**Server resource exhaustion**
+
**503 responses**
+
**legitimate-user impact**

This provides a much stronger basis for investigating a suspected DDoS.

---

# 25. Useful Detection Signals

| Signal | Why it matters |
|---|---|
| Sudden request spike | Possible automated traffic |
| High requests/second | Possible flooding |
| Repeated expensive endpoint | Possible resource exhaustion |
| Many source IPs | Could indicate distributed activity |
| Unusual User-Agent | Could indicate automation |
| Burst timestamps | Could indicate scripted activity |
| Geographic anomalies | Could indicate distributed infrastructure |
| 5xx spike | Server may be overloaded |
| Increased latency | Service may be under pressure |
| CPU/memory spike | Possible resource exhaustion |
| Database overload | Expensive application requests |
| Legitimate-user failures | Evidence of availability impact |

---

# 26. Connection to SOC / Blue Team

For a SOC L1 analyst, the goal is not simply to say:

> "There is a DDoS."

The analyst should establish:

1. What changed?
2. When did it change?
3. What is being targeted?
4. Where is the traffic coming from?
5. How much traffic is involved?
6. Is the traffic automated?
7. Is the infrastructure under pressure?
8. Are legitimate users affected?
9. Which controls are responding?
10. What evidence supports the conclusion?

This creates a defensible incident investigation.

---

# 27. Connection to the Unified Kill Chain

DDoS is particularly relevant to the **Action on Objectives / Impact** side of an attack.

The attacker's objective can be to compromise:

- Availability
- Business operations
- Revenue
- Reputation

Therefore, a DDoS can be understood as an availability-focused attack.

---

# 28. Quick Revision

### DoS
One source attempting to make a service unavailable.

### DDoS
Multiple distributed sources attempting to make a service unavailable.

### Layer 7 DDoS
Targets web/application functionality using application requests.

### Botnet
A collection of compromised systems controlled by an attacker.

### High Request Rate
Large numbers of requests in a short period.

### Logic Abuse
Using expensive application functionality to consume resources.

### WAF
Filters web requests and can allow, block, or challenge them.

### CDN
Distributes/caches content and can help absorb malicious traffic.

### Rate Limiting
Restricts request frequency.

### 5xx Spike
May indicate server-side stress or service failure.

### Baseline
Normal behavior used for comparison.

### Correlation
Combining multiple signals to understand an event.

---

# 29. What I Learned

Today I studied how SOC analysts can detect web-based DoS and DDoS attacks.

The most important lesson is that DDoS detection is not simply about seeing a huge amount of traffic. I need to understand the normal baseline and then identify abnormal patterns such as:

- Sudden request spikes
- Repeated requests to expensive endpoints
- Unusual User-Agents
- Distributed sources
- Increased server errors
- Increased resource utilization
- Legitimate-user impact

I also learned how SIEM platforms such as Splunk can make investigations easier by allowing analysts to aggregate, filter, and visualize web traffic.

I understood the defensive roles of:

- **CDN** — distributes and can absorb traffic
- **WAF** — filters, blocks, or challenges requests
- **Rate limiting** — controls request frequency
- **CAPTCHA / JavaScript challenges** — helps identify automated traffic
- **Secure development** — reduces application-level resource abuse

For a SOC L1 analyst, the important skill is to **correlate evidence rather than immediately label a traffic spike as DDoS**.

---
