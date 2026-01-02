# Personal Portfolio

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

This is a project to create a single personal portfolio page with a clear and simple structure.

🌐 **Live Website**: [https://roberfi.com](https://roberfi.com)

## ✨ Features

- 🌍 **Multi-language support** (EN/ES) using django-modeltranslation
- 🎨 **Modern UI** with Tailwind CSS and DaisyUI
- 🔐 **Cookie consent management** with django-cooco
- 📝 **Admin-editable content** - No code changes needed to update your portfolio
- 📱 **Fully responsive** design
- 🐳 **Docker-ready** for easy deployment

## 🛠️ Tech Stack

### Backend

- **Django 5.1** - Web framework
- **Python 3.13** - Programming language
- **SQLite/PostgreSQL** - Database

### Frontend

- **Tailwind CSS 4** - Utility-first CSS framework
- **DaisyUI** - Component library
- **Webpack 5** - Module bundler
- **Django Cotton** - Component-based templating

### Development Tools

- **uv** - Fast Python package manager
- **ruff** - Python linter and formatter
- **mypy** - Static type checker
- **eslint** - JavaScript linter
- **prettier** - Code formatter
- **djlint** - Django template linter
- **pre-commit** - Git hooks for code quality

## 📋 Prerequisites

- Python 3.13
- Node.js (for frontend development)
- uv (Python package manager)
- Docker and Docker Compose (for deployment)

## 🚀 Getting Started

### Development Environment Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/roberfi/personal-portfolio.git
   ```

2. Install python development environment with uv:

   ```bash
   uv sync --dev
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

4. Install pre-commit tool

   ```bash
   pre-commit install
   ```

5. Go into django project directory

   ```bash
   cd src
   ```

6. Create a mediafiles folder and add `background.jpg`, `background_preview.jpg` and `favicon.ico` inside.
7. Create an environment file (`.env`) with the following enviornment variables:

   ```bash
   DEBUG=true
   SECRET_KEY=<your dev secret key>
   DATABASE_URL=sqlite:///<path to db.sqlite3 file>
   ```

8. Run migrations

   ```bash
   python manage.py migrate

   ```

9. Create a superuser

   ```bash
   python manage.py createsuperuser
   ```

10. Run django

    ```bash
    python manage.py runserver
    ```

11. To enter in frontend environment mode, open a new terminal and install node environment

    ```bash
    npm install
    ```

12. Run webpack in watch mode

    ```bash
    npm run dev
    ```

13. Navigate to localhost:8000 and enjoy

### Production Deployment

1. Clone the repository:

   ```bash
   git clone https://github.com/roberfi/personal-portfolio.git
   ```

2. Go into deploy directory:

   ```bash
   cd src/deploy
   ```

3. Create an environment file (`.env`) with the following enviornment variables:

   ```bash
   SERVER_NAMES=<name of the hosts separated by spaces>
   SECRET_KEY=<strong secret key>
   POSTGRES_DB=<name of the postgres database>
   POSTGRES_USER=<name of the postgres user>
   POSTGRES_PASSWORD=<name of the postgres password for the given user>
   ```

4. Create a folder called `ssl` and store there your `cert.pem` and `key.pem` files
   Note: to test it locally, dummy untrusted certificates can be generated with the following command:

   ```bash
   openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365
   ```

5. Create a mediafiles folder and add `background.jpg`, `background_preview.jpg` and `favicon.ico` inside.
6. Build the docker image with docker compose:

   ```bash
   docker compose build
   ```

7. Run the docker compose containers:

   ```bash
   docker compose up -d
   ```

8. To stop them, execute:

   ```bash
   docker compose down
   ```

## 🧪 Testing

Run the test suite:

```bash
cd src
python manage.py test
```

## 🔍 Code Quality

### Python

```bash
# Run ruff linter
ruff check .

# Run ruff formatter
ruff format .

# Run type checker
mypy .

# Run Django template linter
djlint src --check
```

### JavaScript

```bash
# Run eslint
npm run eslint

# Run prettier
npm run prettier

# Auto-fix issues
npm run eslint-fix
npm run prettier-fix
```

### Pre-commit hooks

All code quality checks run automatically on commit via pre-commit hooks.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
