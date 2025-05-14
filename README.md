# Document Template API

ระบบ API สำหรับจัดการ Document Template พัฒนาด้วย Python, Flask, SQLAlchemy, และ JWT Authentication

## คุณสมบัติหลัก

- RESTful API สำหรับจัดการ Template เอกสาร
- ระบบ Authentication ด้วย JWT
- การจัดการ Template และฟิลด์ที่แก้ไขได้
- การสร้างเอกสารจาก Template
- ระบบจัดการ Station และ Flow การทำงานของเอกสาร
- API Documentation ด้วย Swagger/Flasgger
- สนับสนุนการทำงานแบบ Multi-user

## การติดตั้ง

### วิธีที่ 1: ใช้สคริปต์อัตโนมัติ

```bash
./run.sh
```

สคริปต์จะทำงานตามลำดับดังนี้:
1. สร้าง virtual environment (ถ้ายังไม่มี)
2. ติดตั้ง dependencies
3. สร้างไฟล์ .env (ถ้ายังไม่มี)
4. รัน API server

### วิธีที่ 2: ติดตั้งเอง

1. สร้าง virtual environment:
```bash
python -m venv venv
```

2. เปิดใช้งาน virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

3. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

4. สร้างไฟล์ .env:
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///doctemplate.db
JWT_SECRET_KEY=your-jwt-secret-key
API_PORT=8531
DEBUG=True
```

5. รันแอพพลิเคชัน:
```bash
python run.py
```

## การใช้งาน API

API จะเริ่มทำงานที่ `http://localhost:8531/api/v1`

### API Documentation

เข้าถึง Swagger UI ได้ที่:
```
http://localhost:8531/apidocs/
```

### การทดสอบ API

ใช้สคริปต์ทดสอบ API:
```bash
python test_api.py
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - สมัครผู้ใช้ใหม่
- `POST /api/v1/auth/login` - เข้าสู่ระบบเพื่อรับ JWT token
- `GET /api/v1/auth/me` - ดูข้อมูลผู้ใช้ปัจจุบัน

### Templates
- `GET /api/v1/templates` - รายการ templates ทั้งหมด
- `GET /api/v1/templates/<public_id>` - ดูรายละเอียด template
- `POST /api/v1/templates` - สร้าง template ใหม่
- `PUT /api/v1/templates/<public_id>` - แก้ไข template
- `DELETE /api/v1/templates/<public_id>` - ลบ template

### Documents
- `GET /api/v1/documents` - รายการเอกสารทั้งหมด
- `GET /api/v1/documents/<public_id>` - ดูรายละเอียดเอกสาร
- `POST /api/v1/documents` - สร้างเอกสารใหม่จาก template
- `PUT /api/v1/documents/<public_id>` - แก้ไขเอกสาร
- `DELETE /api/v1/documents/<public_id>` - ลบเอกสาร
- `GET /api/v1/documents/<public_id>/history` - ดูประวัติการเปลี่ยนแปลงของเอกสาร

### Stations
- `GET /api/v1/stations` - รายการ stations ทั้งหมด
- `GET /api/v1/stations/<public_id>` - ดูรายละเอียด station
- `POST /api/v1/stations` - สร้าง station ใหม่
- `PUT /api/v1/stations/<public_id>` - แก้ไข station
- `DELETE /api/v1/stations/<public_id>` - ลบ station
- `GET /api/v1/stations/<public_id>/documents` - ดูเอกสารทั้งหมดใน station

### Flows
- `GET /api/v1/flows` - รายการ flows ทั้งหมด
- `GET /api/v1/flows/<public_id>` - ดูรายละเอียด flow
- `POST /api/v1/flows` - สร้าง flow ใหม่
- `PUT /api/v1/flows/<public_id>` - แก้ไข flow
- `DELETE /api/v1/flows/<public_id>` - ลบ flow
- `GET /api/v1/flows/<public_id>/steps` - ดู steps ทั้งหมดใน flow
- `POST /api/v1/flows/<public_id>/steps` - เพิ่ม step ใหม่ใน flow
- `PUT /api/v1/flows/<flow_public_id>/steps/<step_public_id>` - แก้ไข step ใน flow
- `DELETE /api/v1/flows/<flow_public_id>/steps/<step_public_id>` - ลบ step ออกจาก flow

## การ Deploy

### วิธีที่ 1: ใช้สคริปต์ deploy

```bash
./deploy.sh
```

สคริปต์จะทำงานตามลำดับดังนี้:
1. สร้าง virtual environment (ถ้ายังไม่มี)
2. ติดตั้ง dependencies
3. สร้างไฟล์ .env (ถ้ายังไม่มี)
4. ติดตั้ง Gunicorn
5. คำนวณจำนวนเหมาะสมของ workers
6. รัน API server ด้วย Gunicorn

### วิธีที่ 2: Deploy เอง

1. เปิดใช้งาน virtual environment:
```bash
source venv/bin/activate
```

2. ติดตั้ง Gunicorn:
```bash
pip install gunicorn
```

3. รัน API ด้วย Gunicorn:
```bash
gunicorn --bind 0.0.0.0:8531 --workers 4 'app:create_app()'
```

## โครงสร้างโปรเจค

```
doc-template-api/
├── app/                      # แอพพลิเคชันหลัก
│   ├── __init__.py           # ตัวสร้างแอพพลิเคชัน Flask
│   └── api/                  # โมดูล API
│       └── v1/               # API เวอร์ชัน 1
│           ├── __init__.py   # Blueprint ของ API
│           ├── models/       # โมเดลฐานข้อมูล
│           ├── routes/       # API endpoints
│           └── schemas/      # Schemas สำหรับ validation
├── docs/                     # เอกสารเพิ่มเติม
├── tests/                    # ทดสอบแอพพลิเคชัน
├── .env                      # ตัวแปรสภาพแวดล้อม
├── .gitignore                # ไฟล์ที่ถูกละเว้นจาก Git
├── deploy.sh                 # สคริปต์สำหรับ deploy
├── requirements.txt          # รายการ dependencies
├── run.py                    # สคริปต์สำหรับรันแอพพลิเคชัน
├── run.sh                    # สคริปต์สำหรับรันแอพพลิเคชันอัตโนมัติ
└── test_api.py               # สคริปต์ทดสอบ API
```

## การพัฒนาต่อยอด

สามารถพัฒนาต่อยอดได้หลายด้าน เช่น:
- เพิ่มระบบสิทธิ์การเข้าถึงให้ละเอียดยิ่งขึ้น
- เชื่อมต่อกับฐานข้อมูลภายนอก เช่น PostgreSQL, MySQL
- เพิ่มการทำ Caching เพื่อเพิ่มประสิทธิภาพ
- เพิ่มระบบแจ้งเตือนผ่าน Email หรือ SMS
- เพิ่มการตรวจสอบความสมบูรณ์ของข้อมูล (Validation) ที่ซับซ้อนขึ้น
- พัฒนา Front-end ที่ใช้ API นี้
- ทำการ Containerize ด้วย Docker

## License

[MIT License](LICENSE)
