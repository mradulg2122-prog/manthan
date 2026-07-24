# EventFlow Pro — Youth Parliament 6.0

AI-powered event management platform with automatic registration processing, QR-based attendance, and a real-time admin dashboard.

## Features

- ✅ Student Registration (POST /register)
- ✅ Automatic QR Code Generation
- ✅ Automatic Email with QR Attachment
- ✅ Background Watcher (auto-processes new registrations)
- ✅ Volunteer QR Scanner (mobile-friendly)
- ✅ Live Attendance Tracking
- ✅ Admin Dashboard with Search, Sort, Pagination
- ✅ Manual Attendance Toggle
- ✅ Excel Export
- ✅ JWT Authentication (Admin + Volunteer roles)
- ✅ Health Monitoring
- ✅ System Status Dashboard

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | FastAPI, SQLAlchemy, PostgreSQL    |
| Auth     | JWT (PyJWT), bcrypt                |
| Email    | SMTP (Gmail App Password)          |
| QR       | qrcode + Pillow                    |
| Frontend | Next.js 16, React, TailwindCSS     |
| Scanner  | html5-qrcode                       |
| Export   | openpyxl                           |

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (local or cloud like Neon)
- Gmail account with App Password (for email)

## Installation

### 1. Clone

```bash
git clone <your-repo-url>
cd EventFlow_AI
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
APP_NAME=EventFlow Pro
DEBUG=True
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=your-random-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

### 5. Run

**Terminal 1 — Backend:**

```bash
cd backend
uvicorn app.main:app --reload
```

**Terminal 2 — Frontend:**

```bash
cd frontend
npm run dev
```

## Default Admin

Created automatically on first startup:

| Field    | Value                |
|----------|----------------------|
| Email    | admin@eventflow.com  |
| Password | admin123             |
| Role     | ADMIN                |

> ⚠️ Change the default password in production.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET    | /        | —    | API status |
| GET    | /health  | —    | System health check |
| POST   | /register | —   | Register participant |
| POST   | /scan    | —    | Scan QR for attendance |
| POST   | /login   | —    | Authenticate user |
| POST   | /logout  | —    | Logout |
| GET    | /me      | JWT  | Current user info |
| GET    | /dashboard/stats | ADMIN | Registration stats |
| GET    | /dashboard/participants | ADMIN | Paginated list |
| GET    | /dashboard/participant/{id} | ADMIN | Detail view |
| PATCH  | /dashboard/participant/{id}/attendance | ADMIN | Toggle attendance |
| GET    | /dashboard/activity | ADMIN | Recent check-ins |
| GET    | /dashboard/export | ADMIN | Excel download |

## Frontend Routes

| Route   | Access    | Description |
|---------|-----------|-------------|
| /login  | Public    | Login page |
| /scan   | Auth      | QR Scanner (volunteer/admin) |
| /admin  | Admin     | Dashboard |

## Complete Workflow

```
Student registers via POST /register
        ↓
Watcher detects (every 5s)
        ↓
Registration ID generated (EVT20260001)
        ↓
QR Code generated (generated/qr/)
        ↓
Email sent with QR attachment
        ↓
Database updated (qr_sent, email_sent)
        ↓
Volunteer opens /scan on phone
        ↓
Scans QR → attendance marked
        ↓
Admin sees live updates on /admin
        ↓
Admin exports → Youth_Parliament_6.0_Attendance_<DATE>.xlsx
```

## Project Structure

```
EventFlow_AI/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI routers
│   │   ├── background/    # Watcher, queue, worker
│   │   ├── database/      # SQLAlchemy setup
│   │   ├── models/        # DB models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── config.py      # Settings
│   │   └── main.py        # Entry point
│   ├── generated/         # QR images + state
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── admin/         # Dashboard
│   │   ├── login/         # Login page
│   │   ├── scan/          # QR Scanner
│   │   ├── components/    # Reusable UI
│   │   └── services/      # API layer
│   └── package.json
└── README.md
```

## Deployment

### Backend (Railway / Render)

1. Set environment variables
2. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Set `DEBUG=False` in production

### Frontend (Vercel)

1. Set `NEXT_PUBLIC_API_URL` to your backend URL
2. Deploy from the `frontend/` directory

### Security Checklist

- [ ] Change default admin password
- [ ] Set a strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Use HTTPS
- [ ] Restrict CORS origins

## License

MIT
