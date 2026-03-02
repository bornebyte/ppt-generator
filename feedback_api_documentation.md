# Feedback API Documentation

## 1. **Submit Feedback**
### Endpoint:
`POST /api/feedback`

### Description:
Allows users to submit feedback about the application.

### Request Body:
- `feedback_text` (string, required): The feedback content.
- `rating` (integer, optional): A rating between 1 and 5.
- `user_email` (string, optional): The user's email for follow-up.
- `category` (string, optional): The category of feedback. Possible values:
  - `praise`
  - `feature`
  - `bug`
  - `improvement`
  - `other`

### Example Request:
```json
{
  "feedback_text": "I love the app! It's very user-friendly.",
  "rating": 5,
  "user_email": "user@example.com",
  "category": "praise"
}
```

### Response:
- **201 Created**:
  ```json
  {
    "success": true,
    "message": "Thank you for your feedback!",
    "feedback_id": 123
  }
  ```
- **400 Bad Request**:
  ```json
  {
    "error": "feedback_text is required"
  }
  ```

---

## 2. **Get All Feedback**
### Endpoint:
`GET /api/feedbacks`

### Description:
Retrieve a list of all feedback with optional filtering and pagination.

### Query Parameters:
- `limit` (integer, optional): Maximum number of results to return (default: 50, max: 200).
- `offset` (integer, optional): Number of results to skip (default: 0).
- `feedback_text` (string, optional): Filter by feedback content (partial match).
- `user_email` (string, optional): Filter by user email.
- `category` (string, optional): Filter by category.
- `status` (string, optional): Filter by status (`new`, `reviewed`, `resolved`, `archived`).
- `min_rating` (integer, optional): Minimum rating to filter by.
- `max_rating` (integer, optional): Maximum rating to filter by.
- `start` (string, optional): Start date in ISO format.
- `end` (string, optional): End date in ISO format.
- `q` (string, optional): Global search across key fields.
- `sort_by` (string, optional): Field to sort by (`timestamp`, `rating`, `category`, `status`).
- `sort_dir` (string, optional): Sort direction (`asc` or `desc`).

### Example Request:
`GET /api/feedbacks?category=praise&min_rating=4&sort_by=rating&sort_dir=desc`

### Response:
- **200 OK**:
  ```json
  {
    "total": 2,
    "limit": 50,
    "offset": 0,
    "items": [
      {
        "id": 123,
        "timestamp": "2026-03-02T10:00:00Z",
        "feedback_text": "I love the app! It's very user-friendly.",
        "rating": 5,
        "user_email": "user@example.com",
        "category": "praise",
        "status": "new",
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0"
      },
      {
        "id": 124,
        "timestamp": "2026-03-01T15:30:00Z",
        "feedback_text": "Great app, but it could use more features.",
        "rating": 4,
        "user_email": "anotheruser@example.com",
        "category": "feature",
        "status": "reviewed",
        "ip_address": "192.168.1.2",
        "user_agent": "Mozilla/5.0"
      }
    ]
  }
  ```

---

## 3. **Get Feedback by ID**
### Endpoint:
`GET /api/feedbacks/<feedback_id>`

### Description:
Retrieve details of a specific feedback entry by its ID.

### Example Request:
`GET /api/feedbacks/123`

### Response:
- **200 OK**:
  ```json
  {
    "id": 123,
    "timestamp": "2026-03-02T10:00:00Z",
    "feedback_text": "I love the app! It's very user-friendly.",
    "rating": 5,
    "user_email": "user@example.com",
    "category": "praise",
    "status": "new",
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0"
  }
  ```
- **404 Not Found**:
  ```json
  {
    "error": "Feedback not found"
  }
  ```

---

## 4. **Update Feedback**
### Endpoint:
`PATCH /api/feedbacks/<feedback_id>`

### Description:
Update the status or category of a specific feedback entry.

### Request Body:
- `status` (string, optional): Update the feedback status. Possible values:
  - `new`
  - `reviewed`
  - `resolved`
  - `archived`
- `category` (string, optional): Update the feedback category.

### Example Request:
```json
{
  "status": "reviewed",
  "category": "improvement"
}
```

### Response:
- **200 OK**:
  ```json
  {
    "id": 123,
    "timestamp": "2026-03-02T10:00:00Z",
    "feedback_text": "I love the app! It's very user-friendly.",
    "rating": 5,
    "user_email": "user@example.com",
    "category": "improvement",
    "status": "reviewed",
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0"
  }
  ```
- **404 Not Found**:
  ```json
  {
    "error": "Feedback not found"
  }
  ```

---

## 5. **Export Feedback**
### Endpoint:
`GET /api/feedbacks/export`

### Description:
Export feedback data as CSV or JSON.

### Query Parameters:
- `format` (string, required): Export format. Possible values:
  - `csv`
  - `json`
- `limit` (integer, optional): Maximum number of results to export (default: 5000, max: 10000).
- `offset` (integer, optional): Number of results to skip (default: 0).

### Example Request:
`GET /api/feedbacks/export?format=csv&limit=100`

### Response:
- **200 OK** (CSV):
  ```
  id,timestamp,feedback_text,rating,user_email,category,status,ip_address,user_agent
  123,2026-03-02T10:00:00Z,"I love the app! It's very user-friendly.",5,user@example.com,praise,new,192.168.1.1,"Mozilla/5.0"
  124,2026-03-01T15:30:00Z,"Great app, but it could use more features.",4,anotheruser@example.com,feature,reviewed,192.168.1.2,"Mozilla/5.0"
  ```

- **200 OK** (JSON):
  ```json
  {
    "count": 2,
    "limit": 100,
    "offset": 0,
    "items": [
      {
        "id": 123,
        "timestamp": "2026-03-02T10:00:00Z",
        "feedback_text": "I love the app! It's very user-friendly.",
        "rating": 5,
        "user_email": "user@example.com",
        "category": "praise",
        "status": "new",
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0"
      },
      {
        "id": 124,
        "timestamp": "2026-03-01T15:30:00Z",
        "feedback_text": "Great app, but it could use more features.",
        "rating": 4,
        "user_email": "anotheruser@example.com",
        "category": "feature",
        "status": "reviewed",
        "ip_address": "192.168.1.2",
        "user_agent": "Mozilla/5.0"
      }
    ]
  }
  ```