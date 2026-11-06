# Intro to Digital Forensics --- Detailed Walkthrough Notes

**Study date:** 6 November 2026\
**Platform:** TryHackMe\
**Tasks:** Introduction to Digital Forensics, Digital Forensics Process,
Practical Example

## 1. What Is Digital Forensics?

Forensics is the application of science to investigate crimes and
establish facts. As computers, smartphones, cameras, and digital storage
became common, investigators needed methods to collect and examine
information stored on these devices. This developed into **digital
forensics**.

**Digital forensics** is the application of computer science to
investigate digital evidence for a legal purpose.

Digital evidence may come from: - Desktop computers and laptops -
Smartphones and tablets - Digital cameras - USB flash drives and
external storage - CDs and DVDs

These devices may contain information relevant to an investigation.
Because storage devices can hold tens of gigabytes or several terabytes,
investigators need a structured process and suitable tools.

### Two types of investigations

1.  **Public-sector investigations:** carried out by government or law
    enforcement agencies as part of criminal or civil investigations.
2.  **Private-sector investigations:** carried out by companies, either
    internally or through an outsourced investigator, often following a
    suspected corporate policy violation.

The purpose in both cases is to examine digital evidence and establish
what happened.

## 2. The Digital Forensics Process

The lesson describes a process that begins at the scene and continues in
the forensics laboratory.

### At the scene

1.  **Obtain proper legal authorisation.** Investigators need the
    appropriate authority before beginning.
2.  **Acquire the evidence.** Collect relevant computers, phones,
    storage devices, and other digital media. The lesson notes that
    powered-on computers require special handling, but does not cover
    those procedures.
3.  **Establish the chain of custody.** Record who collected, handled,
    transferred, stored, or accessed the evidence. This helps
    demonstrate that it was controlled and not tampered with.
4.  **Secure the evidence.** Use a suitable container to prevent damage.
    For smartphones, prevent network access so they cannot be remotely
    wiped.
5.  **Transport it to the forensics lab.** Maintain the evidence record
    during transport.

### At the laboratory

1.  Retrieve the evidence from secure storage.
2.  **Create a forensic copy** using suitable forensic software and
    procedures designed to avoid modifying the original.
3.  Return the original evidence to its secure container.
4.  Examine the copy on a forensics workstation.

The investigator works on the copy so that the original remains
preserved. If the working copy is damaged, another can be made from the
original.

### Process summary

  -----------------------------------------------------------------------
  Stage                               Purpose
  ----------------------------------- -----------------------------------
  Legal authorisation                 Ensures the investigation is
                                      authorised

  Acquisition                         Collects relevant devices and media

  Chain of custody                    Tracks who handled the evidence and
                                      when

  Secure storage and transport        Protects evidence from damage or
                                      interference

  Forensic copying                    Allows examination while preserving
                                      the original

  Examination                         Analyses the copy to establish
                                      relevant facts

  Reporting                           Documents the evidence and findings
  -----------------------------------------------------------------------

## 3. Six Important Digital Forensics Principles

The lesson attributes these principles to Ken Zatyko, former director of
the Defense Computer Forensics Laboratory.

### 3.1 Proper search authority

Investigators must have the appropriate legal authority before starting
the investigation.

### 3.2 Chain of custody

A record of who had possession of the evidence and when. It supports
accountability and helps demonstrate that the evidence was not
improperly accessed or altered.

### 3.3 Validation with mathematics --- hashing

A **hash function** is a mathematical function that produces a
fixed-length value from input data. Investigators can calculate hashes
for the original evidence and its forensic copy, then compare them.

Matching hash values support the conclusion that the compared data is
unchanged for that hash check. Different values require further
investigation.

### 3.4 Use of validated tools

Forensic tools should be tested and validated. For example,
investigators need confidence that disk-imaging software creates an
accurate image of the source.

### 3.5 Repeatability

Findings should be reproducible when the appropriate skills, tools, and
procedures are available. Clear documentation helps another investigator
understand how the result was reached.

### 3.6 Reporting

The investigation concludes with a report that communicates the relevant
evidence and findings.

**Quick memory aid:** Authority, Custody, Hashing, Validated tools,
Repeatability, Reporting.

## 4. Practical Example --- The Ransom Letter

The practical task presents a fictional case: a cat named Gado has been
kidnapped, and a document containing the kidnapper's demands is
provided. The task includes files such as:

``` text
letter-image.jpg
ransom-letter.doc
ransom-letter.pdf
ransom-lettter-2.zip
```

The lesson demonstrates how metadata can provide investigative leads.

