# AgenciaCode Studio

Sistema de Gestión de Proyectos — MVC + Web Flask + Bootstrap 5

## Descripción

Aplicación web para la gestión integral de una agencia de desarrollo. Administra clientes, colaboradores, proyectos, tareas y asignaciones con reglas de negocio validadas en base de datos y lógica de aplicación.

**Autor:** Yayo Mery

## Stack Tecnológico

| Componente        | Tecnología                                   |
|------------------|----------------------------------------------|
| Backend          | Python 3.10+ / Flask 3.0 / SQLAlchemy 2.0   |
| Frontend         | Bootstrap 5 + Jinja2 (web) / Tkinter (legacy)|
| Base de Datos    | SQLite (desarrollo) / MySQL 8.0 (producción) |
| Testing          | pytest + pytest-cov                          |
| Contenedores     | Docker + Docker Compose                      |

## Estructura del Proyecto

```
AgenciaCode_Studio/
│
├── app.py                      # Entry point — python app.py
├── run.py                      # Entry point Tkinter (legacy)
├── .env                        # Variables de entorno (no subir a Git)
├── .env.example                # Plantilla del .env
├── requirements.txt            # Dependencias Python
├── docker-compose.yml          # Orquestación Docker
├── README.md                   # Este archivo
├── TESTING_GUIDE.md            # Guía de testing
│
├── app/                        # Código fuente
│   ├── __init__.py             # Flask app factory + config BD
│   ├── routes.py               # 25 rutas web (Flask blueprint)
│   ├── models/                 # Capa de modelos ORM
│   ├── controllers/            # Capa de controladores + reglas de negocio
│   ├── views/                  # Capa de vistas Tkinter (legacy)
│   ├── templates/              # 9 plantillas HTML + Bootstrap 5
│   ├── static/                 # CSS, JS
│   ├── database/               # Config BD, modelos, seed data
│   └── utils/                  # Validadores y constantes
│
├── tests/                      # 35 tests automatizados
├── database/                   # Scripts SQL (schema + seed)
└── docker/                     # Dockerfiles
```

## Módulos Implementados

| Módulo          | Web (Flask) | Tkinter (legacy) | Tests |
|----------------|:-----------:|:----------------:|:-----:|
| Login / Auth   | ✅          | ✅               | ✅    |
| CRUD Clientes  | ✅          | ✅               | ✅    |
| CRUD Colaboradores | ✅      | ✅               | ✅    |
| CRUD Proyectos | ✅          | ✅               | ✅    |
| CRUD Tareas    | ✅          | ✅               | ✅    |
| Asignaciones   | ✅          | ✅               | ✅    |
| Reportes       | ✅          | ✅               | ✅    |

## Reglas de Negocio

| # | Regla | Validación |
|---|-------|------------|
| 1 | Máximo **3 proyectos activos** por colaborador | Controlador + trigger BD |
| 2 | No crear tareas en proyectos **finalizados/cancelados** | Controlador + trigger BD |
| 3 | No eliminar proyectos con **tareas en progreso** | Controlador |
| 4 | Fechas coherentes: inicio < fin, tareas dentro del rango | Controlador + CHECK constraint |

## Instalación y Uso

### Requisitos

- Python 3.10+
- pip

### Local (SQLite — desarrollo)

```bash
git clone <repo-url>
cd agenciacode-studio
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Web (Flask + Bootstrap 5) — recomentado:
python app.py
# Abrir http://localhost:5000

# Tkinter (legacy):
python run.py
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
# Todos los tests (35)
pytest tests/ -v

# Con reporte de cobertura
pytest tests/ --cov=app --cov-report=html

# Solo reglas de negocio
pytest tests/test_business_rules.py -v
```

## Credenciales de Prueba

| Usuario  | Contraseña | Rol   |
|----------|-----------|-------|
| admin    | admin123  | admin |
| usuario1 | user123   | user  |

## Rutas Web

| Método | Ruta                    | Descripción              |
|--------|------------------------|--------------------------|
| GET    | `/login`               | Página de inicio de sesión |
| POST   | `/login`               | Autenticación             |
| GET    | `/dashboard`           | Menú principal            |
| GET    | `/clientes`            | Listado de clientes       |
| POST   | `/clientes/crear`      | Crear cliente             |
| POST   | `/clientes/<id>/editar`| Editar cliente            |
| POST   | `/clientes/<id>/eliminar`| Eliminar cliente        |
| GET    | `/colaboradores`       | Listado de colaboradores  |
| POST   | `/colaboradores/crear` | Crear colaborador         |
| POST   | `/colaboradores/<id>/editar`| Editar colaborador   |
| POST   | `/colaboradores/<id>/eliminar`| Eliminar colaborador|
| GET    | `/proyectos`           | Listado de proyectos      |
| POST   | `/proyectos/crear`     | Crear proyecto            |
| POST   | `/proyectos/<id>/editar`| Editar proyecto          |
| POST   | `/proyectos/<id>/eliminar`| Eliminar proyecto       |
| GET    | `/tareas`              | Listado de tareas         |
| POST   | `/tareas/crear`        | Crear tarea               |
| POST   | `/tareas/<id>/editar`  | Editar tarea              |
| POST   | `/tareas/<id>/eliminar`| Eliminar tarea            |
| GET    | `/asignaciones`        | Listado de asignaciones   |
| POST   | `/asignaciones/crear`  | Asignar colaborador       |
| POST   | `/asignaciones/<id>/remover`| Remover asignación    |
| GET    | `/reportes`            | Reportes (3 tabs)         |
| GET    | `/logout`              | Cerrar sesión             |

## Despliegue en Render

1. Crear servicio **Web Service** en [render.com](https://render.com)
2. Conectar repositorio de GitHub
3. Configurar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:create_app()`
   - **Plan:** Free
4. Agregar variable de entorno:
   - `DATABASE_URL`: `sqlite:///agenciacode.db` (o MySQL externo)
   - `SECRET_KEY`: clave aleatoria segura
5. Desplegar

> **Nota:** Con SQLite en Render los datos se pierden al redeployar.
> Para datos persistentes, usa [Render PostgreSQL](https://render.com/docs/databases)
> o [Railway MySQL](https://railway.app).
