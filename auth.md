# Authentication API Documentation

## Base URL
`/api/v1/auth`

## Endpoints

### 1. Register User
**POST** `/register`

Create a new user account.

#### Request Body
```json
{
  "username": "string",
  "email": "string", 
  "password": "string"
}
```

#### Request Validation
- **username**: 3-50 characters, alphanumeric + underscore/hyphen, must start with letter/number
- **email**: Valid email format
- **password**: 8-128 characters, must contain uppercase, lowercase, number, and special character

#### Success Response (201)
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "created_at": "2024-01-01T12:00:00"
  },
  "status": 201
}
```

#### Error Responses

**400 Bad Request** - User already exists
```json
{
  "success": false,
  "message": "User already exists with that email.",
  "errors": [],
  "status": 400
}
```

**422 Validation Error** - Invalid input
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "password"],
      "msg": "Password must contain at least one uppercase letter",
      "input": "weakpass"
    }
  ]
}
```

---

### 2. Login User
**POST** `/login`

Authenticate user and receive access token.

#### Request Body
```json
{
  "email": "string",
  "password": "string"
}
```

#### Success Response (200)
```json
{
  "success": true,
  "message": "Login successfully",
  "data": {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "access_token": "jwt_token_string",
    "token_type": "Bearer",
    "created_at": "2024-01-01T12:00:00"
  },
  "status": 200
}
```

#### Error Responses

**401 Unauthorized** - Invalid credentials
```json
{
  "success": false,
  "message": "Invalid credentials",
  "errors": [],
  "status": 401
}
```

## Authentication

After successful login, include the access token in subsequent requests:

```
Authorization: Bearer <access_token>
```

## Models

### UserCreate
- `username`: string (required, 3-50 chars)
- `email`: string (required, valid email)
- `password`: string (required, 8-128 chars with complexity requirements)

### UserLogin  
- `email`: string (required)
- `password`: string (required)

### UserRead
- `id`: UUID
- `username`: string
- `email`: string
- `created_at`: datetime

### UserLoginResponse
- Extends UserRead
- `access_token`: string
- `token_type`: string