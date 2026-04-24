Sistema de Gestión de Encomiendas 
Proyecto profesional desarrollado con Django + Docker + PostgreSQL + Nginx.
Taller de Lenguajes de Programación — USS — Sesión 03 (Modelos y ORM)
Tecnologías y Arquitectura
Este proyecto utiliza una arquitectura de microservicios orquestada con Docker:
Backend: Python 3.11 / Django 6.0 (ORM avanzado).
Servidor Web: Nginx (Proxy Inverso y gestión de estáticos).
Base de Datos: PostgreSQL 15.
Gestión DB: pgAdmin 4 (Interfaz gráfica integrada).
Contenerización: Docker + Docker Compose.
Instalación y Configuración
Clonar el repositorio:
bash
git clone https://github.com/Rtawers/Sis_Encomiendas_Django-.git
cd Sis_Encomiendas_Django-
Usa el código con precaución.
Configurar variables de entorno:
Copia la plantilla y asegúrate de que los valores coincidan con tu configuración local:
bash
cp .env.example .env
Usa el código con precaución.
Levantar la infraestructura con Docker:
bash
docker compose up --build -d
Usa el código con precaución.
Preparar la Base de Datos y Estáticos:
bash
# Aplicar migraciones
docker compose exec web python manage.py migrate
# Recolectar archivos estáticos para Nginx
docker compose exec web python manage.py collectstatic --noinput
Usa el código con precaución.
Crear Superusuario (Acceso al Admin):
bash
docker compose exec web python manage.py createsuperuser
Usa el código con precaución.
Puertos y Accesos
Gracias a la configuración de Nginx, los accesos son:
App (vía Nginx): http://localhost (Puerto 80)
Django Admin: http://localhost/admin
pgAdmin 4: http://localhost:5050
User: admin@admin.com | Pass: admin
Estructura de Apps (Sesión 03)
clientes: Gestión de remitentes y destinatarios con QuerySets personalizados.
rutas: Definición de trayectos, precios base y días de entrega.
envios: Lógica central (Encomiendas). Incluye:
validators.py: Reglas de negocio para pesos y códigos.
querysets.py: Consultas avanzadas (ej. buscar encomiendas con retraso).
models.py: Cálculo automático de costos y gestión de historial de estados.
nginx: Configuración del servidor web como proxy inverso.
Comandos Útiles de la Sesión
Entrar a PostgreSQL (Terminal):
docker compose exec db psql -U encomiendas_user -d encomiendas_db
Ver Logs de Nginx:
docker compose logs -f nginx
Shell de Django (Probar QuerySets):
docker compose exec web python manage.py shell
Autor:
Daniel Rodriguez — Universidad Señor de Sipán
Taller de Lenguajes de Programación — IX Ciclo — 2026
