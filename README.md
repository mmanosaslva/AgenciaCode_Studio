# AgenciaCode Studio

Sistema de Gestión de Proyectos de Desarrollo — MVC + Flask + Bootstrap 5

## Descripción

Aplicación web para la gestión integral de una agencia de desarrollo de software. Administra clientes, colaboradores, proyectos, tareas y asignaciones con reglas de negocio validadas en base de datos y lógica de aplicación.

**Autor:** Yayo Mery

## Stack Tecnológico

| Componente        | Tecnología                                   |
|------------------|----------------------------------------------|
| Backend          | Python 3.10+ / Flask 3.0 / SQLAlchemy 2.0   |
| Frontend         | Bootstrap 5 + Jinja2 + CSS custom           |
| Base de Datos    | SQLite (desarrollo) / MySQL 8.0 (producción) |
| Testing          | pytest + pytest-cov (100 tests)              |
| Contenedores     | Docker + Docker Compose                      |
| Deploy           | Gunicorn + Render                            |

## Módulos Implementados

| # | Módulo                         | Implementado | Tests |
|---|-------------------------------|:------------:|:-----:|
| 1 | Acceso al Sistema (Login)      | ✅           | ✅    |
| 2 | Gestión de Usuarios            | ✅           | ✅    |
| 3 | Gestión de Clientes (CRUD)     | ✅           | ✅    |
| 4 | Gestión de Colaboradores (CRUD)| ✅           | ✅    |
| 5 | Gestión de Proyectos (CRUD)    | ✅           | ✅    |
| 6 | Gestión de Tareas (CRUD)       | ✅           | ✅    |
| 7 | Asignaciones (M:N)             | ✅           | ✅    |
| 8 | Consultas y Reportes           | ✅           | ✅    |

## Reglas de Negocio

| # | Regla | Validación |
|---|-------|------------|
| 1 | Máximo **3 proyectos activos** por colaborador | Controlador + trigger BD |
| 2 | No crear tareas en proyectos **finalizados/cancelados** | Controlador + trigger BD |
| 3 | No eliminar proyectos con **tareas en progreso** | Controlador |
| 4 | Fechas coherentes: inicio < fin, tareas dentro del rango | Controlador + CHECK constraint |
| 5 | No eliminar clientes con proyectos asociados | Controlador |

## Arquitectura MVC

```
app/
├── models/          → Capa de Modelo (ORM + lógica de dominio)
├── controllers/     → Capa de Controlador (reglas de negocio)
├── routes.py        → Capa de Vista (rutas Flask + templates Jinja2)
├── templates/       → Plantillas HTML
├── static/          → CSS, JS
├── database/        → Config BD, modelos ORM, seed data
└── utils/           → Validadores, constantes, email service
```

## Estructura del Proyecto

```
AgenciaCode_Studio/
│
├── app.py                      # Entry point — python app.py
├── Procfile                    # Deploy config (gunicorn)
├── .env                        # Variables de entorno
├── .env.example                # Plantilla del .env
├── requirements.txt            # Dependencias Python
├── docker-compose.yml          # Orquestación Docker
├── README.md                   # Este archivo
├── TESTING_GUIDE.md            # Guía de testing
│
├── app/                        # Código fuente (MVC)
│   ├── __init__.py             # Flask app factory + config BD
│   ├── routes.py               # Rutas web (Flask blueprint)
│   ├── models/                 # Modelos de dominio
│   ├── controllers/            # Controladores + reglas de negocio
│   ├── templates/              # Plantillas HTML + Bootstrap 5
│   ├── static/                 # CSS, JS
│   ├── database/               # Config BD, modelos ORM, seed data
│   └── utils/                  # Validadores, constantes, email
│
├── tests/                      # 100 tests automatizados
│   ├── test_controllers.py     # Tests de controladores
│   ├── test_business_rules.py  # Tests de reglas de negocio
│   ├── test_integration.py     # Tests de integración
│   ├── test_e2e.py             # Tests end-to-end
│   ├── test_security.py        # Tests de seguridad
│   └── test_blackbox.py        # Tests de caja negra
│
├── database/                   # Scripts SQL
│   ├── schema.sql              # Schema completo (tablas, triggers, vistas)
│   └── seed_data.sql           # Datos de prueba
│
├── docs/                       # Documentación
│   ├── ANALISIS.md             # Análisis del problema
│   ├── MODELO_RELACIONAL.md    # Modelo relacional
│   ├── diagrams/               # Diagramas MER
│   └── screenshots/            # Capturas de pantalla
│
└── docker/                     # Dockerfiles
    ├── Dockerfile              # App container
    └── Dockerfile.db           # DB container
```

## Base de Datos

### Tablas (7 total)

| Tabla                  | Descripción                          | Tipo         |
|------------------------|--------------------------------------|--------------|
| `users`                | Autenticación de usuarios            | Dominio      |
| `clients`              | Clientes de la agencia               | Dominio      |
| `collaborators`        | Equipo de trabajo                    | Dominio      |
| `projects`             | Proyectos de desarrollo              | Dominio      |
| `tasks`                | Tareas por proyecto                  | Dominio      |
| `collaborator_project` | Relación M:N colaborador-proyecto    | Intermedia   |
| `password_reset_tokens`| Tokens de recuperación de contraseña | Soporte      |

