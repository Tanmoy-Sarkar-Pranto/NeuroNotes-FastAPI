# User API Documentation

## Base URL
`/api/v1/user`

## Authentication Required
All endpoints require Bearer token authentication:
```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. Get Current User
**GET** `/`

Retrieve the authenticated user's information.

#### Request Headers
```
Authorization: Bearer <access_token>
```

#### Success Response (200)
```json
{
  "success": true,
  "message": "Fetched user successfully",
  "data": {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "created_at": "2024-01-01T12:00:00"
  },
  "status": 200
}
```

#### Error Responses

**401 Unauthorized** - Invalid or missing token
```json
{
  "detail": "Could not validate credentials."
}
```

**404 Not Found** - User not found
```json
{
  "success": false,
  "message": "User not found.",
  "errors": [],
  "status": 400
}
```

## Models

### UserRead
- `id`: UUID - Unique user identifier
- `username`: string - User's username
- `email`: string - User's email address
- `created_at`: datetime - Account creation timestamp

## Usage Examples

### Get Current User Information
```bash
curl -X GET "http://localhost:8000/api/v1/user/" \
  -H "Authorization: Bearer your_access_token_here"
```

### JavaScript/Fetch Example
```javascript
const response = await fetch('/api/v1/user/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  }
});

const userData = await response.json();
```

## Security Notes

- This endpoint returns the user information based on the JWT token
- The token is decoded to extract the user ID
- No user ID parameter is needed in the request
- Token expiration is handled automatically (default: 30 minutes)