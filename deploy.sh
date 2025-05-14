#!/bin/bash

# สคริปต์สำหรับ deploy Document Template API ด้วย Gunicorn

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
    echo "DEBUG=False" >> .env
fi

# ตรวจสอบว่ามีการติดตั้ง Gunicorn หรือไม่
if ! pip show gunicorn > /dev/null; then
    echo "Installing Gunicorn..."
    pip install gunicorn
fi

# กำหนดจำนวน worker ตามจำนวน CPU
WORKERS=$(python -c "import multiprocessing; print(multiprocessing.cpu_count() * 2 + 1)")

# รัน Gunicorn
echo "Starting Document Template API with Gunicorn on port 8531 with $WORKERS workers..."
gunicorn --bind 0.0.0.0:8531 --workers $WORKERS --log-level info 'app:create_app()'
