# TryHackMe — Searchlight IMINT  
**Date:** July 17, 2026

---

# What is IMINT?

**IMINT (Imagery Intelligence)** is the process of extracting useful information from images or videos.

It is widely used by:

- Intelligence agencies
- Law enforcement
- Journalists
- Military analysts
- Cybersecurity professionals
- OSINT investigators

Instead of hacking systems, IMINT relies on observation and publicly available information.

---

# Key Principles I Learned

Before using any tools, I learned that I should always analyze the image carefully using my own eyes.

Benjamin Strick's five IMINT elements are:

- Context
- Foreground
- Background
- Map Markings
- Trial and Error

These five principles helped me approach every challenge logically instead of randomly searching online.

---

# Context

Context means understanding where the image came from.

Questions I asked:

- Who uploaded it?
- Why was it taken?
- Is there any description?
- Is there a filename?
- Is there any social media context?

Although most TryHackMe challenges remove context, real investigations usually include valuable contextual clues.

---

# Foreground

The foreground contains objects closest to the camera.

Things I looked for included:

- Shop names
- Road signs
- People
- Vehicles
- Logos
- Telephone numbers
- Building names
- Advertisements

Sometimes a single word was enough to identify the entire location.

---

# Background

The background often contains hidden clues.

Examples include:

- Mountains
- Bridges
- Rivers
- Skylines
- Famous buildings
- Churches
- Towers
- Airports
- Unique architecture

Many challenges were solved simply by recognizing landmarks.

---

# Map Markings

Road information is extremely valuable.

I looked for:

- Street names
- Highway numbers
- Exit numbers
- Traffic signs
- Railway signs
- Station names

These clues helped narrow down the exact location.

---

# Trial and Error

Not every search works the first time.

Sometimes I had to:

- Search different keywords
- Change search order
- Try reverse image search
- Crop the image differently
- Search only parts of an image

This taught me that patience is an important skill in OSINT.

---

# Google Dorking

Many challenges required basic Google searches.

Instead of searching random phrases, I searched only the important keywords visible in the image.

Examples:

```
"Carnaby Street"
```

```
"Piccadilly Circus Station"
```

```
"Coffee Shop Blairgowrie"
```

Using precise keywords significantly reduced search time.

---

# Reverse Image Search

One of the most useful techniques I learned was Reverse Image Searching.

Instead of searching text, I searched using the image itself.

Useful services include:

- Google Lens
- Bing Visual Search
- Yandex Images
- TinEye

Reverse searching helped identify:

- Restaurants
- Statues
- Hotels
- Famous photographs

---

# Challenge 1

## Street Identification

Using visible clues in the image, I identified the street.

**Answer**

```
Carnaby Street
```

---

# Challenge 2

## London Underground

By carefully observing the image and searching the visible station information, I found:

- City
- Station Name
- Opening Year
- Number of Platforms

Results:

- London
- Piccadilly Circus
- 1906
- 4 Platforms

This challenge showed me that transportation systems contain a lot of searchable information.

---

# Challenge 3

## Airport Identification

I identified:

- Vancouver International Airport
- Canada
- Richmond

I mainly relied on signs, architecture, and Google searches.

---

# Challenge 4

## Coffee Shop Investigation

This challenge required finding a small coffee shop in Scotland.

I successfully identified:

- Blairgowrie
- Allan Street
- Phone Number
- Email Address
- Owner's Surname

This felt like a real OSINT investigation because multiple searches were required before finding the exact business.

---

# Challenge 5

## Reverse Image Search

Using reverse image searching techniques, I discovered:

Restaurant:

```
Katz's Deli
```

I also identified the Bon Appétit editor:

```
Andrew Knowlton
```

This challenge demonstrated how powerful reverse image searching can be.

---

# Challenge 6

## Statue Investigation

I identified:

Statue:

```
Rudolph the Chrome Nosed Reindeer
```

Photographer:

```
Kjersti Stensrud
```

This required combining reverse image search with Google searches.

---

# Challenge 7

## Lady Justice

This challenge was more difficult because there were fewer obvious clues.

After analyzing the image carefully, I found:

Character:

```
Lady Justice
```

Location:

```
Alexandria, Virginia
```

Opposite Building:

```
The Westin Alexandria Old Town
```

This challenge taught me to pay attention to surrounding buildings, not just the main object.

---

# Challenge 8

## Hotel Video Investigation

Unlike previous tasks, this challenge used a video instead of a single image.

I learned that a video is simply a sequence of images.

By extracting important frames and analyzing them individually, I identified:

```
Novotel Singapore Clarke Quay
```

This was one of my favorite challenges because it introduced video geolocation.

---

# Techniques I Practiced

Throughout this room I used several OSINT techniques:

- Visual observation
- Keyword extraction
- Google searching
- Google Dorking
- Reverse Image Search
- Landmark identification
- Business lookup
- Map verification
- Context analysis
- Video frame analysis

---

# What I Learned

This room completely changed how I look at images.

Before this room, I would simply look at a photo.

Now I automatically start asking questions like:

- What language is visible?
- Which side of the road do they drive on?
- What type of road signs are present?
- What vehicles are visible?
- What architecture is used?
- Are there mountains?
- Are there business names?
- Are there landmarks?
- Can I search any text?
- Can I reverse search the image?

I realized that every image contains far more information than it first appears.

--