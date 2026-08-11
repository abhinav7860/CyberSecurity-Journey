# Digital Footprint Challenge | TryHackMe
**Date Added:** 11 August 2026

---

## Task 1: The Leaked Photo

The first task gives us a photo of a residential property which is believed to be connected to ACME Jet Solutions.

The objective is to find where the picture was taken.

**Flag format:**
```text
THM{City}
```

### Solution

First, I looked at the image carefully to find anything useful.

The most interesting thing I noticed was the **security sign**.

The sign says:

```text
ADT Armed Response Residential
```

I searched for:

```text
ADT Armed Response residential
```

This gave me a clue that the location is in **South Africa**.

Now the problem was finding the exact city. There are many cities in South Africa, so searching randomly wasn't very useful.

Instead, I focused on the **ADT** security company and searched for its head office location.

From the results, I found that the head office is in **Johannesburg**.

### Answer

```text
THM{Johannesburg}
```

---

# Task 2: Archived Company Website

ACME Jet Solutions claims on social media that they were founded in **2025** and are one of the fastest-growing data companies in Africa.

However, an ex-employee claims that the company existed much earlier.

The objective is to find when the company's website was first published.

**Flag format:**
```text
THM{YYYYMMDDHHMMSS}
```

### Solution

For this task, I used the **Internet Archive**.

I searched for the company's domain in:

```text
https://archive.org/
```

At first, I searched for:

```text
warcarchives
```

but that didn't give me the result I wanted.

So I switched to the **Advanced Search** and searched for:

```text
acme.com
```

This gave me the relevant archived result.

To find the exact timestamp needed for the flag, I checked the archive information and looked at the:

```text
Firstfiledate
```

or

```text
Scandate
```

The timestamp was:

```text
20160210224602
```

### Answer

```text
THM{20160210224602}
```

---

# Task 3: Mysterious Landmark

The next task gives us another image which is connected to the company's international expansion.

The objective is to identify a landmark.

The clue says that there is a building to the right of the landmark which played an important role in the fight for the independence of a particular country.

The name of the building is written on signs outside.

**Flag format:**
```text
THM{Landmark}
```

### Solution

First, I looked at the image and tried to identify the main landmark.

I searched the image using Google Images and found that the landmark was:

```text
The Spire
```

in **Dublin, Ireland**.

After identifying the Spire, I searched for it on Google Maps and checked the buildings next to it.

The building beside the Spire was:

```text
General Post Office
```

The General Post Office is also an important historical location related to Irish independence.

### Answer

```text
THM{General Post Office}
```

---

# Task 4: Internal Documents

This was probably the most frustrating task for me.

The objective is to find the final flag from an internal document that was accidentally leaked by one of the company's developers.

We are given an office document.

### Solution

First, I checked the file type and structure.

I used:

```bash
file /mnt/user-data/uploads/internal-docs-1769695301727.odt
```

The output showed:

```text
/mnt/user-data/uploads/internal-docs-1769695301727.odt: OpenDocument Text
```

So I knew that this was an **ODT** file.

I then copied the file and extracted it using `unzip`.

```bash
cd /tmp
cp /mnt/user-data/uploads/internal-docs-1769695301727.odt .
unzip -q internal-docs-1769695301727.odt
```

After extracting the file, I checked the contents:

```bash
ls -la
```

One file immediately caught my attention:

```text
meta.xml
```

This looked interesting because document metadata can sometimes contain information about the person who created or edited the document.

### Checking `meta.xml`

I opened it using:

```bash
cat meta.xml
```

Inside the metadata, I found:

```xml
<meta:user-defined meta:name="Internal username">markwilliams7243</meta:user-defined>
```

So I found the internal username:

```text
markwilliams7243
```

But this wasn't the final flag yet.

---

## Finding the YouTube Account

The document also mentioned an uploaded video.

That made me think the username could be connected to a YouTube account.

So I searched for:

```text
https://www.youtube.com/@markwilliams7243
```

The YouTube channel appeared.

After checking the channel, I found the final flag.

### Final Answer

```text
THM{Y0u_f0und_7h3_fin4l_fl4g!}
```

---

# What I Learned

This room was a good example of how small pieces of information can be connected together during OSINT.

For example:

```text
Image
  ↓
Security Sign
  ↓
ADT
  ↓
South Africa
  ↓
Johannesburg
```

And in the last task:

```text
ODT File
  ↓
Extract File
  ↓
meta.xml
  ↓
Internal Username
  ↓
YouTube
  ↓
Final Flag
```

The main thing I learned from this challenge is that **we shouldn't ignore small details**. A security sign in an image or metadata hidden inside a document can provide the clue needed to continue the investigation.
