# Add-Like Microservice

## 1. Service Overview

The **Add-Like Microservice** is a specialized component within the pet social media platform that handles the addition of likes to posts. This microservice enables pet owners to express appreciation for posts made by other pets in the social network.

### Purpose
- **Primary Function**: Allows authenticated pet owners to add likes to posts through their pets
- **Business Logic**: Validates pet ownership, prevents duplicate likes, and maintains like counters
- **Event Driven**: Sends webhook notifications to trigger related actions (notifications, analytics, etc.)

### Microservice Interactions
- **Authentication Service**: Validates JWT tokens for user authentication
- **Pet Service**: Verifies pet ownership and retrieval of pet data
- **Post Service**: Validates post existence and updates like counters
- **Notification Service**: Receives webhook events when likes are added
- **Reactions Database**: Stores like records and manages reaction data

## 2. Routes and Endpoints

### POST /likes/add

**Description**: Adds a like to a specific post from a pet owned by the authenticated user.

**Authentication**: Required (Bearer JWT Token)

**Request Body**:
```json
{
  "postId": "123e4567-e89b-12d3-a456-426614174000",
  "petId": "987fcdeb-51a2-43d1-9f12-123456789abc"
}
```

**Response Examples**:

**Success (200)**:
```json
{
  "message": "Like added successfully"
}
```

**Error Responses**:

**Bad Request (400)** - Like already exists:
```json
{
  "detail": "Like already exists"
}
```

**Unauthorized (401)** - Invalid or missing token:
```json
{
  "detail": "Token expired"
}
```

**Forbidden (403)** - Pet ownership validation failed:
```json
{
  "detail": "Responsible does not own the pet trying to like"
}
```

**Not Found (404)** - Post doesn't exist:
```json
{
  "detail": "Post not found"
}
```

### cURL Example

```bash
curl -X POST "http://localhost:6001/likes/add" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "postId": "123e4567-e89b-12d3-a456-426614174000",
    "petId": "987fcdeb-51a2-43d1-9f12-123456789abc"
  }'
```

## 3. Internal Functionality

### Workflow Process

1. **Authentication Validation**: 
   - Extracts and validates JWT token from Authorization header
   - Decodes token to retrieve responsible (user) ID
   - Returns 401/403 for invalid/expired tokens

2. **Pet Ownership Verification**:
   - Queries Pet database to verify the pet belongs to the authenticated user
   - Prevents unauthorized likes from pets not owned by the user
   - Returns 403 if ownership validation fails

3. **Post Existence Check**:
   - Validates that the target post exists in the Post database
   - Returns 404 if post is not found

4. **Duplicate Like Prevention**:
   - Checks if a like already exists for the same post-pet combination
   - Returns 400 if like already exists to prevent duplicates

5. **Like Creation**:
   - Creates new Like record in Reactions database
   - Timestamps the like with UTC creation time
   - Uses UUID for unique identification

6. **Counter Update**:
   - Atomically increments the like counter on the target post
   - Ensures data consistency across databases

7. **Webhook Notification**:
   - Sends event notification to the Notification service
   - Enables real-time notifications and analytics tracking
   - Includes relevant metadata (postId, petId, responsibleId, timestamp)

### Database Interactions

- **Reactions Database**: Stores like records with relationships to posts and pets
- **Pet Database**: Validates pet ownership and retrieves pet information
- **Post Database**: Validates post existence and updates like counters

### Data Models

**Like Model**:
```python
class Like(Base):
    id: UUID           # Primary key
    postId: UUID       # Foreign key to Post
    petId: UUID        # Foreign key to Pet
    createdAt: DateTime # Timestamp
```

## 4. Technologies and Tools

### Core Technologies
- **Language**: Python 3.13
- **Framework**: FastAPI (v0.115.12)
- **ASGI Server**: Uvicorn (v0.34.3)
- **Database ORM**: SQLAlchemy (v2.0.41)
- **Database**: PostgreSQL (multiple databases)

### Key Dependencies
- **Authentication**: PyJWT (v2.10.1), python-jose (v3.5.0)
- **Database**: psycopg2-binary (v2.9.10) - PostgreSQL adapter
- **Validation**: Pydantic (v2.11.5) - Data validation and serialization
- **HTTP Client**: requests (v2.32.4) - For webhook notifications
- **Environment**: python-dotenv (v1.1.0) - Environment variable management
- **Testing**: pytest (v8.4.1) - Unit testing framework
- **Security**: passlib (v1.7.4), bcrypt (v4.3.0) - Password hashing utilities

### Cloud Services Integration
- **Redis**: Available for caching (v6.2.0)
- **Webhook Integration**: HTTP-based notification system
- **Multi-database Architecture**: Separate databases for pets, posts, and reactions

## 5. Authentication and Security

### JWT Authentication
- **Token Type**: Bearer tokens in Authorization header
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: Environment-based JWT secret key
- **Claims**: Contains `userId` mapped to `responsibleId`

### Security Features
- **CORS Configuration**: 
  - Allows all origins (configurable for production)
  - Supports credentials and all HTTP methods
  - Flexible header management

- **Input Validation**: 
  - Pydantic schemas validate all request data
  - UUID validation for postId and petId
  - Required field enforcement

