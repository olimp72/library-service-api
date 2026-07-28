# 📚 Library Service API

RESTful API service for library management automation: handling book catalogs, user management, borrowing processing, and payment system integration.

The project is built using **Django**, **Django REST Framework (DRF)**, **PostgreSQL**, and **Docker**.

---

## 🌟 Key Features

* **Users & Authentication:**
  * User registration and authentication via **JWT** (JSON Web Tokens).
  * Role-based access control: Regular User (Customer) and Administrator (Admin).
* **Books Management:**
  * Browse the list of books (available to all authenticated users).
  * Create, update, and delete books (Admin only).
  * Automatic tracking of available copies (`inventory`).
* **Borrowings Service:**
  * Create book borrowing requests with automatic inventory deduction.
  * Return borrowed books with automatic inventory replenishment.
  * Filter borrowings by status (active/returned) and user ID (Admin only).
* **Integrations & Notifications:**
  * Real-time notifications for new borrowings and returns via **Telegram Bot**.
  * Payment processing for borrowings via **Stripe API**.
* **Code Quality & CI/CD:**
  * Automated code quality checks using **GitHub Actions** (`flake8`, `black`).
  * Integrated interactive API documentation with **Swagger / OpenAPI**.

---

## 🛠 Tech Stack

* **Language:** Python 3.11+
* **Framework:** Django 4.2+, Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Authentication:** djangorestframework-simplejwt
* **Documentation:** drf-spectacular (Swagger UI / Redoc)
* **Code Style & Quality:** Flake8, Black
* **Containerization:** Docker, Docker Compose
* **CI/CD:** GitHub Actions

---

## 🚀 Quickstart Guide

### 1. Clone the repository

```bash
git clone [https://github.com/your-username/library-service-api.git]
(https://github.com/your-username/library-service-api.git)
cd library-service-api

```
Option 1. Running with Docker (Recommended)
Create a .env file in the root directory based on .env.sample:

Bash
cp .env.sample .env
Fill in the necessary variables (
DB credentials, Secret Key, Telegram Bot Token, Stripe keys, etc.
).

Build and start containers:

Bash
docker-compose up --build -d
Apply migrations and create a superuser:

Bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
The server will be available at http://127.0.0.1:8000/.

Option 2. Local Setup (with venv)
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Apply migrations and run the local server:

Bash
python manage.py migrate
python manage.py runserver
📑 API Documentation (Swagger)
Once the server is running, you can explore and test all API endpoints directly in your 
browser:

Swagger UI: http://127.0.0.1:8000/api/doc/swagger/

Redoc: http://127.0.0.1:8000/api/doc/redoc/

🧪 Testing & Linting
Running Unit Tests:
Bash
# Via Docker:
docker-compose exec web python manage.py test

# Locally:
python manage.py test
Code Style Checks:
The project uses flake8 and black configured with a maximum line length of 88 characters.

Bash
# Format code with Black:
black .

# Check code with Flake8:
flake8 .
📂 Project Structure
Plaintext
library-service-api/
├── .github/
│   └── workflows/        # CI/CD configurations (GitHub Actions)
├── books/                # Book management app
├── borrowings/           # Borrowing and returning app
├── library_service/      # Core Django settings and configurations
├── users/                # Custom User model and JWT authentication app
├── .env.sample           # Sample environment configuration file
├── .flake8               # Flake8 linter configuration
├── docker-compose.yml    # Docker Compose setup
├── Dockerfile            # Docker image configuration
├── manage.py
├── README.md
└── requirements.txt      # Project dependencies