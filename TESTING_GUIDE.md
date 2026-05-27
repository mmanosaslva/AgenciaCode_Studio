# Guía de Testing - AgenciaCode Studio

## Estrategia

```
Pirámide de Testing:
- Unit Tests: 65% (reglas de negocio, controladores)
- Integration Tests: 25% (flujos completos)
- E2E Tests: 10% (desde la interfaz)
```

## Requisitos

```bash
pip install pytest pytest-cov pytest-flask
```

## Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=app --cov-report=html

# Solo reglas de negocio
pytest tests/test_business_rules.py -v

# Test específico
pytest tests/test_business_rules.py::TestBusinessRules::test_max_three_active_projects -v
```

## Cobertura Mínima

- General: 85%
- Reglas de negocio: 100%
- Controladores: 90%
- Modelos: 85%

## Tests Implementados

### Reglas de Negocio (test_business_rules.py)
- `test_max_three_active_projects` - Verifica límite de 3 proyectos activos
- `test_assign_to_planification_project_allowed` - Asignación a proyecto en planificación
- `test_no_tasks_in_finished_projects` - Tareas en proyectos finalizados
- `test_no_tasks_in_cancelled_projects` - Tareas en proyectos cancelados
- `test_cannot_delete_project_with_tasks_in_progress` - Eliminar proyecto con tareas en progreso
- `test_can_delete_project_without_tasks_in_progress` - Eliminar proyecto sin tareas en progreso
- `test_project_start_before_end` - Validación de fechas de proyecto
- `test_task_date_within_project_range` - Fechas de tarea dentro del rango
- `test_duplicate_assignment_prevented` - Asignación duplicada
- `test_assign_nonexistent_collaborator` - Asignación a colaborador inexistente
- `test_assign_nonexistent_project` - Asignación a proyecto inexistente

### Controladores (test_controllers.py)
- CRUD Clientes, Colaboradores, Proyectos, Tareas
- Autenticación

### Integración (test_integration.py)
- Flujo completo de proyecto
- Flujo de máximo 3 proyectos

## Docker Testing

```bash
docker-compose exec app pytest tests/ -v
```
