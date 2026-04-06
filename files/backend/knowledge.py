import difflib

SYMPTOM_DISEASE_MAP = {
    # MENTAL HEALTH SYMPTOMS
    frozenset(['anxiety', 'restlessness', 'rapid heartbeat']): {
        'disease': 'Anxiety Disorder', 'treatment': 'Meditation, breathing exercises, therapy', 'doctor': 'Psychologist / Psychiatrist', 'specialty': 'Psychiatry', 'severity': 'Moderate'
    },
    frozenset(['persistent sadness', 'loss of interest']): {
        'disease': 'Depression', 'treatment': 'Counseling, antidepressants (if prescribed), lifestyle changes', 'doctor': 'Psychiatrist', 'specialty': 'Psychiatry', 'severity': 'High'
    },
    frozenset(['hallucinations', 'delusions']): {
        'disease': 'Schizophrenia', 'treatment': 'Antipsychotic medications, therapy', 'doctor': 'Psychiatrist', 'specialty': 'Psychiatry', 'severity': 'Critical'
    },
    frozenset(['sleep disturbance', 'fatigue', 'stress']): {
        'disease': 'Insomnia', 'treatment': 'Sleep hygiene, relaxation, reduce screen time', 'doctor': 'General physician / Psychologist', 'specialty': 'General Medicine', 'severity': 'Low'
    },
    frozenset(['extreme mood swings']): {
        'disease': 'Bipolar Disorder', 'treatment': 'Mood stabilizers, therapy', 'doctor': 'Psychiatrist', 'specialty': 'Psychiatry', 'severity': 'High'
    },
    
    # PHYSICAL SYMPTOMS
    # Fever & Infection
    frozenset(['fever', 'body pain', 'fatigue']): {
        'disease': 'Influenza', 'treatment': 'Rest, fluids, Paracetamol', 'doctor': 'General physician', 'specialty': 'General Medicine', 'severity': 'Moderate'
    },
    frozenset(['high fever', 'rash', 'joint pain']): {
        'disease': 'Dengue Fever', 'treatment': 'Hydration, platelet monitoring', 'doctor': 'Physician', 'specialty': 'General Medicine', 'severity': 'High'
    },
    frozenset(['fever', 'cough', 'breathing issue']): {
        'disease': 'COVID-19', 'treatment': 'Isolation, oxygen (if needed), antivirals', 'doctor': 'Physician', 'specialty': 'General Medicine', 'severity': 'High'
    },
    
    # Respiratory
    frozenset(['wheezing', 'breathlessness']): {
        'disease': 'Asthma', 'treatment': 'Inhalers, avoid triggers', 'doctor': 'Pulmonologist', 'specialty': 'Pulmonology', 'severity': 'Moderate'
    },
    frozenset(['persistent cough', 'weight loss']): {
        'disease': 'Tuberculosis', 'treatment': 'Long-term antibiotics', 'doctor': 'Pulmonologist', 'specialty': 'Pulmonology', 'severity': 'High'
    },
    
    # Cardiac
    frozenset(['chest pain', 'sweating', 'nausea']): {
        'disease': 'Heart Attack', 'treatment': 'Immediate hospitalization', 'doctor': 'Cardiologist', 'specialty': 'Cardiology', 'severity': 'Critical'
    },
    frozenset(['irregular heartbeat']): {
        'disease': 'Arrhythmia', 'treatment': 'Medication, lifestyle changes', 'doctor': 'Cardiologist', 'specialty': 'Cardiology', 'severity': 'Moderate'
    },
    
    # Digestive
    frozenset(['stomach pain', 'diarrhea']): {
        'disease': 'Gastroenteritis', 'treatment': 'ORS, hydration', 'doctor': 'General physician', 'specialty': 'Gastroenterology', 'severity': 'Moderate'
    },
    frozenset(['burning chest', 'acid taste']): {
        'disease': 'Acid Reflux', 'treatment': 'Antacids, avoid spicy food', 'doctor': 'Gastroenterologist', 'specialty': 'Gastroenterology', 'severity': 'Low'
    },
    frozenset(['constipation', 'bloating']): {
        'disease': 'Irritable Bowel Syndrome', 'treatment': 'Fiber diet, stress control', 'doctor': 'Gastroenterologist', 'specialty': 'Gastroenterology', 'severity': 'Moderate'
    },
    
    # Skin
    frozenset(['itching', 'rash']): {
        'disease': 'Allergic Reaction', 'treatment': 'Antihistamines', 'doctor': 'Dermatologist', 'specialty': 'Dermatology', 'severity': 'Low'
    },
    frozenset(['dry skin', 'inflamed skin']): {
        'disease': 'Eczema', 'treatment': 'Moisturizers, creams', 'doctor': 'Dermatologist', 'specialty': 'Dermatology', 'severity': 'Moderate'
    },
    
    # Musculoskeletal
    frozenset(['joint pain', 'stiffness']): {
        'disease': 'Arthritis', 'treatment': 'Pain relievers, physiotherapy', 'doctor': 'Orthopedic', 'specialty': 'Orthopedics', 'severity': 'Moderate'
    },
    frozenset(['muscle pain', 'weakness']): {
        'disease': 'Myositis', 'treatment': 'Rest, medication', 'doctor': 'Physician', 'specialty': 'General Medicine', 'severity': 'Moderate'
    },
    
    # Neurological
    frozenset(['severe headache', 'nausea']): {
        'disease': 'Migraine', 'treatment': 'Pain relief, avoid triggers', 'doctor': 'Neurologist', 'specialty': 'Neurology', 'severity': 'Moderate'
    },
    frozenset(['memory loss', 'confusion']): {
        'disease': "Alzheimer's Disease", 'treatment': 'Cognitive therapy', 'doctor': 'Neurologist', 'specialty': 'Neurology', 'severity': 'High'
    },
    
    # EMERGENCY SYMPTOMS
    frozenset(['sudden paralysis', 'speech difficulty']): {
        'disease': 'Stroke', 'treatment': 'Immediate emergency care', 'doctor': 'Neurologist', 'specialty': 'Neurology', 'severity': 'Critical'
    },
    frozenset(['severe breathing difficulty']): {
        'disease': 'Respiratory Failure', 'treatment': 'Oxygen support', 'doctor': 'Emergency physician', 'specialty': 'Emergency', 'severity': 'Critical'
    },
    frozenset(['heavy bleeding']): {
        'disease': 'Hemorrhage', 'treatment': 'Immediate care', 'doctor': 'Emergency specialist', 'specialty': 'Emergency', 'severity': 'Critical'
    },
    
    # GENERAL COMMON SYMPTOMS
    frozenset(['fatigue', 'weakness']): {
        'disease': 'Anemia', 'treatment': 'Iron supplements', 'doctor': 'Physician', 'specialty': 'General Medicine', 'severity': 'Moderate'
    },
    frozenset(['frequent urination', 'thirst']): {
        'disease': 'Diabetes Mellitus', 'treatment': 'Diet control, insulin', 'doctor': 'Endocrinologist', 'specialty': 'Endocrinology', 'severity': 'High'
    },
    frozenset(['weight gain', 'tiredness']): {
        'disease': 'Hypothyroidism', 'treatment': 'Thyroid medication', 'doctor': 'Endocrinologist', 'specialty': 'Endocrinology', 'severity': 'Moderate'
    },
    frozenset(['weight loss', 'sweating']): {
        'disease': 'Hyperthyroidism', 'treatment': 'Medication', 'doctor': 'Endocrinologist', 'specialty': 'Endocrinology', 'severity': 'Moderate'
    }
,
    # EYE SYMPTOMS
    frozenset(['redness', 'itching', 'watering']): {
        'disease': 'Conjunctivitis', 'treatment': 'Eye drops, maintain hygiene, avoid touching eyes', 'doctor': 'Ophthalmologist', 'specialty': 'Ophthalmology', 'severity': 'Low'
    },
    frozenset(['blurred vision']): {
        'disease': 'Refractive Error', 'treatment': 'Glasses / contact lenses', 'doctor': 'Ophthalmologist', 'specialty': 'Ophthalmology', 'severity': 'Low'
    },
    frozenset(['eye pain', 'sensitivity to light']): {
        'disease': 'Uveitis', 'treatment': 'Anti-inflammatory eye drops', 'doctor': 'Ophthalmologist', 'specialty': 'Ophthalmology', 'severity': 'Moderate'
    },
    frozenset(['dryness', 'burning sensation']): {
        'disease': 'Dry Eye Syndrome', 'treatment': 'Artificial tears, reduce screen time', 'doctor': 'Ophthalmologist', 'specialty': 'Ophthalmology', 'severity': 'Low'
    },
    frozenset(['sudden vision loss']): {
        'disease': 'Retinal Detachment', 'treatment': 'Immediate surgery', 'doctor': 'Eye specialist (Emergency)', 'specialty': 'Ophthalmology', 'severity': 'Critical'
    },
    
    # MOUTH SYMPTOMS
    frozenset(['tooth pain', 'sensitivity']): {
        'disease': 'Dental Caries', 'treatment': 'Filling, root canal if severe', 'doctor': 'Dentist', 'specialty': 'Dentistry', 'severity': 'Low'
    },
    frozenset(['gum swelling', 'bleeding']): {
        'disease': 'Gingivitis', 'treatment': 'Oral hygiene, scaling', 'doctor': 'Dentist', 'specialty': 'Dentistry', 'severity': 'Low'
    },
    frozenset(['mouth ulcers', 'pain']): {
        'disease': 'Aphthous Ulcer', 'treatment': 'Topical gels, avoid spicy food', 'doctor': 'Dentist / General physician', 'specialty': 'Dentistry', 'severity': 'Low'
    },
    frozenset(['white patches in mouth']): {
        'disease': 'Oral Thrush', 'treatment': 'Antifungal medication', 'doctor': 'Dentist', 'specialty': 'Dentistry', 'severity': 'Moderate'
    },
    frozenset(['bad breath']): {
        'disease': 'Halitosis', 'treatment': 'Brushing, mouthwash, hydration', 'doctor': 'Dentist', 'specialty': 'Dentistry', 'severity': 'Low'
    },
    
    # BODY PAIN SYMPTOMS
    frozenset(['muscle pain after activity']): {
        'disease': 'Muscle Strain', 'treatment': 'Rest, ice pack, pain relief', 'doctor': 'Orthopedic', 'specialty': 'Orthopedics', 'severity': 'Low'
    },
    frozenset(['chronic widespread pain']): {
        'disease': 'Fibromyalgia', 'treatment': 'Exercise, stress management, medication', 'doctor': 'Rheumatologist', 'specialty': 'Rheumatology', 'severity': 'Moderate'
    },
    frozenset(['back pain']): {
        'disease': 'Sciatica', 'treatment': 'Physiotherapy, posture correction', 'doctor': 'Orthopedic', 'specialty': 'Orthopedics', 'severity': 'Moderate'
    }
}

