# VMware Linux Guest Slow

## Checks

```bash
uptime
vmstat 1 10
top
dmesg -T | tail
lscpu
lsblk
```

## Possible Causes

- CPU ready time on hypervisor
- Storage latency
- Memory ballooning or swapping
- VMware tools issue
- Oversubscribed host

## Escalation

Collect Linux evidence first, then engage VMware team with timestamp and symptoms.
