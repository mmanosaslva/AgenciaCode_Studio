# AgenciaCode Studio

Sistema de Gestión de Proyectos con arquitectura MVC + Base de Datos Relacional.

## Descripción

AgenciaCode Studio es una aplicación de escritorio para la gestión integral de una agencia de desarrollo. Permite administrar clientes, colaboradores, proyectos, tareas y asignaciones con reglas de negocio validadas tanto en la base de datos como en la lógica de la aplicación.

## Autor

Yayo Mery

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Backend | Python + Flask + SQLAlchemy |
| Frontend | Tkinter |
| Base de Datos | MySQL 8.0 / SQLite (testing) |
| Testing | pytest + pytest-cov |
| Contenedores | Docker + Docker Compose |

## Estructura del Proyecto

```
AgenciaCode_Studio/
├── app/                  # Código fuente
│   ├── models/           # Capa de modelos
│   ├── controllers/      # Capa de controladores
│   ├── views/            # Capa de vistas (Tkinter)
│   ├── database/         # Config BD y modelos ORM
│   └── utils/            # Validaciones y constantes
├── tests/                # Tests automatizados
├── database/             # Scripts SQL
├── docker/               # Dockerfiles
└── docker-compose.yml    # Orquestación
```

## Módulos Implementados

- [x] Login / Autenticación
- [x] CRUD Clientes
- [x] CRUD Colaboradores
- [x] CRUD Proyectos
- [x] CRUD Tareas
- [x] Asignaciones (colaborador ↔ proyecto)
- [x] Reportes (resumen de proyectos, carga de trabajo, tareas por estado)

## Reglas de Negocio

1. **Máximo 3 proyectos activos por colaborador** - Validado en controlador y BD (trigger)
2. **No crear tareas en proyectos finalizados/cancelados** - Validado en controlador y BD (trigger)
3. **No eliminar proyectos con tareas en progreso** - Validado en controlador
4. **Fechas coherentes** - Inicio < Fin, tareas dentro del rango del proyecto

## Instalación y Uso

### Local (sin Docker)

```bash
# Clonar repositorio
git clone <repo-url>
cd agenciacode-studio

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar BD (MySQL)
# Crear base de datos 'agenciacode_db' y ejecutar:
# mysql -u root -p agenciacode_db < database/schema.sql
# mysql -u root -p agenciacode_db < database/seed_data.sql

# Configurar .env (copiar .env.example a .env y editar)

# Ejecutar
python app/main.py
```

### Con Docker

```bash
docker-compose build
docker-compose up -d
docker-compose logs -f app
```

### Testing

```bash
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

## Credenciales de Prueba

- **Usuario:** admin
- **Contraseña:** admin123
