Rails Microservice for Post Likes

## Overview
This project implements a microservice to handle "likes" for posts in a system that may involve pets or similar entities. It is built with Ruby on Rails and incorporates features like **WebSocket** for real-time updates using **ActionCable**. The service also supports JWT-based authentication for secure access to the like functionality.

### Architecture and Technologies:
- **Ruby on Rails**: Used for building the web application and backend API.
- **ActionCable**: Provides real-time WebSocket communication for live updates on likes.
- **PostgreSQL**: The database used to store posts and likes.
- **JWT Authentication**: For user authentication and securing API endpoints.
- **Redis**: Used as a backend for ActionCable to manage WebSocket connections in a production environment.

### Project Structure:
- `app/controllers`: Contains the `LikesController` responsible for handling the "like" logic.
- `app/channels`: Contains the WebSocket channel (`LikeChannel`) to broadcast like updates in real-time.
- `config/routes.rb`: Configures the routes, including Swagger documentation and POST request for liking posts.
- `config/puma.rb`: Configures the Puma web server to bind to port `7001` in both development and production environments.
- `app/javascript`: Contains the frontend JavaScript that manages WebSocket connections to update the UI in real-time.

## Installation

## Routes

### Like a Post
- **POST** `/posts/:post_id/likes`  
  - **Description**: Allows a user to like a specific post. It requires a valid JWT token for authentication.
  - **Request Body**: None (the `post_id` is passed in the URL).
  - **Response**:
    - `201 Created`: Successfully liked the post.
    - `422 Unprocessable Entity`: If the user has already liked the post.
    - `401 Unauthorized`: If the JWT token is invalid or not provided.

## Installation

### Prerequisites:
- Ruby (>= 3.1.2)
- Rails (>= 7.0.0)
- PostgreSQL
- Redis (for ActionCable in production)

### Steps:
**Clone the repository**:
```bash
git clone <repository_url>
cd <repository_folder>
```

**Install dependencies**:
```bash
bundle install
```

**Set up the database**:
Ensure PostgreSQL is running and set up the database for the project.
```bash
rails db:create
rails db:migrate
```

**Start the Redis server** (for ActionCable in production):
```bash
redis-server
```

**Start the Rails server**:
For development, run:
```bash
rails server -b '0.0.0.0' -p 7001
```

If using Docker:
```bash
docker-compose up
```

**Access the application**:
The application will be available at:
```plaintext
http://localhost:7001
```

**Swagger Documentation**:
To view and interact with the API documentation, visit:
```plaintext
http://localhost:7001/api-docs-like
```

### WebSocket Channel for Real-time Updates
- **Channel**: `LikeChannel`
  - **Subscription**: The client can subscribe to a channel based on the `post_id`. Whenever a user likes a post, all clients subscribed to that post will receive updates on the new likes count.

  Example:
  ```javascript
  const likeChannel = consumer.subscriptions.create(
    { channel: "LikeChannel", post_id: postId },
    {
      received(data) {
       
        document.getElementById(`likes-count-${postId}`).innerText = data.likes_count;
      }
    }
  );