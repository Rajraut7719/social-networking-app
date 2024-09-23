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
git clone https://github.com/Rajraut7719/social-networking-application.git
cd social-networking-api
```
### Step 2: Set up the environment
Create a .env file in the root directory and add the following environment variables:

- SECRET_KEY=django-insecure-1mo&tq_y=4r%761^xb-k%3rybb(u*w3uk_jw3n4v10a!ma@44^
- DATABASE_NAME=social_network
- USER_DB_NAME=root
- DB_PASSWORD=root
- DB_HOST_NAME=localhost

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```




