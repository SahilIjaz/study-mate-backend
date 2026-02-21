import sys
import os

# Add the backend folder to Python's path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)