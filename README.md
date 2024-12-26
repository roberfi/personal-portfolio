# Personal Portfolio

This is a project to create a single personal portfolio page with a clear and simple structure.

## How to configure a development environment

1. Clone the repository:
   ```
   git clone https://github.com/roberfi/personal-portfolio.git
   ```
2. Install python development environment with Poetry:
   ```
   poetry install --with dev
   ```
3. Enter in venv shell
   ```
   poetry shell
   ```
4. Install pre-commit tool
   ```
   pre-commit install
   ```
5. Go into django project directory
   ```
   cd src
   ```
6. Create a mediafiles folder and add `background.jpg`, `background_preview.jpg` and `favicon.ico` inside.
7. Create an environment file (`.env`) with the following enviornment variables:
   ```
   DEBUG=true
   SECRET_KEY=<your dev secret key>
   DATABASE_URL=sqlite:///<path to db.sqlite3 file>
   ```
8. Run migrations
   ```
   python manage.py migrate
   ```
9. Create a superuser
   ```
   python manage.py createsuperuser
   ```
10. Run django
    ```
    python manage.py runserver
    ```
11. To enter in frontend environment mode, open a new terminal and install node environment
    ```
    npm install
    ```
12. Run webpack in watch mode
    ```
    npm run dev
    ```
13. Navigate to localhost:8000 and enjoy

## How to deploy

1. Clone the repository:
   ```
   git clone https://github.com/roberfi/personal-portfolio.git
   ```
2. Go into deploy directory:
   ```
   cd src/deploy
   ```
3. Create an environment file (`.env`) with the following enviornment variables:
   ```
   SERVER_NAMES=<name of the hosts separated by spaces>
   SECRET_KEY=<strong secret key>
   POSTGRES_DB=<name of the postgres database>
   POSTGRES_USER=<name of the postgres user>
   POSTGRES_PASSWORD=<name of the postgres password for the given user>
   ```
4. Create a folder called `ssl` and store there your `cert.pem` and `key.pem` files
   Note: to test it locally, dummy untrusted certificates can be generated with the following command:
   ```
   openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365
   ```
5. Create a mediafiles folder and add `background.jpg`, `background_preview.jpg` and `favicon.ico` inside.
6. Build the docker image with docker compose:
   ```
   docker compose build
   ```
7. Run the docker compose containers:
   ```
   docker compose up -d
   ```
8. To stop them, execute:
   ```
   docker compose down
   ```
