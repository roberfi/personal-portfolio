# Oficial python image
FROM python:3.13.1-slim-bookworm AS base

# Set env variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Set workdir
WORKDIR /app

# Use builder image
FROM base AS builder

# Configure Poetry
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.0.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Install nodejs
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Copy installation files
COPY package.json package-lock.json poetry.lock pyproject.toml /app/

# Instal poetry environment
RUN poetry install --with prod

# Install node dependencies
RUN npm install --omit=dev

# Copy the code
COPY . .

# Build frontend
RUN npm run build

# Use final image
FROM base AS final

# Copy the project from builder image
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=builder /app/src ./src

# Copy entrypoint file
COPY ./entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

# Set new workdir
WORKDIR /app/src

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
