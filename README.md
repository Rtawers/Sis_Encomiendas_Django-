# Sistema de Gestión de Encomiendas 

Proyecto desarrollado en Django 5.2 + Docker + PostgreSQL  
Taller de Lenguajes de Programación — USS — Sesión 02

---

##  Tecnologías

- Python 3.11
- Django 5.2
- PostgreSQL 15
- Docker + Docker Compose

---

##  Instalación

1. Clonar el repositorio
git clone https://github.com/Rtawers/Sis_Encomiendas_Django-.git
cd Sis_Encomiendas_Django-

2. Copiar el archivo de variables de entorno
cp .env.ejemplo .env

3. Construir y levantar los contenedores
docker compose up --build -d

4. Aplicar migraciones a PostgreSQL
docker compose exec web python manage.py migrate

5. Crear superusuario (tú defines el usuario y contraseña)
docker compose exec web python manage.py createsuperuser

6. Acceder al sistema
   - App: http://localhost:8000
   - Admin: http://localhost:8000/admin

---

##  Variables de Entorno

El archivo `.env` no se sube a GitHub por seguridad.  
Copia `.env.ejemplo` a `.env` y usa estos valores:
SECRET_KEY=mi-clave-secreta-super-larga-2026-encomiendas
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=encomiendas_db
DB_USER=encomiendas_user
DB_PASSWORD=encomiendas_pass_2026
DB_HOST=db
DB_PORT=5432

---

##  Apps del proyecto

- **envios** — Gestión de encomiendas (modelo principal)
- **clientes** — Gestión de clientes
- **rutas** — Gestión de rutas

---

##  Credenciales de Acceso

El superusuario lo crea cada desarrollador localmente con:
docker compose exec web python manage.py createsuperuser
Ingresa el usuario y contraseña que desees, luego úsalos en:  
http://localhost:8000/admin

---

##  Comandos Docker útiles
Levantar servicios
docker compose up -d
Ver logs
docker compose logs -f web
Apagar servicios
docker compose down
Ejecutar migraciones
docker compose exec web python manage.py migrate
Crear superusuario
docker compose exec web python manage.py createsuperuser

---

##  Estructura del proyecto
encomiendas/
├── config/          ← Configuración global (settings, urls)
├── envios/          ← App de encomiendas
├── clientes/        ← App de clientes
├── rutas/           ← App de rutas
├── Dockerfile       ← Imagen Docker de la app
├── docker-compose.yml ← Orquestación de servicios
├── .env.ejemplo     ← Plantilla de variables de entorno
├── requirements.txt ← Dependencias del proyecto
└── manage.py        ← CLI de Django

---

##  Autor

**Daniel Rodriguez** — Universidad Señor de Sipán  
Taller de Lenguajes de Programación — IX Ciclo — 2026
