# New Fit Physicist

**New Fit Physicist** is a personal blog and portfolio-style web application built with Flask. It features dynamic routing, blog post creation via an admin panel, contact functionality, and sitemap support for SEO. The project is designed to showcase a physicist's work, thoughts, and updates through a sleek, easily maintainable platform.

---

## Features

-  Blog post creation/editing through Flask-Admin
-  User authentication with Flask-Login
-  Contact form with email support (Flask-Mail)
-  Sitemap generation (Flask-Sitemap)
-  SEO-friendly routing
-  SQLite database (can be swapped for PostgreSQL)
-  Modular structure using Blueprints
-  Docker-ready (optional with Gunicorn)

---

##  Project Structure

new_fit_physicist/
├── app.py # Main Flask app
├── admin.py # Admin interface setup
├── models_forms.py # SQLAlchemy models and WTForms
├── routes/ # Flask Blueprints for routing
├── templates/ # Jinja2 HTML templates
├── static/ # CSS, JS, images
├── migrations/ # Alembic database migrations
├── chris_blog.db # SQLite database file
├── requirements.txt # Python dependencies
├── sitemap.xml # Sitemap for SEO
├── google*.html # Google site verification
└── README.md # Project documentation

## Tech Stack
- Backend: Flask, Flask-Login, Flask-Admin, Flask-WTF, SQLAlchemy
- Database: SQLite (default), PostgreSQL (optional)
- Frontend: HTML5, CSS3, Jinja2 templates
- Email: Flask-Mail
- Deployment: Gunicorn

