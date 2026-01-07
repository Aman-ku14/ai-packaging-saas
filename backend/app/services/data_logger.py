import json
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = "ai_decisions.jsonl"

def log_decision(data: dict):
    """
    Appends a decision record to a JSONL file.
    Designed to be failsafe (non-blocking).
    """
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        file_path = os.path.join(LOG_DIR, LOG_FILE)
        
        # Add timestamp if not present
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow().isoformat()
            
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
            
    except Exception as e:
        print(f"Logging failed: {e}")
