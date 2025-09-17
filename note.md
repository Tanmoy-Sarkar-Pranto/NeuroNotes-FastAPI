# Note API Documentation

## Base URL
`/api/v1/notes`

## Authentication Required
All endpoints require Bearer token authentication:
```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. Get All Notes by Topic
**GET** `/{topicId}`

Retrieve all notes for a specific topic.

#### Path Parameters
- `topicId`: UUID - The topic ID

#### Success Response (200)
```json
{
  "success": true,
  "message": "Notes fetched successfully.",
  "data": [
    {
      "id": "uuid",
      "title": "string",
      "content": "string",
      "urls": ["string"],
      "topic_id": "uuid",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00",
      "tags": [
        {
          "id": "uuid",
          "name": "string",
          "color": "string",
          "user_id": "uuid",
          "created_at": "2024-01-01T12:00:00"
        }
      ]
    }
  ],
  "status": 200
}
```

#### Error Responses

**404 Not Found** - Topic or notes not found
```json
{
  "success": false,
  "message": "Topic not found.",
  "errors": [],
  "status": 404
}
```

---

### 2. Create Note
**POST** `/`

Create a new note in a topic.

#### Request Body
```json
{
  "title": "string (optional, max 255 chars)",
  "content": "string (required)",
  "urls": ["string"],
  "topic_id": "uuid",
  "tag_ids": ["uuid1", "uuid2"]
}
```

#### Success Response (200)
```json
{
  "success": true,
  "message": "Note created successfully.",
  "data": {
    "id": "uuid",
    "title": "string",
    "content": "string",
    "urls": ["string"],
    "topic_id": "uuid",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00",
    "tags": [
      {
        "id": "uuid",
        "name": "string",
        "color": "string",
        "user_id": "uuid",
        "created_at": "2024-01-01T12:00:00"
      }
    ]
  },
  "status": 200
}
```

#### Error Responses

**400 Bad Request** - Invalid tags provided
```json
{
  "success": false,
  "message": "Invalid tags provided.",
  "errors": [],
  "status": 400
}
```

**404 Not Found** - Topic not found
```json
{
  "success": false,
  "message": "Topic not found.",
  "errors": [],
  "status": 404
}
```

---

### 3. Get Single Note
**GET** `/single/{noteid}`

Retrieve a specific note by ID.

#### Path Parameters
- `noteid`: UUID - The note ID

#### Success Response (200)
```json
{
  "success": true,
  "message": "Note fetched successfully.",
  "data": {
    "id": "uuid",
    "title": "string",
    "content": "string",
    "urls": ["string"],
    "topic_id": "uuid",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00",
    "tags": [
      {
        "id": "uuid",
        "name": "string", 
        "color": "string",
        "user_id": "uuid",
        "created_at": "2024-01-01T12:00:00"
      }
    ]
  },
  "status": 200
}
```

#### Error Responses

**404 Not Found** - Note not found
```json
{
  "success": false,
  "message": "Note not found.",
  "errors": [],
  "status": 404
}
```

---

### 4. Update Note
**PATCH** `/{noteid}`

Update a specific note by ID.

#### Path Parameters
- `noteid`: UUID - The note ID

#### Request Body
```json
{
  "title": "string (optional)",
  "content": "string (optional)",
  "urls": ["string"],
  "tag_ids": ["uuid1", "uuid2"]
}
```

#### Success Response (200)
```json
{
  "success": true,
  "message": "Note updated successfully.",
  "data": {
    "id": "uuid",
    "title": "string",
    "content": "string",
    "urls": ["string"],
    "topic_id": "uuid",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00",
    "tags": [
      {
        "id": "uuid",
        "name": "string",
        "color": "string",
        "user_id": "uuid",
        "created_at": "2024-01-01T12:00:00"
      }
    ]
  },
  "status": 200
}
```

#### Error Responses

**400 Bad Request** - Invalid tags provided
```json
{
  "success": false,
  "message": "Invalid tags provided.",
  "errors": [],
  "status": 400
}
```

**404 Not Found** - Note not found
```json
{
  "success": false,
  "message": "Note not found.",
  "errors": [],
  "status": 404
}
```

---

### 5. Delete Note
**DELETE** `/{noteid}`

Delete a specific note by ID.

#### Path Parameters
- `noteid`: UUID - The note ID

#### Success Response (204)
```json
{
  "success": true,
  "message": "Note deleted successfully.",
  "data": true,
  "status": 204
}
```

#### Error Responses

**404 Not Found** - Note not found
```json
{
  "success": false,
  "message": "Note not found.",
  "errors": [],
  "status": 404
}
```

## Models

### NoteCreate
- `title`: string (optional, max 255 chars)
- `content`: string (required)
- `urls`: List[string] (optional)
- `topic_id`: UUID (required)
- `tag_ids`: List[UUID] (optional)

### NoteReadWithTags
- `id`: UUID
- `title`: string
- `content`: string
- `urls`: List[string]
- `topic_id`: UUID
- `created_at`: datetime
- `updated_at`: datetime
- `tags`: List[NoteTagRead]

### NoteUpdate
- `title`: string (optional)
- `content`: string (optional)
- `urls`: List[string] (optional)
- `tag_ids`: List[UUID] (optional)

### NoteTagRead
- `id`: UUID
- `name`: string
- `color`: string
- `user_id`: UUID
- `created_at`: datetime

## Tag Management

### Adding Tags to Notes
Include `tag_ids` array in create/update requests:
```json
{
  "content": "Note content",
  "topic_id": "uuid",
  "tag_ids": ["tag-uuid-1", "tag-uuid-2"]
}
```

### Updating Tags
- Provide `tag_ids` array to replace all current tags
- Provide empty array `[]` to remove all tags
- Omit `tag_ids` field to leave tags unchanged

### Tag Validation
- All provided tag IDs must exist and belong to the authenticated user
- Invalid tags will return 400 Bad Request error

## Business Rules

- Notes must belong to a topic owned by the authenticated user
- URLs are stored as an array of strings
- Tags are many-to-many relationships with notes
- All responses include complete tag information
- Deleting notes removes tag associations automatically