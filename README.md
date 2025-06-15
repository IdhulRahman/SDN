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
# Password: rocks
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
