#!/bin/bash

# === CONFIGURATION ===
GARMIN_EMAIL="$GARMIN_EMAIL"
GARMIN_PASSWORD="$GARMIN_PASSWORD"
GARMINDB_DIR="$HOME/GarminDB"
SESSION_FILE="$HOME/.garminconnect"

echo "📧 Garmin Email: $GARMIN_EMAIL"
echo "📁 Target directory: $GARMINDB_DIR"

# === STEP 1: Install system dependencies ===
echo "🔧 Installing Python and required system packages..."
sudo apt update && sudo apt install -y python3 python3-pip git sqlite3

# === STEP 2: Create virtual environment ===

# === STEP 3: Clone GarminDB if not present ===
if [ ! -d "$GARMINDB_DIR" ]; then
  echo "📥 Cloning GarminDB into $GARMINDB_DIR..."
  git clone https://github.com/tcgoetz/GarminDB.git "$GARMINDB_DIR"
fi

cd "$GARMINDB_DIR"
pip install --upgrade pip
pip install -r requirements.txt

# === STEP 4: Run GarminDB fetch ===
echo "🚀 Running GarminDB fetch..."

if [ ! -f "$SESSION_FILE" ]; then
  echo "🔐 First-time login..."
  python3 garmindb.py --username "$GARMIN_EMAIL"
else
  echo "🔁 Using saved session..."
  python3 garmindb.py --no-browser-login
fi

# === STEP 5: Confirm output ===
echo "📂 Checking SQLite output..."
if [ -f "garmindb.sqlite" ]; then
  sqlite3 garmindb.sqlite ".tables"
  echo "✅ Data fetch complete. SQLite database saved to: $GARMINDB_DIR/garmindb.sqlite"
else
  echo "❌ ERROR: garmindb.sqlite not found. Check login or network."
fi