### Access the task files on the AttackBox

``` bash
cd /root/Rooms/introdigitalforensics
ls
```

`cd` changes the current directory; `ls` lists the files in it.

## 5. Document Metadata

**Metadata** is information about a file. A basic text file may have
operating-system metadata such as creation and modification dates. More
advanced formats, such as Microsoft Word documents, can contain
additional information.

Document metadata may include: - Author - Title - Creator application -
PDF producer - Creation and modification dates - Page count - File
format details

Metadata can help investigators understand a file's properties and
recorded history. However, it is not automatic proof of who created a
document: metadata can be missing, changed, or inherited during
conversion.

### Inspect PDF metadata with `pdfinfo`

The lesson uses `pdfinfo`:

``` bash
pdfinfo DOCUMENT.pdf
```

For the task file:

``` bash
pdfinfo ransom-letter.pdf
```

Example output from the lesson:

``` text
Creator:        Microsoft® Word for Office 365
Producer:       Microsoft® Word for Office 365
CreationDate:   Wed Oct 10 21:47:53 2018 EEST
ModDate:        Wed Oct 10 21:47:53 2018 EEST
Tagged:         yes
UserProperties: no
Suspects:       no
Form:           none
JavaScript:     no
Pages:          20
Encrypted:      no
Page size:      595.32 x 841.92 pts (A4)
File size:      560362 bytes
Optimized:      no
PDF version:    1.7
```

  -----------------------------------------------------------------------
  Field                               Meaning
  ----------------------------------- -----------------------------------
  `Creator`                           Application recorded as creating
                                      the document/source content

  `Producer`                          Software recorded as generating the
                                      PDF

  `CreationDate`                      Creation timestamp stored in the
                                      PDF metadata

  `ModDate`                           Modification timestamp stored in
                                      the PDF metadata

  `Pages`                             Number of pages

  `Encrypted`                         Whether the PDF is encrypted

  `File size`                         Size of the PDF

  `PDF version`                       PDF format version
  -----------------------------------------------------------------------

The example indicates Microsoft Word for Office 365 and a recorded
creation date of 10 October 2018.

If `pdfinfo` is missing on Kali Linux, install it using:

``` bash
sudo apt install poppler-utils
```

**Task question:** Use `pdfinfo` to find the author of
`ransom-letter.pdf`.

The lesson text supplied here does not include the actual metadata
output for that task file, so it does not establish the author value.
Run `pdfinfo ransom-letter.pdf` against the actual file and inspect its
`Author` field. Do not mistake the example's `Creator` value for the
file's `Author`.

## 6. Photo EXIF Data

### What is EXIF?

**EXIF** stands for **Exchangeable Image File Format**. It is a standard
for storing metadata in image files.

A photo taken with a smartphone or digital camera may contain: - Camera
or smartphone model - Date and time of capture - Focal length -
Aperture - Shutter speed - ISO setting - GPS coordinates, if location
information was recorded

GPS coordinates may provide a useful lead about where a photograph was
taken.

### Inspect image metadata with ExifTool

The lesson introduces **ExifTool**, a command-line tool that reads and
writes metadata in multiple file formats, including JPEG.

``` bash
exiftool IMAGE.jpg
```

For the task image:

``` bash
exiftool letter-image.jpg
```

Example output from the lesson includes:

``` text
GPS Position : 51 deg 31' 4.00" N, 0 deg 5' 48.30" W
```

This is an example coordinate in the lesson, not necessarily the
coordinate in the task's own image.

If ExifTool is missing on Kali Linux, install it using:

``` bash
sudo apt install libimage-exiftool-perl
```

### Understanding GPS coordinates

GPS coordinates use: - **Latitude:** north/south position. -
**Longitude:** east/west position.

The lesson shows how coordinates can be entered into an online map. Its
map-search example is:

``` text
51°30'51.9"N 0°05'38.7"W
```

Note that this map-search example is slightly different from the earlier
EXIF example coordinate. Treat them as separate examples.

EXIF location data can help investigators develop a lead, but it is not
conclusive by itself. Metadata may be missing, inaccurate, modified, or
removed when an image is shared or processed. It should be corroborated
with other evidence.

## 7. Document Metadata vs EXIF Metadata

  -----------------------------------------------------------------------
  Feature                 Document metadata       EXIF metadata
  ----------------------- ----------------------- -----------------------
  Common file types       PDF and office          Digital photographs and
                          documents               image files

  Tool in this lesson     `pdfinfo`               `exiftool`

  Possible information    Author, creator,        Camera model, capture
                          producer, dates, page   time, camera settings,
                          count                   GPS

  Investigative use       Understand document     Understand image
                          properties and recorded properties and possible
                          details                 capture location

  Limitation              May be changed,         May be changed,
                          missing, or inherited   missing, or stripped
  -----------------------------------------------------------------------

