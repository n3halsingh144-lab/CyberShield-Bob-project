# 🛡️ CyberShield SOC

A fully-featured **Security Operations Center (SOC) dashboard** built with Python and Streamlit.  
All data is fake/demo — no real network connections or databases required.

---

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [Pages & Features](#pages--features)
- [Screenshots](#screenshots)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌑 Dark Theme | GitHub-style dark UI (`#0d1117` background) with custom CSS |
| 🕐 Live Clock | Real-time clock in the top bar, updates on every refresh |
| 📊 Summary Cards | Total alerts, Critical alerts, Open incidents, Resolved incidents |
| 🚨 Live Alert Feed | New alerts auto-generated every 5 seconds (1–3 per cycle) |
| 🏷️ Severity Badges | Color-coded pills — Low 🟢 / Medium 🟡 / High 🟠 / Critical 🔴 |
| 📈 Live Charts | Alerts over time, by type, and severity distribution — update with filters |
| 🔍 Sidebar Filters | Filter by Severity, Type, Status; free-text search by IP or Alert ID |
| ⚡ Alert Actions | Acknowledge, Escalate, Mark False Positive, Create Incident |
| 📋 Incidents Page | Ticket management with priority, assignee, notes and status workflow |
| 🔗 Chain of Custody | Immutable audit log for every action taken on an incident |
| 🗂️ Evidence Log | Add and view evidence artifacts per incident |
| ⬇️ Download Report | One-click `.txt` incident report export |

---

## ⚙️ Requirements

- Python **3.10** or later
- `streamlit`
- `pandas`

> All other imports (`random`, `time`, `datetime`, `uuid`) are part of the Python standard library.

---

## 🚀 Installation

### 1. Install Python

Download and install Python from [https://python.org/downloads](https://python.org/downloads).  
During installation, make sure to check **"Add Python to PATH"**.

### 2. Install dependencies

Open a terminal and run:

```bash
pip install streamlit pandas
```

---

## ▶️ Running the App

### Step 1 — Open a terminal in the project folder

Navigate to the project directory:

```powershell
cd "C:\Users\yaksh\OneDrive\Desktop\CYBER SECURITY"
```

Or right-click the folder in File Explorer and choose **"Open in Terminal"**.

### Step 2 — Launch Streamlit

```bash
streamlit run app.py
```

Streamlit will print a local URL and open it in your browser automatically:

```
  Local URL:  http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## 📁 Project Structure

```
CYBER SECURITY/
│
├── app.py          ← Main application (single file, fully self-contained)
└── README.md       ← This file
```

---

## 🖥️ Pages & Features

### Dashboard Page

- **Top Bar** — App title + live clock
- **Summary Cards** — 4 KPI cards with color-coded counts
- **Charts** (3 columns):
  - Line chart — alerts per hour over the last 12 hours
  - Bar chart — alert count by type (Phishing, Brute Force, Malware, SQL Injection, DDoS)
  - Bar chart — severity distribution with color legend
- **Live Alerts Table** — scrollable table of all alerts, newest first
- **Alert Actions** — select an alert from a dropdown then click:
  - ✅ **Acknowledge** — marks alert as Acknowledged
  - 🔺 **Escalate** — marks alert as Escalated
  - ❌ **Mark False Positive** — marks alert as False Positive
  - 📋 **Create Incident** — auto-creates an incident ticket from the alert

### Incidents Page

- **Incident Table** — overview of all tickets with priority emoji indicators
- **Incident Detail Panel**:
  - Priority, Created date, Assignee (editable dropdown)
  - **Status Workflow** — click through: `Open → Investigating → Contained → Resolved`
  - **Notes** — editable text area with Save button
  - **Evidence Log** — list of artifacts; add new entries inline
  - **Chain of Custody** — timestamped audit trail of every action
- **Download Report** — exports a formatted `.txt` report for the selected incident

---

## 🔧 Sidebar Filters (Dashboard)

| Filter | Options |
|---|---|
| Severity | Low, Medium, High, Critical |
| Type | Phishing, Brute Force, Malware, SQL Injection, DDoS |
| Status | New, Acknowledged, Escalated, False Positive, Closed |
| Search | Free-text match on Source IP or Alert ID |

---

## 📝 Notes

- All data is **randomly generated in memory** — nothing is saved to disk or sent over a network.
- The alert feed holds a maximum of **200 alerts** at a time (oldest are dropped).
- The app **auto-reruns every 5 seconds** to simulate a live feed.
- To stop the app, press `Ctrl + C` in the terminal.

---

## 📄 License

This project is for educational and demonstration purposes only.  
No real threat intelligence or security data is used.
