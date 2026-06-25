---
tags:
  - incident
  - template
---

# Incident Template

## Title

Short issue title.

## Symptoms

- What the user/app/team observed.

## Impact

- Business/application impact.

## Possible Causes

- Cause 1
- Cause 2

## Investigation Commands

```bash
hostname
uptime
df -h
free -h
top
journalctl -xe
```

## Findings

- What was found.

## Resolution

- What was done to restore service.

## Verification

```bash
systemctl status <service>
curl -I http://localhost
```

## Lessons Learned

- What can be improved.