- **Authorization Layers**:
  - Token validation (authentication)
  - Pet ownership verification (authorization)
  - Resource existence validation

### Security Best Practices
- Environment variable management for sensitive data
- Token expiration handling
- SQL injection prevention through ORM
- HTTPS-ready configuration

## 6. Configuration and Execution

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Database Names
PET_DB_NAME=pet_database
POST_DB_NAME=post_database
REACTIONS_DB_NAME=reactions_database

# Authentication
JWT_SECRET=your_jwt_secret_key

# Webhook Configuration
WEBHOOK_NOTIFICATIONS_URL=http://notification-service:8080/webhooks/likes
```

### Local Development Setup

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure Environment**:
```bash
# Copy and edit environment file
cp .env.example .env
# Edit .env with your configuration
```

3. **Database Setup**:
```bash
# Ensure PostgreSQL is running
# Create the required databases:
# - pet_database
# - post_database  
# - reactions_database
```

4. **Run the Service**:
```bash
# Development mode with auto-reload
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 6001 --reload
```

### Docker Deployment

1. **Build Image**:
```bash
docker build -t add-like-service .
```

2. **Run Container**:
```bash
docker run -p 6001:6003 --env-file .env add-like-service
```

### Service Configuration
- **Default Port**: 6001 (development), 6003 (Docker)
- **Host**: 0.0.0.0 (accepts connections from any IP)
- **Reload**: Enabled in development mode

## 7. Swagger Documentation

### Interactive API Documentation

The service provides comprehensive API documentation through Swagger UI:

- **Swagger UI**: `http://localhost:6001/api-docs-addLike`
- **OpenAPI Schema**: `http://localhost:6001/api-docs-likes/openapi.json`
- **ReDoc**: Disabled (set to None)

### API Features in Swagger
- **Interactive Testing**: Test endpoints directly from the browser
- **Request Examples**: Pre-filled examples for all endpoints
- **Response Schemas**: Detailed response structure documentation
- **Authentication Testing**: Built-in Bearer token input
- **Error Code Documentation**: Complete HTTP status code reference

### Accessing Documentation
1. Start the service locally
2. Navigate to `http://localhost:6001/api-docs-addLike`
3. Use the "Authorize" button to input your JWT token
4. Test the `/likes/add` endpoint with sample data

## 8. Testing and Coverage

### Test Structure

The service includes automated tests for critical functionality:

**Test Files**:
- `tests/test_connections.py` - Environment and connection validation

### Test Categories

1. **Environment Tests**:
   - Validates `.env` file existence
   - Checks required environment variables
   - Verifies application importability

2. **Required Environment Variables**:
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`
   - `PET_DB_NAME`, `POST_DB_NAME`, `REACTIONS_DB_NAME`
   - `DB_PORT`, `JWT_SECRET`

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_connections.py

# Run with coverage report
pytest --cov=. --cov-report=html
```

### Test Development Guidelines
- Add integration tests for like creation workflow
- Include authentication middleware tests
- Test database connection handling
- Validate webhook notification functionality

## 9. Contribution Guidelines

### Development Process

1. **Fork the Repository**:
   ```bash
   git clone <repository-url>
   cd add-like
   ```

2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Development Environment**:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Configure your .env file
   ```

4. **Make Changes**:
   - Follow PEP 8 style guidelines
   - Add comprehensive docstrings
   - Include type hints where appropriate
   - Write tests for new functionality

5. **Test Your Changes**:
   ```bash
   pytest
   python app.py  # Ensure service starts correctly
   ```

6. **Commit and Push**:
   ```bash
   git add .
   git commit -m "feat: descriptive commit message"
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**:
   - Provide clear description of changes
   - Include test results
   - Reference any related issues

### Code Standards
- **Style**: Follow PEP 8 Python style guide
- **Documentation**: Include docstrings for all functions and classes
- **Testing**: Maintain test coverage above 80%
- **Security**: Never commit sensitive data (secrets, passwords)

### Local Testing Checklist
- [ ] All tests pass (`pytest`)
- [ ] Service starts without errors
- [ ] API documentation loads correctly
- [ ] Environment variables are properly configured
- [ ] Database connections work correctly

## 10. License

### MIT License

```
MIT License

Copyright (c) 2025 Pet Social Media Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Usage Rights
- **Commercial Use**: ✅ Permitted
- **Modification**: ✅ Permitted
- **Distribution**: ✅ Permitted
- **Private Use**: ✅ Permitted

### Conditions
- **License and Copyright Notice**: Must be included in all copies
- **Changes**: Changes must be documented

### Additional Information
- **Warranty**: No warranty provided
- **Liability**: Authors not liable for damages
- **Trademark**: No trademark rights granted

---

## Quick Start Example

```bash
# 1. Clone and setup
git clone <repository-url>
cd add-like
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your database and JWT settings

# 3. Start service
python app.py

# 4. Test with curl
curl -X POST "http://localhost:6001/likes/add" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"postId": "123e4567-e89b-12d3-a456-426614174000", "petId": "987fcdeb-51a2-43d1-9f12-123456789abc"}'
```

---

**Documentation Version**: 1.0.0  
**Last Updated**: June 28, 2025  
**Service Version**: 1.0.0