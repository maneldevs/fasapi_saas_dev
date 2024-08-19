# Fastapi SAAS dev


## Descripció

- L'objectiu d'aquesta aplicació és el desenvolupament de la llibrería Fastapi SAAS Core.
- Aquesta aplicació simula un projecte que usa la llibreria esmentada.
- La llibrería s'afegirà com un submòdul de git
- Les característiques son:
  - Traducció de api: validation i errors
  - Traducció de web: validation, errors, etiquetes del frontend etiquetes i missatges de èxit
  - Web d'administració
  - Paginació
  - Arquitectura per capes
  - Tests d'integració
  - Manejament d'excepcions
  - Variables d'entorn
  - Desentrrotllament i desplegament en contenidors de Docker
  - Base de dades i migracions


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
pip install pydantic-settings
pip install python-dotenv
pip install jinja2
pip install alembic
pip install sql model
pip install mysqlclient
pip install requests 
pip install pytest
pip install "passlib[bcrypt]"
pip install pyjwt
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

## Variables d'entorn

- Amb les llibreries pydantic-settings i python-dotenv instal·lades
- Crear el fitxer src/app/configuration/settings.py
- Crear el fitxer .env en el arrel del projecte

## Excepcions y el seu manejament

- Crear las excepciones en el fitxer `src/app/configuration/exceptions.py`

```py
class BaseError(Exception):
    def __init__(self, type: str, msg: str, status_code: int, original_exception: Exception = None) -> None:
        self.type = type
        self.msg = msg
        self.status_code = status_code
        self.original_exception = original_exception

class EntityAlreadyExistsError(BaseError):
    def __init__(self, msg: str = "Entity already exists", original_exception: Exception = None) -> None:
        super().__init__(type="database", msg=msg, status_code=400, original_exception=original_exception)

```

- Crear el handler en el fitxer `src/app/configuration/exception_handler.py`

```py
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.app.configuration.exceptions import BaseError

async def base_handler(request: Request, exc: BaseError):
    detail = {
        "args": exc.original_exception.args,
        "input": await request.json(),
    }
    return JSONResponse(
        status_code=exc.status_code,
        content={"type": exc.type, "msg": exc.msg, "status": exc.status_code, "detail": detail},
    )

async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"type": "validation", "msg": "validation error", "status": 422, "detail": exc.errors()},
    )

```

- Asignar els hendlers en el main:

```py
app.add_exception_handler(BaseError, handler.base_handler)
app.add_exception_handler(RequestValidationError, handler.validation_handler)
```

## Database i Alembic

- Comprovar que estan instal·lats alembic i sqlmodel

- Crear els models en src/app/modules/core/domain/models.py

```py
from uuid import uuid4
from sqlmodel import Field, SQLModel

class Group(SQLModel, table=True):
    __tablename__ = "groups"
    id: str = Field(default=uuid4, primary_key=True)
    code: str = Field(unique=True)
    webname: str
    active: bool = True
```

- Crear la base de dades (si estem en un devcontainer conectar amb Workbench al contenidor)

- Iniciar alembic

```bash
alembic init src/alembic
```

- Afegir les variables d'entorn al .env (si es devcontainer vore els valors de la base de dades de docker-compose.yml)

- Afegir las variables d'entorn al settings.py

- Afegir la següent configuració al fitxer src/alembic/env.py

```py
from sqlmodel import SQLModel
from src.app.configuration.settings import settings
import src.app.modules.core.domain.models
...
DB_USERNAME = settings.db_username
DB_PASSWORD = settings.db_password
DB_HOSTNAME = settings.adb_hostname
DB_PORT = settings.db_port
DB_DATABASE = settings.db_name
DB_URL = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"
...
config = context.config
config.set_main_option("sqlalchemy.url", DB_URL)
...
target_metadata = [SqlModel.metadata]
```

- Afegir la següent configuració al fitxer src/alembic/script.py.mako

```py
import sqlmodel
```

- Crear el fitxer de la migració

```bash
alembic revision --autogenerate -m "create groups table"
```

- Executar la migració

```bash
alembic upgrade head
```

- Configurar la connexió de la base de dades

