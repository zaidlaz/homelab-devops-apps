# High CPU Usage

## Commands

```bash
uptime
top
mpstat -P ALL 1 5
pidstat 1 5
ps -eo pid,ppid,user,cmd,%cpu --sort=-%cpu | head -20
```

## Possible Causes

- Runaway process
- Java garbage collection
- Backup or batch job
- Database query
- Monitoring or security scan

## Resolution

- Confirm owner of process
- Restart or stop approved process
- Tune application or schedule
- Escalate if process is business-critical
