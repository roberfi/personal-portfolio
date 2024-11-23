# CV Personal Page

This is a project to create a single personal CV page with a clear and simple structure.

## How to configure a development environment

1. Clone the repository:
   ```
   git clone https://github.com/roberfi/cv-personal-page.git
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
5. Run migrations
   ```
   python cv_personal_page/manage.py migrate
   ```
6. Create a superuser
   ```
   python cv_personal_page/manage.py createsuperuser
   ```
7. Run django
   ```
   python cv_personal_page/manage.py runserver
   ```
8. To enter in frontend environment mode, open a new terminal and install node environment
   ```
   npm install
   ```
9. Run webpack in watch mode
   ```
   npm run dev
   ```
10. Navigate to localhost:8000 and enjoy

## Required Media

### Background picture

It has to be located in `cv_personal_page/media/background.jpg`

### Favicon

It has to be located in `cv_personal_page/media/favicon.ico`
