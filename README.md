\# Backup Manager  
  
\## Overview  
  
Backup Manager is a Python-based automated backup system that allows users to schedule directory backups from the command line. The system runs a background service that checks scheduled times and creates compressed \`.tar\` backups automatically.  
  
This project simulates a real DevOps backup automation tool.  
  
\---  
  
\## Features  
  
\- Schedule directory backups  
\- Run backup service in background  
\- Create compressed \`.tar\` backup files  
\- Delete backup schedules  
\- List scheduled backups  
\- List generated backups  
\- Logging system for all actions  
\- Error handling  
  
\---  
  
\## Project Structure  

backup-manager/  
├── backup\_manager.py  
├── backup\_service.py  
├── logs/  
│ ├── backup\_manager.log  
│ └── backup\_service.log  
├── backups/  
├── backup\_schedules.txt  
└── README.md

  
\---  
  
\## Requirements  
  
\- Python 3  
\- Linux / MacOS (recommended)  
  
No external libraries required (uses Python standard library only)  
  
\---  
  
\## Commands  
  
\### Create Backup Schedule  
  
\`\`\`bash  
python3 backup\_manager.py create "path;HH:MM;backup\_name"

Example:

python3 backup\_manager.py create "test;16:07;backup\_test"

This means:

-   `test` → directory to backup
-   `16:07` → backup time
-   `backup_test` → backup file name

* * *

### List Schedules

python3 backup\_manager.py list

Example Output:

0: test;16:07;backup\_test  
1: docs;16:10;backup\_docs

* * *

### Delete Schedule

python3 backup\_manager.py delete INDEX

Example:

python3 backup\_manager.py delete 0

* * *

### Start Backup Service

python3 backup\_manager.py start

This runs `backup_service.py` in background.

* * *

### Stop Backup Service

python3 backup\_manager.py stop

Stops background backup service.

* * *

### List Backups

python3 backup\_manager.py backups

Example:

backup\_test.tar  
backup\_docs.tar

* * *

## How It Works

### Step 1 — Create a Directory to Backup

mkdir test  
touch test/file.txt

* * *

### Step 2 — Create Backup Schedule

python3 backup\_manager.py create "test;16:07;backup\_test"

* * *

### Step 3 — Start Service

python3 backup\_manager.py start

* * *

### Step 4 — Wait for Scheduled Time

When time matches:

16:07

Backup is created automatically:

backups/  
 └── backup\_test.tar

* * *

### Step 5 — Check Backups

ls backups/

* * *

## Logs

### Backup Manager Logs

logs/backup\_manager.log

Example:

\[10/04/2026 16:07\] New schedule added: test;16:07;backup\_test  
\[10/04/2026 16:07\] backup\_service started

* * *

### Backup Service Logs

logs/backup\_service.log

Example:

\[10/04/2026 16:07\] Backup done for test in backups/backup\_test.tar