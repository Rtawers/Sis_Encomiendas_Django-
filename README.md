


```markdown
# Sistema de Gestión de Encomiendas

Aplicación web full-stack para la administración de envíos de paquetes, con gestión de clientes, rutas, encomiendas y trazabilidad completa de estados. Construida con Django y desplegada sobre una arquitectura contenerizada con Docker.

Universidad Señor de Sipán — Taller de Lenguajes de Programación — IX Ciclo



## Funcionalidades

### Módulo de Encomiendas
- Dashboard con métricas en tiempo real (activas, en tránsito, con retraso, entregadas hoy)
- Listado paginado con filtros por estado y búsqueda por código/cliente
- Vista de detalle con historial completo de cambios de estado
- Formulario de registro con validaciones cliente y servidor
- Generación automática de código (`ENC-YYYYMMDD-XXXXXX`)
- Cálculo automático de costo basado en peso y ruta
- Cambio de estado mediante modal con registro automático en historial

### Módulo de Clientes y Rutas
- CRUD completo desde panel administrativo
- QuerySets personalizados (`activos()`, `con_dni()`, `buscar()`)
- Validaciones de DNI (8 dígitos), RUC y peso positivo

### Autenticación
- Login y logout con sesiones de Django
- Vistas protegidas con `@login_required`
- Asociación User-Empleado para trazabilidad de operaciones
- Navbar dinámico según estado de sesión

### Panel Administrativo
- Título personalizado del Admin
- Badges de color por estado en listados
- Fieldsets organizados por secciones lógicas
- Filtros automáticos sobre Foreign Keys (solo registros activos)
---

## Instalación

### Requisitos
- Docker Desktop
- Git

### Pasos

1. Clonar el repositorio
```bash
git clone https://github.com/Rtawers/Sis_Encomiendas_Django-.git
cd Sis_Encomiendas_Django-
```

**2. Configurar variables de entorno**
```bash
cp .env.example .env
```

Editar `.env` con valores reales:
```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=encomiendas_db
DB_USER=encomiendas_user
DB_PASSWORD=tu-password
DB_HOST=db
DB_PORT=5432
```

**3. Levantar los servicios**
```bash
docker compose up --build -d
```

**4. Aplicar migraciones y archivos estáticos**
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

**5. Crear superusuario**
```bash
docker compose exec web python manage.py createsuperuser
```

---

## Accesos

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Aplicación web | http://localhost | Usuario creado |
| Django Admin | http://localhost/admin | Superusuario |
| pgAdmin 4 | http://localhost:5050 | `admin@admin.com` / `admin` |

---

## Configuración inicial post-instalación

1. Acceder al admin: `http://localhost/admin`
2. Crear un Empleado y asociarlo al usuario superusuario (campo `user`)
3. Registrar Clientes y Rutas
4. Comenzar a registrar Encomiendas desde el frontend

---

## Comandos útiles

```bash
# Ver logs del servicio web
docker compose logs -f web

# Reiniciar el servicio web
docker compose restart web

# Shell de Django
docker compose exec web python manage.py shell

# Conectarse a PostgreSQL
docker compose exec db psql -U encomiendas_user -d encomiendas_db

# Detener todos los servicios
docker compose down
```
