#!/usr/bin/env python

"""
Health Agent System - Entry Point
This script starts the health agent system with both API server and admin dashboard.
"""

import subprocess
import sys
import time
import threading
from pathlib import Path


def start_api_server():
    """Start the FastAPI server"""
    print("Starting API server...")
    try:
        # Change to the api directory and run the server
        result = subprocess.run([
            sys.executable, "-m", "api.main"
        ], cwd=Path(__file__).parent, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("API server started successfully")
        else:
            print(f"API server failed to start: {result.stderr}")
            return False
        
        return True
    except Exception as e:
        print(f"Error starting API server: {e}")
        return False


def start_admin_dashboard():
    """Start the Streamlit admin dashboard"""
    print("Starting admin dashboard...")
    try:
        # Start Streamlit in a separate thread
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", "frontend/admin_dashboard.py"
        ], cwd=Path(__file__).parent, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Admin dashboard started successfully")
        else:
            print(f"Admin dashboard failed to start: {result.stderr}")
            return False
        
        return True
    except Exception as e:
        print(f"Error starting admin dashboard: {e}")
        return False


def main():
    print("Health Agent System - Starting Components")
    print("============================================")
    
    # Start API server
    api_started = start_api_server()
    
    if not api_started:
        print("Failed to start API server. Exiting.")
        return
    
    print("\nAPI server is running on http://localhost:8000")
    print("Admin dashboard will be available on http://localhost:8501 after starting it manually")
    print("\nTo test the system, you can use curl or a REST client to send requests to:")
    print("  - POST http://localhost:8000/query (with message in body)")
    print("  - GET http://localhost:8000/reports")
    print("  - GET http://localhost:8000/health")
    
    # For demonstration purposes, we'll show how to test it
    print("\nTo test the system, you can run these commands in another terminal:")
    print("  curl -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{\"message\": \"Mam błęk i kaszel\"}'")
    print("  curl http://localhost:8000/reports")
    
    print("\nSystem is ready! Press Ctrl+C to stop.")
    
    try:
        # Keep the main process running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down system...")


if __name__ == "__main__":
    main()