```py
from sqlmodel import Session, create_engine
from src.app.configuration.settings import settings

DB_USERNAME = settings.db_username
DB_PASSWORD = settings.db_password
DB_HOSTNAME = settings.db_hostname
DB_PORT = settings.db_port
DB_DATABASE = settings.db_database
DB_URL = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"
engine = create_engine(DB_URL)
def get_session():
    with Session(engine) as session:
        yield session

```

- Crear els models (commands, responses i entitities) i el servici en `src/app/core/domain`

- Crear el controller de l'api en `src/app/core/api`

- Crear el repository en `src/app/core/persistence`


## Traducció

- Crear el fitxer de traducció en `src/app/modules/core/utils/translator.py`:

```py
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # pragma: no cover
    from pydantic.error_wrappers import ErrorDict


class Translator:
    def __init__(self, source: dict[str, dict[str, str]], default_locale: str = "en_US") -> None:
        self.source = source
        self.default_locale = default_locale

    def get_allowed_locales(self) -> list[str]:
        return self.source.keys()

    def get_dictionary(self, locale: str):
        return self.source[locale]

    def get_translation(self, key: str, locale: str):
        if locale not in self.get_allowed_locales():
            locale = self.default_locale
        dictionary = self.get_dictionary(locale)
        return dictionary.get(key, key)

    def t(self, key: str, locale: str, **kwargs: dict[str, str]):
        translation = self.get_translation(key, locale)
        return translation.format(**kwargs)

    def t_errors(self, errors: list["ErrorDict"], locale: str):
        result = []
        for error in errors:
            message = error["msg"]
            translated_message = self.t(message, locale)
            error["msg"] = translated_message
            result.append(error)
        return result
```

- Configuració: Crear el fitxer lang.py en `src/app/configuration/lang.py`:

```py
from src.app.modules.core.utils.translator import Translator

translations = {
    "en_US": {
        "active": "active",
    },
    "es_ES": {
        "active": "activo",
    }
}

tr = Translator(source=translations, default_locale="es_ES")
```

- Crear la dependència per obtindre el locale del header o de query params en `src/app/modules/core/domain/dependencies.py`:

```py
def locale_header(accept_language: Annotated[str | None, Header()] = None) -> str | None:
    locale = accept_language[:5].replace("-", "_") if accept_language else None
    return locale


def locale_query(locale: Annotated[str | None, Query()] = None) -> str | None:
    return locale


def get_locale(
    request: Request,
    locale_query: Annotated[str | None, Depends(locale_query)],
    locale_header: Annotated[str | None, Depends(locale_header)],
) -> str | None:
    locale = locale_query or locale_header or "en_US"
    request.state.locale = locale
    return locale

Locale = Annotated[str, Depends(get_locale)]
```

- Us en un servici:

```py
from src.app.configuration.lang import tr

class AuthService:

    def __init__(self, user_repo: Annotated[UserRepo, Depends()], locale: Locale) -> None:
        self.user_repo = user_repo
        self.locale = locale
...
    tr.t("Invalid credentials", self.locale)
```

- Us en un controller:

```py
@router.post("/", response_class=HTMLResponse)
async def my_router(request: Request):
  ...
  msg=tr.t("Successful operation", request.state.locale)
  ...
```

- Us en validacions: afegir el següent en el content del validation handler `src/app/configuration/exception_handler.py`:

```py
async def validation_handler(request: Request, exc: RequestValidationError):
  ...
  "detail": tr.t_errors(exc.errors(), request.state.locale)
 ...
```

- Us en exceptions afegir el següent en el content del base handler:

```py
async def base_handler(request: Request, exc: BaseError):
  ...
  "msg": tr.t(exc.msg, request.state.locale),
  ...
```

- En Jinja2: En el main `/src/app/main.py` afegir:

```py
app = FastAPI(title=settings.app_name, version=settings.app_version, dependencies=[Depends(get_locale)])

admin = FastAPI(dependencies=[Depends(get_locale)])

templates = Jinja2Templates(directory=app_folder + "/resources/templates")
templates.env.globals['_t'] = tr.t
```


## Testing




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
