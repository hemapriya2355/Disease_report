from flask import Flask, render_template
import os
from database import init_db
from routes import api_blueprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')

app = Flask(__name__, 
            static_folder=os.path.join(FRONTEND_DIR, 'static'), 
            template_folder=os.path.join(FRONTEND_DIR, 'templates'))

app.secret_key = 'healthcare_kg_secret_2024'
app.register_blueprint(api_blueprint)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully")
    print("Starting Modular Healthcare Knowledge Graph App on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
