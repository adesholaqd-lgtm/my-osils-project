
import zipfile
import os
from datetime import datetime

def create_project_zip():
    """Create a zip file containing the entire NOSDRA project"""
    
    # Get current timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"nosdra_oil_spill_system_{timestamp}.zip"
    
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
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add individual files
        for file_path in files_to_include:
            if os.path.exists(file_path):
                zipf.write(file_path)
                print(f"Added: {file_path}")
        
        # Add directories and their contents
        for directory in directories_to_include:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
                        print(f"Added: {file_path}")
        
        # Add README file with project information
        readme_content = """# NOSDRA Oil Spill Incident Logging System

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

Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        zipf.writestr('README.md', readme_content)
        print("Added: README.md")
        
        # Add installation script
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

# Make main.py executable
chmod +x main.py

echo "Installation complete!"
echo "To run the application, execute: python3 main.py"
echo "Then open your browser to http://localhost:5000"
"""
        zipf.writestr('install.sh', install_script)
        print("Added: install.sh")
        
        # Add Windows batch file
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
        print("Added: install.bat")
    
    print(f"\nZip file created successfully: {zip_filename}")
    print(f"File size: {os.path.getsize(zip_filename) / 1024:.2f} KB")
    return zip_filename

if __name__ == "__main__":
    zip_file = create_project_zip()
    print(f"\nYour NOSDRA project has been packaged into: {zip_file}")
    print("This zip file contains all the code, templates, and setup instructions.")
