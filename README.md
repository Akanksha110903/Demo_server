
#  Secure Flask HTTPS Login Server

A lightweight Flask-based HTTPS server that **enforces SSL/TLS**, accepts certificate and key via **command-line arguments**, and provides a clean login UI for testing authentication and certificate workflows.

This project is especially useful for:  
- SSL/TLS debugging  
- Testing certificate validation behavior (CN/SAN mismatch, trust issues)

---

#  1. Overview

This application starts a **Flask web server over HTTPS only**. It prevents accidental HTTP usage by enforcing SSL certificate validation before startup.

Unlike typical Flask apps, this server:

-  Does NOT allow HTTP fallback  
-  Requires valid `.crt` and `.key` files  
-  Stops execution immediately on misconfiguration  

---

#  2. Features

###  Security Features

- Enforced HTTPS (no insecure fallback)  
- CLI-based SSL configuration  
- Strict certificate validation (presence, extension, existence)  

---

#  3. Architecture

```

User (Browser)
↓ HTTPS
Flask Server (app.run with ssl_context)
↓
Certificate + Key Validation (startup phase)
↓
Login Endpoint (/)

```

---

#  4. Installation

## Step 1: Clone / Setup Project : clone the project on your system

```

project/
├── server.py
├── requirements.txt
└── README.md

````

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
````

---

## Step 3: Create SSL Certificates using OpenSSL

This section explains how to generate:

 Private Key (`.key`)
 Self-signed Certificate (`.crt`)
 SAN-enabled certificate (required for IP/hostname access)

---

###  3.1 Prerequisites

Check if OpenSSL is installed:

```bash
openssl version
```

 Expected Output:

```
OpenSSL 3.x.x ...
```

---

###  If Not Installed

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install openssl
```

---

###  3.2 Create Working Directory

```bash
mkdir ssl-demo
cd ssl-demo
```

All certificate files will be generated here.

---

###  3.3 Create OpenSSL Configuration File (SAN Enabled)

Create config file with any name and .cnf extension:

```bash
nano openssl.cnf
```

Paste the following content in the file:

```
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = req_ext

[dn]
C = IN
ST = Maharashtra
L = Mumbai
O = Demo
CN = localhost

[req_ext]
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
IP.2 = 192.168.1.10
```


###  Important

Replace from openssl.cnf file:

```
IP.2 = 192.168.1.10
```

With your server system’s actual IP address

---

###  Save File

* Press `CTRL + O` → Enter
* Press `CTRL + X`

---

###  3.4 Generate Certificate & Key : now run the following command in the same directory

```bash
openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout server.key \
-out server.crt \
-config openssl.cnf
```

---

 Output Files : following files will get generated in the directory

```
server.key   → Private Key
server.crt   → Certificate
```

---

###  3.5 Verify Certificate : to check the content of certificate or verity wether the IP is added run the following command

```bash
openssl x509 -in server.crt -text -noout
```

Look for:

```
X509v3 Subject Alternative Name:
    DNS:localhost, IP Address:127.0.0.1, IP Address:192.168.1.10
```

This confirms SAN is correctly added.

---

#  5. Usage

Basic Command : Enter the following command to start the server

```bash
python server.py --cert <certificate.crt> --key <private.key>
```

---

 Example (Local Files): if the certificate and key are present in local directory you can directly use it

```bash
python server.py --cert server.crt --key server.key
```

---

 Example (Absolute Paths — Recommended): if the certificate and key are located in other directly use absolute path as follows

```bash
python server.py \
  --cert /etc/ssl/certs/server.crt \
  --key /etc/ssl/private/server.key
```

if the arguments are correct the server will start

---

  Access the Server

Open browser: Enter the server IP and port

```
https://<your-ip>:5000
```

Example:

```
https://192.168.1.10:5000
```

A login page will appear
Also download SSL certificate button will appear below login, download the certificate and add into trusted certificate directory to avoid SSL certificate issue.

Steps to Add the certificate in the Trusted Certificate directory

1)For Linux:
Prerequisits:
Install NSS tools using following command: 
```
sudo apt install libnss3-tools
```
verify certutil is Installed
```
certutil -H
```
check whether NSSDB exists using following command:
```
ls ~/.pki/nssdb
```
create NSSDB if not present using following commands:
```
mkdir -p ~/.pki/nssdb
certutil -N -d sql:$HOME/.pki/nssdb
```
You will be asked to set a password

You can press Enter for no password during testing.

after creation verify database files:
```
ls ~/.pki/nssdb
```
You should see:
```
cert9.db
key4.db
pkcs11.txt
```
Add certificate into NSSDB using following command: 
```
certutil -A \
-d sql:$HOME/.pki/nssdb \
-n "Demo Server" \
-t "C,," \
-i server.crt
```
Verify certificate added successfully using
```
certutil -L -d sql:$HOME/.pki/nssdb
```
example output:
```
Certificate Nickname                                         Trust Attributes
                                                             SSL,S/MIME,JAR/XPI

Demo Server                                                  C,,
```

2)For windows :
Download the certificate and install into Trusted Root Certificate Authority directory

After adding the certificate in Trusted Root Certificate Authority directory the SSL certificate issue will not appear

---

#  6. Command-Line Arguments

| Argument | Required | Description                     | Default   |
| -------- | -------- | ------------------------------- | --------- |
| `--cert` |  Yes    | Path to `.crt` certificate file | None      |
| `--key`  |  Yes    | Path to `.key` private key      | None      |
| `--host` |  No     | Server host                     | `0.0.0.0` |
| `--port` |  No     | Server port                     | `5000`    |

---

#  7. SSL Validation Logic

Before the server starts, the following checks are performed:

### 1. Argument Presence

 Both `--cert` and `--key` must be provided

### 2. File Extension Check

 Certificate must end with `.crt`
 Key must end with `.key`

### 3. File Existence Check

 Confirms both files exist

---

###  Failure Behavior

 Prints error message
 Exits using:

```python
sys.exit(1)
```

---

#  8. Application Flow

1. Parse CLI arguments
2. Validate certificate & key
3. Start Flask with SSL context
4. Wait for client requests
5. Render login page
6. Handle login submission

---

#  9. Error Handling

### Missing Arguments

```
ERROR: You MUST provide both --cert and --key
```

---

### Invalid Extension

```
ERROR: Certificate must be a .crt file
```

---

### File Not Found

```
ERROR: Certificate file not found
```

---

### Runtime SSL Failure

```
Failed to start HTTPS server
```

---

#  10. Project Structure

```
project/
│
├── server.py          # Main application
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```


