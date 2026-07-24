# EventFlow AI — Walkthrough

## 1. Project Overview

EventFlow AI is a QR-based smart attendance system built with a multi-agent architecture using LangGraph.

It automates: participant registration → ID generation → QR code creation → email delivery → event-day scanning → attendance tracking.

---

## 2. Folder Structure

```
EventFlow_AI/
├── main.py                  # Run the full registration workflow
├── scanner.py               # Run the event-day QR scanner
├── config.py                # Paths and environment config
├── constants.py             # Column names, status values, settings
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not tracked)
├── .env.example             # Template for .env
│
├── agents/
│   ├── registration_agent.py    # Reads & cleans participant data
│   ├── id_generator_agent.py    # Assigns unique registration IDs
│   ├── qr_generator_agent.py    # Generates QR code images
│   ├── email_qr_agent.py        # Emails QR codes to participants
│   ├── attendance_agent.py      # Marks attendance via scanned QR
│   └── logger_agent.py          # Colored console + file logging
│
├── services/
│   ├── google_sheet_service.py      # Google Sheets authentication & access
│   ├── registration_id_service.py   # ID generation logic
│   ├── qr_service.py               # QR code generation & saving
│   ├── email_service.py            # SMTP email with attachments
│   └── scanner_service.py          # Webcam QR scanning via pyzbar
│
├── orchestrator/
│   └── coordinator.py           # LangGraph workflow orchestration
│
├── generated/qr/               # Generated QR code images
├── logs/                        # system.log
├── credentials/                 # Google service account JSON
└── data/                        # Input data files
```

---

## 3. Required .env Variables

Create a `.env` file from `.env.example`:

```env
# Google Sheets
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_CREDENTIALS_FILE=credentials/service_account.json

# Event
EVENT_NAME=Your Event Name
ORGANIZER_NAME=Your Organization

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

> **Gmail**: Enable 2FA → generate an [App Password](https://myaccount.google.com/apppasswords).

---

## 4. Google Sheets Setup

1. Create a new Google Sheet.
2. Add these column headers in **Row 1**:

| registration_id | name | email | phone | college | event | qr_sent | email_sent | attendance_status | check_in_time |
|---|---|---|---|---|---|---|---|---|---|

3. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```
4. Paste it into `.env` as `GOOGLE_SHEET_ID`.

---

## 5. Service Account Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project → Enable **Google Sheets API** and **Google Drive API**.
3. Create a **Service Account** → download the JSON key.
4. Save it as `credentials/service_account.json`.
5. Share your Google Sheet with the service account email (Editor access).

---

## 6. How to Run

### Install dependencies

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

### Run the full registration workflow

```bash
python main.py
```

This executes: Load Registrations → Generate IDs → Create QR Codes → Send Emails.

### Run the event-day QR scanner

```bash
python scanner.py
```

Opens the webcam, scans QR codes, and marks attendance in real time. Press `q` to quit.

---

## 7. Google Form Workflow

```
Google Form
    ↓
Google Sheet (auto-populated)
    ↓
Registration ID Agent (assigns EVT20260001, ...)
    ↓
QR Generator Agent (creates PNG per participant)
    ↓
Email QR Agent (sends QR via email)
    ↓
Event Day — Scanner (webcam scans QR)
    ↓
Attendance Updated (status + timestamp in sheet)
```

**Pre-event**: `python main.py`
**Event day**: `python scanner.py`

---

## 8. Required Google Sheet Columns

| Column | Description |
|---|---|
| `registration_id` | Auto-generated (EVT20260001) |
| `name` | Participant name |
| `email` | Participant email |
| `phone` | Phone number |
| `college` | College / organization |
| `event` | Event name |
| `qr_sent` | "Yes" after QR is generated |
| `email_sent` | "Yes" after email is sent |
| `attendance_status` | "Checked In" after scanning |
| `check_in_time` | Timestamp of check-in |

> Columns can be empty initially — agents fill them automatically.

---

## 9. Troubleshooting

| Issue | Solution |
|---|---|
| `Credentials file not found` | Place `service_account.json` in `credentials/` |
| `Sheet not found` | Check `GOOGLE_SHEET_ID` in `.env` and share sheet with service account |
| `Worksheet not found` | Ensure the sheet tab is named `Sheet1` |
| `SMTP authentication failed` | Use a Gmail App Password, not your login password |
| `Camera not found` | Check webcam connection, try `camera_index=1` |
| `pyzbar decode error` | Install [zbar](https://github.com/NaturalHistoryMuseum/pyzbar#installation) for your OS |
| `Module not found` | Run `pip install -r requirements.txt` |
| `Permission denied on sheet` | Share the sheet with the service account email as Editor |

---

## 10. Future Improvements

- **Dashboard**: Web-based real-time attendance dashboard.
- **Bulk email**: Threaded email sending for large events.
- **Multi-event**: Support multiple events in one sheet.
- **Reports**: Auto-generate attendance reports (PDF/Excel).
- **Notifications**: Send check-in confirmation via SMS/WhatsApp.
- **Offline mode**: Cache scans locally when internet is down, sync later.
- **Admin panel**: Manage events, view stats, export data.
