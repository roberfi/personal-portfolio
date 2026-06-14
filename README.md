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
- 📧 **Contact form** with email notifications and database storage
- 📊 **Structured logging** - JSON logs in production, human-readable logs in development
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

   # Email Configuration (optional for development - emails print to console)
   CONTACT_EMAIL=contact@localhost

   # Google reCAPTCHA v3 (optional - if not set, form works without reCAPTCHA)
   RECAPTCHA_SITE_KEY=<your site key from Google reCAPTCHA>
   RECAPTCHA_SECRET_KEY=<your secret key from Google reCAPTCHA>
   RECAPTCHA_SCORE_THRESHOLD=0.5  # Score threshold (0.0-1.0), default 0.5
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

Deployments are driven from your machine through the `Makefile`: the Docker image
is **built locally and shipped to the server**, which never builds anything.
The server only holds a _deploy bundle_: configuration, secrets and media.
The `docker-compose.yml` and `nginx/nginx.conf` are pushed automatically
on every deploy, so they never drift.

Every command that talks to the server requires `SSH_HOST=user@host`.

#### First-time server setup

On the server, create the bundle directory (defaults to `~/personal-portfolio`)
with the pieces that live only there:

```bash
mkdir -p ~/personal-portfolio/{ssl,mediafiles,nginx}
```

1. **Environment file** — create `~/personal-portfolio/.env` with:

   ```bash
   SERVER_NAMES=<name of the hosts separated by spaces>
   SECRET_KEY=<strong secret key>
   POSTGRES_DB=<name of the postgres database>
   POSTGRES_USER=<name of the postgres user>
   POSTGRES_PASSWORD=<password for the given postgres user>

   # Email Configuration (required for the contact form)
   EMAIL_HOST=smtp.your-provider.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_USE_SSL=False
   EMAIL_HOST_USER=your-username
   EMAIL_HOST_PASSWORD=your-password
   DEFAULT_FROM_EMAIL=noreply@your-domain.com
   CONTACT_EMAIL=contact@your-domain.com

   # Google reCAPTCHA v3 (spam protection for the contact form)
   # Both keys are required to enable reCAPTCHA; omit them to run the form without it.
   RECAPTCHA_SITE_KEY=<your site key from Google reCAPTCHA>
   RECAPTCHA_SECRET_KEY=<your secret key from Google reCAPTCHA>
   RECAPTCHA_SCORE_THRESHOLD=0.5 # Score threshold (0.0-1.0), default 0.5
   ```

2. **SSL certificates** — place your `cert.pem` and `key.pem` in
   `~/personal-portfolio/ssl/`.
   Note: to test locally, dummy untrusted certificates can be generated with:

   ```bash
   openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365
   ```

3. **Media files** — place `background.jpg`, `background_preview.jpg`,
   `favicon.ico` and `icon.png` in `~/personal-portfolio/mediafiles/`.

The PostgreSQL data lives in a named Docker volume, so it persists across deploys.

#### Deploying

From your machine (Docker installed and SSH access to the server):

```bash
make deploy SSH_HOST=user@your-server
```

This runs the tests, builds the image, ships it to the server, syncs the config
and restarts the stack. By default the image is tagged with the current git short
SHA; pass `TAG=` to override it (e.g. `make deploy SSH_HOST=user@your-server TAG=v1.0.0`).

If the bundle lives somewhere other than `~/personal-portfolio`, override the path
with `REMOTE_DIR=` (e.g. `REMOTE_DIR=/srv/portfolio`).

#### Makefile commands

Run `make` (or `make help`) to list them. Commands marked _remote_ require `SSH_HOST=user@host`.

| Command               | Scope  | Description                                                                             |
| --------------------- | ------ | --------------------------------------------------------------------------------------- |
| `make help`           | local  | List all available commands (default target).                                           |
| `make test`           | local  | Run the Django test suite.                                                              |
| `make build`          | local  | Build the production Docker image locally.                                              |
| `make deploy`         | remote | Test, build, ship the image, sync the config and restart the stack.                     |
| `make sync-config`    | remote | Push `docker-compose.yml` and `nginx/nginx.conf` to the server (never touches secrets). |
| `make restart`        | remote | Restart the remote stack without rebuilding or shipping.                                |
| `make logs`           | remote | Tail the application logs on the server.                                                |
| `make ps`             | remote | Show the status of the remote stack.                                                    |
| `make prune`          | remote | Free disk on the server: drop old image tags (keeps `latest`) and dangling layers.      |
| `make prune-local`    | local  | Same image cleanup on your local machine.                                               |
| `make pull-prod-data` | remote | Replace the local dev database with a copy of production data (wipes local data).       |
| `make ssh`            | remote | Open an interactive SSH session on the server.                                          |

`make pull-prod-data` dumps production data (excluding `auth` users, sessions,
admin logs and contact form submissions) and loads it into the local database via
Django's `dumpdata`/`loaddata`, so it works across the Postgres↔SQLite engines.
It runs `flush` first, which wipes the local database and any local superuser —
recreate one afterwards with `python manage.py createsuperuser`.

## 🧪 Testing

Run the test suite:

```bash
cd src
python manage.py test
```

## 📊 Logging

Logging is configured in [src/core/settings.py](src/core/settings.py) via Django's `LOGGING` setting and
always writes to stdout:

- **Development** (`DEBUG=true`): plain, human-readable lines.
- **Production** (`DEBUG=false`): single-line JSON records (see [src/core/logging.py](src/core/logging.py)),
  ready to be collected by a log aggregator.

Besides Django's own `django` logger, the app defines dedicated loggers for the contact flow:

- `contact` - contact form submissions and email notification outcomes.
- `recaptcha` - reCAPTCHA verification results and API errors.
- `security` - suspicious activity, such as missing or failing reCAPTCHA tokens.

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