### Relaciones

- **1:N** Client → Projects (un cliente tiene muchos proyectos)
- **1:N** Project → Tasks (un proyecto tiene muchas tareas)
- **1:N** Collaborator → Tasks (un colaborador tiene muchas tareas)
- **M:N** Collaborator ↔ Projects (tabla intermedia `collaborator_project`)

## Instalación y Uso

### Requisitos

- Python 3.10+
- pip

### Local (SQLite — desarrollo)

```bash
git clone <repo-url>
cd AgenciaCode_Studio
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

python app.py
# Abrir http://localhost:5000
```

### Con Docker (MySQL — producción)

```bash
docker-compose build
docker-compose up -d
# App: http://localhost:5000
# Adminer (BD): http://localhost:8080

# Ver logs
docker-compose logs -f app

# Detener
docker-compose down
```

### Testing

```bash
# Todos los tests (100)
pytest tests/ -v

# Con reporte de cobertura
pytest tests/ --cov=app --cov-report=html

# Solo reglas de negocio
pytest tests/test_business_rules.py -v

# Solo seguridad
pytest tests/test_security.py -v

# Solo caja negra
pytest tests/test_blackbox.py -v
```

## Credenciales de Prueba

| Usuario  | Contraseña | Rol   |
|----------|-----------|-------|
| admin    | admin123  | admin |
| usuario1 | user123   | user  |

## Rutas Web

| Método | Ruta                       | Descripción                     |
|--------|---------------------------|---------------------------------|
| GET    | `/`                       | Redirige a login o dashboard    |
| GET    | `/login`                  | Página de inicio de sesión      |
| POST   | `/login`                  | Autenticación                   |
| GET    | `/register`               | Página de registro              |
| POST   | `/register`               | Crear cuenta                    |
| GET    | `/forgot-password`        | Recuperar contraseña            |
| POST   | `/forgot-password`        | Enviar enlace de recuperación   |
| GET    | `/reset-password/<token>` | Formulario de nueva contraseña  |
| POST   | `/reset-password/<token>` | Cambiar contraseña              |
| GET    | `/logout`                 | Cerrar sesión                   |
| GET    | `/dashboard`              | Menú principal                  |
| GET    | `/clientes`               | Listado + formulario de clientes|
| POST   | `/clientes`               | Crear cliente                   |
| POST   | `/clientes/<id>`          | Editar/eliminar cliente         |
| GET    | `/colaboradores`          | Listado + formulario            |
| POST   | `/colaboradores`          | Crear colaborador               |
| POST   | `/colaboradores/<id>`     | Editar/eliminar colaborador     |
| GET    | `/proyectos`              | Listado + formulario            |
| POST   | `/proyectos`              | Crear proyecto                  |
| POST   | `/proyectos/<id>`         | Editar/eliminar proyecto        |
| GET    | `/tareas`                 | Listado + filtros + formulario  |
| POST   | `/tareas`                 | Crear tarea                     |
| POST   | `/tareas/<id>`            | Editar/eliminar tarea           |
| GET    | `/asignaciones`           | Listado + formulario            |
| POST   | `/asignaciones`           | Asignar colaborador a proyecto  |
| POST   | `/asignaciones/<id>`      | Remover asignación              |
| GET    | `/reportes`               | Reportes y estadísticas         |
| GET    | `/mis-tareas`             | Tareas del colaborador logueado |
| POST   | `/mis-tareas/<id>`        | Cambiar estado de tarea propia  |
| GET    | `/admin/check-overdue`    | Enviar emails de tareas vencidas|
| GET    | `/admin/test-email`       | Enviar email de prueba          |

## Funcionalidades Clave

- **Filtros de tareas**: por proyecto, colaborador y estado
- **Reportes**: tareas completadas vs pendientes, carga de trabajo, eficiencia
- **Consultas JOIN**: proyecto + cliente + tarea + colaborador + estado
- **Email notifications**: bienvenida, asignación, tareas vencidas, recuperación
- **Validación de inputs**: XSS, inyección, formatos de email/teléfono
- **Control de acceso**: decoradores `login_required` y `admin_required`

## Despliegue en Render

1. Crear servicio **Web Service** en [render.com](https://render.com)
2. Conectar repositorio de GitHub
3. Configurar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn "app:create_app()"`
   - **Plan:** Free
4. Agregar variables de entorno:
   - `DATABASE_URL`: `sqlite:///agenciacode.db` (o MySQL externo)
   - `SECRET_KEY`: clave aleatoria segura
5. Desplegar

> **Nota:** Con SQLite en Render los datos se pierden al redeployar.
> Para datos persistentes, usa [Render PostgreSQL](https://render.com/docs/databases)
> o [Railway MySQL](https://railway.app).
