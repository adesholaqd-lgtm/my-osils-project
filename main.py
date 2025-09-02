
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

@app.route('/download_project')
def download_project():
    """Generate and download the entire project as a zip file"""
    import zipfile
    import tempfile
    from flask import send_file
    
    # Create a temporary zip file
    temp_dir = tempfile.mkdtemp()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"nosdra_oil_spill_system_{timestamp}.zip"
    zip_path = os.path.join(temp_dir, zip_filename)
    
    # Files and directories to include
    files_to_include = [
        'main.py',
        'incidents.json',
        'pyproject.toml',
        '.replit',
        'poetry.lock',
        '.gitignore'
    ]
    
    directories_to_include = [
        'templates',
        'static'
    ]
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add individual files
        for file_path in files_to_include:
            if os.path.exists(file_path):
                zipf.write(file_path)
        
        # Add directories and their contents
        for directory in directories_to_include:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
        
        # Add README file
        readme_content = f"""# NOSDRA Oil Spill Incident Logging System

## Overview
This is a Flask-based web application for the National Oil Spills Detection and Response Agency (NOSDRA) to log, track, and manage oil spill incidents in Nigeria.

## Features
- Incident reporting and logging
- Dashboard with statistics
- Analytics and reports
- Mobile-friendly responsive design
- Real-time incident tracking

## Installation & Setup

1. Install Python 3.11 or higher
2. Install dependencies:
   ```bash
   pip install flask gunicorn
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Access the application at: http://localhost:5000

## Project Structure
- `main.py` - Main Flask application
- `incidents.json` - Data storage for incidents
- `templates/` - HTML templates
- `static/` - Static files (CSS, images, etc.)

## Usage
1. Access the dashboard to view incident statistics
2. Use "Report Incident" to log new oil spill incidents
3. View detailed analytics and reports
4. Track incident status and response actions

## Contact
NOSDRA LZO ICT GIS Unit
National Oil Spills Detection and Response Agency
Nigeria

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        zipf.writestr('README.md', readme_content)
        
        # Add installation scripts
        install_script = """#!/bin/bash
# NOSDRA Oil Spill System Installation Script

echo "Setting up NOSDRA Oil Spill Incident Logging System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Install required packages
echo "Installing required Python packages..."
pip3 install flask gunicorn

echo "Installation complete!"
echo "To run the application, execute: python3 main.py"
echo "Then open your browser to http://localhost:5000"
"""
        zipf.writestr('install.sh', install_script)
        
        windows_script = """@echo off
echo Setting up NOSDRA Oil Spill Incident Logging System...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is required but not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

REM Install required packages
echo Installing required Python packages...
pip install flask gunicorn

echo Installation complete!
echo To run the application, execute: python main.py
echo Then open your browser to http://localhost:5000
pause
"""
        zipf.writestr('install.bat', windows_script)
    
    return send_file(zip_path, as_attachment=True, download_name=zip_filename)

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
