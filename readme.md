Employee Management System

This is a Flask-based web application designed to manage employee data. It provides functionalities to create, update, and view employee information.

Features:

User Authentication: Secure login and logout functionalities.
User Roles: Admin and User roles are supported.
Employee Management: CRUD operations for employee data.
Pagination and Sorting: Navigate through employee data easily with pagination and sorting options.
Data Seeding: Random employee data can be generated using the provided script.

Installation:

1. Clone the repository:
   git clone https://github.com/AmerAl-Koofee/Aplication.git

2. Install dependencies:
   pip install -r requirements.txt

3. Set up environment variables:
   Create a .env file in the root directory and add the following variables:

   - LOCAL_DATABASE_URI = your_database_uri
   - SECRET_KEY = your_secret_key
   - SECURITY_PASSWORD_SALT = your_password_salt

4. Initialize the database:
   - flask db init
   - flask db migrate -m "Initial migration."
   - flask db upgrade

5. Run the application:
   python app.py

Usage:

- Access the application through your web browser at http://localhost:4500.
- Use the provided login page to authenticate.
- username: test@example.com 
- password = password
- roles=['Admin','User']
- Once logged in, you can manage employees, including creating, updating, and viewing their information.

Contributors:
- Amer Al-Koofee
