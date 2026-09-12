============================================================ 
 LINUX FORENSICS INVESTIGATION 
============================================================ 
 
Investigator:    Abhinav
Date:            12 September 2026
System examined: Kali Linux practice VM
Scenario:        Suspected compromise (staged practice scenario) 
Method:          Live + historical examination; suspicious files 
                 examined without execution 
 
 
------------------------------------------------------------ 
 1. SUMMARY 
------------------------------------------------------------ 
 
The investigation was performed as a controlled Linux forensics
practice scenario using staged, harmless evidence. No evidence
from the actual system confirmed a real compromise. A harmless
/tmp/update.sh file was created as suspicious evidence and
examined without execution; it was confirmed to be ASCII text
containing only a harmless placeholder. Authentication history
was incomplete because /var/log/auth.log was unavailable and
the SSH journal returned no entries. Confidence: medium, due to
the limitations of the staged practice environment.
 
 
------------------------------------------------------------ 
 2. INVESTIGATOR'S CHECKLIST FINDINGS 
------------------------------------------------------------ 
 
PROCESSES (what's running that shouldn't be): 
  The process list was reviewed using ps aux. The visible
  processes appeared consistent with normal Kali desktop and
  system activity, including Bluetooth, qterminal, XDG desktop
  portal processes, zsh, systemd-user processes, and kernel
  workers. No clearly suspicious process was identified in the
  reviewed output. In a real investigation, unfamiliar process
  names, unusual resource usage, unexpected execution paths,
  and processes connected to suspicious network activity would
  require further investigation.
 
