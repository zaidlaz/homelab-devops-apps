# Server Slow

## Symptoms

- SSH login is slow
- Application response time is poor
- Monitoring alert for CPU, memory, IO, or load
- Users report timeout or degraded performance

## First Checks

```bash
uptime
hostnamectl
df -h
free -h
vmstat 1 10
top
```

## Decision Flow

```text
Server slow
├── High CPU?       top, mpstat, pidstat
├── High memory?    free, vmstat, ps --sort=-rss
├── High IO wait?   iostat, iotop, sar -d
├── Disk full?      df -h, df -i, du
├── Network issue?  ss, ping, traceroute, sar -n
└── App issue?      logs, systemctl, journalctl
```

## Resolution Examples

- Restart problematic service after approval
- Clear safe temporary files or old logs
- Stop runaway batch job
- Escalate to application/database/network/storage team

## Verification

```bash
uptime
free -h
df -h
systemctl status <service>
```
