# 🔐 Secure Flask HTTPS Login Server

A lightweight Flask-based HTTPS server that **enforces SSL/TLS**, accepts certificate and key via **command-line arguments**, and provides a clean login UI for testing authentication and certificate workflows.

This project is especially useful for:

* 🔧 SSL/TLS debugging
* 🧪 Testing certificate validation behavior (CN/SAN mismatch, trust issues)

---

# 🧭 1. Overview

This application starts a **Flask web server over HTTPS only**. It prevents accidental HTTP usage by enforcing SSL certificate validation before startup.

Unlike typical Flask apps, this server:

* ❌ Does NOT allow HTTP fallback
* ✅ Requires valid `.crt` and `.key` files
* ✅ Stops execution immediately on misconfiguration

---

# 🚀 2. Features

### 🔐 Security Features

* Enforced HTTPS (no insecure fallback)
* CLI-based SSL configuration
* Strict certificate validation (presence, extension, existence)


---

# 🏗️ 3. Architecture

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

# 📦 4. Installation

## Step 1: Clone / Setup Project

```
project/
├── server.py
├── requirements.txt
└── README.md
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ 5. Usage

## 🔑 Basic Command :enter the following command on bash to start the server

```bash
python server.py --cert <certificate.crt> --key <private.key>
```

---

## ✅ Example (Local Files) :If the .crt and .key files are local then you can directly write the name in the command

```bash
python server.py --cert server.crt --key server.key
```

---

## ✅ Example (Absolute Paths — Recommended): if the .crt and .key files are not in local then can give the path

```bash
python server.py \
  --cert /etc/ssl/certs/server.crt \
  --key /etc/ssl/private/server.key
```

---

## 🌐 Access the Server

Open browser: Enter the IP address of server 

```
https://<your-ip>:5000
```

Example:

```
https://192.168.1.10:5000
```

---

# ⚙️ 6. Command-Line Arguments

| Argument | Required | Description                     | Default   |
| -------- | -------- | ------------------------------- | --------- |
| `--cert` | ✅ Yes    | Path to `.crt` certificate file | None      |
| `--key`  | ✅ Yes    | Path to `.key` private key      | None      |
| `--host` | ❌ No     | Server host                     | `0.0.0.0` |
| `--port` | ❌ No     | Server port                     | `5000`    |

---

# 🔍 7. SSL Validation Logic

Before the server starts, the following checks are performed:

### ✅ 1. Argument Presence

* Both `--cert` and `--key` must be provided

### ✅ 2. File Extension Check

* Certificate must end with `.crt`
* Key must end with `.key`

### ✅ 3. File Existence Check

* Confirms both files exist on disk

### ❌ Failure Behavior

* Prints error message
* Exits immediately using `sys.exit(1)`

---

# 🔄 8. Application Flow

1. Parse CLI arguments
2. Validate certificate & key
3. Start Flask with SSL context
4. Wait for client requests
5. Render login page
6. Handle login submission

---


# ❌ 9. Error Handling

The server will NOT start if:

### 🔴 Missing Arguments

```
ERROR: You MUST provide both --cert and --key
```

### 🔴 Invalid Extension

```
ERROR: Certificate must be a .crt file
```

### 🔴 File Not Found

```
ERROR: Certificate file not found
```

### 🔴 Runtime SSL Failure

```
Failed to start HTTPS server
```



---

# 📁 10. Project Structure

```
project/
│
├── server.py          # Main application
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

---

