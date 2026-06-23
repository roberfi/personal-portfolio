# Roadmap

## Where we are

The site (roberfi.com, Django 5.1 / Tailwind v4 / django-cotton) is technically solid but speaks **developer-to-developer**. The hero leads with a tech stack, there is no projects/case-studies page and no clear way to hire, and the framing assumes the reader already understands what a backend developer does. A non-technical visitor can't tell what problems get solved or how to start a conversation.

## Where we want to get

A site aimed at **Spanish-speaking SMBs and startups** that reads as **client-first, not developer-first**:

- Lead with **outcomes and problems solved**, not tools — technologies become supporting detail, never the headline.
- Make the offer concrete: clear **services**, a visible **"how I work"** process (our trust signal until we have testimonials), and **projects framed as Problem → Approach → Outcome**.
- Make hiring obvious: **CTAs throughout** and a **contact form that qualifies the lead** (service, budget, timeline).
- Spanish-first.

**Guiding principle for every design & content decision:** _would a non-technical small-business owner understandthis and feel invited to act?_ Favour plain language, concrete benefits, and visual clarity over technical completeness. This principle should steer layout, component, and copy choices going forward — not just the items below.

## How this file works

Action checklist to get from the current state to the goal above, then to a stable v1.0.0. Each item is roughly **one commit**; tick it when merged.

## Definition of done (applies to every item)

