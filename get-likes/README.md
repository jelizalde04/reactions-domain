# Get-Likes Microservice

## 1. Service Overview

The **Get-Likes Microservice** is a specialized component within the pet social media platform that handles the retrieval and display of like information for posts. This microservice provides both REST API and GraphQL endpoints to query like data, featuring Redis caching for optimal performance and detailed like analytics.

### Purpose
- **Primary Function**: Retrieves like counts and detailed like information for posts
- **Performance Optimization**: Implements Redis caching for frequently accessed like counts
- **Dual API Support**: Provides both REST and GraphQL interfaces for flexible data access
- **Analytics Ready**: Returns detailed like records for analytics and reporting

### Microservice Interactions
- **Post Service**: Validates post existence and retrieves post data
- **Reactions Database**: Queries like records and detailed reaction data
- **Redis Cache**: Stores frequently accessed like counts for performance
- **GraphQL Clients**: Supports modern frontend frameworks with GraphQL queries

## 2. Routes and Endpoints

### GET /likes/{postId}

**Description**: Retrieves comprehensive like information for a specific post, including total count and detailed like records.

**Authentication**: Not Required (Public endpoint)

**Path Parameters**:
- `postId` (string): UUID of the post to retrieve like information for

**Response Example**:

**Success (200)**:
```json
{
  "postId": "123e4567-e89b-12d3-a456-426614174000",
  "likes_count": 5,
  "likes_details": [
    {
      "likeId": "a62731bf-1148-48d7-aa29-9e7c4667be87",
      "postId": "123e4567-e89b-12d3-a456-426614174000",
      "petId": "b35beaad-f5fd-4a77-bf68-9dbca72b36f2",
      "createdAt": "2025-06-27T10:30:00"
    },
    {
      "likeId": "c73842ca-2259-59e8-bb3a-0e8d5778cf98",
      "postId": "123e4567-e89b-12d3-a456-426614174000",
      "petId": "d46953db-3360-60f9-cc4b-1f9e6889d0a9",
      "createdAt": "2025-06-27T11:15:00"
    }
  ]
}
```

**Error Responses**:

**Not Found (404)** - Post doesn't exist:
```json
{
  "detail": "Post not found"
}
```

### GraphQL Endpoint

**Endpoint**: `POST /graphql`

**Description**: Provides GraphQL access to like count information with flexible querying capabilities.

**GraphQL Query Example**:
```graphql
query GetLikesCount($postId: String!) {
  likesCount(postId: $postId) {
    postId
    likesCount
  }
}
```

**Variables**:
```json
{
  "postId": "123e4567-e89b-12d3-a456-426614174000"
}
```

**GraphQL Response**:
```json
{
  "data": {
    "likesCount": {
      "postId": "123e4567-e89b-12d3-a456-426614174000",
      "likesCount": 5
    }
  }
}
```

### cURL Examples

**REST API**:
```bash
curl -X GET "http://localhost:6003/likes/123e4567-e89b-12d3-a456-426614174000" \
  -H "Content-Type: application/json"
```

**GraphQL API**:
```bash
curl -X POST "http://localhost:6003/graphql" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query GetLikesCount($postId: String!) { likesCount(postId: $postId) { postId likesCount } }",
    "variables": { "postId": "123e4567-e89b-12d3-a456-426614174000" }
  }'
```

## 3. Internal Functionality

### Workflow Process

1. **Post Validation**: 
   - Queries Post database to verify the post exists
   - Returns 404 if post is not found

2. **Cache Check (Performance Optimization)**:
   - Checks Redis cache for like count using key `post:{postId}:likes_count`
   - If cached, returns cached value (60-second TTL)
   - If not cached, proceeds to database query

3. **Database Query**:
   - Retrieves like count from Post table
   - Caches the result in Redis for future requests
   - Queries all Like records for detailed information

4. **Data Formatting**:
   - Formats like records with comprehensive details
   - Converts timestamps to ISO format
   - Structures response for both REST and GraphQL consumption

5. **Response Generation**:
   - Returns combined like count and detailed like records
   - Supports different response formats (REST vs GraphQL)

### Caching Strategy

