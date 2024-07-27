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

## Instal·lar fastapi

```bash
source .venv/bin/activate
pip install fastapi
pip freeze > requirements.txt
```
