# Social Networking API

## Overview

This project is a scalable, secure, and efficient social networking application built using Django Rest Framework. 
It provides users with the ability to manage friend requests, search for users, and maintain user activities, including notifications for significant events such as friend requests sent and accepted. 
The application implements robust security and performance optimization measures.

## Features

- **User Authentication**: Sign up and login using JWT token-based authentication.
- **User Search**: Search for users by email or name with pagination.
- **Friend Request Management**: Send, accept, and reject friend requests with rate limiting.
- **Friends List**: Retrieve a list of friends with optimized queries.
- **Pending Friend Requests**: View received friend requests with pagination.
- **User Activity Logging**: Track user activities such as sent or accepted friend requests.
- **Blocking Users**: Prevent users from sending friend requests or viewing profiles.
- **Caching**: Utilize Django's built-in cache framework to optimize performance.

## Technologies Used

- Django
- Django Rest Framework
- MySQL
- Django caching
- JWT for Authentication

## Requirements

- Python 3.8 or higher
- MySQL

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/Rajraut7719/social-networking-app.git
cd social-networking-app
```
### Step 2: Create a virtual environment
Create a virtual environment in the project directory:
```bash
python -m venv .venv
```
### Step 3: Activate the virtual environment
**On Windows:**
```bash
.\.venv\Scripts\activate
```
**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Set up the environment
Create a .env file in the root directory and add the following environment variables:

# S3 Bucket settings
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Migrate the database
```bash
python manage.py migrate
```

### Step 5: Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### Step 6: Start the development server
```bash
python manage.py runserver
```
Once the application is running, you can access the API at http://localhost:8000/api/

### API Documentation
You can find the detailed API documentation
 or Swagger collacetion http://localhost:8000/docs/  provided in this repository.


### Design Choices
- **Token-based Authentication**: JWT is used for stateless user authentication, providing scalability.
- **MySQL**: Selected for its reliability and ease of integration with Django.
- **Caching with Django**: Utilizes Django's caching framework to improve performance by caching frequently accessed data.
- **Django's Built-in Features**: Utilized Django’s ORM and caching framework for efficient data handling.



