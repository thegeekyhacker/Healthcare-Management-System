# 🏥 Healthcare Management System

A CLI-based Healthcare Management System built in Python with MySQL, supporting doctor and admin workflows including patient management, billing, prescriptions, face recognition login, voice-based prescription input, and an MCP server for AI integration.

---

## Features

- **Dual Role Access** — Separate workflows for Doctors and Administrative Staff
- **Authentication** — Password-based login with bcrypt hashing + face recognition via `dlib` / `face_recognition`
- **Patient Management** — Register new patients, view demographics, medical history, prescriptions
- **Appointment Scheduling** — Create and view appointments per doctor
- **Billing** — Generate OPD and Hospital (inpatient) bills as PDF, auto-emailed to patients
- **Prescription Management** — Voice-dictated prescriptions saved as `.txt` files and stored in the database
- **Queue Management** — JSON-based patient queue per doctor with text-to-speech patient calls
- **Telegram Video Calls** — One-click Telegram call link from doctor UI
- **MCP Server** — Read-only Model Context Protocol server exposing hospital data as tools for AI clients (Claude, etc.)
- **Attendance Tracking** — Face recognition login writes timestamped attendance CSV files

---

## Project Structure

```
healthcare-management-system/
├── main.py                          # Entry point
├── config/
│   ├── sql_config.py                # MySQL connection config (via .env)
│   └── email_config.py              # SMTP email config (via .env)
├── connector/
│   └── mysql_connector.py           # Singleton MySQL connection manager
├── services/
│   ├── auth_service.py              # Login, face login, user registration
│   ├── appointment_service.py       # View and create appointments
│   ├── billing_service.py           # OPD and hospital bill generation
│   ├── doctor_service.py            # Schedule, prescriptions (voice input)
│   ├── face_service.py              # Webcam capture and face verification
│   ├── patient_service.py           # Patient details and registration
│   └── queue_service.py             # Patient queue (JSON-backed)
├── ui/
│   ├── admin_ui.py                  # Admin CLI menu
│   └── doctor_ui.py                 # Doctor CLI menu
├── utility/
│   ├── sql_util.py                  # DB query helpers (fetch_all, execute_query, etc.)
│   ├── pdf_util.py                  # ReportLab PDF bill generation
│   ├── mail_util.py                 # SMTP email sender (bills + generic)
│   ├── password_util.py             # bcrypt hashing with pepper
│   ├── passwordhide.py              # Cross-platform hidden password input
│   ├── voice_util.py                # pyttsx3 text-to-speech
│   ├── greeting.py                  # Time-based greeting
│   ├── fix_passwords.py             # One-time migration: hash plain-text passwords
│   └── import_prescriptions.py      # Import prescription .txt files into DB
├── mcp_server/
│   └── server.py                    # FastMCP server with read-only HMS tools
├── queue/
│   └── queue_data.json              # Live patient queue state
├── prescriptions/                   # Generated prescription .txt files
├── bills/
│   ├── opdbill/                     # OPD bill PDFs
│   └── hbill/                       # Hospital bill PDFs
├── Attendance/                      # Daily attendance CSVs (from face login)
├── Images/                          # Reference face images for recognition
├── hcm_database.sql                 # Full DB dump (schema + seed data)
├── healthcare_management_structure.sql  # Schema-only dump
└── requirements.txt
```

---

## Prerequisites

- Python 3.11 (recommended — required for `dlib` / `face_recognition` compatibility)
- MySQL 8.0+
- A webcam (for face recognition features)
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) enabled

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/thegeekyhacker/healthcare-management-system.git
cd healthcare-management-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

> **Note on `dlib`:** On Windows, install a prebuilt wheel for your Python version before running `pip install -r requirements.txt`. Find wheels at [github.com/z-mahmud22/Dlib_Windows_Python3.x](https://github.com/z-mahmud22/Dlib_Windows_Python3.x).

```bash
pip install -r requirements.txt
```

### 4. Set up the MySQL database

```bash
mysql -u root -p < hcm_database.sql
```

This creates the `healthcare_management` database with all tables and seed data.

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DB_PASSWORD=your_mysql_password
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

### 6. Hash existing passwords (first-time setup only)

If you loaded the seed data from `hcm_database.sql`, the passwords are plain-text. Run the migration script to hash them:

```bash
python -m utility.fix_passwords
```

### 7. Run the application

```bash
python main.py
```

---

## Default Credentials (after password hashing)

| User ID | Plain Password   | Role  |
|---------|-----------------|-------|
| A1      | password123      | Admin |
| A2      | securepass       | Admin |
| A3      | adminpass        | Admin |
| D1      | Password@123     | Doctor|
| D2      | Password@231     | Doctor|
| D3      | Password@132     | Doctor|

---

## MCP Server (AI Integration)

The MCP server exposes read-only tools for AI clients like Claude Desktop.

```bash
python -m mcp_server.server
```

Available tools include: `get_patient_summary`, `get_doctor_schedule`, `get_appointments`, `get_patient_bills`, `get_patient_prescriptions`, `get_queue_status`, `get_all_doctors`, `get_all_patients`, `send_hospital_bill_email`, `send_opd_bill_email`, and more.

To connect with Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hms": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/healthcare-management-system"
    }
  }
}
```

---

## Admin Menu Options

| Command      | Action                          |
|--------------|---------------------------------|
| `schedule`   | View a doctor's weekly schedule |
| `appointments` | View appointments for a doctor |
| `createapp`  | Schedule a new appointment      |
| `reg`        | Register a new patient          |
| `opdbill`    | Generate an OPD bill (PDF + email) |
| `hbill`      | Generate a hospital bill (PDF + email) |
| `add`        | Add patient to doctor's queue   |
| `view`       | View queue for a doctor         |
| `logout`     | Exit the session                |

## Doctor Menu Options

| Command      | Action                              |
|--------------|-------------------------------------|
| `schedule`   | View your weekly schedule           |
| `appointments` | View your upcoming appointments   |
| `details`    | View patient details + prescriptions |
| `prescribe`  | Voice-dictate a prescription        |
| `call`       | Call next patient from queue (TTS)  |
| `video`      | Open Telegram call link for patient |
| `logout`     | Exit the session                    |

---

## Security Notes

- Passwords are hashed with **bcrypt** and a custom pepper (`SALT_PREFIX`/`SALT_SUFFIX` in `password_util.py`).
- Several service functions use **f-string SQL queries** which are vulnerable to SQL injection. These should be migrated to parameterised queries (`%s` with `params` tuple) before any production deployment.
- Credentials are stored in `.env` (excluded from version control via `.gitignore`).

---

## Tech Stack

| Layer         | Technology                                      |
|---------------|-------------------------------------------------|
| Language      | Python 3.11                                     |
| Database      | MySQL 8.0 via `mysql-connector-python`          |
| Auth          | bcrypt, dlib, face_recognition, OpenCV          |
| PDF           | ReportLab                                       |
| Email         | smtplib (Gmail SMTP / App Password)             |
| TTS           | pyttsx3                                         |
| STT           | SpeechRecognition + PyAudio                     |
| MCP Server    | FastMCP (`mcp` package)                         |
| Config        | python-dotenv                                   |

---

## License

MIT