FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN groupadd --system --gid 10001 netpulse \
    && useradd --system --uid 10001 --gid netpulse --home-dir /nonexistent --shell /usr/sbin/nologin netpulse

COPY pyproject.toml uv.lock README.md ./
COPY app ./app
RUN python -m pip install --no-cache-dir uv==0.10.0 \
    && uv sync --locked --no-dev --no-editable

USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
