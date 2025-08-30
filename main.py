
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'nosdra_secret_key_2024'

# Data storage (using JSON file for simplicity - no database needed)
DATA_FILE = 'incidents.json'

@app.context_processor
def inject_global_data():
    return dict(
        load_incidents=load_incidents,
        moment=datetime
    )

def load_incidents():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_incidents(incidents):
    with open(DATA_FILE, 'w') as f:
        json.dump(incidents, f, indent=2)

@app.route('/')
def index():
    incidents = load_incidents()
    return render_template('index.html', incidents=incidents)

@app.route('/add_incident')
def add_incident():
    return render_template('add_incident.html')

@app.route('/submit_incident', methods=['POST'])
def submit_incident():
    try:
        incident = {
            'id': len(load_incidents()) + 1,
            'date_reported': request.form['date_reported'],
            'time_reported': request.form['time_reported'],
            'location': request.form['location'],
            'state': request.form['state'],
            'lga': request.form['lga'],
            'coordinates': {
                'latitude': request.form.get('latitude', ''),
                'longitude': request.form.get('longitude', '')
            },
            'incident_type': request.form['incident_type'],
            'source': request.form['source'],
            'cause': request.form['cause'],
            'oil_type': request.form['oil_type'],
            'estimated_volume': request.form['estimated_volume'],
            'severity': request.form['severity'],
            'weather_conditions': request.form['weather_conditions'],
            'water_body_affected': request.form.get('water_body_affected', ''),
            'land_area_affected': request.form.get('land_area_affected', ''),
            'population_affected': request.form.get('population_affected', ''),
            'environmental_impact': request.form['environmental_impact'],
            'response_actions': request.form['response_actions'],
            'response_team': request.form['response_team'],
            'cleanup_status': request.form['cleanup_status'],
            'reported_by': request.form['reported_by'],
            'contact_info': request.form['contact_info'],
            'company_responsible': request.form.get('company_responsible', ''),
            'additional_notes': request.form.get('additional_notes', ''),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        incidents = load_incidents()
        incidents.append(incident)
        save_incidents(incidents)
        
        flash('Incident reported successfully!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error submitting incident: {str(e)}', 'error')
        return redirect(url_for('add_incident'))

@app.route('/view_incident/<int:incident_id>')
def view_incident(incident_id):
    incidents = load_incidents()
    incident = next((inc for inc in incidents if inc['id'] == incident_id), None)
    if incident:
        return render_template('view_incident.html', incident=incident)
    flash('Incident not found', 'error')
    return redirect(url_for('index'))

@app.route('/api/incidents')
def api_incidents():
    return jsonify(load_incidents())

@app.route('/reports')
def reports():
    incidents = load_incidents()
    # Generate basic statistics
    total_incidents = len(incidents)
    severity_stats = {}
    state_stats = {}
    monthly_stats = {}
    
    for incident in incidents:
        # Severity statistics
        severity = incident.get('severity', 'Unknown')
        severity_stats[severity] = severity_stats.get(severity, 0) + 1
        
        # State statistics
        state = incident.get('state', 'Unknown')
        state_stats[state] = state_stats.get(state, 0) + 1
        
        # Monthly statistics
        try:
            date_obj = datetime.strptime(incident.get('date_reported', ''), '%Y-%m-%d')
            month_key = date_obj.strftime('%Y-%m')
            monthly_stats[month_key] = monthly_stats.get(month_key, 0) + 1
        except:
            pass
    
    stats = {
        'total_incidents': total_incidents,
        'severity_stats': severity_stats,
        'state_stats': state_stats,
        'monthly_stats': monthly_stats
    }
    
    return render_template('reports.html', stats=stats, incidents=incidents)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
