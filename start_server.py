#!/usr/bin/env python3
"""
Startup script for the RAG Chatbot API on Render
This script properly configures the Python path before starting the server
"""

import os
import sys
import subprocess

def main():
    # Add the project root to Python path to ensure imports work correctly
    project_root = os.path.dirname(os.path.abspath(__file__))  # This is the project root
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    print(f"Project root added to Python path: {project_root}")
    print(f"Python path: {sys.path[:3]}...")  # Show first few entries

    # Import and run the FastAPI app
    try:
        # Change to the project root directory
        os.chdir(project_root)

        # Set environment variables for the subprocess
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{project_root}:{env.get('PYTHONPATH', '')}"

        # Get the port from environment or default to 8000
        port = os.environ.get('PORT', '8000')

        print(f"Starting uvicorn server on port {port}")

        # Run uvicorn with the correct module path
        cmd = [
            sys.executable, '-m', 'uvicorn',
            'backend.api.main:app',
            '--host', '0.0.0.0',
            '--port', port,
            '--reload' if os.environ.get('DEBUG', '').lower() == 'true' else ''
        ]

        # Remove empty string arguments
        cmd = [arg for arg in cmd if arg]

        print(f"Executing command: {' '.join(cmd)}")

        # Execute the uvicorn command
        result = subprocess.run(cmd, env=env)
        sys.exit(result.returncode)

    except ImportError as e:
        print(f"Failed to import backend.api.main: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()