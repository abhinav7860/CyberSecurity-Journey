# TryHackMe — Google Dorking   
**Platform:** TryHackMe  
**Date:** July 17, 2026

---

# What is a Web Crawler?

A **Web Crawler** (also called a Spider or Bot) is an automated program used by search engines to discover and collect information from websites.

Its main purpose is to:

- Visit websites
- Read their contents
- Follow links
- Store discovered information inside the search engine's index

Examples:

- Googlebot
- Bingbot
- Yahoo Slurp

---

# What Crawlers Collect

When visiting a website, crawlers collect information such as:

- Keywords
- Images
- Titles
- Metadata
- URLs
- Documents
- Internal Links
- External Links

The collected information is then stored inside the search engine.

---

# Crawling Process

The crawler follows these basic steps:

1. Visit a website.
2. Read the webpage contents.
3. Extract keywords and metadata.
4. Save this information.
5. Follow every internal and external link.
6. Repeat the process for newly discovered websites.

Example:

```
mywebsite.com

Contains:

Apple
Banana
Pear
```

Googlebot stores these keywords.

If someone searches for **Apple**, Google already knows this website contains that keyword and can display it in search results.

---

# Indexing

After crawling, the collected information is stored inside a huge database called the **Index**.

Think of it like a giant dictionary.

Example:

| Website | Keyword |
|----------|----------|
| mywebsite.com | Apple |
| mywebsite.com | Banana |
| mywebsite.com | Pear |

Google searches this index instead of scanning the internet every time someone searches.

---

# Crawling External Links

Web crawlers don't stop at one website.

If a website links to another website, the crawler follows it.

Example:

```
mywebsite.com
      │
      ▼
anotherwebsite.com
```

Crawler visits:

```
mywebsite.com

↓

anotherwebsite.com
```

Now Google stores keywords from both websites.

Example:

| Website | Keywords |
|----------|-----------|
| mywebsite.com | Apple, Banana, Pear |
| anotherwebsite.com | Tomatoes, Strawberries, Pineapples |

---

# Search Results

When users search:

```
Apple
```

Google returns:

```
mywebsite.com
```

When users search:

```
Strawberries
```

Google returns:

```
anotherwebsite.com
```

because it already indexed those keywords.

---

# Search Engine Optimization (SEO)

SEO stands for:

**Search Engine Optimization**

SEO is the process of improving a website so that search engines rank it higher.

Higher ranking means:

- More visibility
- More visitors
- Better search results

Many companies spend thousands of dollars improving SEO.

---

# Factors That Improve SEO

Some important ranking factors include:

- Mobile-friendly website
- Fast loading speed
- Easy navigation
- Good keywords
- Sitemap
- Crawlable pages
- Secure HTTPS connection
- Quality content

Search engines use complex algorithms to decide rankings.

---

# Robots.txt

The first file most crawlers look for is:

```
robots.txt
```

Location:

```
https://example.com/robots.txt
```

This file tells search engine crawlers:

- What they can access
- What they cannot access
- Which crawler is allowed
- Where the sitemap is located

---

# Basic robots.txt Example

```txt
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Meaning:

- Any crawler may visit the site.
- Entire website can be indexed.
- Sitemap location is provided.

---

# Blocking Directories

Example:

```txt
User-agent: *

Disallow: /admin/
```

Crawler cannot index:

```
https://example.com/admin/
```

---

# Blocking Multiple Directories

```txt
Disallow: /private/
Disallow: /backup/
```

Both folders are hidden from crawlers.

---

# Allowing Specific Crawlers

Example:

```txt
User-agent: Googlebot
Allow: /

User-agent: msnbot
Disallow: /
```

Meaning:

Googlebot:

✅ Allowed

Bing/MSN Bot:

❌ Blocked

---

# Blocking File Types

Example:

```txt
User-agent: *

Disallow: /*.ini$
```

This prevents crawlers from indexing `.ini` files.

Other sensitive files include:

- `.conf`
- `.env`
- `.bak`
- `.log`
- `.sql`

---

# Important robots.txt Directives

| Directive | Purpose |
|------------|----------|
| User-agent | Specifies crawler |
| Allow | Allows crawling |
| Disallow | Blocks crawling |
| Sitemap | Location of sitemap |

---

# Sitemaps

A Sitemap is a file that tells search engines where website pages are located.

Location:

```
https://example.com/sitemap.xml
```

Format:

```
XML
```

Think of it like a roadmap for your website.

Instead of discovering pages randomly, crawlers receive the entire list immediately.

---

# Benefits of Sitemaps

- Faster crawling
- Better indexing
- Improved SEO
- Easier discovery of hidden pages
- Better search rankings

---

# Example Website Structure

```
Home

├── Products
│     └── Fruits
│          └── Pears
│
├── About
│
└── Blog
      ├── Post 1
      ├── Post 2
      └── Post 3
```

The sitemap lists every important page so crawlers can find them quickly.

---

# Google Dorking

Google Dorking means using advanced Google search operators to find specific publicly indexed information.

It is commonly used during:

- Reconnaissance
- OSINT
- Bug Bounty
- Penetration Testing

Everything found through Google Dorking is publicly accessible.

---

# Common Google Operators

## site:

Search inside one website.

Example:

```
site:tryhackme.com linux
```

Only searches TryHackMe.

---

## filetype:

Search for specific file types.

Example:

```
site:bbc.co.uk filetype:pdf
```

Returns only PDF files.

Useful file types:

- pdf
- doc
- docx
- xls
- xlsx
- sql
- log
- txt
- bak

---

## intitle:

Looks for words inside page titles.

Example:

```
intitle:login
```

Useful for finding login pages.

---

## cache:

Displays Google's cached version of a page.

Example:

```
cache:tryhackme.com
```

---

# Useful Google Dorks

Search PDFs:

```
filetype:pdf
```

Search Word Documents:

```
filetype:docx
```

Search SQL Dumps:

```
filetype:sql
```

Search Login Pages:

```
intitle:login
```

Search Admin Panels:

```
intitle:admin
```

Search within one website:

```
site:example.com password policy
```

---

# Why Google Dorking Matters

Sometimes organizations accidentally expose files like:

- Backup files
- Configuration files
- Logs
- Database dumps
- Password documents

Although these files are public, attackers often discover them before administrators notice.

Ethical hackers use Google Dorking to report these exposures responsibly.

---

# Important Commands Learned

### robots.txt

```
https://example.com/robots.txt
```

---

### Sitemap

```
https://example.com/sitemap.xml
```

---

### Allow Googlebot

```txt
User-agent: Googlebot
Allow: /
```

---

### Block Directory

```txt
Disallow: /dont-index-me/
```

---

### Block Configuration Files

```txt
Disallow: /*.conf$
```

---

### Search PDFs

```
site:example.com filetype:pdf
```

---

### Search Login Pages

```
intitle:login
```

---

### Search Inside Website

```
site:bbc.co.uk flood defences
```

---
