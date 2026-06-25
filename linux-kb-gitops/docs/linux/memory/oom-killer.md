# Out of Memory / OOM Killer

## Symptoms

- Application process killed unexpectedly
- Server becomes slow or unresponsive
- `dmesg` shows OOM messages
- Swap usage increases rapidly

## Commands

```bash
free -h
swapon --show
vmstat 1 10
ps aux --sort=-rss | head -20
dmesg -T | grep -i -E 'oom|killed process'
journalctl -k | grep -i oom
```

## Possible Causes

- Application memory leak
- Java heap too large
- Batch job consumed memory
- Not enough RAM for workload
- Swap misconfiguration

## Resolution

- Restart leaking process after approval
- Tune application heap or memory limit
- Add memory if recurring
- Review cron or batch schedule

## Verification

```bash
free -h
vmstat 1 10
dmesg -T | grep -i oom
```
