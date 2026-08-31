# EventFlow Pro — MANTHAN | The Freshers' Showdown (PRARAMBH 2K26)

AI-powered event management platform featuring automated student registration, QR code generation, SMTP/Gmail email delivery, Google Sheets live backup, mobile volunteer check-in scanner, and real-time admin dashboard.

Hosted by **Saturangle – The Debate Club**, **GLA University**, Mathura for **PRARAMBH 2K26**.

---

## 🚀 Key Features

- **Student Registration**: Fast, validated fresher registration (`POST /register`) collecting Full Name, Roll Number, Course, Email, and WhatsApp Phone.
- **Registration ID Generation**: Automated, collision-free ID assignment (`EVT20260001`).
- **QR Code Generation**: Auto-generated PNG QR assets stored locally.
- **Email Delivery**: Automated confirmation email with QR attachment.
- **Google Sheets Backup**: Automatic secondary backup of registrations and check-ins.
- **Volunteer QR Scanner**: Mobile-friendly camera scanner (`/scan`) for instant check-in.
- **Admin Dashboard**: Live metrics, participant list, search, filter, manual attendance status, CSV export.
- **JWT Authentication**: Role-based access for Admin and Volunteer profiles.
- **Analytics & Observability**: Google Analytics 4 and Microsoft Clarity integrated.

---

## 🏆 Event Overview

- **Parent Event**: PRARAMBH 2K26
- **Organizer**: GLA UNIVERSITY
- **Club**: SATURANGLE – THE DEBATE CLUB
- **Competition**: MANTHAN | THE FRESHERS' SHOWDOWN
- **Description**: A debate and public-speaking competition for freshers.
- **Event Date**: 3rd September 2026 (01:00 PM – 03:00 PM)
- **Tagline**: "Speak. Stand out. Conquer."
- **Secondary Tagline**: "Where Ideas Meet Arguments."
- **Rounds**:
  - **Round 01**: SPEECH ROUND (All participants)
  - **Round 02**: DEBATE ROUND (Shortlisted participants)
- **Coordinators**:
  - Mradul Gaur (7417255432)
  - Nakshtra Chaudhary (9258626362)
- **Location**: GLA University, Mathura

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12/3.14, FastAPI, SQLAlchemy, PostgreSQL / SQLite |
| **Auth** | JWT (PyJWT), bcrypt / passlib |
| **Email** | SMTP / Gmail API |
| **QR Code** | `qrcode` + Pillow |
| **Backup** | Google Sheets API v4 (`google-auth`, Service Account) |
| **Frontend** | React 19, TanStack Start / Vite, TailwindCSS (Light Theme, Ivory/Navy/Gold) |
| **Scanner** | `html5-qrcode` |
| **Analytics** | Google Analytics 4 (`react-ga4`), Microsoft Clarity (`@microsoft/clarity`) |
| **Deployment** | Render (Web Services + PostgreSQL Database) |

---

## 📁 Repository Structure

```
EventFlow_AI/
├── backend/                  # FastAPI Backend Service
│   ├── app/
│   │   ├── api/              # API Route Handlers (auth, dashboard, registration, scan)
│   │   ├── background/       # Background Watcher & Queue Worker
│   │   ├── database/         # SQLAlchemy DB session & table init
│   │   ├── models/           # Participant & User ORM models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── services/         # Auth, Email, QR, ID, Google Sheets
│   │   ├── config.py         # Central configuration from .env
│   │   └── main.py           # FastAPI entry point
│   ├── generated/            # Local QR assets and processing state
│   └── requirements.txt      # Backend Python dependencies
│
├── youth-parliament-portal/  # React / TanStack Start Frontend App
│   ├── src/
│   │   ├── assets/           # Logos & visual assets
│   │   ├── components/       # UI & Site components (Navbar, Footer, QRScanner, AuthCard)
│   │   ├── lib/              # API client & error reporting helpers
│   │   └── routes/           # Pages (Home, Register, Success, Scanner, Admin, Login)
│   ├── public/               # Favicon & static assets
│   └── package.json          # Frontend Node dependencies
│
├── render.yaml               # Render Blueprint Deployment Configuration
└── README.md
```

---

## ⚡ Quick Start (Local Development)

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env`:
```env
APP_NAME=EventFlow Pro
DEBUG=True
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./eventflow.db
SECRET_KEY=dev-secret-key
```

Start backend:
```bash
python -m uvicorn app.main:app --reload
```

---

### 2. Frontend Setup

```bash
cd youth-parliament-portal
npm install
npm run dev
```

Open: `http://localhost:3000` or `http://localhost:8080`

---

## 🔑 Default Accounts

Created automatically on backend startup:

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@eventflow.com` | `admin123` |
| **Volunteer 1** | `volunteer1@eventflow.com` | `vol123` |
| **Volunteer 2** | `volunteer2@eventflow.com` | `vol123` |
| **Volunteer 3** | `volunteer3@eventflow.com` | `vol123` |
