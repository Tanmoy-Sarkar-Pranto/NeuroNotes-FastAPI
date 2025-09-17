# Topic API Documentation

## Base URL
`/api/v1/topics`

## Authentication Required
All endpoints require Bearer token authentication:
```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. Create Topic
**POST** `/`

Create a new topic for the authenticated user.

#### Request Body
```json
{
  "title": "string",
  "description": "string (optional)",
  "node_type": "string (optional, max 20 chars)",
  "position": {
    "x": 0.0,
    "y": 0.0
  },
  "related_topics": ["uuid1", "uuid2"],
  "relation_types": ["relates_to", "depends_on"]
}
```

#### Success Response (200)
```json
{
  "success": true,
  "message": "Topic created successfully.",
  "data": {
    "title": "string",
    "description": "string",
    "node_type": "string",
    "position": {
      "x": 0.0,
      "y": 0.0
    }
  },
  "status": 200
}
```

#### Error Responses

**400 Bad Request** - Topic already exists
```json
{
  "success": false,
  "message": "Topic already exists.",
  "errors": [],
  "status": 400
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

### 2. Get All Topics
**GET** `/`

Retrieve all topics for the authenticated user.

#### Success Response (200)
```json
{
  "success": true,
  "message": "Topics fetched successfully.",
  "data": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string",
      "node_type": "string",
      "position": {
        "x": 0.0,
        "y": 0.0
      },
      "user_id": "uuid",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  ],
  "status": 200
}
```

#### Error Responses

**404 Not Found** - No topics found
```json
{
  "success": false,
  "message": "No topics found.",
  "errors": [],
  "status": 404
}
```

---

### 3. Get Topic by ID
**GET** `/{topicid}`

Retrieve a specific topic by ID.

#### Path Parameters
- `topicid`: UUID - The topic ID

#### Success Response (200)
```json
{
  "success": true,
  "message": "Topic fetched successfully.",
  "data": {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "node_type": "string",
    "position": {
      "x": 0.0,
      "y": 0.0
    },
    "user_id": "uuid",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  },
  "status": 200
}
```

#### Error Responses

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

### 4. Update Topic
**PATCH** `/{topicid}`

Update a specific topic by ID.

#### Path Parameters
- `topicid`: UUID - The topic ID

#### Request Body
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "node_type": "string (optional)",
  "position": {
    "x": 0.0,
    "y": 0.0
  }
}
```

#### Success Response (200)
```json
{
  "success": true,
  "message": "Topic updated successfully.",
  "data": {
    "id": "uuid",
    "title": "string",
    "description": "string", 
    "node_type": "string",
    "position": {
      "x": 0.0,
      "y": 0.0
    },
    "user_id": "uuid",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  },
  "status": 200
}
```

#### Error Responses

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

### 5. Delete Topic
**DELETE** `/{topicid}`

Delete a specific topic by ID.

#### Path Parameters
- `topicid`: UUID - The topic ID

#### Success Response (204)
```json
{
  "success": true,
  "message": "Topic deleted successfully.",
  "data": true,
  "status": 204
}
```

#### Error Responses

**404 Not Found** - Topic not found
```json
{
  "success": false,
  "message": "Topic not found.",
  "errors": [],
  "status": 404
}
```

## Models

### TopicCreate
- `title`: string (required, max 255 chars)
- `description`: string (optional)
- `node_type`: string (optional, max 20 chars)
- `position`: Position object (optional)
- `related_topics`: List[UUID] (optional)
- `relation_types`: List[string] (optional)

### TopicRead
- `id`: UUID
- `title`: string
- `description`: string
- `node_type`: string
- `position`: Position object
- `user_id`: UUID
- `created_at`: datetime
- `updated_at`: datetime

### TopicUpdate
- `title`: string (optional)
- `description`: string (optional)
- `node_type`: string (optional)
- `position`: Position object (optional)

### Position
- `x`: float
- `y`: float

## Business Rules

- Topic titles must be unique per user
- Topics are automatically associated with the authenticated user
- Deleting a topic cascades to delete associated notes
- Position coordinates are stored for graph visualization