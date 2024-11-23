
# Role-Based Content Management System (CMS)

This project provides an API for managing content with role-based access control using FastAPI and SQLAlchemy. It supports features like user management, role and permission handling, article creation and publishing, category and tag management, and commenting. The system includes Alembic for database migrations and an automatic database creation feature.


---

## Installation

### Step 1: Install Dependencies
Ensure that **Python 3.8+** is installed. Then, install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
### Step 2: Configure the Database
The project uses **PostgreSQL** as the database. Make sure **PostgreSQL** is installed and configured. The database details are as follows:

- **Database Name**:  cms_role_based
- **User**: postgres
- **Password**: root
- **Host**: localhost

If the database does not exist, it will be created automatically when the application starts.
## Database Initialization Script
The script automatically creates the database cms_role_based if it doesn't exist:

``` 
import psycopg2

DATABASE_URL = "postgresql://postgres:root@localhost/cms_role_based"

def create_database_if_not_exists():
    try:
        connection = psycopg2.connect(
            dbname="postgres", user="postgres", password="root", host="localhost"
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'cms_role_based'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE cms_role_based")
            print("Database created successfully.")
        else:
            print("Database already exists.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while creating the database: {e}")

```
 

### Step 3: Run Alembic Migrations 
To apply database migrations:
```bash
alembic upgrade head
```
This will create the required tables for the application.


### Step 4: Start the FastAPI Application
Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at: [http://localhost:8000](http://localhost:8000).

---

## API Endpoints

### Authorization
- **POST** `/api/auth/login`: Login user.
- **POST** `/api/auth/register`: Register a new user.

### User Management
- **GET** `/api/users/`: List all users (Admin only).
- **GET** `/api/users/{user_id}`: Get a specific user (Admin only).
- **PUT** `/api/users/{user_id}/role`: Update a user's role (Admin only).

### Role and Permission Management
- **POST** `/api/roles`: Create a role.
- **PUT** `/api/roles`: Update a role.
- **GET** `/api/roles`: Get all roles.
- **DELETE** `/api/roles/{role_id}`: Delete a role.
- **PUT** `/api/roles/{role_id}/permissions`: Assign permissions to a role.
- **DELETE** `/api/roles/{role_id}/permissions`: Remove permissions from a role.
- **GET** `/api/permissions`: Get all available permissions (Admin only).

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