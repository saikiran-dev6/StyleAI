import os
import sys

# Add root project directory to python path for Vercel module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from styleai import create_app

app = create_app()
