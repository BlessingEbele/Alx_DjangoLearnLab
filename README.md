# socail media api
# Social Media API Documentation

## Overview
The Social Media API is designed to provide essential functionality for a social networking platform. It allows users to register, authenticate, manage profiles, interact with posts, follow other users, and view a personalized feed. This documentation covers two core apps:

1. **Accounts**: Manages user authentication, profile information, and follow/unfollow functionality.
2. **Posts**: Handles post creation, retrieval, and dynamic feed generation.

---

## Accounts App

### Features
The Accounts app provides the following functionalities:

1. **User Authentication**:
   - User registration.
   - User login with token-based authentication (JWT).
   - User logout.

2. **User Profile Management**:
   - View and update profile information.

3. **Follow/Unfollow Functionality**:
   - Follow other users.
   - Unfollow users.
   - Retrieve the list of followers and users being followed.

### Endpoints

#### **Registration**
- **URL:** `/accounts/register/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "username": "string",
      "email": "string",
      "password": "string"
  }
  ```
- **Response:**
  ```json
  {
      "message": "User registered successfully.",
      "user": {
          "id": 1,
          "username": "string",
          "email": "string"
      }
  }
  ```

#### **Login**
- **URL:** `/accounts/login/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response:**
  ```json
  {
      "access": "JWT_ACCESS_TOKEN",
      "refresh": "JWT_REFRESH_TOKEN"
  }
  ```

#### **Profile Management**
- **URL:** `/accounts/profile/`
- **Methods:** `GET`, `PUT`
  - `GET`: Retrieve user profile information.
  - `PUT`: Update user profile details.

#### **Follow User**
- **URL:** `/accounts/follow/<int:user_id>/`
- **Method:** `POST`
- **Response:**
  ```json
  {
      "message": "You are now following <username>."
  }
  ```

#### **Unfollow User**
- **URL:** `/accounts/unfollow/<int:user_id>/`
- **Method:** `POST`
- **Response:**
  ```json
  {
      "message": "You have unfollowed <username>."
  }
  ```

#### **List Followers and Following**
- **URL:** `/accounts/<username>/followers/` (followers list)
- **URL:** `/accounts/<username>/following/` (following list)
- **Method:** `GET`
- **Response:**
  ```json
  [
      {
          "id": 2,
          "username": "user2",
          "email": "user2@example.com"
      }
  ]
  ```

---

## Posts App

### Features
The Posts app provides the following functionalities:

1. **Post Management**:
   - Create posts.
   - Retrieve all posts or posts by a specific user.
   - Delete user-owned posts.

2. **Feed Functionality**:
   - Display a feed of posts from followed users.

### Endpoints

#### **Create Post**
- **URL:** `/posts/create/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "content": "string"
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "author": "username",
      "content": "string",
      "created_at": "2024-12-12T10:00:00Z"
  }
  ```

#### **Retrieve Posts**
- **URL:** `/posts/all/`
- **Method:** `GET`
- **Response:**
  ```json
  [
      {
          "id": 1,
          "author": "username",
          "content": "string",
          "created_at": "2024-12-12T10:00:00Z"
      }
  ]
  ```

#### **Retrieve User Posts**
- **URL:** `/posts/user/<username>/`
- **Method:** `GET`
- **Response:**
  ```json
  [
      {
          "id": 1,
          "author": "username",
          "content": "string",
          "created_at": "2024-12-12T10:00:00Z"
      }
  ]
  ```

#### **Delete Post**
- **URL:** `/posts/delete/<int:post_id>/`
- **Method:** `DELETE`
- **Response:**
  ```json
  {
      "message": "Post deleted successfully."
  }
  ```

#### **User Feed**
- **URL:** `/posts/feed/`
- **Method:** `GET`
- **Response:**
  ```json
  [
      {
          "id": 1,
          "author": "user1",
          "content": "First post",
          "created_at": "2024-12-12T10:00:00Z"
      },
      {
          "id": 2,
          "author": "user2",
          "content": "Another post",
          "created_at": "2024-12-12T09:50:00Z"
      }
  ]
  ```

---

## Key Models

### CustomUser (Accounts)
Fields:
- `username`: Unique username.
- `email`: User email address.
- `following`: Many-to-Many field to represent user follow relationships.

### Post (Posts)
Fields:
- `author`: ForeignKey to the `CustomUser` model.
- `content`: Text field for the post content.
- `created_at`: DateTimeField for post creation timestamp.

---

## Testing
Use Postman to test endpoints:

1. Authenticate using `/accounts/login/` and include the `Authorization: Bearer <token>` header.
2. Test each endpoint by sending appropriate requests and verifying the responses.
3. Validate user follow relationships by viewing the `followers` and `following` lists.
4. Confirm the feed displays posts from followed users in descending order of creation.

---

## Future Enhancements
1. **Likes and Comments:** Add the ability to like and comment on posts.
2. **User Search:** Implement search functionality to find users by username.
3. **Media Support:** Enable uploading images and videos with posts.
4. **Notifications:** Notify users about new followers and interactions.

---

## Repository Structure

```
social_media_api/
|-- accounts/
|   |-- models.py
|   |-- views.py
|   |-- serializers.py
|   |-- urls.py
|
|-- posts/
|   |-- models.py
|   |-- views.py
|   |-- serializers.py
|   |-- urls.py
|
|-- social_media_api/
    |-- settings.py
    |-- urls.py
```

