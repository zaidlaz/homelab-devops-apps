---
tags:
  - linux
  - performance
  - cpu
  - memory
  - iowait
---

# Server Slow

## First Checks

```bash
hostname
uptime
date
df -h
free -h
top
```

## CPU

```bash
mpstat 1 10
pidstat 1 10
ps -eo pid,ppid,cmd,%cpu --sort=-%cpu | head
```

## Memory

```bash
free -h
vmstat 1 10
ps aux --sort=-rss | head
```

## Disk I/O

```bash
iostat -xz 1 10
```

## Network

```bash
ss -s
sar -n DEV 1 5
```

## Decision Guide

| Finding | Likely direction |
|---|---|
| High `%user` CPU | Application/process issue |
| High `%wa` | Disk/SAN/NFS latency |
| High swap in/out | Memory pressure |
| Filesystem 100% | Storage cleanup or extension |
| Network retransmits | Network/app connectivity |