- **Tests:** every new feature ships with tests covering it (follow the existing per-model / per-view layout under each app's `tests/`).
- **README:** check [README.md](README.md) after each item and update it if the change affects setup, configuration, features, or usage.

## v0.7.0 — Operations & quality ✅ Released

- [x] **Configurable media via admin** — add a `SiteMedia` django-solo singleton in [src/home/models.py](src/home/models.py) with `ImageField`s for `background_image`, `og_preview_image`, `favicon`, `logo`; register in [src/home/admin.py](src/home/admin.py); wire templates ([src/base/templates/cotton/base.html](src/base/templates/cotton/base.html)) to read from it instead of hardcoded files. _`feat: manage site images from the admin`_
- [x] **Structured logging** — add `logging.config.dictConfig` to [src/core/settings.py](src/core/settings.py): JSON formatter in prod, console in dev, named loggers (`contact`, `recaptcha`, `security`), stdout only. _`feat: add structured logging configuration`_
- [x] **Use logging in contact flow** — replace silent paths in [src/contact/views.py](src/contact/views.py) with the new loggers (submission, reCAPTCHA score, send failures). _`feat: log contact form and reCAPTCHA events`_
- [x] **Add djlint to CI** — extend the `python-lint` job in [.github/workflows/lint-and-test.yml](.github/workflows/lint-and-test.yml) to run `djlint` (already in pre-commit). _`ci: run djlint on templates`_

## v0.8.0 — Structural redesign (homepage, projects & navigation) ✅ Released

- [x] **Project model (replaces SubProject)** — add `home.Project` (title, slug, problem, approach, outcome, technologies M2M → `Technology`, `hero_image`, featured, order) + modeltranslation + admin + migration. Remove the `SubProject` model, its FK/M2M and migration, and the `sub_project.html` / `sub_project_list.html` templates; update `experience_timeline` to no longer render sub-projects. The "Freelance Developer" experience entry keeps a short, generic description (no sub-projects); its individual engagements become independent `Project` rows, flagged `featured` where relevant. _`feat: add Project model, remove SubProject`_
- [x] **Service model** — add `home.Service` (title, slug, `short_description`, `long_description`, `icon_name`, order, `is_active`) + modeltranslation + admin + migration. _`feat: add Service model`_
- [x] **ProcessStep model** — add `home.ProcessStep` (title, description, `icon_name`, order) + modeltranslation + admin + migration. _`feat: add ProcessStep model`_
- [x] **Hero component** — new `c-hero` cotton component (H1, sub-headline, primary + secondary CTA, tech strip); refactor [src/home/templates/index.html](src/home/templates/index.html) to use it, copy sourced from `PersonalInfo`. Content priorities: H1 is an outcome-driven headline (not the name), name/role becomes the sub-headline, tech strip is visually de-emphasized (smaller, lower), primary CTA points to contact/services with "Más sobre mí" as secondary. _`refactor: extract hero into c-hero component`_
- [x] **CTA block component** — new `c-cta-block`, rendered as the home contact CTA section after the hero in [src/home/templates/index.html](src/home/templates/index.html). _Not added to the footer:_ a sitewide footer CTA would also surface on the contact page itself and would stack a second CTA below the home's own contact section. _`feat: add CTA block`_
- [x] **Featured projects section** — `c-project-card` (hero image with CSS fallback, title, `summary` excerpt, tech badges) + a `c-featured-projects` grid on home, rendering `Project` rows where `featured=True`. Added a dedicated `summary` field (`CharField(200)`, translated) to `Project` so cards show intentional copy instead of a truncated `problem`. _`feat: show featured projects on home page`_
- [x] **Services section** — `c-services-grid` + `c-service-card`; render the `Service` grid on home; each card CTA links to `/contact?service=<slug>`. _`feat: show services on the home page`_
- [x] **"Cómo trabajo" section** — `c-process-steps` + `c-process-step`; render `ProcessStep` rows from DB on home. _`feat: add how-I-work process section`_
- [x] **Home page restructure** — assemble the new section order: hero → services → cómo trabajo → featured projects → contact CTA (using `c-cta-block`). _`refactor: restructure home page layout`_
- [x] **Projects page** — new URL `/projects`, list view + detail view (`/projects/<slug>`); `c-project-card` (title, problem-oriented description, tech badges, full-card stretched link) for the list, `c-project-detail` (Problem → Approach → Outcome) for the detail page; CSS collage fallback when no image; JSON-LD `ItemList` on the list page and `CreativeWork` on the detail page; "See all projects" CTA on the home featured-projects section; Projects link in navbar (highlighted on detail pages via `child_urls`); `current_page_url` template tag fixes hreflang/language-switcher on slug-based routes. _`feat: add projects page`_
- [x] **Navigation & footer restructure** — simplify `NAVBAR_DATA` in [src/base/templatetags/base_tags.py](src/base/templatetags/base_tags.py) to Home · Projects · Contact (drop "My Career"); add a "My Career" link in [src/base/templates/cotton/footer.html](src/base/templates/cotton/footer.html) under a new "More" section alongside Legal & Privacy / Follow Me. _`refactor: simplify main navigation, move career page link to footer`_

## v0.8.1 — Deployment fixes and improvements

- [ ] **Fix canonical domain (www vs non-www)** — add `PREPEND_WWW = env.bool("PREPEND_WWW", default=False)` in [src/core/settings.py](src/core/settings.py); set `PREPEND_WWW=true` in production so Django's `CommonMiddleware` redirects non-www requests to `www.roberfi.com`. Resolves the "Google chose different canonical" warning in Search Console. _`fix: make PREPEND_WWW configurable via env`_
- [ ] **Fix request scheme behind proxy** — add `BEHIND_HTTPS_PROXY = env.bool("BEHIND_HTTPS_PROXY", default=False)` in [src/core/settings.py](src/core/settings.py) and conditionally set `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` when true; set `BEHIND_HTTPS_PROXY=true` in production (alongside `proxy_set_header X-Forwarded-Proto https;` in [deploy/nginx/nginx.conf](deploy/nginx/nginx.conf)) so Django generates correct `https://` URLs in `og:url`, `og:image`, `twitter:image`, and JSON-LD. _`fix: make HTTPS proxy header configurable via env`_
- [x] **Nginx deployment mode templates** — add two nginx config templates: `nginx-standalone.conf` (current: SSL termination + 80→443 redirect) and `nginx-proxy.conf` (HTTP-only, port configurable via `${NGINX_PORT}`, passes `X-Forwarded-Proto` from upstream with `$http_x_forwarded_proto`); add Docker Compose profiles (`standalone` / `proxy`) so the deployment mode is selected at run time without editing compose files. _`feat: support standalone and reverse-proxy nginx deployment modes`_
- [ ] **Block Cloudflare email-protection from indexing** — add `ROBOTS_DISALLOW_PATHS = env.list("ROBOTS_DISALLOW_PATHS", default=[])` in [src/core/settings.py](src/core/settings.py) and render one `Disallow:` line per entry in the robots.txt view in [src/core/views.py](src/core/views.py); set `ROBOTS_DISALLOW_PATHS=/cdn-cgi/` in production to stop Google crawling `/cdn-cgi/l/email-protection` (Cloudflare email obfuscation). _`fix: make robots.txt disallow paths configurable via env`_

## v0.9.0 — Client repositioning (content & lead qualification)

- [ ] **Cookie consent — `django_cooco` v2 + template updates** — release a new version of `django_cooco` with: (1) `reject_all_cookies` view + URL so a "Reject all" button can be wired up; (2) `secure=True` and `httponly=True` added to `CooCoManager.set_cooco_cookie`. Then in this repo: add the "Reject all" button directly on the banner in [src/base/templates/cotton/cookie_consent_banner/index.html](src/base/templates/cotton/cookie_consent_banner/index.html); extend [src/base/templates/cotton/google_analytics.html](src/base/templates/cotton/google_analytics.html) to set all four Consent Mode v2 signals (`analytics_storage`, `ad_storage`, `ad_user_data`, `ad_personalization`). _`feat: GDPR-compliant cookie consent v2`_
- [ ] **Default language to Spanish** — `LANGUAGE_CODE = 'es'` and reorder `LANGUAGES` (ES first) in [src/core/settings.py](src/core/settings.py). _`feat: serve Spanish by default`_
- [ ] **Contact form upgrade** — add `service_interest` (FK → `Service`), `budget_range`, `timeline` to [src/contact/models.py](src/contact/models.py) + [src/contact/forms.py](src/contact/forms.py); pre-fill `service_interest` from `?service=<slug>` in [src/contact/views.py](src/contact/views.py); include new fields in the notification email. _`feat: qualify contact submissions by service`_
- [ ] **Structured data** — enrich Person JSON-LD (`jobTitle`, `description`, `sameAs`) and add per-`Service` JSON-LD in [src/home/views.py](src/home/views.py). _`feat: enrich structured data`_

## v1.0.0 — Stabilize & cleanup

- [ ] **Remove cookie_consent app** — drop the thin wrapper, use `django-cooco` directly. _`refactor: drop cookie_consent wrapper`_
- [ ] **Bump Django to v6** — after 6.0.x has at least one patch release. _`chore: upgrade to Django 6`_
- [ ] **Periodic DB backups** — `pg_dump` cron container in [deploy/docker-compose.yml](deploy/docker-compose.yml) pushing daily to S3-compatible storage, 14-day retention. _`feat: add automated database backups`_
- [ ] **Cache strategy review** — move from middleware-level to per-view / fragment caching where it helps; profile first. _`perf: refine caching strategy`_
- [ ] **Release & deploy workflow** — `.github/workflows/release.yml`: on tag, build + push image (GHCR) and SSH-deploy; reuse [.github/actions/python-setup](.github/actions/python-setup) / [node-setup](.github/actions/node-setup). _`ci: build and deploy on tag`_
- [ ] **Squash migrations** — `squashmigrations` per app once the schema is stable (do this last). _`chore: squash migrations`_

## Decisions log

- **Dropped:** separate deploy repo (cross-repo CI complexity not worth it at this scale — deploy stays in this repo).
- **Dropped:** django-baton (pure admin UX, no client value) unless the admin becomes painful.
- **Deferred:** optional blog/writing section — only if committing to ≥1 article/month.
- **Decided:** `SubProject` merged into the new `Project` model; projects are managed fully independently of `Experience` entries (no FK relation).
- **Decided:** "Experience & training" (My Career) page removed from primary navigation; linked from the footer instead.
- **Decided:** `c-cta-block` lives as a per-page section (home contact CTA), not in the sitewide footer — a footer CTA would render on the contact page itself and stack a second CTA right below the home's own contact section.
