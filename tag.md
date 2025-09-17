# Tag API Documentation

## Base URL
`/api/v1/tags`

## Authentication Required
All endpoints require Bearer token authentication:
```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. Create Tag
**POST** `/`

Create a new tag for the authenticated user.

#### Request Body
```json
{
  "name": "string (required, max 50 chars)",
  "color": "string (optional, max 20 chars)"
}
```

#### Success Response (200)
```json
{
  "success": true,
  "message": "Tag created successfully.",
  "data": {
    "id": "uuid",
    "name": "string",
    "color": "string",
    "user_id": "uuid",
    "created_at": "2024-01-01T12:00:00"
  },
  "status": 200
}
```

#### Error Responses

**409 Conflict** - Tag already exists
```json
{
  "success": false,
  "message": "Tag already exists.",
  "errors": [],
  "status": 409
}
```

**401 Unauthorized**
```json
{
  "success": false,
  "message": "Unauthorized.",
  "errors": [],
  "status": 401
}
```

---

### 2. Get All Tags
**GET** `/`

Retrieve all tags for the authenticated user.

#### Success Response (200)
```json
{
  "success": true,
  "message": "Tags fetched successfully.",
  "data": [
    {
      "id": "uuid",
      "name": "string",
      "color": "string",
      "user_id": "uuid",
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "status": 200
}
```

#### Error Responses

**404 Not Found** - No tags found
```json
{
  "success": false,
  "message": "No tags found.",
  "errors": [],
  "status": 404
}
```

---

### 3. Get Tag by ID
**GET** `/{tagid}`

Retrieve a specific tag by ID.

#### Path Parameters
- `tagid`: UUID - The tag ID

#### Success Response (200)
```json
{
  "success": true,
  "message": "Tag fetched successfully.",
  "data": {
    "id": "uuid",
    "name": "string",
    "color": "string",
    "user_id": "uuid",
    "created_at": "2024-01-01T12:00:00"
  },
  "status": 200
}
```

#### Error Responses

**404 Not Found** - Tag not found
```json
{
  "success": false,
  "message": "Tag not found.",
  "errors": [],
  "status": 404
}
```

---

### 4. Update Tag
**PATCH** `/{tagid}`

Update a specific tag by ID.

#### Path Parameters
- `tagid`: UUID - The tag ID

#### Request Body
```json
{
  "name": "string (optional)",
  "color": "string (optional)"
}
```

#### Success Response (200)
```json
{
  "success": true,
  "message": "Tag updated successfully.",
  "data": {
    "id": "uuid",
    "name": "string",
    "color": "string",
    "user_id": "uuid",
    "created_at": "2024-01-01T12:00:00"
  },
  "status": 200
}
```

#### Error Responses

**409 Conflict** - Tag name already exists
```json
{
  "success": false,
  "message": "Tag name already exists.",
  "errors": [],
  "status": 409
}
```

**404 Not Found** - Tag not found
```json
{
  "success": false,
  "message": "Tag not found.",
  "errors": [],
  "status": 404
}
```

---

### 5. Delete Tag
**DELETE** `/{tagid}`

Delete a specific tag by ID.

#### Path Parameters
- `tagid`: UUID - The tag ID

#### Success Response (204)
```json
{
  "success": true,
  "message": "Tag deleted successfully.",
  "data": true,
  "status": 204
}
```

#### Error Responses

**404 Not Found** - Tag not found
```json
{
  "success": false,
  "message": "Tag not found.",
  "errors": [],
  "status": 404
}
```

## Models

### NoteTagCreate
- `name`: string (required, max 50 chars)
- `color`: string (optional, max 20 chars)

### NoteTagRead
- `id`: UUID
- `name`: string
- `color`: string
- `user_id`: UUID
- `created_at`: datetime

### NoteTagUpdate
- `name`: string (optional)
- `color`: string (optional)

## Usage Examples

### Create a Tag
```bash
curl -X POST "http://localhost:8000/api/v1/tags/" \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Important",
    "color": "#ff0000"
  }'
```

### Get All User Tags
```bash
curl -X GET "http://localhost:8000/api/v1/tags/" \
  -H "Authorization: Bearer your_access_token"
```

### Update Tag Color
```bash
curl -X PATCH "http://localhost:8000/api/v1/tags/{tag-id}" \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "color": "#00ff00"
  }'
```

## Business Rules

- Tag names must be unique per user
- Tags are automatically associated with the authenticated user
- Color values are typically hex color codes (e.g., "#ff0000")
- Deleting a tag removes it from all associated notes
- Tags can be reused across multiple notes
- Empty color field defaults to null

## Integration with Notes

Tags can be associated with notes through the Note API:

### When Creating Notes
```json
{
  "content": "Note content",
  "topic_id": "uuid",
  "tag_ids": ["tag-uuid-1", "tag-uuid-2"]
}
```

### When Updating Notes
```json
{
  "tag_ids": ["new-tag-uuid"]  // Replace all current tags
}
```

### When Reading Notes
Notes automatically include tag information:
```json
{
  "id": "note-uuid",
  "content": "Note content",
  "tags": [
    {
      "id": "tag-uuid",
      "name": "Important",
      "color": "#ff0000"
    }
  ]
}
```