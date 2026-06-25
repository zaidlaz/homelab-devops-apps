# Linux Incident Template

## Summary

Brief description of the issue.

## Symptoms

- Server slow
- High CPU
- High memory
- Application timeout

## Initial Checks

```bash
uptime
top -c
free -h
vmstat 1 5
df -h
journalctl -xe