HOSPITALS = [
    {'name': 'Springfield General Hospital', 'location': '100 Medical Blvd, Springfield', 'specializations': ['General Medicine', 'Emergency', 'Surgery'], 'contact': '555-1000', 'rating': 4.5},
    {'name': 'Heart Care Medical Center', 'location': '250 Cardiac Way, Springfield', 'specializations': ['Cardiology', 'Cardiovascular Surgery'], 'contact': '555-2000', 'rating': 4.8},
    {'name': 'NeuroHealth Clinic', 'location': '75 Brain Ave, Springfield', 'specializations': ['Neurology', 'Neurosurgery', 'Psychiatry'], 'contact': '555-3000', 'rating': 4.6},
    {'name': 'Bone & Joint Specialists', 'location': '320 Ortho Dr, Springfield', 'specializations': ['Orthopedics', 'Rheumatology', 'Sports Medicine'], 'contact': '555-4000', 'rating': 4.4},
    {'name': 'Lung & Respiratory Institute', 'location': '180 Breath St, Springfield', 'specializations': ['Pulmonology', 'Allergy', 'Sleep Medicine'], 'contact': '555-5000', 'rating': 4.7},
    {'name': 'GastroDigest Medical', 'location': '90 Gut Lane, Springfield', 'specializations': ['Gastroenterology', 'Hepatology'], 'contact': '555-6000', 'rating': 4.3},
    {'name': 'Endocrine & Diabetes Center', 'location': '415 Hormone Rd, Springfield', 'specializations': ['Endocrinology', 'Diabetes Care', 'Nutrition'], 'contact': '555-7000', 'rating': 4.5},
    {'name': 'DermaSkin Clinic', 'location': '55 Glow Ave, Springfield', 'specializations': ['Dermatology', 'Cosmetic Surgery'], 'contact': '555-8000', 'rating': 4.2},
    {'name': 'MindWell Psychiatric Hospital', 'location': '200 Calm Blvd, Springfield', 'specializations': ['Psychiatry', 'Psychology', 'Addiction Medicine'], 'contact': '555-9000', 'rating': 4.6},
    {'name': 'Infectious Disease Center', 'location': '340 Tropical Blvd, Springfield', 'specializations': ['Infectious Disease', 'Travel Medicine'], 'contact': '555-1100', 'rating': 4.4},
    {'name': 'Urology & Kidney Institute', 'location': '120 Renal Way, Springfield', 'specializations': ['Urology', 'Nephrology'], 'contact': '555-1200', 'rating': 4.5},
    {'name': 'City Emergency & Trauma Center', 'location': '1 Emergency Plaza, Springfield', 'specializations': ['Emergency', 'Trauma Surgery', 'Critical Care'], 'contact': '555-0911', 'rating': 4.9},
]

