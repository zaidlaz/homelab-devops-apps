# High Load Average

## Key Point

High load is not always high CPU. It can also be blocked IO, disk latency, NFS hang, or many runnable processes.

## Commands

```bash
uptime
vmstat 1 10
top
iostat -xz 1 5
ps -eo state,pid,ppid,cmd | awk '$1 ~ /D|R/ {print}'
```

## Investigation

- `R` state usually points to CPU pressure
- `D` state usually points to IO wait or blocked storage
