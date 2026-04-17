# Sistema de Gestión de Encomiendas 

Proyecto desarrollado en Django 5.2 + Docker + PostgreSQL
Taller de Lenguajes de Programación — USS — Sesión 02

## Tecnologías
- Python 3.11
- Django 5.2
- PostgreSQL 15
- Docker + Docker Compose

## Instalación

1. Clonar el repositorio
2. Copiar `.env.ejemplo` a `.env` y configurar variables
3. Ejecutar: `docker compose up --build -d`
4. Aplicar migraciones: `docker compose exec web python manage.py migrate`
5. Crear superusuario: `docker compose exec web python manage.py createsuperuser`
6. Acceder: http://localhost:8000/admin

## Apps
- **envios** — Gestión de encomiendas
- **clientes** — Gestión de clientes  
- **rutas** — Gestión de rutas
