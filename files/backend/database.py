import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

DATABASE_URL = "postgresql://neondb_owner:npg_7xAWzVsCet9X@ep-hidden-glade-ammrnhux-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

class DatabaseWrapper:
    def __init__(self, conn):
        self.conn = conn

    def execute(self, query, params=None):
        cur = self.conn.cursor()
        # Convert SQLite '?' to PostgreSQL '%s'
        query = query.replace('?', '%s')
        cur.execute(query, params or ())
        return cur

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return DatabaseWrapper(conn)

def init_db():
    db = get_db()
    c = db.conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        id SERIAL PRIMARY KEY,
        patient_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        address TEXT,
        blood_group TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS patient_history (
        id SERIAL PRIMARY KEY,
        patient_id TEXT NOT NULL,
        symptoms TEXT NOT NULL,
        predicted_disease TEXT,
        doctor_recommended TEXT,
        hospital_suggested TEXT,
        notes TEXT,
        visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        recorded_by TEXT
    )''')

    users = [
        ('admin', generate_password_hash('admin123'), 'admin', 'System Administrator'),
        ('dr_smith', generate_password_hash('doctor123'), 'doctor', 'Dr. John Smith'),
        ('dr_patel', generate_password_hash('doctor123'), 'doctor', 'Dr. Priya Patel'),
        ('receptionist', generate_password_hash('user123'), 'user', 'Sarah Johnson'),
        ('staff1', generate_password_hash('user123'), 'user', 'Mike Wilson'),
    ]
    for u in users:
        try:
            c.execute('INSERT INTO users (username, password, role, full_name) VALUES (%s,%s,%s,%s)', u)
        except:
            pass

    sample_patients = [
        ('P001', 'Alice Thompson', 34, 'Female', '555-0101', '123 Oak St, Springfield', 'A+'),
        ('P002', 'Bob Martinez', 45, 'Male', '555-0102', '456 Elm Ave, Springfield', 'B-'),
        ('P003', 'Carol White', 28, 'Female', '555-0103', '789 Pine Rd, Springfield', 'O+'),
        ('P004', 'David Lee', 62, 'Male', '555-0104', '321 Maple Dr, Springfield', 'AB+'),
        ('P005', 'Emma Davis', 19, 'Female', '555-0105', '654 Cedar Ln, Springfield', 'A-'),
    ]
    for p in sample_patients:
        try:
            c.execute('INSERT INTO patients (patient_id, name, age, gender, phone, address, blood_group, created_by) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                      (*p, 'admin'))
        except:
            pass

    sample_history = [
        ('P001', 'fever,cough,fatigue', 'Influenza (Flu)', 'General Physician', 'Springfield General Hospital', '2024-01-15', 'dr_smith'),
        ('P002', 'chest pain,shortness of breath,dizziness', 'Cardiovascular Disease', 'Cardiologist', 'Heart Care Medical Center', '2024-02-20', 'dr_patel'),
        ('P003', 'headache,nausea,sensitivity to light', 'Migraine', 'Neurologist', 'NeuroHealth Clinic', '2024-03-10', 'dr_smith'),
        ('P004', 'joint pain,swelling,stiffness', 'Arthritis', 'Rheumatologist', 'Bone & Joint Specialists', '2024-03-22', 'dr_patel'),
        ('P001', 'sore throat,runny nose,sneezing', 'Common Cold', 'General Physician', 'Springfield General Hospital', '2024-04-05', 'dr_smith'),
    ]
    for h in sample_history:
        try:
            c.execute('''INSERT INTO patient_history 
                (patient_id, symptoms, predicted_disease, doctor_recommended, hospital_suggested, visit_date, recorded_by)
                VALUES (%s,%s,%s,%s,%s,%s,%s)''', h)
        except:
            pass

    db.commit()
    db.close()
