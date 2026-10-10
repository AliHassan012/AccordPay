FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py analyzer.py analyzer_worker.py schemas.py gates.py store.py settings.py prompt.txt ./
COPY templates/ templates/
COPY static/ static/
COPY assets/ assets/
RUN mkdir -p /data /app/runtime && useradd --uid 10001 --create-home demo && chown -R demo:demo /app /data
USER demo
ENV DATABASE_PATH=/data/demo.sqlite3 COOKIE_SECURE=true PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000} --no-access-log"]
