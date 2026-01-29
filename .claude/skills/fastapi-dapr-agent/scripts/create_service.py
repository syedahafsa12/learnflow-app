#!/usr/bin/env python3
"""
Create FastAPI + Dapr service structure with Dockerfile and K8s manifests
"""
import os
import sys
from pathlib import Path

def create_service(service_name: str, base_path: str = "."):
    """Create complete FastAPI service with Dapr integration"""

    service_dir = Path(base_path) / service_name
    service_dir.mkdir(parents=True, exist_ok=True)

    # Create main.py
    main_py = f'''from fastapi import FastAPI
from pydantic import BaseModel
import logging

app = FastAPI(title="{service_name}", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
async def health_check():
    return {{"status": "healthy", "service": "{service_name}"}}

@app.get("/")
async def root():
    return {{"message": "Welcome to {service_name}"}}
'''

    (service_dir / "main.py").write_text(main_py)

    # Create requirements.txt
    requirements = '''fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
dapr==1.12.0
'''
    (service_dir / "requirements.txt").write_text(requirements)

    # Create Dockerfile
    dockerfile = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
    (service_dir / "Dockerfile").write_text(dockerfile)

    print(f"✓ Service structure created at {service_dir}")
    print(f"  - main.py")
    print(f"  - requirements.txt")
    print(f"  - Dockerfile")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_service.py <service_name> [base_path]")
        sys.exit(1)

    service_name = sys.argv[1]
    base_path = sys.argv[2] if len(sys.argv) > 2 else "."

    create_service(service_name, base_path)
