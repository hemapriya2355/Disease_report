import codecs
import re

new_func = """def predict_disease(symptoms_list):
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
        
    return {'disease': 'Unidentified Condition', 'doctor': 'Specialist', 'specialty': 'Specialized Medicine', 'severity': 'Unknown', 'treatment': 'Consult a specialist for further medical evaluation.'}"""

with codecs.open(r'c:\Users\USER\Desktop\final project file\files\backend\knowledge.py', 'r', 'utf-8') as f:
    text = f.read()

# Replace everything from 'def predict_disease' to 'def recommend_hospitals'
text = re.sub(r'def predict_disease\(symptoms_list\)[^\n]*.*?def recommend_hospitals', new_func + '\n\ndef recommend_hospitals', text, flags=re.DOTALL)

with codecs.open(r'c:\Users\USER\Desktop\final project file\files\backend\knowledge.py', 'w', 'utf-8') as f:
    f.write(text)
print('Fixed predict_disease')
