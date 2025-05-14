# API Documentation

Document Template API เป็น RESTful API สำหรับจัดการ Document Template และ Workflow ของเอกสาร

## Base URL

```
http://localhost:8531/api/v1
```

## Authentication

API นี้ใช้ JWT (JSON Web Token) สำหรับการพิสูจน์ตัวตน

### Register a new user

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  }
}
```

### Login

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  }
}
```

### Get Current User Profile

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "username": "johndoe",
  "email": "john@example.com",
  "role": "user",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

## Templates

### Get All Templates

**Endpoint:** `GET /templates`

**Query Parameters:**
- `status` (optional): Filter templates by status (`draft`, `active`, `archived`)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Invoice Template",
    "description": "Template for creating invoices",
    "content": "<html><body>Invoice content...</body></html>",
    "editable_fields": {
      "fields": [
        {"name": "customer_name", "type": "text"},
        {"name": "amount", "type": "number"}
      ]
    },
    "status": "active",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  },
  {
    "id": 2,
    "public_id": "9e107d9d-372b-bd97-f7cd-d9d7536e3e6d",
    "name": "Contract Template",
    "description": "Template for legal contracts",
    "content": "<html><body>Contract content...</body></html>",
    "editable_fields": {
      "fields": [
        {"name": "party_name", "type": "text"},
        {"name": "date", "type": "date"}
      ]
    },
    "status": "draft",
    "created_at": "2023-01-02T12:00:00Z",
    "updated_at": "2023-01-02T12:00:00Z"
  }
]
```

### Get a Specific Template

**Endpoint:** `GET /templates/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Invoice Template",
  "description": "Template for creating invoices",
  "content": "<html><body>Invoice content...</body></html>",
  "editable_fields": {
    "fields": [
      {"name": "customer_name", "type": "text"},
      {"name": "amount", "type": "number"}
    ]
  },
  "status": "active",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Create a Template

**Endpoint:** `POST /templates`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Invoice Template",
  "description": "Template for creating invoices",
  "content": "<html><body>Invoice content...</body></html>",
  "editable_fields": {
    "fields": [
      {"name": "customer_name", "type": "text", "required": true},
      {"name": "amount", "type": "number", "required": true}
    ]
  },
  "status": "draft"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Invoice Template",
  "description": "Template for creating invoices",
  "content": "<html><body>Invoice content...</body></html>",
  "editable_fields": {
    "fields": [
      {"name": "customer_name", "type": "text", "required": true},
      {"name": "amount", "type": "number", "required": true}
    ]
  },
  "status": "draft",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Update a Template

**Endpoint:** `PUT /templates/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Updated Invoice Template",
  "description": "Updated template for creating invoices",
  "status": "active"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Updated Invoice Template",
  "description": "Updated template for creating invoices",
  "content": "<html><body>Invoice content...</body></html>",
  "editable_fields": {
    "fields": [
      {"name": "customer_name", "type": "text", "required": true},
      {"name": "amount", "type": "number", "required": true}
    ]
  },
  "status": "active",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T13:00:00Z"
}
```

### Delete a Template

**Endpoint:** `DELETE /templates/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Template deleted successfully"
}
```

## Documents

### Get All Documents

**Endpoint:** `GET /documents`

