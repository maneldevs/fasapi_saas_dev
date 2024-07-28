# Fastapi SAAS dev


## Descripció

- L'objectiu d'aquesta aplicació és el desenvolupament de la llibrería Fastapi SAAS Core.
- Aquesta aplicació simula un projecte que usa la llibreria esmentada.
- La llibrería s'afegirà com un submòdul de git


## Crear el projecte

1. Crear el directori .devcontainer amb els fitxers devcontainer.json, docker-compose.yml i Dockerfile
2. Crear el directori .vscode amb el fitxer settings.json
3. Crear el directori .docs i aquest Readme.md dins
4. Crear el fitxer .gitignore
5. Crear el fitxer pyproject.toml
6. Iniciar git i pujar el primer commit


## Crear el ambient virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
which python
deactivate
```


## Instal·lar fastapi i dependencies

```bash
source .venv/bin/activate
pip install fastapi
pip install python-dotenv
pip install jinja2
pip freeze > requirements.txt
```


## Crear l'entrada a l'aplicació i provar

- crear el fitxer main.js en el directori `src/app`

```py
from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
async def health() -> dict:
    return {"status": "UP"}
```

- executar en mode de desenvolupament amb uvicorn i auto-recàrrega
```bash
fastapi dev src/app/main.py
```

- obrir el navegador y provar la adreça http://localhost:8000/health

- Parar la execució pulsant ctrl+c

## Crear frontend

- Crear un directori resources dins de src/app
- Crear un directori statics dins de resources
- Crear un directori templates dins de resources
- En main.py afegir una subaplicació per el admin frontend:
```py
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app_folder = os.path.dirname(__file__)

# API -> http://localhost/...

app = FastAPI()

@app.get("/health")
async def health() -> dict:
    return {"status": "UP"}

# ADMIN WEB ->   # http://localhost/admin/...

admin = FastAPI()
app.mount("/static", StaticFiles(directory=app_folder + "/resources/static"), name="static")
app.mount("/admin", admin)
templates = Jinja2Templates(directory=app_folder + "/resources/templates")

@admin.get("/health", response_class=HTMLResponse)
async def admin_health(request: Request):
    return templates.TemplateResponse(request=request, name="health.html", context={})
```

- IMPORTANT: Les referencies als fitxers estatics no son com en la documentació:
```html
    <link href="{{ url_for('static', path='/css/base.css') }}" rel="stylesheet"> -> MALAMENT!!!!
    <link href="/static/css/base.css" rel="stylesheet"> -> BÉ!!!!!
```


## Configure contenidors Docker per desplegar darrere de NGINX - GUNICORN - UVICORN sense TLS

- Crear directori .docker

- Crear el fitxer Dockerfile

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY src/app /app
```

- Crear el fitxer docker-compose.yml

```yml
version: '3.8'

services:
  app:
    container_name: fastapi_saas_dev_local
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:80"
    restart: unless-stopped
  nginx:
    container_name: nginx
    image: nginx
    ports:
      - "80:80"
      # - "443:443"
    restart: unless-stopped
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app

```

- Crear el fitxer nginx.conf

```
server {
    listen 80;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_redirect off;
        proxy_pass http://fastapi_saas_dev_local:80;
    }
}
```

## Desplegament en producció

1. Per desplegar en producció sense haver creat una imatge, copiar al mateix nivell en un directori:

  - els tres fitxers de abans: Dockerfile, docker-compose.yml, nginx.conf
  - requirements.txt
  - el directory src y tot el seu contingut

2. Executar: `docker compose up`