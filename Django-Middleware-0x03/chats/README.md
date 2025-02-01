To test the API endpoints using Postman, follow the instructions below to create a Postman collection and ensure the proper functionality of your API for creating conversations, sending messages, and fetching conversations while also testing JWT authentication and access control for private conversations.

### Step 1: **Set Up Postman Collection**
Create a Postman collection for your API endpoints to streamline testing.

1. **Open Postman**.
2. **Create a new Collection**:
    - In Postman, click on the **Collections** tab.
    - Click the **New Collection** button.
    - Name it something like `Messaging API`.

3. **Set Up Authentication for All Requests**:
    - In your Postman collection, add an **Authorization** tab with **Bearer Token** as the authentication type.
    - You'll need to set the JWT token dynamically for each request.

---

### Step 2: **Test Authentication (JWT Token Login)**

1. **Test Login and Obtain JWT Token**:
    - URL: `POST /api/token/`
    - **Request Body** (JSON format):
      ```json
      {
        "username": "your_username",
        "password": "your_password"
      }
      ```
    - **Response**:
      - The response should include the `access` and `refresh` tokens:
      ```json
      {
        "access": "your_access_token",
        "refresh": "your_refresh_token"
      }
      ```

2. **Use JWT Token for Authentication**:
    - For subsequent requests, use the `access` token received from this step.
    - Add it in the **Authorization** tab of Postman for each request as **Bearer Token**.

---

### Step 3: **Test Creating a Conversation (POST Request)**

1. **Create a Conversation**:
    - **URL**: `POST /api/chats/conversations/create/`
    - **Authorization**: Use the JWT token in the **Authorization** tab as **Bearer Token**.
    - **Request Body** (JSON format):
      ```json
      {
        "participants": ["user_id_1", "user_id_2"]
      }
      ```
      Replace `"user_id_1"` and `"user_id_2"` with actual user IDs.

    - **Response**:
      The response should contain the newly created conversation's data:
      ```json
      {
        "id": 1,
        "participants": [
          {"id": 1, "email": "user1@example.com"},
          {"id": 2, "email": "user2@example.com"}
        ],
        "created_at": "2024-12-23T12:00:00Z"
      }
      ```

---

### Step 4: **Test Sending a Message (POST Request)**

1. **Send a Message to the Conversation**:
    - **URL**: `POST /api/chats/messages/`
    - **Authorization**: Use the JWT token in the **Authorization** tab as **Bearer Token**.
    - **Request Body** (JSON format):
      ```json
      {
        "conversation_id": 1,
        "message_body": "Hello, this is a test message."
      }
      ```

    - **Response**:
      The response should contain the message data:
      ```json
      {
        "id": 1,
        "conversation": 1,
        "sender": {"id": 1, "email": "user1@example.com"},
        "message_body": "Hello, this is a test message.",
        "timestamp": "2024-12-23T12:05:00Z"
      }
      ```

---

### Step 5: **Test Fetching Conversations (GET Request)**

1. **Fetch Conversations for Authenticated User**:
    - **URL**: `GET /api/chats/conversations/`
    - **Authorization**: Use the JWT token in the **Authorization** tab as **Bearer Token**.
    - **Response**:
      This should return a list of conversations the user is a part of. For example:
      ```json
      [
        {
          "id": 1,
          "participants": [
            {"id": 1, "email": "user1@example.com"},
            {"id": 2, "email": "user2@example.com"}
          ],
          "created_at": "2024-12-23T12:00:00Z"
        }
      ]
      ```

---

### Step 6: **Test Fetching Messages in a Conversation (GET Request)**

1. **Fetch Messages for a Conversation**:
    - **URL**: `GET /api/chats/messages/`
    - **Authorization**: Use the JWT token in the **Authorization** tab as **Bearer Token**.
    - **Request Params**:
      - `conversation_id=1`
    - **Response**:
      The response should return a list of messages in the specified conversation:
      ```json
      [
        {
          "id": 1,
          "conversation": 1,
          "sender": {"id": 1, "email": "user1@example.com"},
          "message_body": "Hello, this is a test message.",
          "timestamp": "2024-12-23T12:05:00Z"
        }
      ]
      ```

---

### Step 7: **Test Unauthorized Access (GET Request)**

1. **Access without JWT Token**:
    - **URL**: `GET /api/chats/conversations/`
    - **Response**:
      The server should return a `401 Unauthorized` error if no token or an invalid token is provided.
      ```json
      {
        "detail": "Authentication credentials were not provided."
      }
      ```

2. **Access with Invalid JWT Token**:
    - **URL**: `GET /api/chats/conversations/`
    - **Authorization**: Provide an invalid JWT token in the **Authorization** tab.
    - **Response**:
      The server should return a `401 Unauthorized` error:
      ```json
      {
        "detail": "Token is invalid or expired."
      }
      ```

---

### Step 8: **Test Participant Permissions (Authorization Check)**

1. **Non-Participant Trying to Access Conversation**:
    - **URL**: `GET /api/chats/messages/`
    - **Authorization**: Use a JWT token from a user who is **not a participant** of the conversation.
    - **Request Params**:
      - `conversation_id=1`
    - **Response**:
      The response should be a `403 Forbidden` error:
      ```json
      {
        "detail": "You do not have permission to access this conversation."
      }
      ```

---

### Step 9: **Create a Postman Collection File**

After testing all endpoints, export the Postman collection for future use:

1. **Export the Collection**:
    - In Postman, click the three dots on your collection.
    - Select **Export**.
    - Choose the **Collection v2.1** format and click **Export**.
    - Save the collection as a `.json` file.

2. **Upload the Postman Collection**:
    - Upload the exported Postman collection to your GitHub repository, typically under the `messaging_app/postman-Collections` directory.

---

### Summary of Tests

- **JWT Authentication**: Ensure you can login using valid credentials and get a JWT token.
- **Creating a Conversation**: Test creating a conversation by providing participants.
- **Sending Messages**: Test sending a message in an existing conversation.
- **Fetching Conversations**: Test fetching conversations the authenticated user is a participant of.
- **Fetching Messages**: Test fetching messages from a specific conversation.
- **Unauthorized Access**: Ensure that unauthorized users cannot access private conversations.
- **Participant Permissions**: Ensure only participants of a conversation can access it.

By following the above steps, you can test your messaging app API effectively with Postman and ensure that everything is working as expected.
