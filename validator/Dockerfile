# 1. Use a modern Python base with the latest GLIBC
FROM python:3.11-bookworm

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your dependency list first (for faster builds)
COPY requirements.txt .

# 4. Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your Python code into the container
COPY . .

# 6. Run the web server with robust port fallback and multi-threaded concurrency
CMD exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 1 --timeout 0 app:app