## 8. Commands --- Quick Reference

  Purpose                         Command
  ------------------------------- -------------------------------------------
  Enter the task directory        `cd /root/Rooms/introdigitalforensics`
  List task files                 `ls`
  Inspect PDF metadata            `pdfinfo ransom-letter.pdf`
  Inspect image EXIF              `exiftool letter-image.jpg`
  Install PDF utilities on Kali   `sudo apt install poppler-utils`
  Install ExifTool on Kali        `sudo apt install libimage-exiftool-perl`

Example workflow:

``` bash
cd /root/Rooms/introdigitalforensics
ls
pdfinfo ransom-letter.pdf
exiftool letter-image.jpg
```

These commands inspect metadata. They do not independently prove who
created a file or establish that a person was physically present at a
particular location.

## 9. Important Terms

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  Digital forensics                   Applying computer science to
                                      investigate digital evidence for a
                                      legal purpose

  Digital evidence                    Digital information relevant to an
                                      investigation

  Public-sector investigation         Investigation by government or law
                                      enforcement

  Private-sector investigation        Investigation by a company or
                                      corporate investigator

  Acquisition                         Collection of relevant digital
                                      evidence

  Chain of custody                    Record of who handled evidence and
                                      when

  Forensic copy                       Copy made for examination while
                                      preserving the original

  Hash function                       Mathematical function used to
                                      generate a value that can help
                                      validate data integrity

  Validated tool                      Tool tested to establish that it
                                      performs its intended function
                                      correctly

  Repeatability                       Ability to reproduce findings using
                                      appropriate skills, tools, and
                                      procedures

  Metadata                            Information describing a file or
                                      other data

  EXIF                                Exchangeable Image File Format; a
                                      standard for image metadata

  `pdfinfo`                           Tool used in the lesson to display
                                      PDF metadata

  ExifTool                            Tool used to read and write
                                      metadata in image and other file
                                      formats

  GPS coordinates                     Latitude and longitude values that
                                      may indicate a recorded location
  -----------------------------------------------------------------------

## 10. Quick Revision Questions

**1. What is digital forensics?**\
The application of computer science to investigate digital evidence for
a legal purpose.

**2. What are the two types of investigations in this lesson?**\
Public-sector and private-sector investigations.

**3. What is a chain of custody?**\
A record of who collected, handled, transferred, stored, or accessed
evidence.

**4. Why create a forensic copy?**\
To examine a copy while preserving the original evidence.

**5. What is the purpose of hashing?**\
To help validate that data has not changed by comparing hash values.

**6. Why should forensic tools be validated?**\
To establish that they work correctly and produce reliable results.

**7. What does repeatability mean?**\
Findings can be reproduced using the proper skills, tools, and
procedures.

**8. What is the purpose of a forensic report?**\
To document and communicate the evidence and findings.

**9. Which command inspects PDF metadata in this lesson?**\
`pdfinfo`

**10. Which tool inspects image EXIF metadata?**\
`exiftool`

**11. What does EXIF stand for?**\
Exchangeable Image File Format.

**12. Name three kinds of information that may be stored in EXIF.**\
Camera model, capture date/time, and GPS coordinates. Camera settings
may also be present.

**13. Why are GPS coordinates useful?**\
They may provide a location associated with where the photograph was
taken.

**14. Does metadata alone prove who created a file or where a person
was?**\
No. It is an investigative lead that should be checked against other
evidence.

## 11. My Key Takeaways

Today I learned that digital forensics is the process of examining
digital devices and files to establish facts for an investigation.
Computers, smartphones, cameras, USB drives, and other storage media can
all contain information relevant to a case.

I learned that evidence must be handled carefully. Investigators need
proper authority, must maintain a chain of custody, should secure the
original evidence, and should create a forensic copy for examination.
Hashing helps check data integrity, validated tools support reliable
results, repeatability makes findings reviewable, and reporting
documents the investigation.

In the practical task, I learned that files can reveal useful
information through metadata. I can use `pdfinfo` to inspect PDF
properties and `exiftool` to inspect image EXIF information. EXIF may
contain camera details, capture timestamps, and GPS coordinates that can
provide investigative leads.

**Main lesson:** Digital forensics is not simply opening files and
looking for clues. It is a controlled, documented, and repeatable
process that protects evidence and helps investigators establish facts.

