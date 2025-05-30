# Leave Management System

## Deploying to Vercel with SQLite

This project is configured to deploy to Vercel using SQLite in read-only mode. This means that database write operations (like creating new users, submitting forms, etc.) will not work in the deployed version. This is due to Vercel's serverless environment which doesn't support file-based databases like SQLite for write operations.

### How it works

1. The application uses SQLite for both local development and production
2. In the Vercel environment, a custom middleware (`ReadOnlyMiddleware`) intercepts write operations and displays a friendly message
3. Session data is stored in memory instead of the database to allow login functionality

### Deployment Steps

1. **Fork or clone this repository**

2. **Sign up for Vercel** (if you haven't already)

3. **Deploy to Vercel**

   - Connect your GitHub repository to Vercel
   - Vercel will automatically detect the Django project
   - The deployment will use the configuration in `vercel.json`

4. **Limitations in the deployed version**
   - User registration will not work
   - Creating/updating leave requests will not work
   - Any other database write operations will not work
   - Login functionality will work (using in-memory sessions)

### Local Development

For local development with full functionality:

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

### Alternative Deployment Options

For a fully functional deployed application, consider using a hosting provider that supports Django with a persistent database:

1. **PythonAnywhere** - Supports SQLite and MySQL
2. **Heroku** - Use with PostgreSQL add-on
3. **DigitalOcean** - Use App Platform or a Droplet

These options will allow all features of the application to work properly in production.
