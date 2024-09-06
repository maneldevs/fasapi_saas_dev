from src.app.modules.core.utils.translator import Translator

translations = {
    "en_US": {
        "active": "active",
        "Already exists": "{entity} already exists",
        "Are you sure to delete the following entity?": "Are you sure to delete the following entity?",
        "by": "by",
        "Close": "Close",
        "code": "code",
        "Create": "Create",
        "configuration": "configuration",
        "configurations": "configurations",
        "Delete": "Delete",
        "developed with": "developed with",
        "Entity already exists": "Entity already exists",
        "Entity has dependants": "Entity has dependants",
        "Entity not found": "Entity not found",
        "Field required": "Field required",
        "Filter": "Filter",
        "firstname": "firstname",
        "Forbidden": "Forbidden",
        "god": "god",
        "group": "group",
        "groups": "groups",
        "Incorrect username or password": "Incorrect username or password",
        "Invalid credentials": "Invalid credentials",
        "is required": "is required",
        "lastname": "lastname",
        "login": "login",
        "logout": "logout",
        "module": "module",
        "modules": "modules",
        "Not found": "{entity} not found",
        "password": "password",
        "permission": "permission",
        "permissions": "permissions",
        "resource": "resource",
        "resources": "resources",
        "role": "role",
        "roles": "roles",
        "Save": "Save",
        "String should have at least {min_length} characters": "String should have at least {min_length} characters",
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
        "Are you sure to delete the following entity?": "¿Estás seguro de borrar la siguiente entidad?",
        "by": "por",
        "Close": "Cerrar",
        "code": "código",
        "Create": "Crear",
        "configuration": "configuración",
        "configurations": "configuraciones",
        "Delete": "Eliminar",
        "developed with": "desarrollado con",
        "Entity already exists": "La entidad ya existe",
        "Entity has dependants": "La entidad tiene dependencias",
        "Entity not found": "La entiddad no se ha encontrado",
        "Field required": "Campo requerido",
        "Filter": "Filtrar",
        "firstname": "nombre",
        "Forbidden": "No tienes suficientes permisos",
        "god": "dios",
        "group": "grupo",
        "groups": "grupos",
        "Incorrect username or password": "Usuario o contraseña incorrectos",
        "Invalid credentials": "Credenciales no válidas",
        "is required": "es requerido",
        "lastname": "apellidos",
        "login": "acceder",
        "logout": "cerrar sesión",
        "modules": "módulos",
        "module": "módulo",
        "Not found": "{entity} no existe",
        "password": "contraseña",
        "permission": "permiso",
        "permissions": "permisos",
        "resource": "recurso",
        "resources": "recursos",
        "role": "rol",
        "roles": "roles",
        "Save": "Guardar",
        "String should have at least {min_length} characters": "Debe tener al menos {min_length} caracteres",
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
