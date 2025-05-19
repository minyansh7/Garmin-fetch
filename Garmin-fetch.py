import os
import subprocess
import sys
from pathlib import Path

# === CONFIGURATION ===
GARMIN_EMAIL = os.getenv("GARMIN_EMAIL")
GARMIN_PASSWORD = os.getenv("GARMIN_PASSWORD")  # optional, for future use
HOME = str(Path.home())
GARMINDB_DIR = os.getenv("GARMINDB_DIR", f"{HOME}/GarminDB")
SESSION_FILE = f"{HOME}/.garminconnect"

print(f"📧 Garmin Email: {GARMIN_EMAIL}")
print(f"📁 Target directory: {GARMINDB_DIR}")

if not GARMIN_EMAIL:
    print("❌ GARMIN_EMAIL environment variable is not set.")
    sys.exit(1)

# === STEP 1: Ensure Dependencies (system) ===
# This is just a log message — use provisioning tools for actual installs
print("🔧 Ensure Python, pip, git, and sqlite3 are installed before running this script.")

# === STEP 2: Clone GarminDB repo if not present ===
GARMINDB_PATH = Path(GARMINDB_DIR)
if not GARMINDB_PATH.exists():
    print(f"📥 Cloning GarminDB into {GARMINDB_DIR}...")
    subprocess.run(["git", "clone", "https://github.com/tcgoetz/GarminDB.git", GARMINDB_DIR], check=True)

# === STEP 3: Install Python dependencies ===
print("📦 Installing Python dependencies...")
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([sys.executable, "-m", "pip", "install", "-r", f"{GARMINDB_DIR}/requirements.txt"], check=True)

# === STEP 4: Run GarminDB ===
print("🚀 Running GarminDB fetch...")
os.chdir(GARMINDB_DIR)

if not Path(SESSION_FILE).exists():
    print("🔐 First-time login...")
    subprocess.run([sys.executable, "garmindb.py", "--username", GARMIN_EMAIL], check=True)
else:
    print("🔁 Using saved session...")
    subprocess.run([sys.executable, "garmindb.py", "--no-browser-login"], check=True)

# === STEP 5: Confirm SQLite Output ===
DB_FILE = Path("garmindb.sqlite")
print("📂 Checking SQLite output...")
if DB_FILE.exists():
    print("✅ Database created successfully. Showing tables:\n")
    subprocess.run(["sqlite3", "garmindb.sqlite", ".tables"], check=True)
    print(f"✅ SQLite database saved to: {GARMINDB_DIR}/garmindb.sqlite")
else:
    print("❌ ERROR: garmindb.sqlite not found. Check login or network.")
