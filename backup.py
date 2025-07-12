import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import platform

# Load .env variables
load_dotenv()

# Flags from .env
BACKUP_MODE = os.getenv("BACKUP_MODE", "only-db").lower()

VALID_MODES = {"both", "only-db", "only-uploads"}

if BACKUP_MODE not in VALID_MODES:
    print(f"❌ Invalid BACKUP_MODE: '{BACKUP_MODE}'")
    print("Please set BACKUP_MODE to one of: both, only-db, only-uploads")
    exit(1)

# Dynamically resolve the backup directory
system = platform.system()
default_download_dir = {
    "Darwin": str(Path.home() / "Downloads"),
    "Windows": str(Path.home() / "Downloads"),
}.get(system, "./backups")

BASE_BACKUP_DIR = os.getenv("BACKUP_DIR", default_download_dir)

# Load databases list
with open("databases.json") as f:
    databases = json.load(f)

# Timestamp
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")

# Backup all databases
for db in databases:
    db_name = db["name"]
    db_host = db["host"]
    db_port = str(db.get("port", 3306))
    db_user = db["user"]
    db_pass = db["pass"]
    uploads_path = db.get("uploads_path", "")

    # Create folder for backup
    backup_dir = Path(BASE_BACKUP_DIR) / f"BACKUP DB - {date_str}" / db_name
    backup_dir.mkdir(parents=True, exist_ok=True)

    # === DB BACKUP ===
    if BACKUP_MODE in ("both", "only-db"):
        sql_filename = f"{db_name}_{date_str}.sql"
        sql_path = backup_dir / sql_filename

        print(f"🔄 Backing up `{db_name}` from `{db_host}`...")
        cmd = [
            "mysqldump",
            f"-h{db_host}",
            f"-P{db_port}",
            f"-u{db_user}",
            f"-p{db_pass}",
            db_name
        ]
        with open(sql_path, "w") as f:
            subprocess.run(cmd, stdout=f)
        print(f"✅ Saved: {sql_path}")

    # === UPLOADS COPY ===
    if BACKUP_MODE in ("both", "only-uploads"):
        if uploads_path and Path(uploads_path).exists():
            uploads_target = backup_dir / "uploads"
            subprocess.run(["cp", "-r", uploads_path, str(uploads_target)])
            print(f"📂 Copied uploads for `{db_name}` → {uploads_target}")
        else:
            print(f"⚠️ Skipped uploads for `{db_name}` — path not found or not defined.")

print("🎉 All backups completed.")