- **Cache Key Pattern**: `post:{postId}:likes_count`
- **TTL (Time To Live)**: 60 seconds
- **Cache Invalidation**: Automatic expiration (can be extended with cache invalidation on like add/remove)
- **Performance Benefit**: Reduces database load for frequently accessed posts

### Database Interactions

- **Post Database**: Validates post existence and retrieves like counts
- **Reactions Database**: Queries detailed like records with pet and timestamp information
- **Redis Cache**: Stores and retrieves cached like counts

### Data Models

**Like Detail Model**:
```python
class LikeDetail(BaseModel):
    likeId: UUID           # Unique like identifier
    postId: UUID           # Post being liked
    petId: UUID            # Pet that liked the post
    createdAt: Optional[datetime]  # When like was created
```

**Response Model**:
```python
class LikeListResponse(BaseModel):
    postId: UUID                    # Target post
    likes_count: int               # Total like count
    likes_details: List[LikeDetail] # Detailed like records
```

## 4. Technologies and Tools

### Core Technologies
- **Language**: Python 3.13
- **Framework**: FastAPI (v0.115.12)
- **ASGI Server**: Uvicorn (v0.34.3)
- **Database ORM**: SQLAlchemy (v2.0.41)
- **Database**: PostgreSQL (multiple databases)
- **Cache**: Redis (v6.2.0)
- **GraphQL**: Strawberry GraphQL (v0.275.5)

### Key Dependencies
- **Authentication**: PyJWT (v2.10.1), python-jose (v3.5.0) - Available for future auth needs
- **Database**: psycopg2-binary (v2.9.10) - PostgreSQL adapter
- **Validation**: Pydantic (v2.11.5) - Data validation and serialization
- **Caching**: redis (v6.2.0) - Redis client for Python
- **GraphQL**: strawberry-graphql (v0.275.5) - Modern GraphQL library
- **Environment**: python-dotenv (v1.1.0) - Environment variable management
- **Testing**: pytest (v8.4.1) - Unit testing framework

### Architecture Features
- **Multi-database Architecture**: Separate databases for pets, posts, and reactions
- **Dual API Support**: REST and GraphQL endpoints in the same service
- **Caching Layer**: Redis integration for performance optimization
- **Type Safety**: Full Pydantic and Strawberry type definitions

## 5. Authentication and Security

### Current Authentication Status
- **Public Endpoints**: Currently no authentication required for read operations
- **Future Authentication**: JWT middleware available for future implementation
- **Security Ready**: Bearer token infrastructure in place

### Security Features
- **CORS Configuration**: 
  - Allows all origins (configurable for production)
  - Supports credentials and all HTTP methods
  - Flexible header management

- **Input Validation**: 
  - Pydantic schemas validate all request data
  - UUID validation for postId parameters
  - Type-safe GraphQL schema definitions

- **Data Protection**:
  - Read-only operations prevent data modification
  - No sensitive data exposure in like information
  - UUID-based resource identification

### Security Best Practices
- Environment variable management for sensitive data
- SQL injection prevention through ORM
- HTTPS-ready configuration
- Prepared for authentication integration

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

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Authentication (for future use)
JWT_SECRET=your_jwt_secret_key
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

4. **Redis Setup**:
```bash
# Install and start Redis server
# Ubuntu/Debian: sudo apt install redis-server
# macOS: brew install redis
# Windows: Download from https://redis.io/download

# Start Redis server
redis-server
```

5. **Run the Service**:
```bash
# Development mode with auto-reload
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 6003 --reload
```

### Docker Deployment

1. **Build Image**:
```bash
docker build -t get-likes-service .
```

2. **Run with Docker Compose** (recommended):
```yaml
version: '3.8'
services:
  get-likes:
    build: .
    ports:
      - "6003:6001"
    environment:
      - DB_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

3. **Run Container**:
```bash
docker run -p 6003:6001 --env-file .env get-likes-service
```

### Service Configuration
- **Default Port**: 6003 (development), 6001 (Docker)
- **Host**: 0.0.0.0 (accepts connections from any IP)
- **Reload**: Enabled in development mode

## 7. Swagger Documentation

### Interactive API Documentation

The service provides comprehensive API documentation through Swagger UI:

- **Swagger UI**: `http://localhost:6003/api-docs-getLikes`
- **OpenAPI Schema**: `http://localhost:6003/api-docs-getLikes/openapi.json`
- **GraphQL Playground**: `http://localhost:6003/graphql` (Interactive GraphQL IDE)
- **ReDoc**: Disabled (set to None)

