<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>

<h1>🔐 Password Manager System</h1>

<p>A secure, production-grade Password Manager with:</p>
<ul>
  <li>MySQL database storage (inside Docker)</li>
  <li>AES-256 encryption (or optional AWS KMS)</li>
  <li>Flask Web Interface (Bootstrap 5 styled)</li>
  <li>Authentication and 2FA (Google Authenticator / Authy apps)</li>
  <li>Production deployment using Gunicorn + Nginx (inside Docker)</li>
</ul>

<hr>

<h2>🚀 Capabilities</h2>

<ul>
  <li>🔒 Secure storage of usernames, passwords, credential names, and addresses</li>
  <li>🛡️ AES-256 encryption (or optional AWS KMS for enterprise-grade security)</li>
  <li>🧩 Web interface with login, dashboard, and management features</li>
  <li>📱 Two-Factor Authentication (2FA) with TOTP (Google Authenticator compatible)</li>
  <li>🔍 Search credentials by name instantly</li>
  <li>📋 Pagination for easy browsing of many credentials</li>
  <li>➕ Add new credentials securely</li>
  <li>✏️ Edit existing credentials</li>
  <li>🗑️ Delete credentials securely</li>
  <li>📈 Password strength checking when adding or editing entries</li>
  <li>🚪 Secure login and logout sessions with session timeout</li>
  <li>🛠️ CLI-based database initialization and maintenance tools</li>
  <li>🐳 Full containerized setup with Docker (MySQL, Web App, Nginx)</li>
  <li>🌐 Production-ready deployment with Gunicorn and Nginx</li>
</ul>

<hr>

<h2>⚙️ Installation & Configuration</h2>

<h3>1. Install Docker and Docker Compose</h3>
<p>If you do not already have Docker installed, follow these steps:</p>
<ul>
  <li><a href="https://docs.docker.com/get-docker/" target="_blank">Install Docker</a> for your operating system.</li>
  <li>Ensure Docker Compose is installed (comes bundled with Docker Desktop).</li>
  <li>Verify installation:</li>
</ul>
<pre><code>docker --version
docker-compose --version
</code></pre>

<h3>2. Clone the Repository</h3>
<pre><code>git clone https://github.com/your-repo/password-manager.git
cd password-manager
</code></pre>

<h3>3. Create a Virtual Environment (Optional but Recommended)</h3>
<pre><code>python3 -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows
</code></pre>

<h3>4. Install Python Dependencies</h3>
<pre><code>pip install -r requirements.txt
</code></pre>

<h3>5. Set Up Environment Variables (.env File)</h3>

Create a <code>.env</code> file in the project root with:

<pre><code>
# Database settings
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=password_manager_db
MYSQL_USER=user
MYSQL_PASSWORD=userpassword

# Flask Secret Key
SECRET_KEY=change_this_to_a_random_secret

# Encryption (local AES by default)
ENCRYPTION_MODE=LOCAL
AES_KEY=your-32-byte-strong-key

# (Optional) AWS KMS
AWS_REGION=your-region
AWS_KMS_KEY_ID=your-kms-key-id

# 2FA (TOTP)
TOTP_SECRET=your-initial-2fa-secret
</code></pre>

<h3>6. Start the MySQL Database Container</h3>
<p>In the <code>docker</code> folder, start the MySQL container first:</p>
<pre><code>cd docker
docker-compose up -d mysql
</code></pre>

<h3>7. Initialize the Database Schema</h3>
<p>After MySQL is running, run the database initializer:</p>
<pre><code>cd ..
python main.py --init-db
</code></pre>

<h3>8. Start the Entire Application Stack</h3>
<p>This launches MySQL, the Web Application (Flask + Gunicorn), and Nginx proxy:</p>
<pre><code>docker-compose up --build
</code></pre>

<h3>9. Access the Web Interface</h3>

Visit:

<pre><code>http://localhost
</code></pre>

Login with the default admin account:

<ul>
<li><b>Username:</b> admin</li>
<li><b>Password:</b> adminpassword</li>
</ul>

You will also be asked to complete Two-Factor Authentication (2FA) using an authenticator app like Google Authenticator.

---

<h2>📂 Project File & Folder Structure (With Detailed Explanations)</h2>

<pre>
password-manager/
├── app/                        # Core backend application code
│   ├── __init__.py              # Marks 'app' as a Python package
│   ├── database.py              # Connects to MySQL and initializes the 'credentials' table
│   ├── encryption.py            # Handles AES-256 encryption and AWS KMS encryption
│   ├── manager.py               # Business logic for adding, editing, deleting, reporting credentials
│   ├── password_utils.py        # Password strength checker (enforces strong password rules)
│
├── web/                         # Frontend Flask app
│   ├── __init__.py              # Flask app creation, login manager initialization
│   ├── auth.py                  # User authentication, session management, 2FA verification
│   ├── routes.py                # Web routes: dashboard, add/edit/delete credentials, search, pagination
│   ├── templates/               # HTML Templates (Jinja2)
│   │   ├── base.html            # Common layout for all pages (navigation, styling)
│   │   ├── login.html           # Login form page
│   │   ├── 2fa.html             # Two-Factor Authentication form page
│   │   ├── index.html           # Main dashboard: list credentials with search/pagination
│   │   ├── add.html             # Form to add new credentials
│   │   ├── edit.html            # Form to edit existing credentials
│   ├── static/
│   │   ├── styles.css           # Custom frontend styling (Bootstrap-enhanced)
│
├── docker/                      # Docker and Nginx setup
│   ├── docker-compose.yml       # Defines Docker containers (MySQL, Web App, Nginx)
│   ├── Dockerfile.web            # Dockerfile to containerize the Flask application
│   ├── nginx/
│   │   ├── nginx.conf            # Nginx configuration file (reverse proxy for web app)
│
├── .env                          # Environment variable settings (database, encryption, keys)
├── requirements.txt              # All Python dependencies to install
├── main.py                       # CLI tool to initialize the database manually
└── README.html                   # This documentation file
</pre>

---

<h2>✅ Features in Production Mode</h2>
<ul>
  <li>Gunicorn serves the Flask app with multiple workers</li>
  <li>Nginx reverse proxies HTTP requests to the web app securely</li>
  <li>All sensitive data encrypted with AES-256 or AWS KMS</li>
  <li>Database and application are isolated inside Docker containers</li>
</ul>

---

<h2>🎯 Future Improvements</h2>
<ul>
  <li>Password reset workflows</li>
  <li>Multi-user accounts with role-based access</li>
  <li>Backup code generation for 2FA device loss</li>
  <li>Scheduled encrypted database backups</li>
</ul>

---

<h2>👨‍💻 Author</h2>

<ul>
  <li><a href="https://github.com/joshuanmoses">Joshua Moses</a> — AI & Threat Expert</li>
</ul>

</body>
</html>
