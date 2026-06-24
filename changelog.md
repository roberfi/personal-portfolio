# Changelog

## 0.8.1 — 2026-06-24

- Support standalone and reverse-proxy nginx deployment modes via Docker Compose profiles
- Redirect non-www requests to `www.` via the `PREPEND_WWW` environment variable
- Trust `X-Forwarded-Proto: https` from the upstream proxy in production so Django generates correct `https://` URLs
- Make robots.txt `Disallow` paths configurable via `ROBOTS_DISALLOW_PATHS` environment variable

## 0.8.0 — 2026-06-21

- Add projects with Problem → Approach → Outcome structure, replacing sub-projects
- Add drag-and-drop project ordering in the admin
- Add drag-and-drop technology ordering in the admin
- Add Service model with drag-and-drop ordering in the admin
- Add ProcessStep model with drag-and-drop ordering in the admin
- Redesign hero section: outcome-driven headline, two-column layout with portrait frame and decorative accents
- Align the navbar, footer, contact and my-career views with the new hero design
- Add a call-to-action block to the home page
- Add a featured projects section to the home page, with a dedicated project summary field for card excerpts
- Add a services section to the home page
- Add a "How I work" process steps section to the home page
- Add projects list page (`/projects/`) and project detail page (`/projects/<slug>/`)
- Simplify main navigation to Home · Projects · Contact
- Move My Career page link to the footer under a new "More" section
- Serve CSS as a static minimized stylesheet extracted from the JS bundle
- Normalize and improve page titles and headings across views
- Improve technology badges
- Use Inter font
- Create a custom 404 page
- Implement maintenance mode
- Make the contact page intro text configurable from the admin

## 0.7.0

- Improve UI
- Add contact form page with reCAPTCHA v3 protection
- Change the structure of cookie consent banner
- Split experience timeline template into different cotton components
- Implement structured logging
- Bump python and javascript dependencies to fix security vulnerabilities
- Run djlint on templates in CI
- Manage site images (background, favicon, logo) from the admin
- Switch to tag-based releases and automate deployment via a Makefile

## 0.6.0

- Re-design Home view
- Split my career into a different view
- Add Education section into my_career view
- Improvements in the Navigation Bar
- Add technology badges to home page and experiences
- Add sub-projects to experiences
- Add a footer note with a link to the GitHub repository
- Add SEO improvements
- Add MIT license
- Bump python and javascript dependencies

## 0.5.0

- Implement django-cooco library
- Update the way experiences duration is calculated
- Use the name of the Legal and Privacy Sections to title the text
- Bump tailwindcss to v4 and daisyui to v5
- Bump other dependencies

## v0.4.1

- Fix no cookie consent banner if no optional cookies set
- Fix CookieGroup version starting with value 2

## v0.4.0

- Implement cookie consent management
- Implement Google Analytics
- Some improvements in navbar
- Bump dependencies

## v0.3.0

- Implement django-cotton
- Add footer with "Legal & Privacy" and "Follow me" sections
- Implement @tailwindcss/typography module for markdown rendering styles
- Implement django-solo for singleton Django models
- Bump dependencies

## v0.2.0

- Implement frontend building on deploy
- Implement deployment by docker compose
- Use Roboto font
- Bump python version to 3.12
- Fix showing the elements with no css styles
- Rename the project to personal-portfolio
- Move media files serving to nginx
- Add HTML meta cards

## v0.1.0

- Minor UI improvements
- Create views to serve media files
- Implement Django cache system
- Implement CompressedManifestStaticFilesStorage staticfiles storage after fixing the error
- Add support for markdown in experiences description field

## v0.0.2

- Sort experiences by end_date
- Add experiences duration and remove the day from dates displaying
- Humanize titles of database models
- Re-design UI

## v0.0.1

- First release