### API Features in Swagger
- **Interactive Testing**: Test REST endpoints directly from the browser
- **Request Examples**: Pre-filled examples for all endpoints
- **Response Schemas**: Detailed response structure documentation
- **Error Code Documentation**: Complete HTTP status code reference

### GraphQL Features
- **Interactive Playground**: Test GraphQL queries with syntax highlighting
- **Schema Introspection**: Explore available queries and types
- **Query Validation**: Real-time query validation and suggestions
- **Documentation**: Auto-generated documentation from schema

### Accessing Documentation
1. Start the service locally
2. **REST API**: Navigate to `http://localhost:6003/api-docs-getLikes`
3. **GraphQL API**: Navigate to `http://localhost:6003/graphql`
4. Test the endpoints with sample post IDs

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
- Add integration tests for like retrieval workflow
- Include Redis caching tests
- Test GraphQL query functionality
- Validate response formatting
- Test error scenarios (non-existent posts)
- Performance tests for cached vs non-cached requests

## 9. Contribution Guidelines

### Development Process

1. **Fork the Repository**:
   ```bash
   git clone <repository-url>
   cd get-likes
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

4. **Start Dependencies**:
   ```bash
   # Start Redis server
   redis-server
   
   # Ensure PostgreSQL is running
   ```

5. **Make Changes**:
   - Follow PEP 8 style guidelines
   - Add comprehensive docstrings
   - Include type hints where appropriate
   - Write tests for new functionality
   - Update GraphQL schema if needed

6. **Test Your Changes**:
   ```bash
   pytest
   python app.py  # Ensure service starts correctly
   # Test both REST and GraphQL endpoints
   ```

7. **Commit and Push**:
   ```bash
   git add .
   git commit -m "feat: descriptive commit message"
   git push origin feature/your-feature-name
   ```

8. **Create Pull Request**:
   - Provide clear description of changes
   - Include test results
   - Reference any related issues

### Code Standards
- **Style**: Follow PEP 8 Python style guide
- **Documentation**: Include docstrings for all functions and classes
- **Testing**: Maintain test coverage above 80%
- **Security**: Never commit sensitive data (secrets, passwords)
- **GraphQL**: Follow GraphQL schema design best practices

### Local Testing Checklist
- [ ] All tests pass (`pytest`)
- [ ] Service starts without errors
- [ ] REST API documentation loads correctly
- [ ] GraphQL playground works correctly
- [ ] Redis connection is functional
- [ ] Environment variables are properly configured
- [ ] Both API endpoints return correct responses

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
cd get-likes
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your database and Redis settings

# 3. Start Redis (if not running)
redis-server

# 4. Start service
python app.py

# 5. Test REST API
curl -X GET "http://localhost:6003/likes/123e4567-e89b-12d3-a456-426614174000"

# 6. Test GraphQL API
curl -X POST "http://localhost:6003/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { likesCount(postId: \"123e4567-e89b-12d3-a456-426614174000\") { postId likesCount } }"}'
```

---

## Key Features Summary

- **Dual API Support**: Both REST and GraphQL endpoints
- **Redis Caching**: 60-second TTL for like counts
- **Detailed Analytics**: Complete like records with timestamps
- **High Performance**: Optimized for read-heavy workloads
- **Type Safety**: Full Pydantic and Strawberry type definitions
- **Public Access**: No authentication required for read operations
- **Interactive Documentation**: Swagger UI and GraphQL Playground

---

## Performance Considerations

- **Caching Strategy**: Redis caching reduces database load by up to 90%
- **Database Optimization**: Separate queries for counts vs. details
- **Connection Pooling**: SQLAlchemy connection management
- **Async Ready**: FastAPI foundation supports async operations
- **Scalability**: Stateless design enables horizontal scaling

---

**Documentation Version**: 1.0.0  
**Last Updated**: June 28, 2025  
**Service Version**: 1.0.0