NETWORK CONNECTIONS (what it's talking to): 
  The listening sockets were reviewed using ss -tuln. The output
  showed DNS listeners on 10.0.3.1:53 and
  [fc42:5009:ba4b:5ab0::1]:53, along with a DHCP-related UDP
  listener on 0.0.0.0%lxcbr0:67. These listeners alone were not
  enough to establish malicious activity. The command used did
  not display process names or PIDs, so the sockets could not be
  directly correlated with specific processes from this output.
 
LOGS (the history / timeline): 
  The traditional /var/log/auth.log file was not present on the
  system. The SSH systemd journal was also checked using:
 
  sudo journalctl _SYSTEMD_UNIT=ssh.service
 
  Result:
 
  -- No entries --
 
  Therefore, no real SSH login, failed-login, sudo, or account-
  creation events could be established from the available
  authentication evidence.
 
  A synthetic authentication-log example was created separately
  for learning purposes to practise recognizing a failed-login
  followed by successful authentication and privileged activity.
  This synthetic evidence was not treated as evidence from the
  actual Kali system.
 
ACCOUNTS (who exists / who can sudo): 
  The /etc/passwd file was reviewed. The root account, kali
  account, and multiple system/service accounts were present.
  No obviously rogue account could be concluded from the reviewed
  account list.
 
  The sudo group was checked using:
 
  getent group sudo
 
  Result:
 
  sudo:x:27:kali
 
  This confirms that the kali account is a member of the sudo
  group and therefore has administrative privileges through sudo.
 
SCHEDULED TASKS (persistence): 
  The user's cron table was checked using crontab -l and returned:
 
  no crontab for kali
 
  This means there were no user-level cron jobs configured for
  the kali account.
 
  The system cron directory /etc/cron.d was also reviewed. It
  contained e2scrub_all, john, php, and sysstat. No rogue
  scheduled task was identified from the reviewed output.
 
  In a real compromise, an unexpected cron entry or script would
  be important because scheduled execution can provide
  persistence after initial access.
 
FILES (suspicious files): 
  The staged file /tmp/update.sh was investigated using:
 
  ls -l /tmp/update.sh
  file /tmp/update.sh
  cat /tmp/update.sh
 
  Its properties were:
 
  - Owner: kali
  - Group: kali
  - Permissions: -rw-rw-r--
  - Size: 38 bytes
  - Timestamp observed: Sep 12 00:27
  - File type: ASCII text
  - Content: fake malicious placeholder - harmless
 
  The file was examined as text and was not executed.
 
  A recent-file search using find /tmp -mtime -1 also returned
  several system-managed temporary directories and files. A
  recent-file search in the home directory also identified
  normal recently modified items as well as the staged
  recent_marker.txt file. These results showed why recently
  modified files need context before being considered suspicious.
 
 
------------------------------------------------------------ 
 3. TIMELINE OF EVENTS 
------------------------------------------------------------ 
 
  12 Sep 2026 00:27  -  The staged /tmp/update.sh file was
                        observed as recently created/modified.
 
  12 Sep 2026         -  Recent-file searches were performed in
                        /tmp and the Kali home directory.
 
  12 Sep 2026         -  /tmp/update.sh was examined using ls,
                        file, and cat without executing it. The
                        contents showed that it was a harmless
                        placeholder.
 
  12 Sep 2026         -  Process activity was reviewed using
                        ps aux.
 
  12 Sep 2026         -  Listening network sockets were reviewed
                        using ss -tuln.
 
  12 Sep 2026         -  The traditional authentication log was
                        unavailable, and the SSH journal query
                        returned no entries.
 
  12 Sep 2026         -  Account and privilege information was
                        reviewed. The kali account was confirmed
                        as a sudo group member.
 
  12 Sep 2026         -  User and system cron configuration was
                        reviewed for possible persistence.
 
  12 Sep 2026         -  Staged evidence files were removed:
                        /tmp/update.sh,
                        ~/evidence_note.txt,
                        ~/recent_marker.txt.
 
  12 Sep 2026         -  Final cleanup was verified by listing
                        /tmp. The staged update.sh file was no
                        longer present.
 
  The findings arranged in time order show a controlled forensic
  exercise rather than a confirmed real intrusion. The available
  evidence does not establish an actual attacker timeline.
 
 
------------------------------------------------------------ 
 4. VERDICT AND CONFIDENCE 
------------------------------------------------------------ 
 
Verdict:     INCONCLUSIVE
Confidence:  MEDIUM
 
Evidence-based reasoning: 
  The system was used for a staged practice scenario containing
  a deliberately created harmless file in /tmp. The file was
  confirmed to be ASCII text and contained only a harmless
  placeholder.
 
  No clearly suspicious process was identified in the reviewed
  ps aux output. The network output showed DNS and DHCP-related
  listeners, but the command used did not provide process
  correlation.
 
  No user cron jobs were present, and no rogue persistence
  mechanism was identified from the reviewed /etc/cron.d output.
  The kali account was confirmed as a sudo member, but this is
  not evidence of compromise.
 
  The verdict is INCONCLUSIVE rather than NOT COMPROMISED because
  the available authentication history was incomplete. The
  traditional auth.log file was absent and the SSH journal query
  returned no entries.
 
  The staged suspicious file itself was not malicious and was
  removed during cleanup.
 
 
------------------------------------------------------------ 
 5. HOW THE ATTACKER GOT IN AND STAYED 
------------------------------------------------------------ 
 
Entry:        No real attacker entry method was established.
              Authentication evidence was unavailable from the
              examined auth.log and SSH journal sources.
 
Actions:      In the training scenario, the main suspicious
              artifact was the deliberately staged
              /tmp/update.sh file. It was examined without
              execution. The available evidence does not show
              a real attacker performing actions on the system.
 
Persistence:  No user-level cron persistence was found for the
              kali account. The reviewed /etc/cron.d directory
              contained existing entries, but no rogue scheduled
              task was identified from the evidence reviewed.
              No confirmed attacker persistence mechanism was
              established.
 
 
------------------------------------------------------------ 
 6. RECOMMENDATIONS 
------------------------------------------------------------ 
 
  [x] Remove the dropped file and any persistence found.
      The staged artifacts were removed during cleanup.
 
  [ ] Remove rogue accounts; reset compromised credentials.
      No rogue account or confirmed credential compromise was
      established, but this should be checked in a real incident.
 
  [x] Find and remove ALL persistence (miss one, they
      return). User and system cron locations were reviewed as
      part of this exercise. A real investigation should also
      examine other persistence mechanisms.
 
  [x] Apply hardening (Day 64) to prevent recurrence:
      updates, least privilege, SSH keys, monitoring.
 
  [x] Preserve evidence; escalate per incident process.
      In a real incident, evidence should be preserved before
      cleanup or remediation, and findings should be escalated
      according to the incident-response process.
 
 
------------------------------------------------------------ 
 7. SCOPE AND LIMITATIONS 
------------------------------------------------------------ 
 
  This was a staged practice scenario designed to demonstrate
  Linux forensic investigation techniques without using real
  malware or compromising a real system. The exercise combined
  process inspection, network inspection, account review, cron
  persistence checks, authentication-log investigation, recent
  file analysis, timeline construction, evidence-based reasoning,
  and cleanup.
 
  The suspicious /tmp/update.sh file was intentionally harmless
  and was examined without execution. The authentication-log
  portion had an important limitation because /var/log/auth.log
  was not present and the SSH systemd journal query returned no
  entries.
 
  A synthetic authentication-log example was used only as a
  learning aid and was not considered real system evidence.
 
  A real investigation would require a broader evidence set,
  including complete authentication and system logs, historical
  process information, process-to-network correlation, file
  metadata, account-change history, persistence locations, and
  preserved forensic artifacts.
 
  Conclusions in this exercise therefore apply only to the
  evidence available in the controlled practice environment.
 
 
============================================================ 
 END OF INVESTIGATION 
============================================================