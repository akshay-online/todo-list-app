# Login System Documentation

## Overview
This implementation adds a complete authentication system to the todo-list-app using React frontend with Tailwind CSS and Flask backend with SQL Server database support.

## Features Implemented

### 📱 Frontend (React + Tailwind CSS)
- **Login Screen**: Clean, responsive design with username and password fields
- **Forgot Password**: Email-based password reset functionality
- **Form Validation**: Client-side validation with loading states
- **Error Handling**: User-friendly error messages and success notifications
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS

### 🚀 Backend (Flask + SQL Server)
- **Authentication API**: RESTful endpoints for login, registration, and password reset
- **Password Security**: Bcrypt hashing for secure password storage
- **JWT Tokens**: Secure token-based authentication
- **Database Models**: User and Task models with SQLAlchemy ORM
- **SQL Server Support**: Configurable database connection (SQLite for dev, SQL Server for production)

## API Endpoints

### Authentication
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/forgot-password` - Password reset request
- `POST /api/auth/reset-password` - Password reset with token
- `POST /api/auth/verify-token` - JWT token verification

### Tasks (Legacy + New API)
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create new task
- `DELETE /api/tasks/<id>` - Delete task

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- SQL Server (for production) or SQLite (for development)

### Backend Setup
1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure database (optional for production):
   ```bash
   export SQL_SERVER_CONNECTION="mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server"
   ```

4. Run Flask application:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   ```

## Configuration

### Environment Variables
- `SECRET_KEY`: JWT signing key (required for production)
- `SQL_SERVER_CONNECTION`: SQL Server connection string (optional, defaults to SQLite)

### Default Users
The system creates a default admin user on first run:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

## Security Features
- ✅ Password hashing using bcrypt
- ✅ JWT token authentication
- ✅ CORS protection
- ✅ Input validation
- ✅ Password reset token expiration (1 hour)
- ✅ Secure token generation

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reset_token VARCHAR(100),
    reset_token_expires DATETIME
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    user_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## Usage

### Login
1. Navigate to `http://localhost:3000`
2. Enter username and password
3. Click "Sign in"
4. Receive JWT token for authenticated requests

### Forgot Password
1. Click "Forgot your password?" link
2. Enter email address
3. Click "Reset Password"
4. Check server logs for reset token (in production, this would be sent via email)

### Password Reset
Use the `/api/auth/reset-password` endpoint with the token from the forgot password process.

## Production Deployment

### SQL Server Configuration
1. Install SQL Server ODBC driver
2. Set the `SQL_SERVER_CONNECTION` environment variable
3. Update connection string format as needed

### Security Considerations
1. Set a strong `SECRET_KEY` environment variable
2. Use HTTPS in production
3. Configure proper CORS settings
4. Implement email service for password resets
5. Add rate limiting for authentication endpoints

## Testing
- Frontend: `npm test` (in frontend directory)
- Backend: Tests can be added using pytest
- Integration: Use the provided default admin credentials for testing