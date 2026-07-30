# Bulk Notifications API

A Django REST Framework API for creating a sender and multiple customer notifications in a single request.

The API is designed to efficiently create notifications across multiple channels such as **email**, **SMS**, and **push notifications**.

## Features
* Create a sender and multiple notifications in a single API request.
* Validate the complete request using Django REST Framework serializers before saving data.
* Use Django's `bulk_create()` to efficiently insert notifications.
* Use `transaction.atomic()` to ensure the operation is all-or-nothing.
* Support multiple notification channels:

  * `email`
  * `sms`
  * `push`
* Return clear HTTP success and validation error responses.

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* `uv` for Python environment and dependency management

## Project Structure

```text
bulk_notifications_api/
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── notifications/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── pyproject.toml
└── README.md
```

## Data Model

### Sender

| Field   | Type    | Description            |
| ------- | ------- | ---------------------- |
| `id`    | Integer | Primary key            |
| `name`  | String  | Sender's name          |
| `email` | Email   | Sender's email address |

### Notification

| Field     | Type        | Description                             |
| --------- | ----------- | --------------------------------------- |
| `id`      | Integer     | Primary key                             |
| `title`   | String      | Notification title                      |
| `message` | Text        | Notification content                    |
| `channel` | String      | `email`, `sms`, or `push`               |
| `sender`  | Foreign Key | Sender associated with the notification |

A sender can have multiple notifications.

```text
Sender
  │
  ├── Notification
  ├── Notification
  └── Notification
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mordecai-Wambua/Bulk-Notifications-API.git
cd bulk_notifications_api
```

### 2. Install dependencies

Using `uv`:

```bash
uv sync
```

### 3. Apply migrations

```bash
uv run python manage.py migrate
```

### 4. Start the development server

```bash
uv run python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Endpoint

### Create Sender and Bulk Notifications

```http
POST /api/notifications/bulk/
```

### Request Body

```json
{
    "name": "Alice Kamau",
    "email": "alice@example.com",
    "notifications": [
        {
            "title": "Welcome",
            "message": "Thank you for joining us.",
            "channel": "email"
        },
        {
            "title": "Reminder",
            "message": "Your subscription renews tomorrow.",
            "channel": "sms"
        }
    ]
}
```

### Successful Response

HTTP `201 Created`

```json
{
    "message": "Sender and notifications created successfully.",
    "sender_id": 1,
    "notifications_created": 2
}
```

## Validation

The API validates the complete request before creating database records.

### Required sender fields

* `name`
* `email`
* `notifications`

### Required notification fields

* `title`
* `message`
* `channel`

### Supported channels

```text
email
sms
push
```

### Empty notifications

A request without notifications is rejected.

Example:

```json
{
    "name": "Alice Kamau",
    "email": "alice@example.com",
    "notifications": []
}
```

Response:

```http
400 Bad Request
```

```json
{
  "non_field_errors": [
    "At least one notification is required"
  ]
}
```

Other invalid data, such as an invalid email address or unsupported notification channel, is also rejected before any database changes are made.

## Implementation Details

### Nested serializers

The request is handled using a nested serializer structure:

```text
SenderSerializer
    └── NotificationSerializer
```

This allows the API to validate the sender and all notifications as one request.

### Transaction handling

The creation process is wrapped in:

```python
@transaction.atomic
```

This ensures that the operation is atomic.

If creating the sender or notifications fails, the transaction is rolled back and partial data is not left in the database.

### Bulk insertion

Notifications are constructed in memory and inserted using:

```python
Notification.objects.bulk_create(notifications)
```

This avoids creating notifications individually with repeated database operations.

Conceptually, the process is:

```text
Validate request
       ↓
Create Sender
       ↓
Build Notification objects
       ↓
bulk_create()
       ↓
Return 201 Created
```

## Testing the API

The API can be tested using the included `testing.http` file.

Start the Django development server:

```bash
uv run python manage.py runserver
```

Then open `testing.http` in your IDE **(like PyCharm's built-in HTTP client or VS Code's REST Client)** and execute the request

The `testing.http` file can also contain additional requests for testing validation and error cases, such as missing fields, invalid email addresses, and unsupported notification channels.


## Running Migrations

Whenever models are changed:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

## License

This project was created as a technical assessment/demo project.
