# Server Slow Troubleshooting Flow

<div class="mermaid">
flowchart TD
    A([Alert: Server Slow]) --> B{Can you SSH?}
    B -->|No| C[Check VM, network, firewall, console]
    B -->|Yes| D[Check uptime and load average]

    D --> E{Load average high?}
    E -->|Yes| F[Check CPU with top, ps, pidstat]
    E -->|No| G[Check memory with free and vmstat]

    F --> H{High CPU process found?}
    H -->|Yes| I[Identify process owner and application]
    H -->|No| J[Check IO wait and kernel activity]

    G --> K{Swap used or memory low?}
    K -->|Yes| L[Check OOM logs and top memory processes]
    K -->|No| M[Check filesystem]

    M --> N{Filesystem full?}
    N -->|Yes| O[Clean logs, check deleted files, extend LVM]
    N -->|No| P[Check disk IO with iostat]

    P --> Q{IO wait high?}
    Q -->|Yes| R[Investigate storage or VMware datastore]
    Q -->|No| S[Check network and application logs]

    S --> T([Document RCA and verification])
</div>
