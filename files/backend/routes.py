from flask import Blueprint, request, jsonify, session
from database import get_db
from knowledge import predict_disease, recommend_hospitals, ALL_SYMPTOMS
from werkzeug.security import check_password_hash
import random, string

api_blueprint = Blueprint('api', __name__)

def require_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@api_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    role = data.get('role', '')
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username=? AND role=?', (username, role)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['full_name'] = user['full_name']
        return jsonify({'success': True, 'user': {'username': user['username'], 'role': user['role'], 'full_name': user['full_name']}})
    return jsonify({'success': False, 'message': 'Invalid credentials or role mismatch'}), 401

@api_blueprint.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@api_blueprint.route('/api/me', methods=['GET'])
def me():
    if 'username' not in session:
        return jsonify({'authenticated': False}), 401
    return jsonify({'authenticated': True, 'user': {'username': session['username'], 'role': session['role'], 'full_name': session['full_name']}})

@api_blueprint.route('/api/patients', methods=['GET'])
@require_auth
def get_patients():
    search = request.args.get('search', '')
    conn = get_db()
    if search:
        patients = conn.execute("SELECT * FROM patients WHERE name LIKE ? OR patient_id LIKE ? ORDER BY created_at DESC", (f'%{search}%', f'%{search}%')).fetchall()
    else:
        patients = conn.execute('SELECT * FROM patients ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(p) for p in patients])

@api_blueprint.route('/api/patients', methods=['POST'])
@require_auth
def add_patient():
    if session.get('role') == 'user':
        return jsonify({'success': False, 'message': 'Unauthorized to add patients'}), 403
    data = request.get_json()
    pid = 'P' + ''.join(random.choices(string.digits, k=6))
    conn = get_db()
    try:
        conn.execute('''INSERT INTO patients (patient_id, name, age, gender, phone, address, blood_group, created_by) VALUES (?,?,?,?,?,?,?,?)''',
                     (pid, data['name'], data.get('age'), data.get('gender'), data.get('phone'), data.get('address'), data.get('blood_group'), session['username']))
        conn.commit()
        patient = conn.execute('SELECT * FROM patients WHERE patient_id=?', (pid,)).fetchone()
        conn.close()
        return jsonify({'success': True, 'patient': dict(patient)})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 400

@api_blueprint.route('/api/patients/<pid>', methods=['GET'])
@require_auth
def get_patient(pid):
    conn = get_db()
    patient = conn.execute('SELECT * FROM patients WHERE patient_id=?', (pid,)).fetchone()
    conn.close()
    if not patient: return jsonify({'error': 'Patient not found'}), 404
    return jsonify(dict(patient))

@api_blueprint.route('/api/patients/<pid>', methods=['PUT'])
@require_auth
def update_patient(pid):
    data = request.get_json()
    conn = get_db()
    conn.execute('''UPDATE patients SET name=?, age=?, gender=?, phone=?, address=?, blood_group=? WHERE patient_id=?''',
                 (data['name'], data.get('age'), data.get('gender'), data.get('phone'), data.get('address'), data.get('blood_group'), pid))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@api_blueprint.route('/api/predict', methods=['POST'])
@require_auth
def predict():
    if session.get('role') == 'user':
        return jsonify({'success': False, 'message': 'Unauthorized to predict symptoms'}), 403

    data = request.get_json()
    symptoms = data.get('symptoms', [])
    patient_id = data.get('patient_id', '')
    notes = data.get('notes', '')

    prediction = predict_disease(symptoms)
    hospitals = recommend_hospitals(prediction['specialty'])

    if patient_id:
        conn = get_db()
        conn.execute('''INSERT INTO patient_history (patient_id, symptoms, predicted_disease, doctor_recommended, hospital_suggested, notes, recorded_by) VALUES (?,?,?,?,?,?,?)''',
                     (patient_id, ','.join(symptoms), prediction['disease'], prediction['doctor'], hospitals[0]['name'] if hospitals else 'N/A', notes, session['username']))
        conn.commit()
        conn.close()

    return jsonify({'prediction': prediction, 'hospitals': hospitals, 'symptoms': symptoms})

@api_blueprint.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    return jsonify(ALL_SYMPTOMS)

@api_blueprint.route('/api/history', methods=['GET'])
@require_auth
def get_all_history():
    patient_id = request.args.get('patient_id', '')
    disease_filter = request.args.get('disease', '')
    conn = get_db()
    query = '''SELECT ph.*, p.name as patient_name FROM patient_history ph LEFT JOIN patients p ON ph.patient_id = p.patient_id WHERE 1=1'''
    params = []
    if patient_id: query += ' AND ph.patient_id=?'; params.append(patient_id)
    if disease_filter: query += ' AND ph.predicted_disease LIKE ?'; params.append(f'%{disease_filter}%')
    query += ' ORDER BY ph.visit_date DESC'
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@api_blueprint.route('/api/knowledge-graph', methods=['GET'])
@require_auth
def knowledge_graph():
    patient_id = request.args.get('patient_id', '')
    conn = get_db()
    nodes, links, node_ids = [], [], set()

    def add_node(nid, label, group, size=20):
        if nid not in node_ids:
            nodes.append({'id': nid, 'label': label, 'group': group, 'size': size})
            node_ids.add(nid)

    def add_link(source, target, label=''):
        links.append({'source': source, 'target': target, 'label': label})

    query = 'SELECT ph.*, p.name FROM patient_history ph LEFT JOIN patients p ON ph.patient_id=p.patient_id'
    params = []
    if patient_id: query += ' WHERE ph.patient_id=?'; params.append(patient_id)
    query += ' LIMIT 30'
    rows = conn.execute(query, params).fetchall()
    conn.close()

    for row in rows:
        pid, pname = row['patient_id'], row['name'] or row['patient_id']
        add_node(f'patient_{pid}', pname, 'patient', 30)
        symptoms = [s.strip() for s in row['symptoms'].split(',') if s.strip()]
        for sym in symptoms:
            sid = f'symptom_{sym}'
            add_node(sid, sym, 'symptom', 15)
            add_link(f'patient_{pid}', sid, 'has')
        disease = row['predicted_disease']
        if disease:
            did = f'disease_{disease}'
            add_node(did, disease, 'disease', 25)
            for sym in symptoms: add_link(f'symptom_{sym}', did, 'indicates')
        doctor = row['doctor_recommended']
        if doctor:
            drid = f'doctor_{doctor}'
            add_node(drid, doctor, 'doctor', 20)
            if disease: add_link(f'disease_{disease}', drid, 'treated by')
        hospital = row['hospital_suggested']
        if hospital:
            hid = f'hospital_{hospital}'
            add_node(hid, hospital, 'hospital', 22)
            if doctor: add_link(f'doctor_{doctor}', hid, 'works at')

    return jsonify({'nodes': nodes, 'links': links})

@api_blueprint.route('/api/stats', methods=['GET'])
@require_auth
def get_stats():
    conn = get_db()
    total_patients = conn.execute('SELECT COUNT(*) as c FROM patients').fetchone()['c']
    total_visits = conn.execute('SELECT COUNT(*) as c FROM patient_history').fetchone()['c']
    top_diseases = conn.execute('''SELECT predicted_disease, COUNT(*) as cnt FROM patient_history GROUP BY predicted_disease ORDER BY cnt DESC LIMIT 5''').fetchall()
    top_symptoms_raw = conn.execute('SELECT symptoms FROM patient_history').fetchall()
    conn.close()

    symptom_count = {}
    for row in top_symptoms_raw:
        for s in row['symptoms'].split(','):
            s = s.strip()
            if s: symptom_count[s] = symptom_count.get(s, 0) + 1
    top_symptoms = sorted(symptom_count.items(), key=lambda x: -x[1])[:5]

    return jsonify({'total_patients': total_patients, 'total_visits': total_visits, 'top_diseases': [dict(d) for d in top_diseases], 'top_symptoms': [{'symptom': s, 'count': c} for s, c in top_symptoms]})