SYMPTOM_SYNONYMS = {
    'stomach pain': 'abdominal pain',
    'stomach ache': 'abdominal pain',
    'stomach cramps': 'abdominal pain',
    'stomachache': 'abdominal pain',
    'tummy pain': 'abdominal pain',
    'tummy ache': 'abdominal pain',
    'abdominal cramps': 'abdominal pain',
    'high fever': 'fever',
    'feverish': 'fever',
    'low fever': 'fever',
    'body aches': 'body ache',
    'muscle aches': 'muscle pain',
    'joint aches': 'joint pain',
    'painful urination': 'burning urination',
    'urinary frequency': 'frequent urination',
    'urinary urgency': 'frequent urination',
    'nauseous': 'nausea',
    'vomit': 'vomiting',
    'throwing up': 'vomiting',
    'head ache': 'headache',
    'dizzy': 'dizziness',
    'lightheaded': 'dizziness',
    'light-headed': 'dizziness',
    'breathlessness': 'shortness of breath',
    'chest pressure': 'chest pain',
    'chest discomfort': 'chest pain',
    'tightness in chest': 'chest tightness',
    'wheeze': 'wheezing',
    'nasal congestion': 'runny nose',
    'stuffed nose': 'runny nose',
    'sneeze': 'sneezing',
    'itchy': 'itching',
    'joint stiffness': 'stiffness',
    'backache': 'back pain',
    'leg ache': 'leg pain',
    'weight loss': 'weight loss',
    'loss of interest': 'loss of interest',
    'sleep trouble': 'sleep problems',
    'insomnia': 'sleep problems',
    'sad': 'sadness',
    'depressed': 'sadness',
    'yellowing of skin': 'yellow skin',
    'pale stool': 'pale stools',
    'dark urine': 'dark urine',
    'pale stools': 'pale stools',
    'lower abdominal pain': 'lower abdominal pain',
    'burning urination': 'burning urination',
    'frequent urination': 'frequent urination',
    'blurred vision': 'blurred vision',
    'loss of appetite': 'loss of appetite',
    'headache': 'headache',
    'sore throat': 'sore throat',
    'runny nose': 'runny nose',
    'vomiting': 'vomiting',
    'nausea': 'nausea',
    'dizziness': 'dizziness',
    'chest pain': 'chest pain',
    'cough': 'cough',
    'fever': 'fever',
    'fatigue': 'fatigue',
    'weakness': 'weakness',
    'rash': 'rash',
    'skin rash': 'skin rash',
    'worry': 'worry',
    'anxious': 'worry',
    'restlessness': 'restlessness',
    'racing heart': 'racing heart',
    'palpitations': 'racing heart',
    'difficulty concentrating': 'difficulty concentrating',
    'depression': 'sadness',
    'mental illness': 'sadness',
    'panic attack': 'racing heart',
    'anxiety': 'worry'
}

