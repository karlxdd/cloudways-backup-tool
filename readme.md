# Cloudways Backup Tool
> Automated local backups for Cloudways-hosted MySQL databases and uploaded files using Docker.

## Introduction
This is a personal project I built and use to **automatically back up databases and uploaded files** (such as images) from Cloudways-hosted applications to a **local machine** using Docker.

## Notes:
- Designed specifically for **Cloudways-hosted applications**
- Backs up **MySQL databases** using `mysqldump`
- Optionally backs up **uploaded files** (e.g., images) from your app's `public_html` directory
- Configurable using `.env` and `databases.json` files
- Runs inside a **Docker container**, no Python or MySQL client installation needed on your host
- Can be scheduled using **cron (Linux/macOS)** or **Task Scheduler (Windows)** for automated backups

## Requirements

Before using this project, make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (required)
- Python is handled automatically inside the container
- Access to your Cloudways database and file paths

## Setup

### 1. Clone this repo

```bash
git clone https://github.com/your-username/cloudways-backup.git
cd cloudways-backup
```

### 2. Create your .env file
The .env file controls global settings such as whether or not to include uploaded files (e.g., images) in your backup.

Create it from the sample file:
```bash
cp .env.sample .env
```

### 3. Set up your database configurations
Copy the sample database config file and update it with your actual database details and optional upload paths:
```bash
cp databases-sample.json databases.json
```

### 4. Run the backup using Docker Compose
Once you've set everything up, run the backup using (only include `--build` if you haven't built the image yet or made changes):
```bash
docker-compose up --build
```
This will:
- Build the Docker image (if not already built)
- Load your environment variables from .env
- Mount your volumes (local backups folder, databases.json, and application uploads)
- Execute the backup script

To stop the container after the run (Use docker-compose down if you also want to remove the container.):
```bash
docker-compose stop
```

### 5. Schedule Automatic Backups (Optional)
To automate backups, use tools like cron (Linux/macOS) or Task Scheduler (Windows) to run the following from your project directory:
```bash
docker-compose up --no-build
```
Make sure Docker is running before the scheduled job starts.
