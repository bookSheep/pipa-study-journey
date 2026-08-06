# My TCM PIPA Certification Study Journey

This repository documents my hands-on learning as I work toward the **TCM Security Practical IoT Pentest Associate (PIPA)** certification — a self-directed deep dive into hardware and IoT security following my CISSP, built to develop practical offensive skills that complement the certification.

Everything here is built from scratch to deepen my understanding of embedded device security, serial/UART communication, firmware analysis, and IoT penetration testing fundamentals.

---

## Educational Use Only

All work is performed against my own lab equipment — a TP-Link TL-WR841N router (the device used in Andrew Bellini's *Beginner's Guide to IoT and Hardware Hacking* course) and a Kali Linux virtual machine — which I own specifically for security learning.

These projects are shared to document my learning process and should only ever be used on devices you own or have explicit permission to test.

---

## Study Process

My general methodology for analyzing the lab router:

1. **Physical access** — Connect the TP-Link router to my Kali Linux VM via UART
2. **Boot analysis** — Observe the boot process; optionally interrupt the bootloader to reach the U-Boot command line
3. **Shell access** — Obtain a root shell over serial (notably, no login was required — a finding in itself)
4. **Enumeration & extraction** — Enumerate the filesystem and extract files of interest (via TFTP, and separately via direct chip-off firmware dump)
5. **Analysis** — Static analysis and reverse engineering of extracted binaries
6. **Findings & write-up** — Document methodology and results

![WR841N UART setup](https://i.imgur.com/Ym4bkII.jpeg)

---

## Projects

### 01 — Serial Console Process Logger
A Python script that connects to an embedded Linux device over UART and continuously logs running processes to a file. My first project learning `pyserial` and Python automation from scratch.

### 02 — TFTP BusyBox Setup
Automates transferring a full BusyBox binary onto the lab router. The router's embedded Linux shipped with only a stripped-down BusyBox that included `tftp` — so the course approach is to use that limited `tftp` to pull down a full BusyBox build, enabling much deeper on-device enumeration.

### 03 — Bootloader Interrupt
A Python script that reboots the router and spams the interrupt command to drop into the locked-down U-Boot CLI — documented as a recon exercise, including the finding that this bootloader's usual functionality is stripped.

### 04 — Serial Console Brute Forcer *(in progress)*
A credential-testing tool demonstrating the technique for brute-forcing a serial console login against IoT default credentials.

### 05 — Firmware Extraction via EPROM Programmer
Direct chip-off firmware extraction using a CH341A programmer and SOIC clip — including OSINT chip identification, a hardware troubleshooting walkthrough, dual-read MD5 verification, entropy analysis, and binwalk extraction of the filesystem.

---

## Tooling & Skills Developed

- Serial/UART communication with embedded devices
- Python automation for hardware interaction (`pyserial`)
- Firmware acquisition (TFTP transfer and direct EPROM chip-off)
- Firmware analysis with binwalk and entropy analysis
- Reverse engineering with Ghidra
- CI/CD basics — automated linting on every push via GitHub Actions
- Git version control and portfolio hygiene (`.gitignore`, secret exclusion)

---

## Background

I started this journey knowing PowerShell but no Python. Each project here represents working through the language and the underlying security concepts one piece at a time — learning by building rather than by copying.

---

