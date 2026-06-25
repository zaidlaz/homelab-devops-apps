# Incident Title

## Summary

A brief summary of the incident.

---

## Symptoms

- High CPU
- Server slow
- Application timeout

---

## Environment

| Item | Value |
|------|-------|
| OS | RHEL 8 |
| Application | Oracle |
| Environment | Production |
| Server | server01 |

---

## Investigation

### Commands

```bash
top
free -h
vmstat 1
iostat -x 1
df -h
journalctl -xe
```

### Findings

Describe what was discovered.

---

## Root Cause

Describe the actual root cause.

---

## Resolution

Step-by-step resolution.

Example:

```bash
systemctl restart httpd
```

---

## Verification

How was the issue verified?

```bash
systemctl status httpd
curl localhost
```

---

## Prevention

- Monitoring
- Alerting
- Capacity planning
- Patch

---

## Lessons Learned

What should be improved?

---

## Related Articles

- High CPU
- Memory Leak
- OOM Killer

---

## Tags

linux
cpu
memory
oracle
production
