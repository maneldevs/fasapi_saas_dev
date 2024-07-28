## UVICORN -> http://localhost:8000/api/health

# FROM python:3.12.4-bookworm
# WORKDIR /usr/src/application
# COPY requirements.txt /usr/src/application/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY src /usr/src/application/
# CMD ["fastapi", "run", "app/main.py", "--port", "8000"]


## GUNICOR + UVICORN
### http://localhost:8000/api/health (NO NGINX)
### http://localhost/api/health (NGINX)

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY src/app /app/app
