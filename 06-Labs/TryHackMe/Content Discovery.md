# TryHackMe -- Content Discovery

**Date Completed:** 24 September 2026\
**Platform:** TryHackMe\
**Room:** Content Discovery\
**Category:** Web Application Reconnaissance\

## 1. Overview

I completed the **Content Discovery** room on TryHackMe.

This room focused on discovering files, directories, endpoints,
technologies, subdomains, and virtual hosts that may not be immediately
visible from a website's normal navigation.

The room covered three main approaches:

1.  Manual discovery
2.  OSINT-based discovery
3.  Automated discovery

The main idea is that these techniques complement each other. Manual
techniques can reveal quick information, OSINT can uncover information
already exposed publicly, and automated tools can search a much larger
number of possible paths.

## 2. What is Content Discovery?

Content discovery is the process of identifying resources that exist on
a web application, including directories, files, login pages,
administration portals, hidden endpoints, API endpoints, backup files,
development files, subdomains, and virtual hosts.

A website may visibly expose only a small number of pages while
additional resources still exist on the server. Content discovery helps
create a clearer picture of the application's attack surface.

## 3. Manual Discovery

The manual section covered:

-   `robots.txt`
-   `sitemap.xml`
-   HTTP headers
-   HTML source code
-   Framework identification

## 4. robots.txt

I checked:

``` text
http://<TARGET-IP>/robots.txt
```

`robots.txt` provides instructions to search engine crawlers. For
example:

``` text
User-agent: *
Allow: /
Disallow: /staff-portal
```

The important lesson is that `robots.txt` is **not an access-control
mechanism**. A path listed under `Disallow` can still be accessed
directly if the application permits it.

In the room, `/staff-portal` was revealed through `robots.txt`.

**Key lesson:** Disallow does not mean protected.

## 5. sitemap.xml

I then checked:

``` text
http://<TARGET-IP>/sitemap.xml
```

A sitemap provides search engines with URLs that the website wants them
to discover. It can therefore act as a useful map of the application's
pages.

The sitemap revealed endpoints such as:

``` text
/news
/contact
/news/article?id=1
/news/article?id=2
/news/article?id=3
/customers/login
/s3cr3t-area
```

The article URLs contained an `id` parameter:

``` text
/news/article?id=1
```

This showed that the application accepts user-controlled input. The
presence of a parameter does not prove a vulnerability, but it
identifies a potential input point for later testing.

**Key lesson:** Sitemaps can reveal endpoints that are not obvious from
normal navigation.

## 6. HTTP Headers

I used:

``` bash
curl http://<TARGET-IP> -v
```

The `-v` option enables verbose output and allows the request and
response headers to be viewed.

Important information included:

``` text
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Content-Type: text/html; charset=UTF-8
X-Powered-By: THM-Framework
```

### Server header

``` text
Server: nginx/1.18.0 (Ubuntu)
```

This revealed the web server software, version, and operating system
information exposed by the application.

### X-Powered-By

``` text
X-Powered-By: THM-Framework
```

This revealed the application framework.

Technology identification is useful because it allows a tester to
research the application's expected structure and documentation.

## 7. Custom Headers

The HTTP response also contained custom headers:

``` text
X-FLAG: [flag value]
X-FLAG: [flag value]
```

The room specifically required careful inspection of the response
headers because a flag was exposed through a custom header.

This demonstrated that useful information may exist outside the visible
webpage.

**Key lesson:** Always inspect the complete HTTP response during
reconnaissance, not just the rendered page.

## 8. HTML Source Code

I inspected the website's source code using the browser's **View Page
Source** functionality.

The source contained information that was not immediately visible on the
rendered webpage, including HTML comments, hidden endpoints, framework
information, and links that were easy to overlook.

### `/new-home-beta`

A source-code comment revealed:

``` text
/new-home-beta
```

This was an example of information disclosed through an HTML comment.

### `/secret-page`

The source also contained a link similar to:

``` html
<a href="/secret-page">to</a>
```

This revealed:

``` text
/secret-page
```

The endpoint was not obvious from the normal visible page.

## 9. Framework Identification

At the bottom of the page source, I found:

``` text
THM Framework v1.2
```

The comment also provided a link to the framework documentation.

This was an important clue because the documentation could be used to
understand the framework's default structure.

## 10. Finding the Administration Portal

I followed the framework documentation.

The documentation revealed that the administration login was located at:

``` text
/thm-framework-login
```

I accessed:

``` text
http://<TARGET-IP>/thm-framework-login
```

The room provided the default credentials:

``` text
Username: admin
Password: admin
```

Using these credentials allowed access to the administration portal.

The final flag was:

``` text
THM{CHANGE_DEFAULT_CREDENTIALS}
```

### Security lesson

Default credentials should always be changed before an application is
deployed.

Leaving:

``` text
admin : admin
```

enabled can allow unauthorized access to administrative functionality.

