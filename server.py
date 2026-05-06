from flask import Flask, request, render_template_string, send_file
import argparse
import os
import sys

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }

        .login-card {
            background: white;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 300px;
            text-align: center;
        }

        h2 {
            margin-bottom: 20px;
            color: #333;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 6px;
            border: 1px solid #ccc;
            outline: none;
        }

        input:focus {
            border-color: #667eea;
        }

        button {
            width: 100%;
            padding: 10px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
        }

        button:hover {
            background: #5a67d8;
        }

        .message {
            margin-top: 15px;
            font-weight: bold;
        }

        .success {
            color: green;
        }

        .error {
            color: red;
        }
    </style>
</head>
<body>

<div class="login-card">
    <h2> Login</h2>

    <form method="POST">
        <input name="username" placeholder="Username" required>
        <input name="password" type="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>

    <br>

    <a href="/download-cert">
        <button type="button">Download SSL Certificate</button>
    </a>

    {% if message %}
        <div class="message {{ 'success' if 'successful' in message else 'error' }}">
            {{ message }}
        </div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            message = "Login successful ?"
        else:
            message = "Invalid credentials ?"

    return render_template_string(HTML, message=message)
    
@app.route("/download-cert")
def download_cert():
    return send_file(
        CERT_FILE,
        as_attachment=True
    )

def validate_ssl_files(cert, key):
    # Check presence
    if not cert or not key:
        print("\n ERROR: You MUST provide both --cert and --key\n")
        sys.exit(1)

    # Check extension (basic sanity check)
    if not cert.endswith(".crt"):
        print(f"\n ERROR: Certificate must be a .crt file ? {cert}")
        sys.exit(1)

    if not key.endswith(".key"):
        print(f"\n ERROR: Private key must be a .key file ? {key}")
        sys.exit(1)

    # Check existence
    if not os.path.isfile(cert):
        print(f"\n ERROR: Certificate file not found ? {cert}")
        sys.exit(1)

    if not os.path.isfile(key):
        print(f"\n ERROR: Key file not found ? {key}")
        sys.exit(1)

    print("\n SSL files validated successfully")
    print(f"   Cert: {cert}")
    print(f"   Key : {key}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Strict HTTPS Flask Server (SSL required)"
    )

    parser.add_argument("--cert", help="Path to server certificate (.crt)")
    parser.add_argument("--key", help="Path to private key (.key)")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)

    args = parser.parse_args()

    # ?? Enforce SSL (no fallback allowed)
    validate_ssl_files(args.cert, args.key)
    
    # Store certificate path globally
    global CERT_FILE
    CERT_FILE = args.cert

    try:
        app.run(
            host=args.host,
            port=args.port,
            ssl_context=(args.cert, args.key)
        )
    except Exception as e:
        print("\n Failed to start HTTPS server")
        print(f"Reason: {e}\n")
        sys.exit(1)