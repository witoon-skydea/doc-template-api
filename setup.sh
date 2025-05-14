#!/bin/bash

echo "┌───────────────────────────────────────────────┐"
echo "│                                               │"
echo "│     Document Template API - Release Script    │"
echo "│                                               │"
echo "└───────────────────────────────────────────────┘"

# กำหนดไดเรกทอรีของโปรเจค
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# ตรวจสอบ dependencies
echo "📋 Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# ตรวจสอบว่า virtual environment ได้ถูกสร้างแล้วหรือไม่
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# เปิดใช้งาน virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# ติดตั้ง dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# รัน tests
echo "🧪 Running tests..."
pytest tests/

# ตรวจสอบไฟล์ .env
if [ ! -f ".env" ]; then
    echo "🔑 Creating default .env file..."
    echo "SECRET_KEY=development-secret-key-change-in-production" > .env
    echo "DATABASE_URL=sqlite:///doctemplate.db" >> .env
    echo "JWT_SECRET_KEY=jwt-secret-key-change-in-production" >> .env
    echo "API_PORT=8531" >> .env
    echo "DEBUG=True" >> .env
fi

# จัดการฐานข้อมูล
echo "🗄️ Setting up database..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

echo "✨ Project setup complete! ✨"
echo "📝 API Documentation: http://localhost:8531/apidocs/"
echo "🚀 Run the API: ./run.sh"
echo "🌐 Deploy with Gunicorn: ./deploy.sh"
echo ""
echo "For more information, please refer to the README.md file."