## 11. OSINT

The OSINT section introduced Open-Source Intelligence: collecting
information from publicly available sources.

Resources covered included:

-   Search engines
-   Google Dorking
-   Wappalyzer
-   Wayback Machine
-   GitHub
-   Public cloud resources such as S3 buckets

## 12. Google Dorking

Important Google search operators covered in the room included:

  -----------------------------------------------------------------------
  Operator                Example                 Purpose
  ----------------------- ----------------------- -----------------------
  `site:`                 `site:example.com`      Restrict results to a
                                                  specific website

  `inurl:`                `inurl:admin`           Search for a word in
                                                  URLs

  `filetype:`             `filetype:pdf`          Search for a specific
                                                  file type

  `intitle:`              `intitle:admin`         Search page titles

  `intext:`               `intext:password`       Search page content

  `cache:`                `cache:example.com`     Search cached content
                                                  where supported
  -----------------------------------------------------------------------

### Question

**What Google dork operator limits results to a specific site?**

Answer:

``` text
site:
```

Example:

``` text
site:tryhackme.com
```

## 13. Wappalyzer

The room introduced **Wappalyzer** as a technology identification tool
and browser extension.

It can identify technologies used by a website, including:

-   Frameworks
-   CMS platforms
-   JavaScript libraries
-   Web servers
-   CDNs
-   Analytics technologies

This is useful during reconnaissance because technology identification
helps determine what technologies may need further investigation.

## 14. Automated Discovery

Manual and OSINT techniques cannot efficiently test thousands of
possible paths. The room therefore introduced automated content
discovery.

The main tool used was **Gobuster**.

Gobuster is an open-source enumeration tool written in Go and supports:

``` text
dir
dns
vhost
```

## 15. Gobuster Wordlists

Gobuster uses wordlists containing possible directory, file, or
subdomain names.

The room introduced **SecLists** as a useful collection of security
testing wordlists.

Common AttackBox paths include:

``` text
/usr/share/wordlists/SecLists/
```

Useful web-content wordlists include:

``` text
/usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt
```

and:

``` text
/usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

## 16. Gobuster dir Mode

The `dir` mode is used to discover directories and files.

Basic syntax:

``` bash
gobuster dir -u "http://<TARGET-IP>" -w <wordlist>
```

Important options:

  Flag   Purpose
  ------ -------------------------------------
  `-u`   Target URL
  `-w`   Wordlist
  `-t`   Number of threads
  `-o`   Save output to a file
  `-x`   Search for specific file extensions
  `-r`   Follow redirects
  `-k`   Skip TLS certificate verification
  `-s`   Specify status codes

## 17. Gobuster Directory Enumeration Results

The scan discovered:

``` text
/assets
/contact
/customers
/development.log
/monthly
/news
/private
/robots.txt
/sitemap.xml
```

### `/customers`

This endpoint redirected to:

``` text
/customers/login
```

This indicated the existence of a customer login system.

### `/development.log`

This was an interesting discovery because development log files can
sometimes contain sensitive information.

### `/private`

A private directory was also discovered.

### `/monthly`

The room asked:

**What is the name of the directory beginning with `/mo`?**

Answer:

``` text
monthly
```

### Log file question

**What is the name of the log file discovered?**

Answer:

``` text
development.log
```

## 18. DNS Enumeration

Gobuster's `dns` mode is used to discover possible subdomains.

A subdomain is resolved through DNS. For example:

``` text
blog.example.thm
```

may be a DNS record pointing to an IP address.

Basic syntax:

``` bash
gobuster dns -d example.thm -w <wordlist>
```

The important required flags are:

``` text
-d
-w
```

### Question

**Apart from `dns` and `-w`, which shorthand flag is required for DNS
mode?**

Answer:

``` text
-d
```

The `-d` flag specifies the target domain.

## 19. DNS Enumeration Results

The room demonstrated DNS enumeration against:

``` text
example.thm
```

The scan discovered:

``` text
shop.example.thm
www.shop.example.thm
webdisk.shop.example.thm
autodiscover.shop.example.thm
autoconfig.shop.example.thm
academy.example.thm
primary.example.thm
```

These results demonstrate why subdomain discovery is important.
Different subdomains can host different applications or services and may
have different security configurations.

## 20. Subdomains vs Virtual Hosts

An important concept was the difference between **subdomains** and
**virtual hosts**.

### Subdomain

A subdomain is resolved through DNS.

Example:

``` text
blog.example.thm
```

### Virtual host

A virtual host is handled by the web server. Multiple websites can share
the same IP address, with the server using the HTTP `Host:` header to
decide which site to serve.

Therefore:

``` text
DNS mode  → discovers DNS-based subdomains
vhost mode → discovers websites configured on the web server
```

## 21. Preparing DNS Resolution

The room used local DNS configuration so the AttackBox could resolve the
lab domains.

The configuration involved:

``` text
/etc/resolv-dnsmasq
```

The lab DNS server was configured as the nameserver and the Dnsmasq
service was restarted.

## 22. Updating /etc/hosts

The room also required a manual hostname-to-IP mapping in:

``` text
/etc/hosts
```

For example:

``` text
10.49.174.138 example.thm
```

This allows the AttackBox to resolve the lab hostname locally.

The mapping can be verified with:

``` bash
ping example.thm
```

## 23. Gobuster vhost Mode

The `vhost` mode does not perform DNS lookups. Instead, Gobuster sends
HTTP requests while changing the `Host:` header.

For example:

``` text
Host: admin.example.thm
Host: dev.example.thm
Host: shop.example.thm
```

This can identify virtual hosts that may not be present in public DNS.

The room used options including:

``` text
--domain
--append-domain
--exclude-length
```

`--append-domain` combines wordlist entries with the specified domain.

`--exclude-length` filters responses with common body lengths and helps
reduce false positives.

## 24. Virtual Host Question

The room asked:

**How many virtual hosts on `acmeitsupport.thm` respond with status code
200?**

The scan must be run in **vhost mode** against `acmeitsupport.thm`,
using the current target IP supplied by the TryHackMe machine.

Example:

``` bash
gobuster vhost -u "http://<TARGET-IP>" --domain acmeitsupport.thm -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain --exclude-length 250-320
```

The results should be reviewed for virtual hosts responding with:

``` text
200
```

Only successful `200 OK` virtual hosts should be counted.

## 25. Important Gobuster Flags

  Flag                 Meaning
  -------------------- --------------------------------------
  `-u`                 Target URL
  `-w`                 Wordlist
  `-d`                 Domain for DNS enumeration
  `-t`                 Number of threads
  `-o`                 Output file
  `-x`                 File extensions
  `-r`                 Follow redirects
  `-k`                 Disable TLS certificate verification
  `-s`                 Select status codes
  `--domain`           Domain used by vhost enumeration
  `--append-domain`    Append domain to wordlist entries
  `--exclude-length`   Filter responses by body length

## 26. Complete Content Discovery Methodology

The complete workflow covered by this room can be summarized as:

``` text
                    TARGET
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       Manual        OSINT     Automated
          |           |           |
          v           v           v
    robots.txt    Google       Gobuster
    sitemap.xml   Dorking          |
    Headers       Wappalyzer   +----+-----+
    Source        Wayback      dir  dns  vhost
    Framework     GitHub
                  S3
          |           |           |
          +-----------+-----------+
                      |
                      v
                Attack Surface
                      |
                      v
               Further Testing
