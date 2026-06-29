# AuthCore - Flask Authentication Service

A robust, production-ready Flask authentication and user management API service featuring JWT-based authentication, rate limiting, refresh token rotation, session management, Swagger UI documentation, and Role-Based Access Control (RBAC).

---

## Features

- **JWT Authentication**: Secure stateless authentication using `Flask-JWT-Extended` with Access and Refresh tokens.
- **Refresh Token Rotation**: Protects against replay attacks by invalidating and rotating refresh tokens on every refresh request.
- **Session & Device Management**: Support for logging out of the current session or logging out of all active devices/sessions simultaneously.
- **Rate Limiting**: Integrated `Flask-Limiter` to protect endpoints against brute force attacks and resource abuse.
- **Swagger Documentation**: Self-documenting API using `flask-smorest` accessible at `/swagger`.
- **Database Migrations**: Managed schema updates using `Flask-Migrate` (Alembic).
- **Role-Based Access Control (RBAC)**: Fine-grained user permissions with the following default roles and permission hierarchy:
  - **User**: Can view self profile, update self profile, and delete self profile.
  - **Moderator**: Can view self profile, update self profile, and view all registered users.
  - **Admin**: Has all moderator permissions + can update user roles and delete any user.

---

## Project Structure

```text
AuthCore/
├── app/
│   ├── errors/          # Custom exceptions and global error handlers
│   ├── models/          # SQLAlchemy Database Models (User, Tokens, etc.)
│   ├── repositories/    # Database queries and persistence layer (Repository Pattern)
│   ├── routes/          # API Blueprints & route controllers (Auth, Users)
│   ├── schemas/         # Marshmallow validation and serialization schemas
│   ├── services/        # Business logic layer
│   ├── utils/           # Utilities (Permissions, JWT helpers)
│   ├── extensions.py    # Flask Extensions registration
│   └── __init__.py      # App factory initializer
├── instance/            # Local instance folder (SQLite database location)
├── migrations/          # Alembic migrations folder
├── config.py            # Configuration settings (environment loading)
├── run.py               # Main application entry point
└── requirements.txt     # Python dependencies
```

---

## Setup and Installation

### Prerequisites
- Python 3.8+
- Virtualenv (`pip install virtualenv`)

### 1. Clone & Set Up Virtual Environment
```bash
git clone <repository-url>
cd AuthCore
python -m venv .venv
```

Activate the virtual environment:
- **Windows**:
  ```powershell
  .venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```env
DATABASE_URL=sqlite:///data.db
SECRET_KEY=your-fallback-flask-secret-key
JWT_SECRET_KEY=your-fallback-jwt-secret-key

# Optional (Flask-Mail SMTP configuration)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 4. Database Initialization & Migration
Initialize and upgrade your database schema:
```bash
flask db upgrade
```

### 5. Running the Application
Run the Flask development server:
```bash
python run.py
```
The server will start on `http://127.0.0.1:5000/`. You can view the interactive Swagger documentation at `http://127.0.0.1:5000/swagger`.

---

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/register`: Create a new user account.
- `POST /auth/login`: Authenticate and obtain JWT tokens.
- `POST /auth/refresh`: Rotate refresh token and obtain new access token.
- `POST /auth/forgot-password`: Request a password reset link (via email).
- `POST /auth/reset-password/<token>`: Reset password using the verification token.
- `POST /auth/logout`: Revoke active JWT tokens.
- `POST /auth/logout-all`: Invalidate all sessions/refresh tokens across all devices.

### User & Admin Operations (`/users`)
- `GET /users/me`: Retrieve current user profile.
- `PATCH /users/update`: Update user email and phone number.
- `PATCH /users/change-password`: Update account password (rate-limited).
- `GET /users`: List all users *(Moderator/Admin only)*.
- `PATCH /users/<user_id>/role`: Change a user's role *(Admin only)*.
- `DELETE /users/<user_id>`: Delete account *(User themselves or Admin)*.

---

## RBAC Permission Reference

Permissions are mapped to roles dynamically inside `app/utils/permissions.py`:

| Permission | User | Moderator | Admin | Description |
|---|:---:|:---:|:---:|---|
| `view_own_user` | ✓ | ✓ | ✓ | View self profile (`/users/me`) |
| `update_own_user` | ✓ | ✓ | ✓ | Update own data (`/users/update`) / change password |
| `delete_own_user` | ✓ | | ✓ | Delete own account |
| `view_all_users` | | ✓ | ✓ | View list of all users (`GET /users`) |
| `change_user_role`| | | ✓ | Modify user role (`PATCH /users/<id>/role`) |
| `delete_any_user` | | | ✓ | Delete another user's account |
