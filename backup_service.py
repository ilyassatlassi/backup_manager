#!/usr/bin/env python3

import os
import time
import datetime
import tarfile

LOG_DIR = "./logs"
LOG_FILE = "./logs/backup_service.log"
SCHEDULE_FILE = "backup_schedules.txt"
BACKUPS_DIR = "./backups"


# Ensure directories exist
def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(BACKUPS_DIR, exist_ok=True)


# Logging function
def log(message):
    ensure_dirs()
    timestamp = datetime.datetime.now().strftime("[%d/%m/%Y %H:%M]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {message}\n")


# Read schedules
def read_schedules():
    if not os.path.exists(SCHEDULE_FILE):
        return []

    with open(SCHEDULE_FILE, "r") as f:
        return f.readlines()


# Write schedules
def write_schedules(lines):
    with open(SCHEDULE_FILE, "w") as f:
        f.writelines(lines)


# Create backup
def create_backup(path, backup_name):
    try:
        backup_path = f"{BACKUPS_DIR}/{backup_name}.tar"

        with tarfile.open(backup_path, "w") as tar:
            tar.add(path)

        log(f"Backup done for {path} in backups/{backup_name}.tar")

    except Exception as e:
        log(f"Error: {str(e)}")


# Main service loop
def main():
    while True:
        try:
            schedules = read_schedules()
            remaining = []

            current_time = datetime.datetime.now().strftime("%H:%M")

            for schedule in schedules:
                schedule = schedule.strip()

                if not schedule:
                    continue

                try:
                    path, schedule_time, name = schedule.split(";")

                    if current_time == schedule_time:
                        create_backup(path, name)
                    else:
                        remaining.append(schedule + "\n")

                except Exception:
                    log(f"Error: malformed schedule: {schedule}")

            write_schedules(remaining)

        except Exception as e:
            log(f"Error: {str(e)}")

        time.sleep(45)


if __name__ == "__main__":
    main()