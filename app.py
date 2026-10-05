"""
Streamlit Root Entry Point for Cloud Deployment (Streamlit Cloud & Hugging Face Spaces)
"""
import os
import sys

# Ensure current working directory is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Delegate to dashboard/app.py
dashboard_path = os.path.join(BASE_DIR, "dashboard", "app.py")
with open(dashboard_path, "r", encoding="utf-8") as f:
    code = f.read()

exec(code, globals())
