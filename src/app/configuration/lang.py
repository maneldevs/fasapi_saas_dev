from src.app.modules.core.utils.translator import Translator

translations = {
    "en_US": {
        "active": "active",
        "Already exists": "{entity} already exists",
        "by": "by",
        "code": "code",
        "Create": "Create",
        "configuration": "configuration",
        "configurations": "configurations",
        "developed with": "developed with",
        "Entity already exists": "Entity already exists",
        "Entity not found": "Entity not found",
        "Filter": "Filter",
        "firstname": "firstname",
        "Forbidden": "Forbidden",
        "god": "god",
        "group": "group",
        "groups": "groups",
        "Incorrect username or password": "Incorrect username or password",
        "Invalid credentials": "Invalid credentials",
        "lastname": "lastname",
        "login": "login",
        "logout": "logout",
        "module": "module",
        "modules": "modules",
        "Not found": "{entity} not found",
        "password": "password",
        "role": "role",
        "roles": "roles",
        "Save": "Save",
        "Successful operation": "Successful operation",
        "Token expired": "Token expired",
        "Token invalid": "Token invalid",
        "Update": "Update",
        "user": "user",
        "users": "users",
        "username": "username",
        "webname": "name",
        "Welcome to": "Welcome to",
    },
    "es_ES": {
        "active": "activo",
        "Already exists": "{entity} ya existe",
        "by": "por",
        "code": "código",
        "Create": "Crear",
        "configuration": "configuración",
        "configurations": "configuraciones",
        "developed with": "desarrollado con",
        "Entity already exists": "La entidad ya existe",
        "Entity not found": "La entiddad no se ha encontrado",
        "Filter": "Filtrar",
        "firstname": "nombre",
        "Forbidden": "No tienes suficientes permisos",
        "god": "dios",
        "group": "grupo",
        "groups": "grupos",
        "Incorrect username or password": "Usuario o contraseña incorrectos",
        "Invalid credentials": "Credenciales no válidas",
        "lastname": "apellidos",
        "login": "acceder",
        "logout": "cerrar sesión",
        "modules": "módulos",
        "module": "módulo",
        "Not found": "{entity} no existe",
        "password": "contraseña",
        "role": "rol",
        "roles": "roles",
        "Save": "Guardar",
        "Successful operation": "Operación realizada con éxito",
        "Token expired": "Token caducado",
        "Token invalid": "Token no válido",
        "Update": "Editar",
        "user": "usuario",
        "users": "usuarios",
        "username": "usuario",
        "webname": "nombre",
        "Welcome to": "Bienvenido a",
    }
}

tr = Translator(source=translations, default_locale="es_ES")
