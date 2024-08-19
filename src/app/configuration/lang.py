from src.app.modules.core.utils.translator import Translator

translations = {
    "en_US": {
        "Already exists": "{entity} already exists",
        "Entity already exists": "Entity already exists",
        "Entity not found": "Entity not found",
        "Forbidden": "Forbidden",
        "Incorrect username or password": "Incorrect username or password",
        "Invalid credentials": "Invalid credentials",
        "Not found": "{entity} not found",
        "Successful operation": "Successful operation",
        "Token expired": "Token expired",
        "Token invalid": "Token invalid",
    },
    "es_ES": {
        "Already exists": "{entity} ya existe",
        "Entity already exists": "La entidad ya existe",
        "Entity not found": "La entiddad no se ha encontrado",
        "Forbidden": "No tienes suficientes permisos",
        "Incorrect username or password": "Usuario o contraseña incorrectos",
        "Invalid credentials": "Credenciales no válidas",
        "Not found": "{entity} no existe",
        "Successful operation": "Operación realizada con éxito",
        "Token expired": "Token caducado",
        "Token invalid": "Token no válido",
    }
}

tr = Translator(source=translations, default_locale="es_ES")
