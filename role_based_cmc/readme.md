
# Role-Based Content Management System (CMS)

This project provides an API for managing content with role-based access control using FastAPI and SQLAlchemy. It supports features like user management, role and permission handling, article creation and publishing, category and tag management, and commenting. The system includes Alembic for database migrations and an automatic database creation feature.


---

## Installation

### Step 1: Install Dependencies
Ensure that **Python 3.8+** is installed. Then, install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
---
## Database Initialization and Migrations
This project includes both **Alembic migrations** for managing database schema changes and a script to initialize default roles and the admin user. Follow these steps to set up your database with the correct schema and essential data.
### Step 1:Apply Alembic Migrations
Before running the initialization script, you need to apply the Alembic migrations to ensure the schema (tables, columns, etc.) is set up correctly in your database.

Run the following command to apply all migrations:
```bash
alembic upgrade head
```
This will apply any schema changes that are defined in your migration files, creating the necessary tables and structures based on your models.


### Step 2:Configure the Database
Ensure **PostgreSQL** is installed and configured on your system. You should also update your **settings.py** file with the correct database credentials.

- **Database Name**: cms_role_based
- ****User**:** postgres
- ****Password**:** root
- **Host:** localhost

### Step 3:Initialize the Database and Create Default Roles
After applying migrations, you can run the initialize.py script to create the default roles and admin user. This script will check if the database exists, create the necessary roles (Admin, Editor, Reader), and add a default admin user.

1. Navigate to the scripts/ directory where initialize.py is located.
2. Run the initialization script:
```bash
python scripts/initialize.py

```

### Step 4: What the Script Does
- **Database Creation**: The script checks if the database (cms_role_based) exists. If not, it creates the database.

- **Role Setup**: The script creates the following default roles:
   1. Admin
   2. Editor
   3. Author
   4. Reader
- **Admin User**: The script creates a default admin user with the following credentials:
   - Email: admin@example.com
   - Username: admin
   - Password: Admin@123
   - Role: Admin
The script will print messages indicating whether the database was created or if the roles and admin user were successfully initialized.

### Step 5: Verify Database and Users
You can verify that the database, roles, and users have been correctly initialized by connecting to your **PostgreSQL** database:
```bash
psql -h localhost -U postgres -d cms_role_based
```
Once connected, check the roles and users tables:

```sql
SELECT * FROM roles;
SELECT * FROM users;
```


## API Endpoints

### Authorization
- **POST** `/api/auth/login`: Login user.

### User Management
- **POST** `/api/users/register`.
- **GET** `/api/users/`: List all users (Admin only).
- **GET** `/api/users/{user_id}`: Get a specific user (Admin only).
- **PUT** `/api/users/{user_id}/role`: Update a user's role (Admin only).
- **PUT** `/api/users/{user_id}/approve`: Admin approves a user with the Author role.
### Role and Permission Management
- **POST** `/api/roles`: Create a role.
- **PUT** `/api/roles`: Update a role.
- **GET** `/api/roles`: Get all roles.
- **DELETE** `/api/roles/{role_id}`: Delete a role.

### Article Management
- **POST** `/api/articles/`: Create an article (Author only).
- **GET** `/api/articles/`: Get all articles (Admin/Editor only).
- **GET** `/api/articles/{article_id}`: Get a specific article (Admin/Editor only).
- **PUT** `/api/articles/{article_id}`: Update an article.
- **DELETE** `/api/articles/{article_id}`: Delete an article (Admin/Editor only).
- **PATCH** `/api/articles/{article_id}/status`: Update article status (Admin/Editor only).
- **PUT** `/api/articles/{article_id}/submit`: Submit an article for review (Author only).
- **PUT** `/api/articles/{article_id}/publish`: Publish an article (Admin/Editor only).
- **GET** `/api/articles/published`: Get all published articles (Readers).
- **GET** `/api/articles/search`: Search articles based on categories, tags, or keywords (Readers).
- **GET** `/api/articles/filter`: Filter articles by status, author, or creation date (Readers).

### Comments
- **POST** `/api/comments/{article_id}`: Add a comment to an article.
- **GET** `/api/comments/{article_id}`: Get comments for a specific article.
- **PUT** `/api/comments/comment/{comment_id}`: Update a comment.
- **DELETE** `/api/comments/{article_id}`: Delete a comment (Admin/Editor only).

### Categories
- **POST** `/api/categories/`: Create a category.
- **GET** `/api/categories/`: Get all categories.
- **GET** `/api/categories/{category_id}`: Get a specific category.
- **PUT** `/api/categories/{category_id}`: Update a category.
- **DELETE** `/api/categories/{category_id}`: Delete a category.
- **GET** `/api/categories/{category_id}/articles`: Get all articles associated with a category.

