# 05 — Firmware Extraction via EPROM Programmer

## Overview

This project documents the direct extraction of firmware from the TP-Link WR841N router using a CH341A EPROM programmer and SOIC clip — without needing the device to boot. This is an alternative firmware acquisition method to TFTP transfer and provides a complete, unmodified 4MB dump of the entire flash chip including bootloader, kernel, rootfs, config, and radio partitions.

> All work performed on personally owned lab equipment for educational purposes as part of TCM Security PIPA certification study.

---

## Hardware Used

- **Target chip**: EON EN25QH32A SPI NOR flash (4MB, SOP8 package)
- **Programmer**: CH341A USB EPROM programmer
- **Clip**: SOIC8 clip for in-circuit reading
- **Host machine**: Kali Linux VM (VirtualBox, USB passthrough)
- **Tool**: flashrom v1.6.0

---

## Firmware Extraction Methods

There are several ways to obtain router firmware:

1. Download from the manufacturer's website
2. Dump via TFTP transfer from the router shell to a local machine
3. Read via bootloader commands over serial
4. **Read directly from the ROM chip** ← this project

Option 4 was chosen because it gives a complete, raw 4MB dump of the entire flash — bypassing any software-level restrictions and not requiring the device to boot at all.

---

## Physically Identifying the Chip

The flash chip was identified using OSINT before touching any hardware:

- The router's **FCC ID** was used to look up internal photos on [fccid.io](https://fccid.io)
- Internal photos revealed the chip markings on the PCB
- Cross-referencing the markings with the manufacturer datasheet confirmed the chip as the **EON EN25QH32A**
- The datasheet was also used to identify **pin 1 orientation** — pin 1 is marked by a dot on the top-left corner of the chip package

![Full setup with CH341A programmer and SOIC clip connected to router PCB](https://i.imgur.com/BlPaEi0.jpeg)
---
*Fun fact: Hudson River Park is a great place : https://hudsonriverpark.org/ *
---

## Extraction Process

The router was powered off before connecting anything. The CH341A programmer was connected to the EN25QH32A flash chip via SOIC clip, with each wire traced to ensure correct signal alignment (chip select, MISO, MOSI, CLK, VCC, GND).

### Troubleshooting — Pin Orientation

Initial extraction attempts all returned `No EEPROM/flash device found`. After ruling out software issues (USB passthrough confirmed working via `lsusb`, correct chip name confirmed via `flashrom -L`), the root cause was identified:

**Pin 1 orientation was incorrect on both the flash chip and the CH341A programmer.** The programmer's pin layout is printed on the back of the board — this had not been checked initially. Once both orientations were corrected, the extraction succeeded.

This is a common mistake with SOIC clips and a critical detail to verify before any in-circuit read.

![CH341A programmer with SOIC clip cable](https://i.imgur.com/jxvrgB3.jpeg)

### Working Command

```bash
sudo flashrom -p ch341a_spi -c EN25QH32B -r tp_link_wr841n_ext.bin
```

Flag breakdown:
- `-p ch341a_spi` — specifies the CH341A as the programmer interface
- `-c EN25QH32B` — explicitly names the chip (EN25QH32A is not in flashrom's database by exact name; EN25QH32B is the closest match and works correctly)
- `-r` — read mode, outputs to the specified file

![PCB close-up showing MediaTek SoC, Zentel DRAM, and SOIC clip seated on flash chip](https://i.imgur.com/SpymfHS.jpeg)

---

## Verification

The firmware was read **twice** and MD5 hashes compared to confirm a clean, consistent extraction. Matching hashes across two independent reads rules out read errors or noise on the SPI bus.

```bash
# Read twice
sudo flashrom -p ch341a_spi -c EN25QH32B -r tp_link_wr841n_ext.bin
sudo flashrom -p ch341a_spi -c EN25QH32B -r tp_link_wr841n_fw_2ext.bin

# Compare hashes
diff <(md5sum tp_link_wr841n_ext.bin) <(md5sum tp_link_wr841n_fw_2ext.bin)

# Binary comparison
cmp tp_link_wr841n_ext.bin tp_link_wr841n_fw_2ext.bin && echo "IDENTICAL"
```

Both reads produced identical MD5 hash: `732b7ac4b726d24410deaac2fbe78173`

Binary comparison confirmed: **IDENTICAL** — dump is verified clean.

> The firmware binary is excluded from this repository via `.gitignore` (`*.bin`). The MD5 hash above serves as the integrity reference.

---

## Entropy Analysis

Binwalk was used to perform entropy analysis on the extracted firmware:

```bash
binwalk -E tp_link_wr841n_ext.bin
```

> Note: The `python3-numba` package caused a compatibility error with binwalk's entropy module. Removing it (`sudo apt remove python3-numba`) resolved the issue by falling back to pure Python entropy calculation.

![Entropy analysis graph and output](https://i.imgur.com/A8kcApc.png)

The entropy graph confirmed the internal partition structure, mapping closely to the MTD partition table:

| Offset | Entropy | Partition | Notes |
|---|---|---|---|
| 0x0 – 0x10000 | Low/Medium (~0.53) | `boot` | U-Boot bootloader, uncompressed |
| 0x10000 – 0xFE000 | High (~0.98) | `kernel` | Compressed kernel |
| 0x100000 – 0x3D4000 | High (~0.97) | `rootfs` | Compressed squashfs filesystem |
| 0x3D4000 – 0x400000 | Lower (~0.46) | `config` / `radio` | Config data and radio calibration |

High entropy (~0.98) is the signature of compressed data — squashfs and the kernel are compressed by design. The lower entropy at the end confirms uncompressed config and calibration data. This independently corroborated the expected partition layout without requiring the device to boot.

---

## Binwalk Extraction

```bash
binwalk -e tp_link_wr841n_ext.bin
```

This carved the firmware into its component parts, extracting the squashfs filesystem for further analysis. The extracted filesystem contains the complete router OS including `/etc`, `/bin`, `/sbin`, config files, and binaries — the starting point for further reverse engineering in Ghidra.

---

## Key Findings

- Direct chip extraction via EPROM programmer provides a complete, unmodified firmware dump without booting the device
- Pin 1 orientation must be verified on **both** the target chip and the programmer — a common failure point
- Entropy analysis independently confirmed the expected MTD partition layout
- The extracted squashfs filesystem is available for further static analysis and reverse engineering
