# Filesystem Full

## Symptoms

- `No space left on device`
- Application cannot write logs
- Login or service startup failure

## Commands

```bash
df -h
df -i
du -xh /var | sort -h | tail -20
find /var/log -type f -size +100M -ls
lsof | grep deleted
```

## Resolution

- Compress or remove approved old logs
- Clean temporary files
- Restart process holding deleted files if approved
- Extend LVM/filesystem if required
