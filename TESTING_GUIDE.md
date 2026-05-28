# Guía de Testing — AgenciaCode Studio

**35 tests • 4 suites • pytest + pytest-cov**

## Estrategia

```
Pirámide de Testing (actual):
- Unit Tests (reglas de negocio):     11 tests  →  31%
- Controller Tests:                    16 tests  →  46%
- Integration Tests:                    6 tests  →  17%
- E2E Tests:                            2 tests  →   6%
```

## Requisitos

```bash
pip install -r requirements.txt
# Incluye: pytest, pytest-cov, pytest-flask
```

## Ejecutar Tests

```bash
# Todos los tests (35)
pytest tests/ -v

# Con reporte de cobertura HTML
pytest tests/ --cov=app --cov-report=html
# Abrir htmlcov/index.html

# Suite específica
pytest tests/test_business_rules.py -v
pytest tests/test_controllers.py -v
pytest tests/test_integration.py -v
pytest tests/test_e2e.py -v

# Test individual
pytest tests/test_business_rules.py::TestBusinessRules::test_max_three_active_projects -v

# Sin cacheo de DB (base limpia)
pytest tests/ -v --clean

# Último resultado (35/35 ✅)
pytest tests/ -v --tb=short  # <-- recomendado para diagnóstico rápido
```

## Cobertura Actual (13/4/2026)

| Módulo       | Líneas | Cubiertas | Cobertura |
|-------------|-------:|----------:|----------:|
| controllers | ~380   | ~350      | **92%**   |
| database    | ~180   | ~170      | **94%**   |
| utils       | ~40    | ~38       | **95%**   |
| routes      | ~480   | ~240      | 50% *     |
| **Total**   | ~1080  | ~798      | **74%**   |

\* *routes.py tiene baja cobertura porque se testea vía E2E/test client.
El objetivo es ≥85% general y 100% en reglas de negocio.*

## Tests Implementados

### Reglas de Negocio (11) — `test_business_rules.py`

| Test | Descripción | Estado |
|------|------------|--------|
| `test_max_three_active_projects` | Máx 3 proyectos activos por colaborador | ✅ |
| `test_assign_to_planification_project_allowed` | Asignación a proyecto en planificación | ✅ |
| `test_no_tasks_in_finished_projects` | No crear tareas en proyectos finalizados | ✅ |
| `test_no_tasks_in_cancelled_projects` | No crear tareas en proyectos cancelados | ✅ |
| `test_cannot_delete_project_with_tasks_in_progress` | No eliminar con tareas en progreso | ✅ |
| `test_can_delete_project_without_tasks_in_progress` | Eliminar sin tareas en progreso sí permite | ✅ |
| `test_project_start_before_end` | Validación fecha inicio < fin | ✅ |
| `test_task_date_within_project_range` | Tarea dentro del rango del proyecto | ✅ |
| `test_duplicate_assignment_prevented` | No asignación duplicada | ✅ |
| `test_assign_nonexistent_collaborator` | Error si colaborador no existe | ✅ |
| `test_assign_nonexistent_project` | Error si proyecto no existe | ✅ |

### Controladores (16) — `test_controllers.py`

| Test | Descripción | Estado |
|------|------------|--------|
| CRUD Clientes (4) | Crear, leer, editar, eliminar | ✅ |
| CRUD Colaboradores (4) | Crear, leer, editar, eliminar | ✅ |
| CRUD Proyectos (4) | Crear, leer, editar, eliminar | ✅ |
| CRUD Tareas (4) | Crear, leer, editar, eliminar | ✅ |

### Integración (6) — `test_integration.py`

| Test | Descripción | Estado |
|------|------------|--------|
| `test_full_project_flow` | CRUD completo de un proyecto con tareas y asignaciones | ✅ |
| `test_max_three_active_projects_flow` | Usuario crea 4 proyectos activos → el 4º falla | ✅ |
| `test_assign_collaborator_to_multiple_projects` | Colaborador en ≤3 proyectos funciona | ✅ |
| `test_report_project_summary` | Reporte de resumen de proyecto | ✅ |
| `test_report_workload` | Reporte de carga de trabajo por colaborador | ✅ |
| `test_report_tasks_by_status` | Reporte de tareas por estado | ✅ |

### E2E (2) — `test_e2e.py`

| Test | Descripción | Estado |
|------|------------|--------|
| `test_login_logout_flow` | Login exitoso y cierre de sesión | ✅ |
| `test_redirect_if_not_logged_in` | Redirección a /login si no hay sesión | ✅ |

## Variables de Entorno para Testing

| Variable | Valor por defecto | Descripción |
|----------|------------------|-------------|
| `DATABASE_URL` | `sqlite:///test.db` | BD temporal para tests |
| `SECRET_KEY` | `test-secret-key` | Clave de sesión |
| `FLASK_ENV` | `testing` | Modo testing (desactiva debug) |

## Docker Testing

```bash
# Ejecutar tests dentro del contenedor
docker-compose exec app pytest tests/ -v

# Con cobertura
docker-compose exec app pytest tests/ --cov=app --cov-report=html
```

## Debugging

```bash
# Test con prints (no capturar stdout)
pytest tests/ -v -s

# Test específico con stacktrace completo
pytest tests/test_business_rules.py::TestBusinessRules::test_max_three_active_projects -v --tb=long

# Recargar BD de prueba (forzar recreate)
$env:DATABASE_URL="sqlite:///test.db"; pytest tests/ -v
```
