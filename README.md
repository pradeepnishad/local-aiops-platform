# 🚀 Local AIOps Platform – ML-Based Anomaly Detection

A **local-first AIOps monitoring platform** that simulates infrastructure metrics, applies **machine learning–based anomaly detection**, and visualizes abnormal behavior using a web dashboard.
This project demonstrates how **AIOps concepts** can be implemented end-to-end using **FastAPI and unsupervised machine learning**, without relying on cloud services or paid tools.

--

## 🧠 Project Motivation

Traditional monitoring systems depend heavily on **static thresholds** (for example, CPU > 80%).  
Such rules are often brittle and generate false alerts when system behavior changes.

This project explores an alternative approach:
> **Let the system learn what “normal” looks like and flag deviations automatically using ML.**

---

## 🏗️ Architecture Overview

Synthetic Metric Generator
↓
SQLite Database (Local)
↓
ML Anomaly Detection Engine
↓
FastAPI Backend
↓
Web Dashboard

---

## ⚙️ Tech Stack

### Backend
- **FastAPI** – Web framework
- **SQLAlchemy** – ORM
- **SQLite** – Lightweight local database
- **Jinja2** – Server-side HTML templates

### Machine Learning
- **scikit-learn**
- **Isolation Forest** (unsupervised anomaly detection)
- **StandardScaler**

### Frontend
- HTML, CSS
- **Chart.js** for time-series visualization
- Dark-themed monitoring dashboard

### Deployment
- **Render (Free Tier)**

---

## 📊 Metrics Collected

Each metric record contains:

- CPU usage (%)
- Memory usage (%)
- Disk usage (%)
- Network activity
- Error rate
- Timestamp

Metrics are generated periodically while the application is running.

---

## 🔄 Data Generation

- Data is **synthetically generated** to simulate infrastructure behavior
- The generator produces:
  - Mostly normal operating values
  - Occasional abnormal spikes
- No anomaly labels are assigned during generation  
  (anomalies are detected purely by ML)

---

## 🤖 Machine Learning Approach

### Model Used
- **Isolation Forest**
- Unsupervised learning (no labeled anomaly data required)

### Why Isolation Forest?
- Designed specifically for anomaly detection
- Works well when anomalies are rare
- Does not require predefined thresholds
- Suitable for infrastructure metrics


- **Anomaly Flag**
  - `1` → Anomaly detected
  - `0` → Normal behavior

The model learns normal patterns from historical data and flags deviations as anomalies.

---

## 🖥️ Dashboard Features

- 📦 Total number of records
- 🚨 Total anomalies detected
- 📈 Time-series charts:
  - CPU usage
  - Memory usage
  - Disk usage
- 📋 Tabular view of recent metrics
- 🔍 Ability to view only anomaly records
- 🔐 Login-protected access

---

## 🔐 Authentication

- Simple login system
- Session-based authentication
- Dashboard accessible only after successful login
- Credentials are not exposed in the UI by default

Username : admin
Password : admin123

---

## ▶️ Application Workflow

1. User logs in
2. System generates metrics periodically
3. Data is stored locally in SQLite
4. ML model runs anomaly detection
5. Dashboard displays metrics and detected anomalies

---

## ▶️ Run Locally

Clone the repository and start the application locally:

```bash
git clone https://github.com/<your-username>/local-aiops-platform
cd local-aiops-platform
pip install -r requirements.txt
uvicorn app.main:app --reload

Open in browser
http://127.0.0.1:8000


⚠️ Limitations
Uses synthetic data (not real production logs)
Anomaly detection depends on data distribution
Not designed for large-scale production workloads
No alerting or notification system (yet)
These limitations are intentional to keep the project simple, explainable, and local-first.

🧑‍💻 Author
Pradeep
Aspiring DevOps & AIOps Engineer
Focused on machine learning–driven infrastructure monitoring


