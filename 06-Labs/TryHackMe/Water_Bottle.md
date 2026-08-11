# Water Bottle | TryHackMe CTF Writeup
**Date Added:** 11 August 2026

## Locate a missing water station using only fragments of memory and OSINT.

---

## Challenge Scenario

The challenge gives us a situation where someone returned to their hometown and needed a water refill from a station they frequently used until 2014.

The only information remembered was:

- The station was near **Boni Avenue**
- The contact number is a **12-digit number**
- The number starts with **63922**
- A new water refilling establishment now stands where the original station used to be

The goal is to find the **name and contact number of the original water station**.

### Flag Format

```text
THM{Water Station name in lowercase + _ + Contact Number}
```

Example:

```text
THM{happystation_12345678}
```

---

# Investigation

In 2014, the person was returning to his hometown and needed to refill his water.

Recently, while driving near Boni Avenue, he noticed that a new water refilling station had replaced the original one that used to be there.

So the two main clues we have are:

```text
Location: Near Boni Avenue
Mobile Number: Starts with 63922
```

---

## Step 1: Finding Boni Avenue

I started by searching Google for **Boni Avenue**.

From the search results, I found that Boni Avenue is located in **Mandaluyong City, Philippines**.

This gave me the area where I needed to search for the water station.

---

## Step 2: Searching Google Maps

Next, I used Google Maps to search for water refilling stations around Boni Avenue.

There were quite a lot of water refilling stations in the area, so I couldn't identify the correct one immediately.

I had to examine the locations individually and check their map history to see whether another water station existed at that location back in 2014.

This took around two hours, but eventually I found two locations where another water refilling station had been present in 2014.

The two locations were:

1. **Morning Crystal Water Refilling Station**
2. **Alkafresco Water Refilling Station**

---

## Step 3: Checking the Old Images

I compared the recent images of these locations with the images from 2014.

The idea was to find the original water station that had been replaced by the current establishment.

However, neither of these locations had a contact number displayed on the shop board that matched the `63922` clue.

This was confusing because the locations seemed to match the historical information, but the phone number clue didn't match.

So I continued searching.

---

## Step 4: Searching for Aquabest Mandaluyong

I then searched Google for:

```text
Aquabest Mandaluyong
```

This gave me several websites and contact pages.

One of the results had a strange-looking domain and contained contact information for an **Aquabest** location in Mandaluyong.

The contact number started with:

```text
63922
```

This matched the clue from the challenge.

The number I found was:

```text
639228721288
```

At this point, I had both the water station name and the required contact number.

---

# Final Answer

The water station was:

```text
Aquabest
```

The contact number was:

```text
639228721288
```

Since the flag requires the station name in lowercase:

```text
THM{aquabest_639228721288}
```

### Flag

```text
THM{aquabest_639228721288}
```

---

# Investigation Summary

The investigation followed this path:

```text
Boni Avenue
      ↓
Mandaluyong City, Philippines
      ↓
Search water refilling stations
      ↓
Check Google Maps
      ↓
Compare current and 2014 locations
      ↓
Morning Crystal / Alkafresco
      ↓
Phone number clue still didn't match
      ↓
Search "Aquabest Mandaluyong"
      ↓
Find contact number starting with 63922
      ↓
Aquabest
      ↓
THM{aquabest_639228721288}
```

---

# What I Learned

This challenge was a good example of how OSINT can require combining multiple small clues instead of relying on one search.

The location clue helped narrow down the area, while the historical map information helped identify possible locations.

The phone number prefix `63922` was also important because it helped confirm the final result.

The main thing I learned from this challenge is that **historical information can be just as important as current information** when investigating something that no longer exists.

