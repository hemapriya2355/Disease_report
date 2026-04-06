# 🧬 MedGraph — Healthcare Knowledge Graph Application

## ▶️ Run in 2 steps

```bash
pip install flask werkzeug
python3 app.py
```

Then open → **http://localhost:5000**

---

## 🔐 Login Credentials

| Username       | Password    | Role   |
|----------------|-------------|--------|
| `admin`        | `admin123`  | Admin  |
| `dr_smith`     | `doctor123` | Doctor |
| `dr_patel`     | `doctor123` | Doctor |
| `receptionist` | `user123`   | User   |
| `staff1`       | `user123`   | User   |

---

## 📁 Files (all in this folder)

```
medgraph/
├── app.py          ← Flask backend + all API endpoints
├── index.html      ← Full frontend (HTML + CSS + JS + D3.js)
├── healthcare.db   ← SQLite database (auto-created/seeded)
└── README.md       ← This file
```

---

## 🌐 API Endpoints

| Endpoint                  | Method | Description                     |
|---------------------------|--------|---------------------------------|
| `/api/login`              | POST   | Authenticate user               |
| `/api/logout`             | POST   | End session                     |
| `/api/me`                 | GET    | Current session user            |
| `/api/patients`           | GET    | List / search patients          |
| `/api/patients`           | POST   | Register new patient            |
| `/api/patients/<id>`      | GET    | Get single patient              |
| `/api/patients/<id>`      | PUT    | Update patient                  |
| `/api/predict`            | POST   | AI disease prediction           |
| `/api/symptoms`           | GET    | All known symptoms              |
| `/api/history`            | GET    | Visit history (filterable)      |
| `/api/knowledge-graph`    | GET    | Graph nodes & links             |
| `/api/stats`              | GET    | Dashboard statistics            |

---

## 🧠 Disease Knowledge Base (15+ mappings)

| Symptoms                              | Disease                 | Doctor               |
|---------------------------------------|-------------------------|----------------------|
| fever + cough + fatigue               | Influenza               | General Physician    |
| chest pain + shortness of breath      | Cardiovascular Disease  | Cardiologist         |
| headache + nausea + light sensitivity | Migraine                | Neurologist          |
| joint pain + swelling + stiffness     | Arthritis               | Rheumatologist       |
| excessive thirst + blurred vision     | Diabetes Mellitus       | Endocrinologist      |
| wheezing + chest tightness            | Asthma                  | Pulmonologist        |
| sadness + fatigue + loss of interest  | Depression              | Psychiatrist         |
| …and 8 more                           |                         |                      |
