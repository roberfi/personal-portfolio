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

## v0.7.0 — Operations & quality

- [x] **Configurable media via admin** — add a `SiteMedia` django-solo singleton in [src/home/models.py](src/home/models.py) with `ImageField`s for `background_image`, `og_preview_image`, `favicon`, `logo`; register in [src/home/admin.py](src/home/admin.py); wire templates ([src/base/templates/cotton/base.html](src/base/templates/cotton/base.html)) to read from it instead of hardcoded files. _`feat: manage site images from the admin`_
- [x] **Structured logging** — add `logging.config.dictConfig` to [src/core/settings.py](src/core/settings.py): JSON formatter in prod, console in dev, named loggers (`contact`, `recaptcha`, `security`), stdout only. _`feat: add structured logging configuration`_
- [x] **Use logging in contact flow** — replace silent paths in [src/contact/views.py](src/contact/views.py) with the new loggers (submission, reCAPTCHA score, send failures). _`feat: log contact form and reCAPTCHA events`_
- [x] **Add djlint to CI** — extend the `python-lint` job in [.github/workflows/lint-and-test.yml](.github/workflows/lint-and-test.yml) to run `djlint` (already in pre-commit). _`ci: run djlint on templates`_

## v0.8.0 — Structural redesign (homepage, projects & navigation)

- [ ] **Project model (replaces SubProject)** — add `home.Project` (title, slug, problem, approach, outcome, technologies M2M → `Technology`, `hero_image`, featured, order) + modeltranslation + admin + migration. Remove the `SubProject` model, its FK/M2M and migration, and the `sub_project.html` / `sub_project_list.html` templates; update `experience_timeline` to no longer render sub-projects. The "Freelance Developer" experience entry keeps a short, generic description (no sub-projects); its individual engagements become independent `Project` rows, flagged `featured` where relevant. _`feat: add Project model, remove SubProject`_
- [ ] **Service model** — add `home.Service` (title, slug, `short_description`, `long_description`, `icon_name`, order, `is_active`) + modeltranslation + admin + migration. _`feat: add Service model`_
- [ ] **Hero component** — new `c-hero` cotton component (H1, sub-headline, primary + secondary CTA, tech strip); refactor [src/home/templates/index.html](src/home/templates/index.html) to use it, copy sourced from `PersonalInfo`. Content priorities: H1 is an outcome-driven headline (not the name), name/role becomes the sub-headline, tech strip is visually de-emphasized (smaller, lower), primary CTA points to contact/services with "Más sobre mí" as secondary. _`refactor: extract hero into c-hero component`_
- [ ] **CTA block component** — new reusable `c-cta-block`, used for the home contact CTA section and the footer ([src/base/templates/cotton/footer.html](src/base/templates/cotton/footer.html)). _`feat: add reusable CTA block`_
- [ ] **Featured projects section** — `c-project-card` + a featured-projects grid on home, rendering `Project` rows where `featured=True` (3-4 cards). _`feat: show featured projects on home page`_
- [ ] **Services section** — `c-services-grid` + `c-service-card`; render the `Service` grid on home; each card CTA links to `/contact?service=<slug>`. _`feat: show services on the home page`_
- [ ] **"Cómo trabajo" section** — `c-process-steps` + `c-process-step`; render 4 hardcoded steps on home. _`feat: add how-I-work process section`_
- [ ] **Home page restructure** — assemble the new section order: hero → featured projects → services → cómo trabajo → contact CTA (using `c-cta-block`). _`refactor: restructure home page layout`_
- [ ] **Projects page** — new URL `/projects`, list view + detail view (`/projects/<slug>`); `c-project-card` (title, problem-oriented description, tech badges) for the list, `c-project-detail` (Problem → Approach → Outcome) for the detail page; CSS collage fallback when no image. _`feat: add projects page`_
- [ ] **Navigation & footer restructure** — simplify `NAVBAR_DATA` in [src/base/templatetags/base_tags.py](src/base/templatetags/base_tags.py) to Home · Proyectos · Contacto (drop "My Career"); add a link to the `my-career` page in [src/base/templates/cotton/footer.html](src/base/templates/cotton/footer.html) alongside Legal & Privacy / Follow Me. _`refactor: simplify main navigation, move career page link to footer`_

## v0.9.0 — Client repositioning (content & lead qualification)

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
