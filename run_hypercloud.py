import os
import subprocess
import sys

def setup_and_run():
    print("="*60)
    print("HYPERCLOUD PORTABLE LAUNCHER")
    print("="*60)

    # 1. Check for Virtual Environment
    venv_dir = 'venv'
    if not os.path.exists(venv_dir):
        print(f"\n[PHASE 1] Creating virtual environment in {venv_dir}...")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            print("Virtual environment created successfully.")
        except Exception as e:
            print(f"Error creating venv: {e}")
            return

    # 2. Determine venv python path
    if os.name == 'nt': # Windows
        venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')
    else: # Linux/Mac
        venv_python = os.path.join(venv_dir, 'bin', 'python')

    # 3. Install Dependencies
    if os.path.exists('requirements.txt'):
        print("\n[PHASE 2] Installing/updating dependencies...")
        try:
            subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("Dependencies installed successfully.")
        except Exception as e:
            print(f"Error installing dependencies: {e}")
            # If standard pip fails, it might be due to pip not being in venv or system restriction
            print("Attempting fallback installation...")
            subprocess.run([venv_python, "-m", "ensurepip", "--default-pip"], check=False)
            subprocess.run([venv_python, "-m", "pip", "install", "flask", "flask-sqlalchemy"], check=False)

    # 4. Initialize/Sync Database if not present
    db_path = os.path.join('instance', 'cloud_bill.db')
    if not os.path.exists(db_path):
        print("\n[PHASE 3] Initializing Hypercloud database...")
        try:
            subprocess.run([venv_python, "init_db.py"], check=True)
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing DB: {e}")

    # 5. Run the Application
    print("\n[PHASE 4] Launching Hypercloud GUI...")
    print("Visit http://localhost:5000 in your browser.")
    print("="*60)
    try:
        subprocess.run([venv_python, "app.py"])
    except KeyboardInterrupt:
        print("\nHypercloud stopped.")

if __name__ == "__main__":
    setup_and_run()