**Query Parameters:**
- `status` (optional): Filter documents by status (`draft`, `submitted`, `approved`, `rejected`)
- `template_id` (optional): Filter documents by template public ID
- `station_id` (optional): Filter documents by current station public ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Invoice #12345",
    "content": "<html><body>Invoice content with filled values...</body></html>",
    "template_id": 1,
    "status": "draft",
    "current_station_id": 1,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z",
    "template": {
      "id": 1,
      "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "name": "Invoice Template"
    },
    "current_station": {
      "id": 1,
      "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "name": "Draft Station",
      "type": "draft"
    }
  }
]
```

### Get a Specific Document

**Endpoint:** `GET /documents/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Invoice #12345",
  "content": "<html><body>Invoice content with filled values...</body></html>",
  "template_id": 1,
  "status": "draft",
  "current_station_id": 1,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z",
  "template": {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Invoice Template"
  },
  "current_station": {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Draft Station",
    "type": "draft"
  }
}
```

### Create a Document

**Endpoint:** `POST /documents`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Invoice #12345",
  "content": "<html><body>Invoice content with filled values...</body></html>",
  "template_id": 1,
  "status": "draft",
  "current_station_id": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Invoice #12345",
  "content": "<html><body>Invoice content with filled values...</body></html>",
  "template_id": 1,
  "status": "draft",
  "current_station_id": 1,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Update a Document

**Endpoint:** `PUT /documents/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Updated Invoice #12345",
  "status": "submitted",
  "current_station_id": 2
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Updated Invoice #12345",
  "content": "<html><body>Invoice content with filled values...</body></html>",
  "template_id": 1,
  "status": "submitted",
  "current_station_id": 2,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T13:00:00Z"
}
```

### Delete a Document

**Endpoint:** `DELETE /documents/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Document deleted successfully"
}
```

### Get Document History

**Endpoint:** `GET /documents/{public_id}/history`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "public_id": "9e107d9d-372b-bd97-f7cd-d9d7536e3e6d",
    "document_id": 1,
    "action": "moved",
    "description": "Moved from Draft Station to Review Station",
    "user_id": 1,
    "station_id": 2,
    "created_at": "2023-01-01T13:00:00Z",
    "updated_at": "2023-01-01T13:00:00Z",
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com"
    },
    "station": {
      "id": 2,
      "name": "Review Station",
      "type": "review"
    }
  },
  {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "document_id": 1,
    "action": "created",
    "description": "Document created",
    "user_id": 1,
    "station_id": 1,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z",
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com"
    },
    "station": {
      "id": 1,
      "name": "Draft Station",
      "type": "draft"
    }
  }
]
```

## Stations

### Get All Stations

**Endpoint:** `GET /stations`

**Query Parameters:**
- `type` (optional): Filter stations by type

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Draft Station",
    "description": "Station for drafting documents",
    "type": "draft",
    "responsible_role": "user",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  },
  {
    "id": 2,
    "public_id": "9e107d9d-372b-bd97-f7cd-d9d7536e3e6d",
    "name": "Review Station",
    "description": "Station for reviewing documents",
    "type": "review",
    "responsible_role": "user",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  }
]
```

### Get a Specific Station

**Endpoint:** `GET /stations/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Draft Station",
  "description": "Station for drafting documents",
  "type": "draft",
  "responsible_role": "user",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Create a Station

**Endpoint:** `POST /stations`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Approval Station",
  "description": "Station for document approval",
  "type": "approval",
  "responsible_role": "admin"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "public_id": "d85b1174-5e25-4678-b67a-10f9e1934de7",
  "name": "Approval Station",
  "description": "Station for document approval",
  "type": "approval",
  "responsible_role": "admin",
  "created_at": "2023-01-01T14:00:00Z",
  "updated_at": "2023-01-01T14:00:00Z"
}
```

### Update a Station

**Endpoint:** `PUT /stations/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Updated Approval Station",
  "responsible_role": "manager"
}
```

**Response (200 OK):**
```json
{
  "id": 3,
  "public_id": "d85b1174-5e25-4678-b67a-10f9e1934de7",
  "name": "Updated Approval Station",
  "description": "Station for document approval",
  "type": "approval",
  "responsible_role": "manager",
  "created_at": "2023-01-01T14:00:00Z",
  "updated_at": "2023-01-01T15:00:00Z"
}
```

### Delete a Station

**Endpoint:** `DELETE /stations/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Station deleted successfully"
}
```

### Get Documents at a Station

**Endpoint:** `GET /stations/{public_id}/documents`

**Query Parameters:**
- `status` (optional): Filter documents by status

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Invoice #12345",
    "content": "<html><body>Invoice content with filled values...</body></html>",
    "template_id": 1,
    "status": "draft",
    "current_station_id": 1,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z",
    "template": {
      "id": 1,
      "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "name": "Invoice Template"
    }
  }
]
```

## Flows

### Get All Flows

**Endpoint:** `GET /flows`

