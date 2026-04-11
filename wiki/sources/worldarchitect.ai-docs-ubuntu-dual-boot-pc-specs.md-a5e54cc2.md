---
title: "Ubuntu Dual Boot System Information"
type: source
tags: [ubuntu, dual-boot, hardware, pc-specs, linux]
sources: []
source_file: docs/ubuntu-dual-boot-pc-specs.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary
Comprehensive system specifications and dual boot setup guide for a high-end desktop PC featuring Intel i9-13900K, 64GB RAM, NVIDIA RTX 4090, and 2TB NVMe storage. The system is rated as "ideal" for Ubuntu dual boot with UEFI/GPT configuration.

## Key Claims
- **CPU**: Intel Core i9-13900K (24 cores, 32 threads) — fully supported by Ubuntu 22.04/24.04
- **Memory**: 64GB RAM — massive overhead above Ubuntu's ~4GB minimum requirement
- **Storage**: 2TB NVMe SSD with 988GB free on C: drive, 938GB free on G: drive
- **Graphics**: NVIDIA GeForce RTX 4090 — requires proprietary drivers for optimal performance
- **Boot**: UEFI/GPT — ideal for secure dual boot configuration

## Partition Strategy
- **Option 1**: Shrink C: drive by 200-500GB → create 200GB Ubuntu root + 16GB swap
- **Option 2**: Use G: drive (938GB free, FAT32) — convert/repartition for Linux

## Driver Recommendations
- **NVIDIA**: Install `nvidia-driver-545` or newer for RTX 4090
- **WiFi/Bluetooth**: Intel chipset — should work out-of-box
- **Audio**: PulseAudio/PipeWire compatible

## System Assessment
This configuration is rated **EXCELLENT** for Ubuntu dual boot — high-end hardware with excellent Linux support, modern UEFI designed for dual boot, and powerful enough to run virtualization workloads.