FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN groupadd --system --gid 10001 lab && useradd --system --uid 10001 --gid lab --home-dir /nonexistent --shell /usr/sbin/nologin lab
COPY server.py ./server.py
USER 10001:10001
EXPOSE 8080
CMD ["python", "server.py"]
