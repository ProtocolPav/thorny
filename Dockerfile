FROM python:3.13-alpine

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (layer caching — only re-resolves if these change)
COPY pyproject.toml uv.lock /thorny/
COPY nexuscore-client /thorny/nexuscore-client

# Install dependencies
RUN uv sync --frozen --no-dev --project /thorny

# Copy the rest of the source
COPY . /thorny/

ENV PYTHONPATH="${PYTHONPATH}:/thorny/"
ENV UV_LINK_MODE=copy

WORKDIR /thorny/src

CMD ["uv", "run", "--project", "/thorny", "python", "-u", "thorny.py"]