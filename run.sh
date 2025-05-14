#!/bin/bash

# สคริปต์สำหรับรันแอพพลิเคชัน Document Template API

# กำหนดไดเรกทอรีของโปรเจค
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# ตรวจสอบว่า virtual environment ได้ถูกสร้างแล้วหรือไม่
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# เปิดใช้งาน virtual environment
source venv/bin/activate

# ติดตั้ง dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# ตรวจสอบไฟล์ .env
if [ ! -f ".env" ]; then
    echo "Creating default .env file..."
    echo "SECRET_KEY=development-secret-key-change-in-production" > .env
    echo "DATABASE_URL=sqlite:///doctemplate.db" >> .env
    echo "JWT_SECRET_KEY=jwt-secret-key-change-in-production" >> .env
    echo "API_PORT=8531" >> .env
    echo "DEBUG=True" >> .env
fi

# รันแอพพลิเคชัน
echo "Running Document Template API on port 8531..."
python run.py