### Tags
- **POST** `/api/tags/`: Create a tag.
- **GET** `/api/tags/`: Get all tags.
- **DELETE** `/api/tags/{tag_id}`: Delete a tag.

---
## Register New User
- **POST** `/api/users/register`:

###  Allows users to register for the system with role-based restrictions. Roles like "Admin" and "Editor" cannot be self-assigned during registration.
### Request Payload:
```
{
  "username": "example_user",
  "email": "example_user@example.com",
  "password": "securepassword",
  "role": "Author"
}
```
### Behavior:
1. Role Validation: Users can only register with roles such as "Author" or "Reader." Attempting to register as "Admin" or "Editor" results in an error.
2. Approval for Authors: Users registering as "Author" are marked as inactive by default and require admin approval.

### Response:
- Successful Registration (Reader):
```angular2html
{
  "user": {
    "id": 1,
    "username": "example_user",
    "email": "example_user@example.com",
    "is_active": true,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z",
    "role": "Reader"
  },
  "message": "User registered successfully"
}
```
- Successful Registration (Author):
```angular2html
{
  "user": {
    "id": 2,
    "username": "example_author",
    "email": "example_author@example.com",
    "is_active": false,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z",
    "role": "Author"
  },
  "message": "Wait for the admin's approval to be able to enjoy the role's privileges"
}
```
### Error Responses:
- #### Restricted Role:
```angular2html
{
  "detail": "You cannot register for this role."
}

```
- #### Duplicate Email:
```angular2html
{
  "detail": "Email 'example_user@example.com' already exists"
}

```
- #### Duplicate Username:
```angular2html
{
  "detail": "Username 'example_user' already exists"
}

```
- #### Invalid Role:
```angular2html
{
  "detail": "Role 'InvalidRole' does not exist"
}

```
### Notes:
- Passwords are hashed using bcrypt for security.
- The registration process ensures that only valid roles are assigned to new users.
- Admin approval is required for "Author" accounts to activate.
---
## Authentication : 
### POST `/api/auth/login` : 
**This endpoint allows a user to log in using their username and password. Upon successful authentication, an access token will be issued, which can be used for subsequent requests requiring authentication.**
#### Request: 
- **Body:** A **LoginRequest** containing the username and password of the user:
```json
{
  "username": "user_example",
  "password": "user_password"
}
```
#### Response:
-Success: Upon successful login, the response will return an access token and the token type:
```json
{
  "access_token": "your_access_token_here",
  "token_type": "bearer"
}
```
- Error: If the credentials are invalid, a 401 Unauthorized status will be returned:
```json
{
  "detail": "Invalid credentials"
}

```
### Token Management
**After the user successfully logs in, an access token is created using JWT (JSON Web Token). This token is used for authentication in subsequent requests that require the user to be logged in.**

#### Token Creation:
**The create_access_token function creates a JWT token that encodes the user's username and role. The token expires after a specified period defined in the settings.**
 - Expiration: The token expires after a set period (default: 15 minutes) and needs to be refreshed or re-authenticated.

#### Token Verification:
To verify the token, use the verify_access_token function. It checks whether the token is valid and whether it has expired. If the token is invalid or expired, a 401 Unauthorized error is returned.

#### Revoke and Deactivate Tokens:
Tokens can be revoked by the admin or deactivated if expired. The UserTokenService provides methods to manage token deactivation and revocation.
* Revoke Token: Admin or authorized users can revoke a token to invalidate it manually.
* Deactivate Expired Tokens: Expired tokens are automatically deactivated to ensure that only active tokens are valid.

#### **Notes on Token Management:**
**Token Expiry: JWT tokens expire based on the configuration in the settings.py file. Ensure the expiration time is set properly.**





---
## Running Locally

1. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application using `uvicorn`:
   ```bash
   uvicorn main:app --reload
   ```

---

## Testing

To test the endpoints, use tools like **Postman** or **cURL**. Alternatively, you can access the interactive Swagger documentation at:
[http://localhost:8000/docs](http://localhost:8000/docs).

---

## Future Modifications

The following features and enhancements are planned for the future:
1. **Database Integration**:
   - Add a database to store users, roles, articles, comments, categories, and tags.
   - Use an ORM like SQLAlchemy to handle migrations and models.
2. **Enhanced Security**:
   - Implement JWT-based authentication for secure token generation and validation.
   - Ensure role-based permissions are strictly enforced.
3. **Full API Functionality**:
   - Ensure each API endpoint is fully functional with the database.
   - Improve the ability to filter, search, and sort data.
4. **Advanced Authorization**:
   - Add granular permission management for roles.
   - Allow admins to customize access levels for each role dynamically.

---