# Accessing My Recipe App from Android and iPhone

## Overview

The My Recipe application is hosted in the Homelab Kubernetes cluster and is accessible using the following URL:

```text
https://recipe.lab
```

To access the application from Android and iPhone devices, the device must be connected to the home Wi-Fi network and use the Homelab DNS server (AdGuard Home).

---

# Homelab Architecture

```text
Android / iPhone
        |
        | Wi-Fi
        |
TP-Link BE9700 Router
        |
        | DNS
        v
AdGuard Home
192.168.13.10
        |
        | DNS Rewrite
        |
recipe.lab -> 192.168.13.240
        |
        v
Traefik Ingress
192.168.13.240
        |
        v
My Recipe Application
```

---

# Requirements

## Network Requirements

The mobile device must:

* Be connected to the home Wi-Fi network
* Receive DNS settings from DHCP
* Have Private DNS disabled or set to Automatic

## DNS Configuration

The router DHCP server is configured as follows:

| Setting         | Value         |
| --------------- | ------------- |
| Default Gateway | 192.168.13.1  |
| Primary DNS     | 192.168.13.10 |
| Secondary DNS   | 1.1.1.1       |

AdGuard Home DNS Rewrite:

| Hostname   | IP Address     |
| ---------- | -------------- |
| recipe.lab | 192.168.13.240 |

---

# Android Configuration

## Step 1 - Connect to Wi-Fi

Connect the Android phone to the home Wi-Fi network.

---

## Step 2 - Verify Private DNS

Navigate to:

```text
Settings
→ Network & Internet
→ Private DNS
```

Select:

```text
Automatic
```

or

```text
Off
```

Do NOT use:

```text
Private DNS Provider Hostname
```

Example:

```text
dns.google
one.one.one.one
```

These services bypass the Homelab DNS server and prevent recipe.lab from resolving.

---

## Step 3 - Reconnect to Wi-Fi

If DNS changes were recently made:

1. Forget the Wi-Fi network
2. Reconnect
3. Verify internet connectivity

---

## Step 4 - Access Application

Open Chrome and browse to:

```text
https://recipe.lab
```

The My Recipe application should load successfully.

---

# iPhone Configuration

## Step 1 - Connect to Wi-Fi

Connect the iPhone to the home Wi-Fi network.

---

## Step 2 - Verify DNS Configuration

Navigate to:

```text
Settings
→ Wi-Fi
→ (i) Information Icon
```

Ensure:

```text
Configure DNS
```

is set to:

```text
Automatic
```

Do not manually configure public DNS servers.

---

## Step 3 - Reconnect to Wi-Fi

If DNS changes were recently made:

1. Forget the Wi-Fi network
2. Reconnect to Wi-Fi

---

## Step 4 - Access Application

Open Safari and browse to:

```text
https://recipe.lab
```

The My Recipe application should load successfully.

---

# Troubleshooting

## Cannot Resolve recipe.lab

Symptoms:

```text
This site can't be reached
DNS_PROBE_FINISHED_NXDOMAIN
```

Verify:

* Device connected to home Wi-Fi
* Private DNS disabled (Android)
* Automatic DNS enabled (iPhone)
* AdGuard Home is running

---

## Verify AdGuard Home

Browse:

```text
http://192.168.13.10
```

If AdGuard Home is inaccessible:

* Check VM status in Proxmox
* Verify network connectivity
* Verify DNS service is running

---

## Verify DNS Resolution

From a Windows PC:

```powershell
nslookup recipe.lab 192.168.13.10
```

Expected:

```text
Name: recipe.lab
Address: 192.168.13.240
```

---

# Remote Access (Optional)

For access outside the home network:

Install Tailscale on the mobile device.

Requirements:

* Tailscale installed
* User authenticated to the Homelab Tailnet
* Subnet routing enabled

This allows secure remote access without exposing services to the public Internet.

---

# Service Information

| Service      | URL                      |
| ------------ | ------------------------ |
| My Recipe    | https://recipe.lab       |
| AdGuard Home | http://192.168.13.10     |
| Proxmox VE   | https://proxmox.lab:8006 |
| Grafana      | https://grafana.lab      |
| ArgoCD       | https://argocd.lab       |

---

# Last Updated

Homelab Environment:

* Proxmox VE 9.x
* Kubernetes (kubeadm)
* Traefik Ingress
* MetalLB
* cert-manager
* AdGuard Home
* TP-Link BE9700
* Tailscale
