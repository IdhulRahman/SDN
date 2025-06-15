# 💡 ONOS + Mininet Installation Guide

This guide explains the step-by-step installation of **Mininet**, **Java 8**, and **ONOS 2.0.0**, including how to run them for SDN (Software Defined Networking) simulations.

---

## 🔧 1. Install Mininet

```bash
# Clone the Mininet repository
git clone https://github.com/mininet/mininet
cd mininet

# List available versions
git tag

# Checkout a stable version (example: v2.2.2)
git checkout -b mininet-2.2.2

# Run the installer
cd ..
mininet/util/install.sh -nfv  # n: no Wireshark, f: OpenFlow, v: Open vSwitch
```

---

## ☕ 2. Install Java 8

```bash
# Install Java 8
sudo apt install openjdk-8-jdk
```

Add the following environment variables to your `~/.bashrc` file:

```bash
nano ~/.bashrc
```

Then add at the bottom of the file:

```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH
```

Apply the changes:

```bash
source ~/.bashrc
```

---

## 📦 3. Install ONOS 2.0.0

```bash
# Download ONOS
wget https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.0.0/onos-2.0.0.tar.gz

# Extract the archive
tar zxvf onos-2.0.0.tar.gz

# Move ONOS to system directory
sudo mkdir /opt/onos
sudo cp -r onos-2.0.0/* /opt/onos
```

---

## 🔐 4. Configure SSH (required for ONOS CLI access)

Edit your SSH config:

```bash
nano ~/.ssh/config
```

Add the following lines:

```bash
HostKeyAlgorithms +ssh-rsa
PubkeyAcceptedKeyTypes +ssh-rsa
```

---

## ▶️ 5. Run ONOS

```bash
# Start ONOS service
sudo /opt/onos/bin/onos-service start

# Access ONOS CLI
/opt/onos/bin/onos -l onos
# Password: rocks or karaf
```

### ✅ Activate ONOS Applications

```bash
# Basic pipeline support (P4)
app activate org.onosproject.pipelines.basic

# Automatic MAC/IP-based forwarding
app activate org.onosproject.fwd

# OpenFlow protocol support
app activate org.onosproject.openflow

# ONOS Web GUI support
app activate org.onosproject.gui
```

Press `Ctrl+D` to exit the ONOS CLI.

---

## 🌐 Access ONOS Web GUI

Open your browser and navigate to:

```
http://<ONOS-IP>:8181/onos/ui
```

**Login Credentials:**

* **Username:** `onos`
* **Password:** `rocks`

---

## 🔥 \[Optional] Enable ACL Firewall in ONOS

### 1️⃣ Activate the ACL App via ONOS CLI

Before applying firewall rules, make sure the ACL (Access Control List) application is active:

```bash
app activate org.onosproject.acl
```

> ✅ This enables ONOS to receive and enforce ACL rules via the REST API.

---

### 2️⃣ Prepare Your Environment

* Ensure Python 3 is installed.
* Install the required library:

```bash
pip install requests
```

---

### 📄 Example Policy File: `Rules/firewall-policies.csv`

```csv
id,mac_0,mac_1
1,56:0F:44:DC:59:5E,06:B2:FF:87:6D:43
2,06:16:78:2D:63:05,5A:F5:1C:E6:D5:8C
3,BA:9A:99:26:1B:6F,CE:4C:6E:70:38:BB
```

---

### 🚀 Add Firewall Rules: `Rules/Firewall.py`

```python
import csv
import requests

host = "10.0.2.15"  # Replace with your ONOS IP
port = "8181"
username = "karaf"
password = "karaf"
url = f"http://{host}:{port}/onos/v1/acl/rules"
headers = {'Content-type': 'application/json'}

policyFile = "Firewall/firewall-policies.csv"
firewall_rules = []
with open(policyFile, 'r') as csvfile:
    rows = csv.reader(csvfile)
    next(rows)  # skip header
    for row in rows:
        firewall_rules.append((row[1], row[2]))

for rule in firewall_rules:
    resp = requests.post(
        url,
        json={
            "srcIp": "10.0.0.0/24",
            "dstIp": "10.0.0.0/24",
            "srcMac": rule[0],
            "dstMac": rule[1]
        },
        auth=(username, password)
    )
    print(resp.text)
```

---

### ❌ Delete All Firewall Rules: `Rules/delete_firewall.py`

```python
import requests

host = "10.0.2.15"  # Replace with your ONOS IP
port = "8181"
username = "onos"
password = "rocks"
url = f"http://{host}:{port}/onos/v1/acl/rules"

resp = requests.delete(url, auth=(username, password))
print(resp.text)
```

---

### 🔍 Verify Rules in ONOS

After running the script, check that the rules were successfully applied:

```
http://<ONOS-IP>:8181/onos/v1/acl/rules
```

You can open this URL in your browser or fetch it via terminal:

```bash
curl -u onos:rocks http://<ONOS-IP>:8181/onos/v1/acl/rules | jq
```

---
