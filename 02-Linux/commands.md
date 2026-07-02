# Linux Commands - Day 01

Today I learned some of the basic Linux commands that are used almost every day while working on Linux systems. These commands help in navigating through directories, creating files, managing folders, checking permissions, and many other basic tasks.

---

## man

I use the `man` command whenever I don't know how a command works. It opens the manual page of that command and explains its syntax, options, and usage.

```bash
man ls
```

Think of it as Linux's built-in documentation.

---

## ls

The `ls` command lists all the files and folders in the current directory.

```bash
ls
```

Some useful variations:

```bash
ls -l
```

Shows files in a detailed format.

```bash
ls -a
```

Shows hidden files.

```bash
ls -la
```

Shows hidden files along with detailed information.

This is probably one of the commands I'll use the most.

---

## cd

`cd` stands for Change Directory.

I use it to move from one folder to another.

```bash
cd Documents
```

Go back one directory.

```bash
cd ..
```

Go to my home directory.

```bash
cd ~
```

---

## pwd

Whenever I forget where I am inside the Linux file system, I use:

```bash
pwd
```

It prints the complete path of my current directory.

---

## mkdir

Used to create a new directory.

```bash
mkdir Projects
```

Very useful while organizing files.

---

## rmdir

Removes an empty directory.

```bash
rmdir Projects
```

If the folder contains files, this command won't remove it.

---

## touch

Creates a new empty file.

```bash
touch notes.txt
```

I noticed that this is one of the quickest ways to create files from the terminal.

---

## cp

Copies files or folders.

```bash
cp notes.txt backup.txt
```

I can also copy an entire directory using:

```bash
cp -r Folder BackupFolder
```

---

## mv

Used for two things:

- Moving files
- Renaming files

Example:

```bash
mv notes.txt linux-notes.txt
```

or

```bash
mv notes.txt Documents/
```

---

## cat

Displays the contents of a file.

```bash
cat notes.txt
```

Simple and useful for small text files.

---

## less

When a file is too large, `cat` becomes difficult to read.

```bash
less logfile.txt
```

This lets me scroll through the file page by page.

Press **q** to quit.

---

## grep

One of the most useful commands.

It searches for specific words inside files.

```bash
grep "error" logfile.txt
```

I know this command will become very important later while analyzing logs during cybersecurity labs.

---

## find

Used to search for files or directories.

```bash
find . -name "*.txt"
```

Instead of manually checking every folder, Linux searches everything for me.

---

## chmod

Changes file permissions.

Example:

```bash
chmod 755 script.sh
```

I still need more practice with Linux permissions because the numbers (755, 644, etc.) are new to me.

---

## chown

Changes the owner of a file.

```bash
sudo chown user file.txt
```

Mostly used by administrators.

---

## echo

Prints text on the terminal.

```bash
echo "Hello Linux"
```

It can also be used to write text into files.

```bash
echo "Hello" > notes.txt
```

---

## tar

Used to archive multiple files into a single file.

Create archive

```bash
tar -cvf archive.tar Folder/
```

Extract archive

```bash
tar -xvf archive.tar
```

---

## gzip

Compresses a file.

```bash
gzip notes.txt
```

---

## gunzip

Extracts a compressed file.

```bash
gunzip notes.txt.gz
```

---

## tail

Shows the last few lines of a file.

```bash
tail logfile.txt
```

Useful for checking the latest log entries.

---

## wc

Counts lines, words, and characters.

```bash
wc notes.txt
```

---

## sort

Sorts data alphabetically.

```bash
sort names.txt
```

---

## uniq

Removes duplicate lines.

```bash
sort names.txt | uniq
```

Usually used together with `sort`.

---

## diff

Compares two files.

```bash
diff file1.txt file2.txt
```

Helps me see what has changed between files.

---

## du

Checks how much disk space a folder uses.

```bash
du -sh Documents
```

---

## df

Shows available disk space.

```bash
df -h
```

---

## basename

Returns only the filename from a path.

```bash
basename /home/abhinav/report.txt
```

Output:

```
report.txt
```

---

## dirname

Returns only the directory path.

```bash
dirname /home/abhinav/report.txt
```

Output:

```
/home/abhinav
```

---

# My Notes

Today's class was mostly about getting comfortable with the Linux terminal. At first, remembering all the commands felt overwhelming, but after practicing them a few times, I realized many of them are straightforward. Commands like `ls`, `cd`, `pwd`, `mkdir`, `touch`, and `cat` are already becoming second nature.

I also learned that Linux provides a manual (`man`) whenever I get stuck, so I don't have to memorize everything. The commands `grep`, `find`, and `chmod` seem especially important for cybersecurity, and I plan to spend more time practicing them.

This is just the beginning, but these basic commands form the foundation for working with Linux systems and will be useful throughout my cybersecurity journey.