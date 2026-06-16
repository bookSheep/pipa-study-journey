# My TCM PIPA Certification Study Journey

This repository documents my hands-on learning as I work toward the
**TCM Security Practical IoT Pentest Associate (PIPA)** certification that I'm doing just for funsies as I was feeling like lost soul after obtaining my CISSP.

I'm building these tools from scratch to deepen my understanding of
embedded device security, serial/UART communication, and IoT
penetration testing fundamentals.

##  Educational Use Only

All scripts here are written for use against **my own test lab of hardware equipment and a kali linux virtual machine
**  The recommended TP-Link TL-WR841N router in Andrew Bellini's "Beginner's Guide to IoT and Hardware hacking course. I own specifically for security learning.
These tools are shared to document my learning process and should
only ever be used on devices you own or have explicit permission
to test.

## Study Process for the TCM Security's Practical IoT Pentest Associate Exam

A. Connect my lab TP-Link router to my Kali Linux VM via UART:

![WR841N UART setup](https://i.imgur.com/Ym4bkII.jpeg)

  aa. Interrupt the Linux boot process to drop into the U-Bootloader command line 


  
B. Get a root shell  (easy, just press enter..there wasn't any root login)

C. Enumeration of files + File extraction via TFTP
  cc. Looking at the bin folder, see what binaries are there. Busybox is there!! https://busybox.net/about.html

D. Analysis

E. Findings Write up


### Automating repetitive tasks with Python:

  ### 01 - Serial Connection Process Logger
A Python script that connects to an embedded Linux device over UART
and continuously logs running processes to a file. My first project
learning `pyserial` and Python automation from scratch.

### 02 - TFTP BusyBox Setup *(in progress)*
Automating the transfer of BusyBox tooling onto a test router.

### 03 - Shell Brute Forcer *(in progress)*
A credential testing tool for understanding why IoT default
passwords are dangerous.

## What I'm Learning

- Serial/UART communication with embedded devices
- Python automation for hardware interaction
- Reverse engineering router firmware with Ghidra
- The real-world risks of weak IoT security practices

## Background

I started this journey knowing PowerShell but no Python. Each script
here represents working through the language and the security
concepts one piece at a time.


Will write up the final challenge walkthrough, and then hopefully, pass the exam.
