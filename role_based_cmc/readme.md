
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
- **GET** `/api/users/inactive/` : Get all users who have the role (author) and are waiting for activation from the admin
- **PUT** `/api/users/{user_id}/active/`: Admin approves a user with the Author role.
### Role and Permission Management
- **GET** `/api/roles`: Get all roles.
- **GET** `/api/roles/{role_id}/users/`: Get role with users.

### Article Management
- **POST** `/api/articles/`: Create an article (Author only).
- **GET** `/api/articles/`: Get all articles (Admin/Editor only).
- **GET** `/api/articles/{article_id}`: Get a specific article (Admin/Editor only).
- **PUT** `/api/articles/{article_id}`: Update an article.
- **DELETE** `/api/articles/{article_id}`: Delete an article (Admin/Editor only).
- **PATCH** `/api/articles/{article_id}/status`: Update article status (Admin/Editor only).
- **PUT** `/api/articles/{article_id}/publish`: Publish an article (Admin/Editor only).

### Author 
- **GET** `/api/authors/articles/`: Get all articles(Author)
- **PUT** `/api/authors/articles/{article_id}/submit`: Submit Article for Review

### Reader
- **GET** `/api/readers/article/all-published`: Get All Published Article
- **GET** `/api/readers/article/search` Search Articles
- **GET** `/api/readers/article/filter` Filter Articles 

### Comments
- **POST** `/api/comments/{article_id}`: Add a comment to an article.
- **GET** `/api/comments/{article_id}`: Get comments for a specific article.
- **PUT** `/api/comments/comment/{comment_id}`: Update a comment (Admin/Editor only).
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
# Middleware Security 
## Overview
**The application uses JWT (JSON Web Token) middleware to secure API endpoints. This middleware verifies tokens in request headers, authenticates users, and enforces role-based access control (RBAC).**


### JWT Middleware
The JWTMiddleware class ensures secure communication by:
1. Public Path Handling: Bypassing authentication for specified public endpoints.
2. Token Verification: Validating tokens to check their authenticity and expiration status.
3. User Context: Extracting user information from tokens and making it available in the request state.
```python
class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, public_paths: list[str] = None):
        self.public_paths = public_paths or []
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.public_paths:
            return await call_next(request)
        try:
            db = next(get_db())
            user_token_service = UserTokenService(db=db)
            payload = verify_access_token(request, user_token_service)
            request.state.user = payload
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
```
### Role-Based Access Control
RBAC is enforced via the **require_role** function, ensuring that only users with specific roles can access certain endpoints.

```python
def require_role(allowed_roles: list):
    def role_checker(request: Request):
        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized: No user data found")
        user_role = user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient role permissions")

    return role_checker
```
#### Example Endpoint with Role-Based Access
The following endpoint demonstrates how to restrict access to users with "Admin," "Editor," or "Author" roles:
```python
@router.post(
    "/",
    response_model=ArticleResponse,
    summary="Create an Article (Author)",
    description="Allows authors to create a new article with a default status of 'Draft'.",
    dependencies=[Depends(require_role(["Admin", "Editor", "Author"]))],
)

```
## Key Features
1. Global Middleware Security: Secures all API endpoints unless explicitly added to the public_paths.
2. Role-Based Control: Ensures endpoint access is limited to users with sufficient permissions.
3. Error Handling: Provides meaningful error messages (401 for unauthorized access, 403 for insufficient roles).
4. Configurable Paths: Specify public paths to allow unauthenticated access where necessary.




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

## Development Notes:
### Security
* Passwords are hashed using bcrypt for storage security.
* Authentication and authorization are handled using JWT tokens.
* The system ensures role-based restrictions for each endpoint to maintain secure access to resources.

### Middleware
The API uses middleware to enforce authentication and validate permissions. Each role has specific capabilities, ensuring a robust access control mechanism.

### Testing
To test the API, use tools like Postman or curl. Ensure that a valid JWT token is included in the Authorization header for requests that require authentication.



---