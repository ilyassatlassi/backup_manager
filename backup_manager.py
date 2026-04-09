import sys

#!/usr/bin/env python3

import sys
import os
import datetime
import subprocess
import signal

LOG_DIR = "./logs"
BACKUPS_DIR = "./backups"
LOG_FILE = "./logs/backup_manager.log"
SCHEDULE_FILE = "backup_schedules.txt"
PID_FILE = "backup_service.pid"


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


# Create schedule
def create_schedule(schedule):
    try:
        parts = schedule.split(";")

        if len(parts) != 3:
            log(f"Error: malformed schedule: {schedule}")
            return

        with open(SCHEDULE_FILE, "a") as f:
            f.write(schedule + "\n")

        log(f"New schedule added: {schedule}")

    except Exception as e:
        log(f"Error: {str(e)}")


# List schedules
def list_schedules():
    try:
        if not os.path.exists(SCHEDULE_FILE):
            log("Error: can't find backup_schedules.txt")
            return

        log("Show schedules list")

        with open(SCHEDULE_FILE, "r") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            print(f"{index}: {line.strip()}")

    except Exception as e:
        log(f"Error: {str(e)}")


# Delete schedule
def delete_schedule(index):
    try:
        if not os.path.exists(SCHEDULE_FILE):
            log("Error: can't find backup_schedules.txt")
            return

        with open(SCHEDULE_FILE, "r") as f:
            lines = f.readlines()

        index = int(index)

        if index < 0 or index >= len(lines):
            log(f"Error: can't find schedule at index {index}")
            return

        lines.pop(index)

        with open(SCHEDULE_FILE, "w") as f:
            f.writelines(lines)

        log(f"Schedule at index {index} deleted")

    except Exception as e:
        log(f"Error: {str(e)}")


# Start backup service
def start_service():
    try:
        if os.path.exists(PID_FILE):
            log("Error: backup_service already running")
            return

        process = subprocess.Popen(
            ["python3", "backup_service.py"],
            start_new_session=True
        )

        with open(PID_FILE, "w") as f:
            f.write(str(process.pid))

        log("backup_service started")

    except Exception as e:
        log(f"Error: {str(e)}")


# Stop backup service
def stop_service():
    try:
        if not os.path.exists(PID_FILE):
            log("Error: can't stop backup_service")
            return

        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())

        os.kill(pid, signal.SIGTERM)

        os.remove(PID_FILE)

        log("backup_service stopped")

    except Exception as e:
        log("Error: can't stop backup_service")


# List backups
def list_backups():
    try:
        if not os.path.exists(BACKUPS_DIR):
            log("Error: can't find backups directory")
            return

        log("Show backups list")

        files = os.listdir(BACKUPS_DIR)

        for file in files:
            print(file)

    except Exception as e:
        log(f"Error: {str(e)}")


# Main CLI
def main():
    try:
        if len(sys.argv) < 2:
            log("Error: No command provided")
            return

        command = sys.argv[1]

        if command == "create":
            if len(sys.argv) < 3:
                log("Error: missing schedule")
                return
            create_schedule(sys.argv[2])

        elif command == "list":
            list_schedules()

        elif command == "delete":
            if len(sys.argv) < 3:
                log("Error: missing index")
                return
            delete_schedule(sys.argv[2])

        elif command == "start":
            start_service()

        elif command == "stop":
            stop_service()

        elif command == "backups":
            list_backups()

        else:
            log(f"Error: Unknown command {command}")

    except Exception as e:
        log(f"Error: {str(e)}")


if __name__ == "__main__":
    main()