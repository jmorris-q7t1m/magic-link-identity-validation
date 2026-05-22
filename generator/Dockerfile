# 1. Use a modern Python base with the latest GLIBC
FROM python:3.11-bookworm

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your dependency list first (for faster layer caching)
COPY requirements.txt .

# 4. Install the required open-source libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the sanitized application code into the container
COPY . .

# 6. Run the web server using Gunicorn.
# Includes a robust port fallback so it executes seamlessly locally or on any cloud platform.
CMD exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 1 --timeout 0 app:app
