# High Memory Usage

## Commands

```bash
free -h
vmstat 1 10
top
ps -eo pid,ppid,user,cmd,%mem,rss --sort=-rss | head -20
pmap -x <pid> | tail -20
```

## Investigation

Check whether memory is used by application RSS, filesystem cache, shared memory, or swap pressure.

## Verification

Memory should stabilise and swap activity should reduce.