**Query Parameters:**
- `active` (optional): Filter flows by active status (true/false)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Approval Flow",
    "description": "Standard approval flow for documents",
    "is_active": true,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  }
]
```

### Get a Specific Flow

**Endpoint:** `GET /flows/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Approval Flow",
  "description": "Standard approval flow for documents",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z",
  "steps": [
    {
      "id": 1,
      "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "flow_id": 1,
      "from_station_id": 1,
      "to_station_id": 2,
      "condition": "status == 'submitted'",
      "order": 1,
      "created_at": "2023-01-01T12:00:00Z",
      "updated_at": "2023-01-01T12:00:00Z",
      "from_station": {
        "id": 1,
        "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "name": "Draft Station",
        "type": "draft"
      },
      "to_station": {
        "id": 2,
        "public_id": "9e107d9d-372b-bd97-f7cd-d9d7536e3e6d",
        "name": "Review Station",
        "type": "review"
      }
    }
  ]
}
```

### Create a Flow

**Endpoint:** `POST /flows`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Approval Flow",
  "description": "Standard approval flow for documents",
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Approval Flow",
  "description": "Standard approval flow for documents",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Update a Flow

**Endpoint:** `PUT /flows/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Updated Approval Flow",
  "is_active": false
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Updated Approval Flow",
  "description": "Standard approval flow for documents",
  "is_active": false,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T13:00:00Z"
}
```

### Delete a Flow

**Endpoint:** `DELETE /flows/{public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Flow deleted successfully"
}
```

### Get Flow Steps

**Endpoint:** `GET /flows/{public_id}/steps`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "flow_id": 1,
    "from_station_id": 1,
    "to_station_id": 2,
    "condition": "status == 'submitted'",
    "order": 1,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z",
    "from_station": {
      "id": 1,
      "public_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "name": "Draft Station",
      "type": "draft"
    },
    "to_station": {
      "id": 2,
      "public_id": "9e107d9d-372b-bd97-f7cd-d9d7536e3e6d",
      "name": "Review Station",
      "type": "review"
    }
  }
]
```

### Add a Flow Step

**Endpoint:** `POST /flows/{public_id}/steps`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "from_station_id": 2,
  "to_station_id": 3,
  "condition": "status == 'reviewed'",
  "order": 2
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "public_id": "9e107d9d-372b-bd97-f7cd-d9d7536e3e6d",
  "flow_id": 1,
  "from_station_id": 2,
  "to_station_id": 3,
  "condition": "status == 'reviewed'",
  "order": 2,
  "created_at": "2023-01-01T13:00:00Z",
  "updated_at": "2023-01-01T13:00:00Z"
}
```

### Update a Flow Step

**Endpoint:** `PUT /flows/{flow_public_id}/steps/{step_public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "condition": "status == 'reviewed' && user_role == 'manager'",
  "order": 3
}
```

**Response (200 OK):**
```json
{
  "id": 2,
  "public_id": "9e107d9d-372b-bd97-f7cd-d9d7536e3e6d",
  "flow_id": 1,
  "from_station_id": 2,
  "to_station_id": 3,
  "condition": "status == 'reviewed' && user_role == 'manager'",
  "order": 3,
  "created_at": "2023-01-01T13:00:00Z",
  "updated_at": "2023-01-01T14:00:00Z"
}
```

### Delete a Flow Step

**Endpoint:** `DELETE /flows/{flow_public_id}/steps/{step_public_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Flow step deleted successfully"
}
```

## Error Handling

API จะส่งกลับข้อผิดพลาดในรูปแบบ JSON ดังนี้:

```json
{
  "error": "Error message",
  "messages": {
    "field_name": ["Validation error message"]
  }
}
```

### HTTP Status Codes

- `200 OK` - คำขอสำเร็จ
- `201 Created` - สร้างรายการใหม่เรียบร้อยแล้ว
- `400 Bad Request` - ข้อมูลที่ส่งมาไม่ถูกต้อง
- `401 Unauthorized` - ไม่มีการตรวจสอบตัวตนหรือ token ไม่ถูกต้อง
- `403 Forbidden` - ไม่มีสิทธิ์เข้าถึงทรัพยากร
- `404 Not Found` - ไม่พบทรัพยากรที่ร้องขอ
- `500 Internal Server Error` - เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์