```

## 27. Security Lessons

### Information disclosure

Websites can reveal information through:

-   Headers
-   HTML comments
-   Source code
-   `robots.txt`
-   Sitemaps
-   Development files

### Hidden does not mean secure

A URL that is not linked from the homepage can still be accessible.

### Default credentials

The administration portal used default credentials in the lab.

The flag:

``` text
THM{CHANGE_DEFAULT_CREDENTIALS}
```

reinforced the importance of changing default credentials.

### Technology fingerprinting

Knowing the server and framework can help guide further reconnaissance.

### Attack surface mapping

Directories, files, subdomains, and virtual hosts all contribute to
understanding the application's attack surface.

## 28. Questions and Answers

  Question                                        Answer
  ----------------------------------------------- -----------------------------------
  Google dork operator for a specific site        `site:`
  Technology identification tool/extension        `Wappalyzer`
  Directory beginning with `/mo`                  `monthly`
  Log file discovered                             `development.log`
  Required shorthand flag for Gobuster DNS mode   `-d`
  Administration portal flag                      `THM{CHANGE_DEFAULT_CREDENTIALS}`

### Virtual host question

The room also asks:

**How many virtual hosts on `acmeitsupport.thm` respond with status code
200?**

This should be determined from the vhost scan output by counting only
the discovered hosts returning HTTP `200`.

## 29. Tools Used

-   TryHackMe AttackBox
-   Firefox
-   `curl`
-   Gobuster
-   SecLists
-   Google
-   Wappalyzer
-   Browser Page Source
-   Linux terminal
-   `nano`
-   `ping`
-   Dnsmasq

## 30. Final Takeaway

The most important lesson from this room is that content discovery
should be performed using multiple approaches.

Manual discovery can reveal information quickly.

OSINT can reveal information that has already been made publicly
available or indexed.

Automated enumeration can search thousands of possible resources
efficiently.

A strong reconnaissance process combines all three:

``` text
Manual Discovery
       +
OSINT
       +
Automated Enumeration
       |
       v
Better Attack Surface Visibility
       |
       v
More Informed Security Testing
```

This room improved my practical understanding of web application
reconnaissance, manual content discovery, OSINT, Google Dorking,
technology fingerprinting, directory enumeration, DNS enumeration, and
virtual host discovery.