def normalize_symptom(symptom):
    value = symptom.lower().replace('-', ' ').strip()
    value = ' '.join(value.split())
    return SYMPTOM_SYNONYMS.get(value, value)

ALL_SYMPTOMS = sorted([
    'fever', 'cough', 'fatigue', 'body ache', 'shortness of breath', 'chest pain',
    'headache', 'nausea', 'vomiting', 'dizziness', 'sore throat', 'runny nose',
    'sneezing', 'mild fever', 'abdominal pain', 'stomach pain', 'stomach ache', 'stomach cramps', 'stomachache', 'tummy pain', 'tummy ache', 'abdominal cramps',
    'diarrhea', 'joint pain', 'swelling', 'stiffness', 'skin rash', 'itching', 'redness',
    'back pain', 'backache', 'leg pain', 'leg ache', 'numbness', 'weakness', 'high blood pressure',
    'wheezing', 'chest tightness', 'chest pressure', 'chest discomfort', 'rash',
    'muscle pain', 'muscle aches', 'sensitivity to light', 'blurred vision', 'excessive thirst',
    'frequent urination', 'urinary frequency', 'urinary urgency', 'burning urination', 'lower abdominal pain',
    'sweating', 'loss of interest', 'loss of appetite', 'sleep problems', 'sleep trouble', 'insomnia',
    'sadness', 'sad', 'depressed', 'weight loss', 'yellow skin', 'yellowing of skin', 'dark urine',
    'pale stools', 'pale stool', 'vomit', 'throwing up', 'dizzy', 'lightheaded', 'light headed', 'breathlessness',
    'wheeze', 'nasal congestion', 'stuffed nose', 'sneeze', 'itchy', 'joint stiffness',
    'worry', 'anxious', 'restlessness', 'racing heart', 'palpitations', 'difficulty concentrating',
    'depression', 'anxiety', 'mental illness', 'panic attack'
])

