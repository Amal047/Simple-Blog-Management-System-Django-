# Simple-Blog-Management-System-Django-

Implement a secure login system using session-based authentication. Build a Blog Post Management module with the following capabilities Create a blog post with: Title, Content, Image upload, Tag input (as a comma-separated string or related model) Edit an existing blog post Delete a blog post List all posts in a table with pagination

# Simple Blog Management System (Django)

A web-based blog management system built with Django that allows users to register, create, edit, and delete blog posts. Admin users have additional privileges including managing users and revoking blog posts.

## Features

### 🔐 Authentication

- User registration with email-based OTP verification
- Secure login and logout
- Admin and regular user role separation

### 📝 Blog Management

- Create, edit, and delete personal blog posts
- View all blog posts on the homepage with pagination
- Admins can revoke (delete) any user's post

### 🧑‍💼 Admin Dashboard

- View all registered users and their details
- View all blog posts across users
- Delete non-admin users (with confirmation and self-deletion protection)

### 👤 User Dashboard

- Personalized dashboard listing all posts by the logged-in user
- Update personal information with optional password change

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/blogSystem.git
   cd blogSystem
   ```

Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate # or `venv\Scripts\activate` on Windows

Install Dependencies
pip install -r requirements.txt

Apply Migrations
python manage.py migrate

Create Superuser
python manage.py createsuperuser

Run the Server
python manage.py runserver

Notes
Replace your-email@gmail.com in views.py with your actual email or configure a proper email backend for production.

Ensure CSRF protection is enabled on forms (already included).

User deletion and post revocation actions require confirmation.

## SuperUser details:

# username:admin

# password:adminadmin
