# Sistema de Gestión de Encomiendas 
Proyecto profesional desarrollado con **Django + Docker + PostgreSQL + Nginx**.  
*Taller de Lenguajes de Programación — USS — Sesión 03 (Modelos y ORM)*

##  Tecnologías y Arquitectura
Este proyecto utiliza una arquitectura de microservicios orquestada con Docker:
*   **Backend:** Python 3.11 / Django 6.0 (ORM avanzado).
*   **Servidor Web:** Nginx (Proxy Inverso y gestión de estáticos).
*   **Base de Datos:** PostgreSQL 15.
*   **Gestión DB:** pgAdmin 4 (Interfaz gráfica integrada).
*   **Contenerización:** Docker + Docker Compose.

##  Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com
    cd Sis_Encomiendas_Django-
    ```

2.  **Configurar variables de entorno:**
    ```bash
    cp .env.example .env
    ```

3.  **Levantar la infraestructura con Docker:**
    ```bash
    docker compose up --build -d
    ```

4.  **Preparar la Base de Datos y Estáticos:**
    ```bash
    docker compose exec web python manage.py migrate
    docker compose exec web python manage.py collectstatic --noinput
    ```

5.  **Crear Superusuario (Acceso al Admin):**
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

##  Puertos y Accesos
*   **App (vía Nginx):** [http://localhost](http://localhost)
*   **Django Admin:** [http://localhost/admin](http://localhost/admin)
*   **pgAdmin 4:** [http://localhost:5050](http://localhost:5050)
    *   *User:* `admin@admin.com` | *Pass:* `admin`

##  Estructura de Apps (Sesión 03)
*   **`clientes`**: Gestión de remitentes y destinatarios con QuerySets personalizados.
*   **`rutas`**: Definición de trayectos, precios base y días de entrega.
*   **`envios`**: Lógica central. Incluye validadores de negocio, QuerySets avanzados y cálculo automático de costos.
*   **`nginx`**: Configuración del servidor web como proxy inverso.

##  Comandos Útiles
*   **Entrar a PostgreSQL:**
    `docker compose exec db psql -U encomiendas_user -d encomiendas_db`
*   **Ver Logs de Nginx:**
    `docker compose logs -f nginx`
*   **Shell de Django:**
    `docker compose exec web python manage.py shell`

---
**Autor:**  
Daniel Rodriguez — **Universidad Señor de Sipán**  
Taller de Lenguajes de Programación — IX Ciclo — 2026