def predict_disease(symptoms_list):
    raw_text = " ".join(symptoms_list).lower()
    normalized_symptoms = [s.lower().strip() for s in symptoms_list]
    
    best_match = None
    best_weight = 0
    best_score = 0

    for key_symptoms, info in SYMPTOM_DISEASE_MAP.items():
        score = 0
        matched_db_syms = set()
        
        # 1. Exact string matching (including synonyms)
        for db_sym in key_symptoms:
            if db_sym in normalized_symptoms:
                score += 2.5
                matched_db_syms.add(db_sym)
            elif db_sym in raw_text:
                score += 1.0
                matched_db_syms.add(db_sym)
            else:
                for syn, mapped in SYMPTOM_SYNONYMS.items():
                    if mapped == db_sym:
                        if syn in normalized_symptoms:
                            score += 2.5
                            matched_db_syms.add(db_sym)
                            break
                        elif syn in raw_text:
                            score += 1.0
                            matched_db_syms.add(db_sym)
                            break
        
        # 2. Token-level fuzzy matching
        words = [w.strip() for w in raw_text.replace(',', ' ').split() if w.strip()]
        for db_sym in key_symptoms:
            if db_sym in matched_db_syms: continue
            
            db_words = db_sym.split()
            if len(db_words) == 1:
                for w in words:
                    if difflib.SequenceMatcher(None, w, db_sym).ratio() > 0.8:
                        score += 0.8
                        matched_db_syms.add(db_sym)
                        break
            else:
                significant_db_words = [w for w in db_words if len(w) > 3]
                for sw in significant_db_words:
                    for w in words:
                        if difflib.SequenceMatcher(None, w, sw).ratio() > 0.85:
                            score += 0.4
                            
        percentage = score / len(key_symptoms)
        weight = score + percentage
        
        if weight > best_weight:
            best_weight = weight
            best_score = score
            best_match = info

    if best_match:
        return best_match
        
    return {'disease': 'Unidentified Condition', 'doctor': 'Specialist', 'specialty': 'Specialized Medicine', 'severity': 'Unknown', 'treatment': 'Consult a specialist for further medical evaluation.'}

def recommend_hospitals(specialty):
    matched = [h for h in HOSPITALS if specialty in h['specializations']]
    if not matched:
        matched = [h for h in HOSPITALS if 'General Medicine' in h['specializations']]
    return matched[:3]
