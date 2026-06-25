# VCS Service Group Offline

## Symptoms

- Service group is offline
- Application VIP or mount is unavailable
- Cluster failover alert triggered

## Commands

```bash
hastatus -sum
hagrp -state
hares -state
hares -dep <resource>
```

## Investigation

- Check which resource failed
- Check dependency order
- Check mount, disk group, IP, NIC, and application resource
- Review engine logs

## Note

Keep this article generic and avoid real cluster names from banking environments.
